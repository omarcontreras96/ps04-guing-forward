"""Evidence helpers shared by the editorial, content, review and publishing stages.

Item records are always obtained through `data/store.sh get` (the store interface); retained text and
segment assets are then read from disk by path. Quote matching normalises whitespace, case, curly
quotes and dashes, so "exact" means verbatim up to typography.
"""
import difflib
import json
import os
import re
import subprocess
from functools import lru_cache

from util import load_json


@lru_cache(maxsize=None)
def _store_get(item_id, version_id):
    args = ["bash", "data/store.sh", "get", item_id] + ([version_id] if version_id else [])
    res = subprocess.run(args, capture_output=True, text=True)
    if res.returncode != 0 or not res.stdout.strip():
        return None
    return res.stdout


def store_get(item_id, version_id=None):
    raw = _store_get(item_id, version_id)
    return json.loads(raw) if raw else None


@lru_cache(maxsize=None)
def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def load_text(item):
    return _read(item["text_path"])


def load_segments(item):
    return json.loads(_read(item["segments_path"])) if item.get("segments_path") else None


def fmt_ts(seconds):
    s = int(seconds or 0)
    h, m, sec = s // 3600, (s % 3600) // 60, s % 60
    return f"{h}:{m:02d}:{sec:02d}" if h else f"{m:02d}:{sec:02d}"


def media_link(item, segment):
    start = int(segment["start_seconds"])
    if item["kind"] == "youtube":
        return f"{item['url']}&t={start}s"
    return item["url"]


def publisher_label(item):
    return item.get("source_name") or item.get("publisher_id")


def render_item(item, max_chars=60000, segment_ids=None, context=6):
    """Item header plus body; transcripts carry [segment-id start-end] markers.

    segment_ids: if given (long transcripts), include only those segments +/- `context` neighbours.
    """
    head = [
        f"ITEM {item['item_id']}",
        f"version_id: {item['version_id']}",
        f"kind: {item['kind']} | publisher: {publisher_label(item)} ({item['publisher_id']}) | perspective: {item.get('perspective')}",
        f"title: {item['title']}",
        f"published_at: {item['published_at']} | url: {item['url']}",
    ]
    if item.get("duration_seconds"):
        head.append(f"duration: {fmt_ts(item['duration_seconds'])}"
                    + (" (transcript truncated)" if item.get("transcript_truncated") else ""))
    segs = load_segments(item)
    if segs is None:
        body = load_text(item)
    else:
        keep = None
        if segment_ids:
            idx = {s["segment_id"]: i for i, s in enumerate(segs)}
            keep = set()
            for sid in segment_ids:
                if sid in idx:
                    keep.update(range(max(0, idx[sid] - context), min(len(segs), idx[sid] + context + 1)))
        lines, prev = [], None
        for i, s in enumerate(segs):
            if keep is not None and i not in keep:
                continue
            if keep is not None and prev is not None and i != prev + 1:
                lines.append("[...]")
            lines.append(f"[{s['segment_id']} {fmt_ts(s['start_seconds'])}-{fmt_ts(s['end_seconds'])}] {s['text']}")
            prev = i
        body = "\n".join(lines)
    truncated = len(body) > max_chars
    if truncated:
        body = body[:max_chars] + "\n[... truncated for length ...]"
    return "\n".join(head) + "\n---\n" + body + "\n=== END ITEM ===\n"


_TRANS = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-",
                        " ": " ", "…": "..."})


def norm(s):
    return re.sub(r"\s+", " ", (s or "").translate(_TRANS)).strip().lower()


def quote_in_text(quote, text):
    q = norm(quote)
    return bool(q) and q in norm(text)


def closest_passage(quote, text, threshold=0.88):
    """Return the verbatim passage in `text` that best matches a near-miss quote, or None."""
    words = text.split()
    qn = norm(quote).split()
    n = len(qn)
    if n < 4 or not words:
        return None
    starts = {w for w in qn[:3]}
    best, best_ratio = None, 0.0
    target = " ".join(qn)
    for i in range(len(words)):
        if norm(words[i]) not in starts:
            continue
        for size in (n - 1, n, n + 1):
            cand = words[i:i + size]
            r = difflib.SequenceMatcher(None, norm(" ".join(cand)), target).ratio()
            if r > best_ratio:
                best, best_ratio = " ".join(cand), r
    return best if best_ratio >= threshold else None


def resolve_ref(ref):
    """Resolve an evidence reference. Returns dict with ok/error plus item, passage, timestamp, link."""
    item = store_get(ref.get("item_id", ""), ref.get("version_id"))
    if not item:
        return {"ok": False, "error": f"item/version not in store: {ref.get('item_id')} {ref.get('version_id')}"}
    loc = ref.get("locator") or {}
    if loc.get("type") == "text":
        if not quote_in_text(loc.get("quote", ""), load_text(item)):
            return {"ok": False, "item": item, "error": f"quote not found in {item['text_path']}: {loc.get('quote', '')[:80]!r}"}
        return {"ok": True, "item": item, "passage": loc["quote"], "timestamp": None, "link": item["url"]}
    if loc.get("type") == "segment":
        segs = load_segments(item) or []
        seg = next((s for s in segs if s["segment_id"] == loc.get("segment_id")), None)
        if not seg:
            return {"ok": False, "item": item, "error": f"segment {loc.get('segment_id')} not in {item.get('segments_path')}"}
        return {"ok": True, "item": item, "passage": seg["text"], "segment": seg,
                "timestamp": f"{fmt_ts(seg['start_seconds'])}-{fmt_ts(seg['end_seconds'])}", "link": media_link(item, seg)}
    return {"ok": False, "item": item, "error": f"unknown locator type {loc.get('type')!r}"}


def run_meta(run_dir):
    return load_json(os.path.join(run_dir, "run.json"))


def read_text_file(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def project_brief(run_dir):
    p = load_json(os.path.join(run_dir, "config", "project.json"))
    keys = ["publication_name", "topic", "audience", "central_question", "voice", "themes", "includes", "excludes"]
    return "# Project brief\n" + json.dumps({k: p[k] for k in keys if k in p}, indent=2, ensure_ascii=False)


def evidence_pack(brief):
    """Human/model-readable listing of every claim with its resolved evidence passages."""
    lines = []
    for c in brief["claims"]:
        lines.append(f"[{c['claim_id']}] ({c['type']}) {c['statement']}")
        for r in c["evidence"]:
            res = resolve_ref(r)
            if not res["ok"]:
                lines.append(f"    - UNRESOLVED: {res['error']}")
                continue
            it = res["item"]
            where = f" at {res['timestamp']}" if res.get("timestamp") else ""
            lines.append(f"    - {publisher_label(it)}, \"{it['title']}\" ({it['kind']}, {it['published_at'][:10]}){where}: "
                         f"{res['link']}\n      passage: \"{res['passage']}\"")
    return "\n".join(lines)


def claim_sources(brief):
    """claim_id -> list of resolved source descriptors (for references and source notes)."""
    out = {}
    for c in brief["claims"]:
        refs = []
        for r in c["evidence"]:
            res = resolve_ref(r)
            if res["ok"]:
                it = res["item"]
                refs.append({"publisher": publisher_label(it), "title": it["title"], "kind": it["kind"],
                             "date": it["published_at"][:10], "link": res["link"], "timestamp": res.get("timestamp"),
                             "passage": res["passage"], "item_id": it["item_id"], "version_id": it["version_id"],
                             "locator": r["locator"]})
        out[c["claim_id"]] = refs
    return out
