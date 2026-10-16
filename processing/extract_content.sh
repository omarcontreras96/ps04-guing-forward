#!/usr/bin/env bash
# processing/extract_content.sh RUN_DIR < candidates.jsonl > items.jsonl
# Retrieve full written text or media, prepare timestamped transcripts, and emit normalized items.
# Retained assets: data/assets/text/, data/assets/segments/; original downloads: data/media/.
# Unchanged stored material is reused (queried through data/store.sh get), not re-fetched.
# Exit 1 when some items could not be processed (they are listed in the receipt); 2 on malformed input.
set -uo pipefail
source "$(dirname "$0")/../lib/common.sh"
pl_stage_begin extract_content "$@"

cat > "$PL_WORK/input.jsonl"
"$PY" processing/extract.py "$RUN_DIR" "$PL_ERRORS" < "$PL_WORK/input.jsonl" > "$PL_WORK/items.jsonl"
rc=$?
cat "$PL_WORK/items.jsonl"

in=$(pl_count_lines "$PL_WORK/input.jsonl"); out=$(pl_count_lines "$PL_WORK/items.jsonl")
note=$(jq -rs 'group_by(.extraction) | map("\(.[0].extraction)=\(length)") | join(" ")' "$PL_WORK/items.jsonl" 2>/dev/null)
status=completed; [[ $rc -eq 1 ]] && status=incomplete; [[ $rc -ge 2 ]] && status=failed
pl_stage_end "$status" "$rc" "$in" "$out" "urllib,trafilatura,yt-dlp,ffmpeg,whisper.cpp($(basename "${WHISPER_MODEL:-ggml-base.en.bin}"))" "$note"
exit $rc
