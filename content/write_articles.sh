#!/usr/bin/env bash
# content/write_articles.sh RUN_DIR < briefs.jsonl > articles.jsonl
# Generates three Substack article drafts (650-850 words) with inspectable claim markers such as [01-c2]
# from the briefs and their resolved evidence passages. Writes RUN_DIR/articles/01.md, 02.md, 03.md and emits
# manifest records {piece_id, path, claim_ids} (+ word_count, unused_claims, unknown_markers).
set -uo pipefail
source "$(dirname "$0")/../lib/common.sh"
pl_stage_begin write_articles "$@"

cat > "$PL_WORK/input.jsonl"
"$PY" content/draft.py article "$RUN_DIR" "$PL_ERRORS" < "$PL_WORK/input.jsonl" > "$PL_WORK/manifest.jsonl"
rc=$?
cat "$PL_WORK/manifest.jsonl"
in=$(pl_count_lines "$PL_WORK/input.jsonl"); out=$(pl_count_lines "$PL_WORK/manifest.jsonl")
note=$(jq -rs 'map("\(.piece_id):\(.word_count)w") | join(" ")' "$PL_WORK/manifest.jsonl" 2>/dev/null)
status=completed; [[ $rc -ne 0 ]] && status=$([[ $out -gt 0 ]] && echo incomplete || echo failed)
pl_stage_end "$status" "$rc" "$in" "$out" "anthropic-api" "$note"
exit $rc
