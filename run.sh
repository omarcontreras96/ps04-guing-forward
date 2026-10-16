#!/usr/bin/env bash
# run.sh — pipeline entry point (coordination only).
#
#   bash run.sh                     new live run: validate config, snapshot it, collect, create the series,
#                                   check content, stop for human review (status awaiting_review)
#   bash run.sh --resume RUN_DIR    continue an interrupted run's series workflow (no recollection; completed
#                                   stages and finished drafts are kept), then recheck and resummarize
#   bash run.sh --package RUN_DIR   rerun content checks and, with a matching human approval.json,
#                                   assemble RUN_DIR/package/ (never recollects or regenerates drafts)
#
# Options for a new run:
#   --mode live|replay              replay marks a labelled demonstration run (default live)
#   --note TEXT                     free-text label stored in run.json (e.g. "policy v2 comparison")
#   --reuse-evidence RUN_DIR        replay only: copy that run's collection artifacts (candidates through
#                                   eligible/exclusions) instead of collecting, so a policy or prompt change
#                                   can be compared on identical evidence
# Environment: PIPELINE_SIMULATE_FAILURE=source_id[,..] deliberately fails those sources (recorded as simulated).
#
# Prints the run summary JSON on stdout. Exit 0 when the run reached awaiting_review/ready_for_production,
# 1 when it failed, 2 for invalid arguments or configuration.
set -uo pipefail
source "$(dirname "$0")/lib/common.sh"
cd "$PL_REPO_ROOT" || exit 1
PL_STAGE=run

die_usage() { echo "run.sh: $*" >&2; echo "usage: bash run.sh [--mode live|replay] [--note TEXT] [--reuse-evidence RUN_DIR] | bash run.sh --resume RUN_DIR | bash run.sh --package RUN_DIR" >&2; exit 2; }

summarize() {  # always the last step; works for incomplete runs
  bash reporting/summarize_run.sh "$1" > "$1/summary.json.tmp" 2>> "$1/logs/summarize_run.stderr.log" \
    && mv "$1/summary.json.tmp" "$1/summary.json"
  cat "$1/summary.json"
  [[ "$(jq -r .status "$1/summary.json")" != "failed" ]]
}

# ---------------------------------------------------------------- --package mode
if [[ "${1:-}" == "--package" ]]; then
  [[ $# -eq 2 && -f "$2/run.json" ]] || die_usage "--package needs an existing run directory"
  RUN_DIR="$(pl_relpath "$2")"
  pl_log "re-checking content for $RUN_DIR"
  if bash review/check_content.sh "$RUN_DIR" > "$RUN_DIR/review.json.tmp" 2>> "$RUN_DIR/logs/check_content.stderr.log"; then
    [[ -f "$RUN_DIR/review.json" ]] && cp "$RUN_DIR/review.json" "$RUN_DIR/logs/review-$(date -u +%Y%m%dT%H%M%SZ).json"
    mv "$RUN_DIR/review.json.tmp" "$RUN_DIR/review.json"
  else
    rm -f "$RUN_DIR/review.json.tmp"; pl_log "content check could not run"
  fi
  pl_log "preparing package"
  bash publishing/prepare_package.sh "$RUN_DIR" > "$RUN_DIR/logs/package_manifest.stdout.json" 2> >(tee -a "$RUN_DIR/logs/prepare_package.stderr.log" >&2) \
    || pl_log "package not prepared (see messages above)"
  summarize "$RUN_DIR"; exit $?
fi

# ---------------------------------------------------------------- --resume mode
if [[ "${1:-}" == "--resume" ]]; then
  [[ $# -eq 2 && -f "$2/run.json" ]] || die_usage "--resume needs an existing run directory"
  RUN_DIR="$(pl_relpath "$2")"
  [[ "$(jq -r '.usable // false' "$RUN_DIR/collection_status.json" 2>/dev/null)" == "true" ]] \
    || { echo "run.sh: $RUN_DIR has no usable collection to resume from; start a new run" >&2; exit 1; }
  pl_log "resuming series workflow for $RUN_DIR (collection is not repeated)"
  PIPELINE_RESUME=1 bash workflows/create_series.sh "$RUN_DIR" || pl_log "series workflow did not complete (see receipts)"
  summarize "$RUN_DIR"; exit $?
fi

# ---------------------------------------------------------------- new run
MODE=live; NOTE=""; REUSE=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode) MODE="${2:-}"; shift 2 ;;
    --note) NOTE="${2:-}"; shift 2 ;;
    --reuse-evidence) REUSE="${2:-}"; shift 2 ;;
    *) die_usage "unknown argument '$1'" ;;
  esac
done
[[ "$MODE" == "live" || "$MODE" == "replay" ]] || die_usage "--mode must be live or replay"
if [[ -n "$REUSE" ]]; then
  [[ "$MODE" == "replay" ]] || die_usage "--reuse-evidence is only allowed with --mode replay"
  [[ -s "$REUSE/eligible.jsonl" && -f "$REUSE/run.json" ]] || die_usage "--reuse-evidence: $REUSE has no eligible.jsonl"
  REUSE="$(pl_relpath "$REUSE")"
fi

# Validate configuration before creating anything.
jq -e '[.publication_name, .topic, .audience, .central_question] | all(type=="string" and length>0)' config/project.json >/dev/null 2>&1 \
  || { echo "run.sh: config/project.json needs nonempty publication_name, topic, audience, central_question" >&2; exit 2; }
jq -e 'type=="array" and length>0 and all(.[]; (.source_id|type)=="string" and (.publisher_id|type)=="string" and (.url|type)=="string" and (.kind|IN("feed","youtube","podcast")))
       and ([.[].source_id] | length == (unique|length))' config/sources.json >/dev/null 2>&1 \
  || { echo "run.sh: config/sources.json must be a nonempty array of {source_id (unique), publisher_id, kind: feed|youtube|podcast, url}" >&2; exit 2; }
for f in config/editorial_policy.md prompts/select_items.md prompts/create_briefs.md prompts/write_articles.md prompts/write_video_scripts.md; do
  [[ -s "$f" ]] || { echo "run.sh: $f is empty" >&2; exit 2; }
done

STARTED="$(pl_now)"
AS_OF="${STARTED:0:10}"                      # actual UTC execution date, captured once
RUN_ID="$MODE-$(date -u +%Y%m%dT%H%M%SZ)"
RUN_DIR="runs/$RUN_ID"
PREV=$(ls -d runs/live-* 2>/dev/null | sort | tail -1)
PREV_ID=$([[ -n "$PREV" ]] && basename "$PREV" || echo "")
mkdir -p "$RUN_DIR/logs" "$RUN_DIR/config" "$RUN_DIR/prompts"
jq -n --arg id "$RUN_ID" --arg s "$STARTED" --arg d "$AS_OF" --arg m "$MODE" --arg p "$PREV_ID" --arg note "$NOTE" \
      --arg sim "${PIPELINE_SIMULATE_FAILURE:-}" \
  '{run_id:$id, started_at:$s, as_of_date:$d, mode:$m, previous_run_id:(if $p == "" then null else $p end),
    note:(if $note == "" then null else $note end), simulated_failures:($sim|split(",")|map(select(.!="")))}' > "$RUN_DIR/run.json"
cp config/project.json config/sources.json config/editorial_policy.md "$RUN_DIR/config/"
cp prompts/*.md "$RUN_DIR/prompts/"
pl_log "run $RUN_ID (as-of $AS_OF, previous: ${PREV_ID:-none})"

bash data/store.sh init || { pl_log "store init failed"; summarize "$RUN_DIR"; exit 1; }

if [[ -n "$REUSE" ]]; then
  # Replay: identical evidence from an earlier run; nothing is collected or written to the store.
  pl_log "replay: reusing collection artifacts from $REUSE (no collection)"
  mkdir -p "$RUN_DIR/candidates"
  cp "$REUSE"/candidates/*.jsonl "$RUN_DIR/candidates/"
  for f in candidates.jsonl items.jsonl changes.jsonl corpus.jsonl eligible.jsonl exclusions.jsonl collection_status.json; do
    cp "$REUSE/$f" "$RUN_DIR/$f"
  done
  jq --arg from "$(basename "$REUSE")" '. + {evidence_reused_from: $from}' "$RUN_DIR/run.json" > "$RUN_DIR/run.json.tmp" && mv "$RUN_DIR/run.json.tmp" "$RUN_DIR/run.json"
  rc_collect=0
else
  pl_log "collection workflow"
  bash workflows/collect_sources.sh "$RUN_DIR"
  rc_collect=$?
fi
if [[ "$(jq -r '.usable // false' "$RUN_DIR/collection_status.json" 2>/dev/null)" == "true" ]]; then
  [[ $rc_collect -ne 0 ]] && pl_log "collection incomplete (see collection_status.json); continuing with usable evidence"
  pl_log "series workflow"
  bash workflows/create_series.sh "$RUN_DIR" || pl_log "series workflow did not complete (see receipts)"
else
  pl_log "no usable evidence; series workflow not started"
fi

summarize "$RUN_DIR"
