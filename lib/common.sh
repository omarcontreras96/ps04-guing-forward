#!/usr/bin/env bash
# Shared shell helpers sourced by every pipeline component.
# Holds only plumbing (paths, interpreter, receipts); no stage logic lives here.

PL_REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PL_REPO_ROOT

# Credentials come from the environment or an untracked .env file (never committed).
if [[ -f "$PL_REPO_ROOT/.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  . "$PL_REPO_ROOT/.env"
  set +a
fi

# Python interpreter: explicit override, then the project venv, then system python3.
PY="${PIPELINE_PYTHON:-}"
if [[ -z "$PY" ]]; then
  for candidate in .venv.nosync/bin/python .venv/bin/python; do
    if [[ -x "$PL_REPO_ROOT/$candidate" ]]; then PY="$PL_REPO_ROOT/$candidate"; break; fi
  done
fi
PY="${PY:-python3}"
export PY
export PYTHONPATH="$PL_REPO_ROOT/lib${PYTHONPATH:+:$PYTHONPATH}"
export PYTHONDONTWRITEBYTECODE=1

pl_now() { date -u +%Y-%m-%dT%H:%M:%SZ; }
pl_log() { echo "[$(date -u +%H:%M:%S)] ${PL_STAGE:-pipeline}: $*" >&2; }

# Convert a RUN_DIR argument (relative to the caller's cwd) into a repo-relative path.
pl_relpath() {
  local abs
  abs="$(cd "$1" 2>/dev/null && pwd)" || return 1
  if [[ "$abs" == "$PL_REPO_ROOT" ]]; then echo "."; return 0; fi
  if [[ "$abs" == "$PL_REPO_ROOT/"* ]]; then echo "${abs#"$PL_REPO_ROOT"/}"; else echo "$abs"; fi
}

# pl_stage_begin STAGE RUN_DIR — validate arguments, cd to the repo root, open a work area.
# Exits 2 (invalid arguments) when RUN_DIR is missing or lacks run.json.
pl_stage_begin() {
  PL_STAGE="$1"; shift
  if [[ $# -lt 1 || -z "${1:-}" ]]; then
    echo "usage: $PL_STAGE RUN_DIR" >&2; exit 2
  fi
  if [[ ! -f "$1/run.json" ]]; then
    echo "$PL_STAGE: '$1' is not a run directory (missing run.json)" >&2; exit 2
  fi
  RUN_DIR="$(pl_relpath "$1")"
  cd "$PL_REPO_ROOT" || exit 1
  mkdir -p "$RUN_DIR/logs"
  PL_STARTED="$(pl_now)"
  PL_WORK="$(mktemp -d "$RUN_DIR/logs/.work-$PL_STAGE-XXXXXX")"
  PL_ERRORS="$PL_WORK/errors.jsonl"
  export LLM_USAGE_FILE="$PL_WORK/llm_usage.jsonl"
  export PL_STAGE RUN_DIR PL_STARTED PL_WORK PL_ERRORS
  : > "$PL_ERRORS"
}

# pl_stage_end STATUS EXIT_CODE INPUT_COUNT OUTPUT_COUNT TOOLS [NOTE] — write the receipt.
# STATUS: completed | incomplete | failed. Counts may be "null".
pl_stage_end() {
  "$PY" "$PL_REPO_ROOT/lib/receipt.py" \
    --run-dir "$RUN_DIR" --stage "$PL_STAGE" --status "$1" --exit-code "$2" \
    --started "$PL_STARTED" --input-count "$3" --output-count "$4" \
    --tools "$5" --note "${6:-}" \
    --errors-file "$PL_ERRORS" --usage-file "$LLM_USAGE_FILE" >/dev/null \
    || echo "$PL_STAGE: warning: could not write receipt" >&2
  rm -rf "$PL_WORK"
}

# pl_error MESSAGE [ITEM_OR_SOURCE] — append a structured error for the receipt.
pl_error() {
  jq -cn --arg m "$1" --arg s "${2:-}" '{message:$m, subject:(if $s == "" then null else $s end), at:(now|todate)}' >> "$PL_ERRORS"
}

pl_count_lines() { if [[ -f "$1" ]]; then grep -c . "$1" || true; else echo 0; fi; }
