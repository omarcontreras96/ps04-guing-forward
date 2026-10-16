"""Discover recent videos from configured YouTube channels/playlists/videos (via yt-dlp metadata only).

Identity: item_id = "youtube:<native video id>". published_at = release/upload timestamp from
YouTube (UTC); if only a date is known it is recorded at 00:00:00Z; unknown -> null.
Skips scheduled/live streams and clips shorter than min_seconds (default 180; Shorts/teasers).
Optional include_keywords filter the channel listing by title (scan_depth entries, newest first)
before metadata is fetched; max_items applies after filtering.
"""
import json
import re
import subprocess
import sys
from datetime import datetime, timezone

from util import keyword_match, log_error, now_iso, simulated_failures, sources_of_kind

FIELDS = "%(.{id,title,timestamp,release_timestamp,upload_date,duration,channel,channel_id,live_status,description,webpage_url})j"


def ytdlp(args, timeout=120):
    res = subprocess.run(["yt-dlp", "--no-warnings", "--ignore-config", *args],
                         capture_output=True, text=True, timeout=timeout)
    if res.returncode != 0:
        raise RuntimeError(res.stderr.strip().splitlines()[-1] if res.stderr.strip() else f"yt-dlp exit {res.returncode}")
    return res.stdout


def published(meta):
    ts = meta.get("release_timestamp") or meta.get("timestamp")
    if ts:
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    d = meta.get("upload_date")
    if d and re.fullmatch(r"\d{8}", d):
        return f"{d[:4]}-{d[4:6]}-{d[6:]}T00:00:00Z"
    return None


def main(run_dir, errors_path):
    failed = 0
    simulated = simulated_failures()
    for src in sources_of_kind(run_dir, "youtube"):
        sid = src["source_id"]
        if sid in simulated:
            log_error(errors_path, "SIMULATED FAILURE (deliberate, PIPELINE_SIMULATE_FAILURE): channel not listed", sid)
            failed += 1
            continue
        max_items = int(src.get("max_items", 3))
        try:
            if "watch?v=" in src["url"] or "youtu.be/" in src["url"]:
                ids = [ytdlp(["--print", "%(id)s", "--skip-download", src["url"]]).split()[0]]
            else:
                depth = int(src.get("scan_depth", max_items * 3))
                listing = ytdlp(["--flat-playlist", "--playlist-end", str(depth), "--print", "%(id)s\t%(title)s", src["url"]])
                ids = [line.split("\t", 1)[0] for line in listing.splitlines()
                       if line.strip() and keyword_match(line.split("\t", 1)[-1], src.get("include_keywords"))]
        except Exception as exc:  # noqa: BLE001
            log_error(errors_path, f"listing failed: {exc}", sid)
            failed += 1
            continue

        emitted = 0
        for vid in ids:
            if emitted >= max_items:
                break
            try:
                meta = json.loads(ytdlp(["--skip-download", "-O", FIELDS, f"https://www.youtube.com/watch?v={vid}"]))
            except Exception as exc:  # noqa: BLE001
                log_error(errors_path, f"metadata failed for {vid}: {exc}", sid)
                failed += 1
                continue
            if meta.get("live_status") in ("is_upcoming", "is_live"):
                continue
            if (meta.get("duration") or 0) < int(src.get("min_seconds", 180)):
                continue
            emitted += 1
            print(json.dumps({
                "item_id": f"youtube:{meta['id']}",
                "source_id": sid,
                "publisher_id": src["publisher_id"],
                "kind": "youtube",
                "title": meta.get("title", "").strip(),
                "url": f"https://www.youtube.com/watch?v={meta['id']}",
                "published_at": published(meta),
                "retrieved_at": now_iso(),
                "media_url": None,
                "duration_seconds": meta.get("duration"),
                "channel": meta.get("channel"),
                "source_name": src.get("name", sid),
                "perspective": src.get("perspective"),
                "description_excerpt": (meta.get("description") or "")[:600],
            }))
        print(f"fetch_youtube: {sid}: emitted {emitted}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
