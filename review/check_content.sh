#!/usr/bin/env bash
# review/check_content.sh RUN_DIR > review.json
# Checks required files, three distinct pieces, resolvable evidence (via the store), dates, publisher counts,
# media coverage, article/script consistency and approximate lengths. Emits {review_id, passed, issues}.
# Exit 0 whenever the assessment completed, even if passed=false (callers must inspect `passed`).
set -uo pipefail
source "$(dirname "$0")/../lib/common.sh"
pl_stage_begin check_content "$@"

"$PY" review/check.py "$RUN_DIR" > "$PL_WORK/review.json"
rc=$?
if [[ $rc -eq 0 ]] && jq -e .review_id "$PL_WORK/review.json" >/dev/null 2>&1; then
  cat "$PL_WORK/review.json"
  note=$(jq -r '"passed=\(.passed) errors=\(.error_count) warnings=\(.warning_count) review_id=\(.review_id[0:12])"' "$PL_WORK/review.json")
  pl_stage_end completed 0 3 1 "python" "$note"
  exit 0
fi
pl_error "assessment could not run (exit $rc)"
pl_stage_end failed 1 null 0 "python"
exit 1
