"""Drafting helper shared by content/write_articles.sh and content/write_video_scripts.sh.

Both read the SAME briefs and the SAME resolved evidence passages, so article and script claims stay
consistent. Each piece is one model call (with PIPELINE_RESUME=1, pieces already written are kept). If the length misses the target band, one revision call
follows. Claim markers such as [01-c2] stay in the drafts and are resolved to reader-facing sources at
packaging time.
"""
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta

import llm
from evidence import evidence_pack, project_brief, read_text_file
from util import load_json, log_error

KINDS = {
    "article": {"prompt": "write_articles.md", "dir": "articles", "band_key": "article_words", "label": "article"},
    "script": {"prompt": "write_video_scripts.md", "dir": "video_scripts", "band_key": "script_words", "label": "video script"},
}
MARKER = re.compile(r"\[(\d{2}-c\d+)\]")


def count_words(kind, md):
    if kind == "article":
        body = re.split(r"\n##\s+References", md, maxsplit=1)[0]
        body = re.sub(r"^\*As of.*$", "", body, flags=re.M)
    else:
        body = "\n".join(re.findall(r"\*\*Narration:\*\*(.*)", md))
    return len(MARKER.sub("", body).split())


def main(kind, run_dir, errors_path):
    spec = KINDS[kind]
    briefs = [json.loads(l) for l in sys.stdin if l.strip()]
    if sorted(b.get("piece_id") for b in briefs) != ["01", "02", "03"]:
        print(f"{kind}: expected three briefs 01-03 on stdin", file=sys.stderr)
        return 2
    run = load_json(os.path.join(run_dir, "run.json"))
    cfg = load_json(os.path.join(run_dir, "config", "project.json"))
    lo, hi = cfg.get("pipeline", {}).get(spec["band_key"], [600, 900])
    as_of = date.fromisoformat(run["as_of_date"])
    window = f"{(as_of - timedelta(days=29)).isoformat()} to {as_of.isoformat()}"
    prompt = read_text_file(os.path.join(run_dir, "prompts", spec["prompt"]))
    prompt = prompt.replace("{as_of_date}", run["as_of_date"]).replace("{window}", window)
    policy = read_text_file(os.path.join(run_dir, "config", "editorial_policy.md"))
    system = project_brief(run_dir) + "\n\n# Editorial policy\n" + policy + "\n\n# Instructions\n" + prompt
    os.makedirs(os.path.join(run_dir, spec["dir"]), exist_ok=True)

    resume = os.environ.get("PIPELINE_RESUME") == "1"

    def write(brief):
        pid = brief["piece_id"]
        path = os.path.join(run_dir, spec["dir"], f"{pid}.md")
        if resume and os.path.exists(path):  # finished before an interruption; keep it
            md = open(path, encoding="utf-8").read()
            brief_ids = [c["claim_id"] for c in brief["claims"]]
            used = set(MARKER.findall(md))
            print(f"{kind}: resume: reusing existing {path}", file=sys.stderr)
            return {"piece_id": pid, "path": path, "claim_ids": [c for c in brief_ids if c in used],
                    "unknown_markers": sorted(used - set(brief_ids)), "unused_claims": [c for c in brief_ids if c not in used],
                    "word_count": count_words(kind, md), "target_words": [lo, hi], "resumed": True}
        others = [f"{b['piece_id']}: {b['argument']}" for b in briefs if b["piece_id"] != pid]
        user = (f"As-of date: {run['as_of_date']}. Evidence window: {window}.\n"
                f"Series context (the other two pieces argue, do not repeat them): {others}\n\n"
                f"BRIEF:\n{json.dumps(brief, indent=1, ensure_ascii=False)}\n\n"
                f"EVIDENCE PASSAGES (the only material you may use):\n{evidence_pack(brief)}\n\n"
                f"Write the {spec['label']} now. Target: {lo}-{hi} words "
                f"({'excluding References' if kind == 'article' else 'of narration'}). Output Markdown only.")
        md = llm.call(run_dir, f"write_{spec['dir']}", f"{pid}", "writer", system, user, max_tokens=32000, effort="high")
        n = count_words(kind, md)
        if not (lo * 0.95 <= n <= hi * 1.05):
            revise = (user + f"\n\nYOUR DRAFT:\n{md}\n\nThe draft has {n} words "
                      f"({'excluding References' if kind == 'article' else 'of narration'}); the target is {lo}-{hi}. "
                      "Revise to fit the target while keeping the argument, every claim marker, and the format. Output the full revised Markdown only.")
            md = llm.call(run_dir, f"write_{spec['dir']}", f"{pid}-length-revision", "writer", system, revise,
                          max_tokens=32000, effort="high")
            n = count_words(kind, md)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(md.strip() + "\n")
        brief_ids = [c["claim_id"] for c in brief["claims"]]
        used = set(MARKER.findall(md))
        return {"piece_id": pid, "path": path, "claim_ids": [c for c in brief_ids if c in used],
                "unknown_markers": sorted(used - set(brief_ids)), "unused_claims": [c for c in brief_ids if c not in used],
                "word_count": n, "target_words": [lo, hi]}

    failed = 0
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = {b["piece_id"]: pool.submit(write, b) for b in sorted(briefs, key=lambda b: b["piece_id"])}
    for pid, fut in futures.items():
        try:
            print(json.dumps(fut.result()))
        except Exception as exc:  # noqa: BLE001
            failed += 1
            log_error(errors_path, f"{kind} {pid} failed: {exc}", pid)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
