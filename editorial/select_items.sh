#!/usr/bin/env bash
# editorial/select_items.sh RUN_DIR < eligible.jsonl > decisions.jsonl
# Applies the run's snapshotted editorial policy and selection prompt through the model.
# One decision per eligible item: accept | reject | defer, with reason and intended piece IDs.
# Side artifacts: RUN_DIR/digests.jsonl, RUN_DIR/selection_notes.json, RUN_DIR/llm/select_items/ (exact requests).
set -uo pipefail
source "$(dirname "$0")/../lib/common.sh"
pl_stage_begin select_items "$@"

cat > "$PL_WORK/input.jsonl"
"$PY" editorial/selection.py "$RUN_DIR" "$PL_ERRORS" < "$PL_WORK/input.jsonl" > "$PL_WORK/decisions.jsonl"
rc=$?
cat "$PL_WORK/decisions.jsonl"
in=$(pl_count_lines "$PL_WORK/input.jsonl"); out=$(pl_count_lines "$PL_WORK/decisions.jsonl")
note=$(jq -rs 'group_by(.decision) | map("\(.[0].decision)=\(length)") | join(" ")' "$PL_WORK/decisions.jsonl" 2>/dev/null)
status=completed; [[ $rc -ne 0 ]] && status=$([[ $out -gt 0 ]] && echo incomplete || echo failed)
pl_stage_end "$status" "$rc" "$in" "$out" "anthropic-api" "$note"
exit $rc
