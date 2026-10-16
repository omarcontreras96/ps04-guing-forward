#!/usr/bin/env bash
# collectors/fetch_podcasts.sh RUN_DIR > candidates/podcasts.jsonl
# Discover recent podcast episodes and their audio enclosure URLs from the run's `podcast` sources.
# Exit 1 when any feed failed; valid partial results are still emitted.
set -uo pipefail
source "$(dirname "$0")/../lib/common.sh"
pl_stage_begin fetch_podcasts "$@"

n_sources=$(jq '[.[] | select(.kind=="podcast")] | length' "$RUN_DIR/config/sources.json") || { pl_stage_end failed 2 null null ""; exit 2; }
"$PY" collectors/podcasts.py "$RUN_DIR" "$PL_ERRORS" > "$PL_WORK/out.jsonl"
rc=$?
cat "$PL_WORK/out.jsonl"
out=$(pl_count_lines "$PL_WORK/out.jsonl")
status=completed; [[ $rc -ne 0 ]] && status=incomplete
pl_stage_end "$status" "$rc" "$n_sources" "$out" "urllib,feedparser" "input_count = configured podcast sources"
exit $rc
