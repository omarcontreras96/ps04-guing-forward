#!/usr/bin/env bash
# content/write_video_scripts.sh RUN_DIR < briefs.jsonl > video_scripts.jsonl
# Generates three narrated scene-by-scene scripts for Google Vids with visual directions and on-screen sources
# from the briefs and their resolved evidence passages. Writes RUN_DIR/video_scripts/01.md, 02.md, 03.md and emits
# manifest records {piece_id, path, claim_ids} (+ word_count, unused_claims, unknown_markers).
set -uo pipefail
source "$(dirname "$0")/../lib/common.sh"
pl_stage_begin write_video_scripts "$@"

cat > "$PL_WORK/input.jsonl"
"$PY" content/draft.py script "$RUN_DIR" "$PL_ERRORS" < "$PL_WORK/input.jsonl" > "$PL_WORK/manifest.jsonl"
rc=$?
cat "$PL_WORK/manifest.jsonl"
in=$(pl_count_lines "$PL_WORK/input.jsonl"); out=$(pl_count_lines "$PL_WORK/manifest.jsonl")
note=$(jq -rs 'map("\(.piece_id):\(.word_count)w") | join(" ")' "$PL_WORK/manifest.jsonl" 2>/dev/null)
status=completed; [[ $rc -ne 0 ]] && status=$([[ $out -gt 0 ]] && echo incomplete || echo failed)
pl_stage_end "$status" "$rc" "$in" "$out" "anthropic-api" "$note"
exit $rc
