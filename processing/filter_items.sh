#!/usr/bin/env bash
# processing/filter_items.sh RUN_DIR < corpus.jsonl > eligible.jsonl
# Mechanical 30-day eligibility check against run.json's as_of_date (window D-29..D, UTC).
# Writes exclusion records (item_id, version_id, reason, detail) to RUN_DIR/exclusions.jsonl.
# Editorial relevance is NOT judged here; that belongs to editorial/select_items.sh.
set -uo pipefail
source "$(dirname "$0")/../lib/common.sh"
pl_stage_begin filter_items "$@"

cat > "$PL_WORK/input.jsonl"
"$PY" processing/filter.py "$RUN_DIR" "$RUN_DIR/exclusions.jsonl" < "$PL_WORK/input.jsonl" > "$PL_WORK/eligible.jsonl"
rc=$?
cat "$PL_WORK/eligible.jsonl"

in=$(pl_count_lines "$PL_WORK/input.jsonl"); out=$(pl_count_lines "$PL_WORK/eligible.jsonl")
if [[ $rc -eq 0 ]]; then
  reasons=$(jq -rs 'group_by(.reason) | map("\(.[0].reason)=\(length)") | join(" ")' "$RUN_DIR/exclusions.jsonl")
  pl_stage_end completed 0 "$in" "$out" "python" "excluded: ${reasons:-none}"
else
  pl_error "filter exited $rc"
  pl_stage_end failed "$rc" "$in" "$out" "python"
fi
exit $rc
