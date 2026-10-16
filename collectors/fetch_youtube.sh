#!/usr/bin/env bash
# collectors/fetch_youtube.sh RUN_DIR > candidates/youtube.jsonl
# Discover recent videos from the run's configured `youtube` sources (native IDs, upload metadata).
# Exit 1 when any source or video lookup failed; valid partial results are still emitted.
set -uo pipefail
source "$(dirname "$0")/../lib/common.sh"
pl_stage_begin fetch_youtube "$@"

n_sources=$(jq '[.[] | select(.kind=="youtube")] | length' "$RUN_DIR/config/sources.json") || { pl_stage_end failed 2 null null ""; exit 2; }
"$PY" collectors/youtube.py "$RUN_DIR" "$PL_ERRORS" > "$PL_WORK/out.jsonl"
rc=$?
cat "$PL_WORK/out.jsonl"
out=$(pl_count_lines "$PL_WORK/out.jsonl")
status=completed; [[ $rc -ne 0 ]] && status=incomplete
pl_stage_end "$status" "$rc" "$n_sources" "$out" "yt-dlp $(yt-dlp --version 2>/dev/null)" "input_count = configured youtube sources"
exit $rc
