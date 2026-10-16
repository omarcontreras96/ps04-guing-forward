#!/usr/bin/env bash
# workflows/create_series.sh RUN_DIR
# Coordinates the series: select_items -> create_briefs -> (write_articles & write_video_scripts) -> check_content.
# Saves each named artifact before continuing and stops at the first failed requirement (it never fills gaps).
# PIPELINE_RESUME=1 (set by run.sh --resume) skips stages whose artifacts are already complete.
# Writes RUN_DIR/series_status.json. Exit 0 when drafts and a review exist, 1 otherwise.
set -uo pipefail
source "$(dirname "$0")/../lib/common.sh"
pl_stage_begin create_series "$@"
errlog() { echo "$RUN_DIR/logs/$1.stderr.log"; }
steps=()
finish() {  # finish STATUS RC NOTE
  printf '%s\n' "${steps[@]}" | jq -Rn --arg s "$1" --arg note "$3" '{status:$s, note:$note, steps:[inputs|select(.!="")|split("=")|{(.[0]):(.[1]|tonumber)}]|add}' \
    > "$RUN_DIR/series_status.json"
  [[ "$1" != completed ]] && pl_error "$3"
  pl_stage_end "$1" "$2" "$(pl_count_lines "$RUN_DIR/eligible.jsonl")" "$(ls "$RUN_DIR"/articles/*.md 2>/dev/null | wc -l | tr -d ' ')" "bash" "$3"
  exit "$2"
}

[[ -s "$RUN_DIR/eligible.jsonl" ]] || finish failed 1 "no eligible evidence"

RESUME="${PIPELINE_RESUME:-0}"
if [[ "$RESUME" == 1 && -s "$RUN_DIR/decisions.jsonl" && $(pl_count_lines "$RUN_DIR/decisions.jsonl") -eq $(pl_count_lines "$RUN_DIR/eligible.jsonl") ]]; then
  pl_log "resume: decisions.jsonl is complete; selection not rerun"; rc=0
else
  bash editorial/select_items.sh "$RUN_DIR" < "$RUN_DIR/eligible.jsonl" > "$RUN_DIR/decisions.jsonl" 2> >(tee -a "$(errlog select_items)" >&2)
  rc=$?
fi
steps+=("select_items=$rc")
[[ -s "$RUN_DIR/decisions.jsonl" ]] || finish failed 1 "selection produced no decisions"
[[ $rc -ne 0 ]] && pl_log "selection incomplete (exit $rc); continuing with recorded decisions"

if [[ "$RESUME" == 1 && $(pl_count_lines "$RUN_DIR/briefs.jsonl") -eq 3 ]]; then
  pl_log "resume: briefs.jsonl is complete; briefs not regenerated"; rc=0
else
  bash editorial/create_briefs.sh "$RUN_DIR" < "$RUN_DIR/decisions.jsonl" > "$RUN_DIR/briefs.jsonl" 2> >(tee -a "$(errlog create_briefs)" >&2)
  rc=$?
fi
steps+=("create_briefs=$rc")
[[ $rc -eq 0 && $(pl_count_lines "$RUN_DIR/briefs.jsonl") -eq 3 ]] \
  || finish failed 1 "brief creation failed; see briefs_validation.json (no unsupported briefs were created)"

bash content/write_articles.sh "$RUN_DIR" < "$RUN_DIR/briefs.jsonl" > "$RUN_DIR/articles.jsonl" 2> >(tee -a "$(errlog write_articles)" >&2) & p_a=$!
bash content/write_video_scripts.sh "$RUN_DIR" < "$RUN_DIR/briefs.jsonl" > "$RUN_DIR/video_scripts.jsonl" 2> >(tee -a "$(errlog write_video_scripts)" >&2) & p_v=$!
wait $p_a; rc_a=$?; wait $p_v; rc_v=$?
steps+=("write_articles=$rc_a" "write_video_scripts=$rc_v")

bash review/check_content.sh "$RUN_DIR" > "$RUN_DIR/review.json" 2> >(tee -a "$(errlog check_content)" >&2)
rc=$?; steps+=("check_content=$rc")
[[ $rc -eq 0 ]] || finish failed 1 "content check could not run"
[[ $rc_a -eq 0 && $rc_v -eq 0 ]] || finish incomplete 1 "some drafts failed to generate; review.json lists what is missing"
finish completed 0 "awaiting human review: passed=$(jq -r .passed "$RUN_DIR/review.json")"
