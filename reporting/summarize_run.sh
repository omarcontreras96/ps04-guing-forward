#!/usr/bin/env bash
# reporting/summarize_run.sh RUN_DIR > summary.json
# Reports source coverage, changes, stage outcomes, elapsed time, models/tools, costs (known and unknown)
# and remaining manual work, using only saved artifacts and receipts. Works for incomplete runs.
set -uo pipefail
source "$(dirname "$0")/../lib/common.sh"
pl_stage_begin summarize_run "$@"

"$PY" reporting/summarize.py "$RUN_DIR" > "$PL_WORK/summary.json"
rc=$?
if [[ $rc -eq 0 ]]; then
  cat "$PL_WORK/summary.json"
  pl_stage_end completed 0 null 1 "python" "status=$(jq -r .status "$PL_WORK/summary.json")"
else
  pl_error "summary failed (exit $rc)"
  pl_stage_end failed 1 null 0 "python"
fi
exit $rc
