#!/usr/bin/env bash
# editorial/create_briefs.sh RUN_DIR < decisions.jsonl > briefs.jsonl
# Develops exactly three briefs (01 what changed, 02 what holds up, 03 what it means) from accepted
# evidence, with typed claims whose evidence references are validated against stored item versions.
# Exit 1 (no briefs on stdout) when evidence is insufficient or references cannot be validated.
set -uo pipefail
source "$(dirname "$0")/../lib/common.sh"
pl_stage_begin create_briefs "$@"

cat > "$PL_WORK/input.jsonl"
"$PY" editorial/briefs.py "$RUN_DIR" "$PL_ERRORS" < "$PL_WORK/input.jsonl" > "$PL_WORK/briefs.jsonl"
rc=$?
cat "$PL_WORK/briefs.jsonl"
in=$(pl_count_lines "$PL_WORK/input.jsonl"); out=$(pl_count_lines "$PL_WORK/briefs.jsonl")
note=$(jq -r '"validation=\(.status) quote_corrections=\((.quote_corrections // [])|length)"' "$RUN_DIR/briefs_validation.json" 2>/dev/null)
status=completed; [[ $rc -ne 0 ]] && status=failed
pl_stage_end "$status" "$rc" "$in" "$out" "anthropic-api" "$note"
exit $rc
