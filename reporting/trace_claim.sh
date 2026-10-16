#!/usr/bin/env bash
# reporting/trace_claim.sh RUN_DIR CLAIM_ID
# Read-only helper: trace one published claim back through the pipeline, printing
#   published sentence -> brief claim -> evidence reference -> stored item version (via data/store.sh)
#   -> exact passage / timestamp -> editorial decision -> discovery (candidate + configured source).
set -uo pipefail
source "$(dirname "$0")/../lib/common.sh"
[[ $# -eq 2 && -f "$1/run.json" ]] || { echo "usage: reporting/trace_claim.sh RUN_DIR CLAIM_ID" >&2; exit 2; }
RUN_DIR="$(pl_relpath "$1")"; cd "$PL_REPO_ROOT" || exit 1
"$PY" - "$RUN_DIR" "$2" <<'PY'
import json, os, re, subprocess, sys
from evidence import resolve_ref, fmt_ts
from util import read_jsonl
run, cid = sys.argv[1], sys.argv[2]
pid = cid.split("-")[0]
brief = next((b for b in read_jsonl(f"{run}/briefs.jsonl") if b["piece_id"] == pid), None)
claim = next((c for c in (brief or {}).get("claims", []) if c["claim_id"] == cid), None)
if not claim:
    sys.exit(f"claim {cid} not found in {run}/briefs.jsonl")
def h(t): print(f"\n=== {t}")
h(f"1. PUBLISHED / DRAFT TEXT ({run}/articles/{pid}.md)")
for line in open(f"{run}/articles/{pid}.md", encoding="utf-8"):
    if f"[{cid}]" in line and not line.startswith("- **["):
        for sent in re.split(r"(?<=[.!?\]])\s+", line.strip()):
            if f"[{cid}]" in sent:
                print("  " + sent)
h(f"2. BRIEF CLAIM ({run}/briefs.jsonl, piece {pid}: \"{brief['title']}\")")
print(f"  type: {claim['type']}\n  statement: {claim['statement']}")
decisions = {d["item_id"]: d for d in read_jsonl(f"{run}/decisions.jsonl")}
candidates = {c["item_id"]: c for c in read_jsonl(f"{run}/candidates.jsonl")}
sources = {s["source_id"]: s for s in json.load(open(f"{run}/config/sources.json"))}
for i, ref in enumerate(claim["evidence"], 1):
    res = resolve_ref(ref)
    it = res.get("item") or {}
    h(f"3.{i} EVIDENCE REFERENCE -> STORED VERSION (bash data/store.sh get {ref['item_id']} {ref['version_id'][:12]}...)")
    print(f"  item_id: {ref['item_id']}\n  version_id: {ref['version_id']}\n  locator: {json.dumps(ref['locator'])}")
    if not res["ok"]:
        print("  UNRESOLVED:", res["error"]); continue
    print(f"  {it['kind']} | {it.get('source_name')} | \"{it['title']}\" | published {it['published_at']} | retrieved {it['retrieved_at']}")
    print(f"  url: {it['url']}")
    print(f"  retained: text_path={it['text_path']} segments_path={it.get('segments_path')}")
    print(f"  extraction: {it.get('extraction_method')}")
    if res.get("segment"):
        s = res["segment"]
        print(f"  passage [{s['segment_id']} {fmt_ts(s['start_seconds'])}-{fmt_ts(s['end_seconds'])}]: \"{s['text']}\"")
    else:
        print(f"  exact quote (verified in text_path): \"{res['passage']}\"")
    hist = subprocess.run(["bash", "data/store.sh", "history", ref["item_id"]], capture_output=True, text=True).stdout
    for line in hist.splitlines():
        v = json.loads(line)
        print(f"  store history: version {v['version_id'][:12]} first seen {v['first_seen_run']}, observed in {v['observed_in_runs']}")
    d = decisions.get(ref["item_id"])
    h(f"4.{i} EDITORIAL DECISION ({run}/decisions.jsonl)")
    if d:
        print(f"  {d['decision'].upper()} for pieces {d['piece_ids']}\n  reason: {d['reason']}\n  credibility: {d.get('credibility')}")
    c = candidates.get(ref["item_id"])
    src = sources.get(it.get("source_id"), {})
    h(f"5.{i} DISCOVERY ({run}/candidates.jsonl + config/sources.json)")
    print(f"  source_id: {it.get('source_id')} ({src.get('kind')}: {src.get('url')}) publisher_id: {it['publisher_id']}")
    print(f"  discovered this run: {'yes' if c else 'no (retained in store from an earlier run)'}; media_url: {it.get('media_url')}")
PY
