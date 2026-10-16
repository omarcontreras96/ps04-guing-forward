#!/usr/bin/env bash
# collectors/fetch_feeds.sh RUN_DIR > candidates/feeds.jsonl
# Discover written items from the run's configured `feed` sources and emit candidate JSONL.
# Exit 1 when any feed failed (partial results are still emitted and the failures are in the receipt).
set -uo pipefail
source "$(dirname "$0")/../lib/common.sh"
pl_stage_begin fetch_feeds "$@"

n_sources=$(jq '[.[] | select(.kind=="feed")] | length' "$RUN_DIR/config/sources.json") || { pl_stage_end failed 2 null null ""; exit 2; }
"$PY" collectors/feeds.py "$RUN_DIR" "$PL_ERRORS" > "$PL_WORK/out.jsonl"
rc=$?
cat "$PL_WORK/out.jsonl"
out=$(pl_count_lines "$PL_WORK/out.jsonl")
status=completed; [[ $rc -ne 0 ]] && status=incomplete
pl_stage_end "$status" "$rc" "$n_sources" "$out" "urllib,feedparser" "input_count = configured feed sources"
exit $rc
