#!/usr/bin/env bash
# workflows/collect_sources.sh RUN_DIR
# Coordinates collection only: runs the three collectors concurrently, combines their valid records,
# then extraction -> store upsert -> store list | date filter. Each step's logic lives in its component.
# Writes RUN_DIR/collection_status.json. Exit 0 = complete, 1 = incomplete coverage (usable results may
# still exist; see collection_status.json), 2 = invalid arguments.
set -uo pipefail
source "$(dirname "$0")/../lib/common.sh"
pl_stage_begin collect_sources "$@"
mkdir -p "$RUN_DIR/candidates"
errlog() { echo "$RUN_DIR/logs/$1.stderr.log"; }

# 1. Collectors run concurrently; each keeps its own stream, stderr log, and receipt.
bash collectors/fetch_feeds.sh    "$RUN_DIR" > "$RUN_DIR/candidates/feeds.jsonl"    2> >(tee -a "$(errlog fetch_feeds)" >&2) & p_feeds=$!
bash collectors/fetch_youtube.sh  "$RUN_DIR" > "$RUN_DIR/candidates/youtube.jsonl"  2> >(tee -a "$(errlog fetch_youtube)" >&2) & p_yt=$!
bash collectors/fetch_podcasts.sh "$RUN_DIR" > "$RUN_DIR/candidates/podcasts.jsonl" 2> >(tee -a "$(errlog fetch_podcasts)" >&2) & p_pod=$!
wait $p_feeds; rc_feeds=$?
wait $p_yt;    rc_yt=$?
wait $p_pod;   rc_pod=$?

# Combine only well-formed candidate records (a failed collector may leave partial output).
cat "$RUN_DIR"/candidates/{feeds,youtube,podcasts}.jsonl \
  | jq -cR 'fromjson? | select(type=="object" and (.item_id|type)=="string")' > "$RUN_DIR/candidates.jsonl"
pl_log "candidates: $(pl_count_lines "$RUN_DIR/candidates.jsonl") (feeds rc=$rc_feeds youtube rc=$rc_yt podcasts rc=$rc_pod)"

# 2. Extraction (stdin -> stdout).
bash processing/extract_content.sh "$RUN_DIR" < "$RUN_DIR/candidates.jsonl" > "$RUN_DIR/items.jsonl" 2> >(tee -a "$(errlog extract_content)" >&2)
rc_extract=$?

# 3. Persist through the store interface.
bash data/store.sh upsert "$RUN_DIR" < "$RUN_DIR/items.jsonl" > "$RUN_DIR/changes.jsonl" 2> >(tee -a "$(errlog store)" >&2)
rc_store=$?

# 4. Export latest stored versions and pipe them through the date filter (a real pipe).
rc_list=1; rc_filter=1
if [[ $rc_store -eq 0 ]]; then
  bash data/store.sh list | tee "$RUN_DIR/corpus.jsonl" | bash processing/filter_items.sh "$RUN_DIR" > "$RUN_DIR/eligible.jsonl" 2> >(tee -a "$(errlog filter_items)" >&2)
  rcs=("${PIPESTATUS[@]}"); rc_list=${rcs[0]}; rc_filter=${rcs[2]}
fi

status_of() { case "$1" in 0) echo completed;; 1) echo incomplete;; *) echo failed;; esac; }
jq -n \
  --arg feeds "$(status_of $rc_feeds)" --argjson rc_feeds $rc_feeds \
  --arg yt "$(status_of $rc_yt)" --argjson rc_yt $rc_yt \
  --arg pod "$(status_of $rc_pod)" --argjson rc_pod $rc_pod \
  --argjson rc_extract $rc_extract --argjson rc_store $rc_store --argjson rc_list $rc_list --argjson rc_filter $rc_filter \
  --argjson n_cand "$(pl_count_lines "$RUN_DIR/candidates.jsonl")" \
  --argjson n_items "$(pl_count_lines "$RUN_DIR/items.jsonl")" \
  --argjson n_elig "$(pl_count_lines "$RUN_DIR/eligible.jsonl")" \
  --arg simulated "${PIPELINE_SIMULATE_FAILURE:-}" \
  '{collectors: {feeds: {status:$feeds, exit_code:$rc_feeds}, youtube: {status:$yt, exit_code:$rc_yt}, podcasts: {status:$pod, exit_code:$rc_pod}},
    extract_content: {exit_code:$rc_extract}, store_upsert: {exit_code:$rc_store}, store_list: {exit_code:$rc_list}, filter_items: {exit_code:$rc_filter},
    counts: {candidates:$n_cand, items:$n_items, eligible:$n_elig},
    simulated_failures: ($simulated | split(",") | map(select(. != ""))),
    complete: ([$rc_feeds,$rc_yt,$rc_pod,$rc_extract,$rc_store,$rc_list,$rc_filter] | all(. == 0)),
    usable: ($rc_store == 0 and $rc_filter == 0 and $n_elig > 0)}' > "$RUN_DIR/collection_status.json"

complete=$(jq -r .complete "$RUN_DIR/collection_status.json")
usable=$(jq -r .usable "$RUN_DIR/collection_status.json")
if [[ "$complete" == "true" ]]; then rc=0; status=completed; elif [[ "$usable" == "true" ]]; then rc=1; status=incomplete; else rc=1; status=failed; fi
for r in $rc_feeds $rc_yt $rc_pod $rc_extract; do [[ $r -ne 0 ]] && pl_error "a collection step exited $r (see collection_status.json and that step's receipt)"; done
pl_stage_end "$status" "$rc" "$(pl_count_lines "$RUN_DIR/candidates.jsonl")" "$(pl_count_lines "$RUN_DIR/eligible.jsonl")" "bash" "usable=$usable"
exit $rc
