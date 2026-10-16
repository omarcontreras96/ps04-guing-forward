#!/usr/bin/env bash
# publishing/prepare_package.sh RUN_DIR > package_manifest.json
# Requires a passing CURRENT content check whose review_id matches review.json and a human approval.json
# (decision=approve). Re-verifies this itself, so direct invocation cannot package stale material.
# Builds RUN_DIR/package/ for Google Vids, YouTube and Substack; never regenerates drafts.
# Exit 1 with the reasons when review/approval is missing, failing or stale.
set -uo pipefail
source "$(dirname "$0")/../lib/common.sh"
pl_stage_begin prepare_package "$@"

"$PY" publishing/package.py "$RUN_DIR" > "$PL_WORK/manifest.json" 2> "$PL_WORK/stderr.log"
rc=$?
cat "$PL_WORK/stderr.log" >&2
if [[ $rc -eq 0 ]]; then
  cat "$PL_WORK/manifest.json"
  pl_stage_end completed 0 3 "$(jq '.pieces|length' "$PL_WORK/manifest.json")" "python" "package at $RUN_DIR/package"
else
  while IFS= read -r line; do pl_error "$line"; done < "$PL_WORK/stderr.log"
  pl_stage_end failed 1 3 0 "python" "package not prepared"
fi
exit $rc
