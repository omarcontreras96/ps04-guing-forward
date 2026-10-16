#!/usr/bin/env bash
# review/record_approval.sh RUN_DIR approve|revise "REVIEWER NAME" "NOTES"
# Helper for the HUMAN reviewer: writes RUN_DIR/approval.json bound to the current review.json review_id.
# Run it only after reading the drafts, scripts and review issues yourself. Record factual corrections
# and their reasons in NOTES (or in RUN_DIR/corrections.md, which is referenced automatically if present).
set -euo pipefail
[[ $# -eq 4 && -f "$1/review.json" && ( "$2" == approve || "$2" == revise ) ]] \
  || { echo 'usage: review/record_approval.sh RUN_DIR approve|revise "Reviewer" "Notes"' >&2; exit 2; }
corr=null; [[ -f "$1/corrections.md" ]] && corr="\"$1/corrections.md\""
jq -n --arg id "$(jq -r .review_id "$1/review.json")" --arg d "$2" --arg r "$3" --arg n "$4" --argjson c "$corr" \
  '{review_id:$id, decision:$d, reviewer:$r, reviewed_at:(now|todate), notes:$n, corrections_file:$c}' > "$1/approval.json"
cat "$1/approval.json"
