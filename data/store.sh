#!/usr/bin/env bash
# data/store.sh — the only component that reads or writes the evidence index (data/evidence/).
#
#   bash data/store.sh init                         create missing storage, never erases evidence
#   bash data/store.sh upsert RUN_DIR < items.jsonl  save new items/versions, emit one change record per input
#   bash data/store.sh list                         latest version of every stored item (JSONL)
#   bash data/store.sh get ITEM_ID [VERSION_ID]      one item (latest when VERSION_ID omitted); exit 1 if absent
#   bash data/store.sh history ITEM_ID               version history with the runs that observed each version
#
# Backend: SQLite at data/evidence/evidence.sqlite (see data/store_db.py for the schema).
# Exit codes: 0 ok, 1 not found / operational failure, 2 invalid arguments or malformed input.
set -uo pipefail
source "$(dirname "$0")/../lib/common.sh"

if [[ "${1:-}" == "upsert" ]]; then
  # Only upsert belongs to a run, so only upsert writes a receipt.
  [[ $# -eq 2 ]] || { echo "usage: store.sh upsert RUN_DIR" >&2; exit 2; }
  pl_stage_begin store_upsert "$2"
  "$PY" data/store_db.py upsert "$RUN_DIR" > "$PL_WORK/changes.jsonl"
  rc=$?
  cat "$PL_WORK/changes.jsonl"
  out=$(pl_count_lines "$PL_WORK/changes.jsonl")
  summary=$(jq -rs 'group_by(.change) | map("\(.[0].change)=\(length)") | join(" ")' "$PL_WORK/changes.jsonl")
  if [[ $rc -eq 0 ]]; then
    pl_stage_end completed 0 "$out" "$out" "sqlite3" "$summary"
  else
    pl_error "upsert failed with exit $rc"
    pl_stage_end failed "$rc" null "$out" "sqlite3"
  fi
  exit $rc
fi

cd "$PL_REPO_ROOT" || exit 1
exec "$PY" data/store_db.py "$@"
