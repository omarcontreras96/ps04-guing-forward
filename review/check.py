"""Machine content checks. Emits {review_id, passed, issues[]} as one JSON object.

review_id = sha256 over the as-of date, briefs.jsonl, both manifests, every draft and script file, and the
resolved evidence (item_id, version_id, locator) of every claim. Any edit to these changes the ID.
Errors block packaging; warnings flag matters for human judgment. A passing check cannot establish that an
interpretation is sound.
"""
import difflib
import hashlib
import json
import os
import re
import sys
from datetime import date, timedelta

from evidence import resolve_ref
from util import load_json, read_jsonl

PIECES = ["01", "02", "03"]
MARKER = re.compile(r"\[(\d{2}-c\d+)\]")
issues = []


def issue(artifact, severity, message, piece_id=None):
    issues.append({"piece_id": piece_id, "artifact": artifact, "severity": severity, "message": message})


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def main(run_dir):
    run = load_json(os.path.join(run_dir, "run.json"))
    as_of = date.fromisoformat(run["as_of_date"])
    start = as_of - timedelta(days=29)
    cfg = load_json(os.path.join(run_dir, "config", "project.json")).get("pipeline", {})
    art_lo, art_hi = cfg.get("article_words", [600, 900])
    scr_lo, scr_hi = cfg.get("script_words", [430, 720])
    h = hashlib.sha256()
    h.update(f"as_of={run['as_of_date']}\n".encode())

    def fp(label, path):
        h.update(f"\n## {label}\n".encode())
        h.update(open(path, "rb").read() if os.path.exists(path) else b"<missing>")

    # -- required files
    required = ["briefs.jsonl", "articles.jsonl", "video_scripts.jsonl"] + \
               [f"articles/{p}.md" for p in PIECES] + [f"video_scripts/{p}.md" for p in PIECES]
    for r in required:
        if not os.path.exists(os.path.join(run_dir, r)):
            issue(r, "error", "required file is missing")
    for r in ["briefs.jsonl", "articles.jsonl", "video_scripts.jsonl"]:
        fp(r, os.path.join(run_dir, r))
    for p in PIECES:
        fp(f"articles/{p}.md", os.path.join(run_dir, "articles", f"{p}.md"))
        fp(f"video_scripts/{p}.md", os.path.join(run_dir, "video_scripts", f"{p}.md"))

    briefs = {b["piece_id"]: b for b in read_jsonl(os.path.join(run_dir, "briefs.jsonl"))} \
        if os.path.exists(os.path.join(run_dir, "briefs.jsonl")) else {}
    if sorted(briefs) != PIECES:
        issue("briefs.jsonl", "error", f"expected exactly three briefs 01, 02, 03; found {sorted(briefs)}")

    # -- briefs: structure, evidence resolution, dates, publishers, media coverage
    kinds = set()
    for pid, b in sorted(briefs.items()):
        for f in ["title", "question", "argument", "synthesis", "limitations", "claims"]:
            if not b.get(f):
                issue("briefs.jsonl", "error", f"brief field '{f}' is empty", pid)
        pubs = set()
        for c in b.get("claims", []):
            if c.get("type") not in ("reported_fact", "source_claim", "inference"):
                issue("briefs.jsonl", "error", f"{c.get('claim_id')}: invalid claim type {c.get('type')!r}", pid)
            if not c.get("evidence"):
                issue("briefs.jsonl", "error", f"{c.get('claim_id')}: claim has no evidence", pid)
            for r in c.get("evidence", []):
                h.update(json.dumps([c["claim_id"], r], sort_keys=True).encode())
                res = resolve_ref(r)
                if not res["ok"]:
                    issue("briefs.jsonl", "error", f"{c['claim_id']}: unresolvable evidence: {res['error']}", pid)
                    continue
                it = res["item"]
                pub = (it.get("published_at") or "")[:10]
                if not pub or not (start.isoformat() <= pub <= as_of.isoformat()):
                    issue("briefs.jsonl", "error", f"{c['claim_id']}: {it['item_id']} published {pub or 'unknown'} is outside {start}..{as_of}", pid)
                pubs.add(it["publisher_id"])
                kinds.add(it["kind"])
        if len(pubs) < 3:
            issue("briefs.jsonl", "error", f"evidence from {len(pubs)} independent publisher(s); at least 3 required", pid)
        inferences = [c["claim_id"] for c in b.get("claims", []) if c.get("type") == "inference"]
        issue(f"articles/{pid}.md", "warning",
              "Human judgment required: check that inference claims " + (", ".join(inferences) or "(none)") +
              " follow from the cited passages, and that the counterargument is fairly represented.", pid)
    for k in {"feed", "youtube", "podcast"} - kinds:
        issue("series", "error", f"no {k} evidence is cited anywhere in the series")

    # -- distinctness of the three arguments
    ids = sorted(briefs)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = briefs[ids[i]], briefs[ids[j]]
            if a.get("title", "").strip().lower() == b.get("title", "").strip().lower():
                issue("briefs.jsonl", "error", f"pieces {ids[i]} and {ids[j]} have the same title")
            sim = difflib.SequenceMatcher(None, a.get("argument", "").lower(), b.get("argument", "").lower()).ratio()
            if sim > 0.6:
                issue("briefs.jsonl", "warning", f"arguments of {ids[i]} and {ids[j]} are textually similar ({sim:.2f}); confirm they are distinct")

    # -- drafts vs manifests vs briefs; article/script consistency; lengths; as-of statement
    manifests = {}
    for kind, mf in (("article", "articles.jsonl"), ("script", "video_scripts.jsonl")):
        path = os.path.join(run_dir, mf)
        manifests[kind] = {m["piece_id"]: m for m in read_jsonl(path)} if os.path.exists(path) else {}
    for pid in PIECES:
        b = briefs.get(pid, {"claims": []})
        brief_ids = [c["claim_id"] for c in b["claims"]]
        used = {}
        for kind, d in (("article", "articles"), ("script", "video_scripts")):
            path = os.path.join(run_dir, d, f"{pid}.md")
            if not os.path.exists(path):
                continue
            md = read(path)
            markers = set(MARKER.findall(md))
            used[kind] = markers
            m = manifests[kind].get(pid)
            if not m:
                issue(f"{d}.jsonl", "error", "no manifest record for this piece", pid)
            elif set(m.get("claim_ids", [])) != (markers & set(brief_ids)):
                issue(f"{d}.jsonl", "error", "manifest claim_ids do not match the markers in the draft", pid)
            for x in sorted(markers - set(brief_ids)):
                issue(f"{d}/{pid}.md", "error", f"marker [{x}] does not exist in brief {pid}", pid)
            missing = [c for c in brief_ids if c not in markers]
            if missing and kind == "article":
                issue(f"{d}/{pid}.md", "warning", f"brief claims not used in the article: {missing}", pid)
            if kind == "article":
                body = re.split(r"\n##\s+References", md, maxsplit=1)[0]
                n = len(MARKER.sub("", re.sub(r"^\*As of.*$", "", body, flags=re.M)).split())
                if not (art_lo <= n <= art_hi):
                    issue(f"{d}/{pid}.md", "warning", f"article body is {n} words (target {art_lo}-{art_hi})", pid)
                if run["as_of_date"] not in md:
                    issue(f"{d}/{pid}.md", "error", f"article does not state the as-of date {run['as_of_date']}", pid)
            else:
                n = len(MARKER.sub("", "\n".join(re.findall(r"\*\*Narration:\*\*(.*)", md))).split())
                if not (scr_lo <= n <= scr_hi):
                    issue(f"{d}/{pid}.md", "warning",
                          f"narration is {n} words, about {n / 150:.1f} min at 150 wpm (target {scr_lo}-{scr_hi} words for 3-5 min)", pid)
                if "## YouTube description" not in md:
                    issue(f"{d}/{pid}.md", "warning", "script has no YouTube description section", pid)
        if "article" in used and "script" in used:
            extra = used["script"] - used["article"]
            if extra:
                issue(f"video_scripts/{pid}.md", "error",
                      f"script relies on claims the article does not make: {sorted(extra)} (article/script must stay consistent)", pid)

    review_id = h.hexdigest()
    passed = not any(i["severity"] == "error" for i in issues)
    print(json.dumps({"review_id": review_id, "run_id": run["run_id"], "as_of_date": run["as_of_date"],
                      "passed": passed,
                      "error_count": sum(i["severity"] == "error" for i in issues),
                      "warning_count": sum(i["severity"] == "warning" for i in issues),
                      "issues": issues}, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
