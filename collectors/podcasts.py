"""Discover recent episodes (with audio enclosure URLs) from configured podcast RSS feeds.

Optional include_keywords: theme filter over episode title + description (discovery only; editorial
relevance is still judged in editorial/select_items.sh). max_items applies after filtering.

Identity: item_id = "podcast:<publisher_id>:" + first 12 hex of sha256(episode GUID, else enclosure URL).
"""
import json
import sys

import feedparser

from util import http_get, keyword_match, log_error, now_iso, sha256, simulated_failures, sources_of_kind, struct_to_iso


def duration_seconds(value):
    if not value:
        return None
    try:
        parts = [float(p) for p in str(value).split(":")]
    except ValueError:
        return None
    secs = 0.0
    for p in parts:
        secs = secs * 60 + p
    return int(secs)


def main(run_dir, errors_path):
    failed = 0
    simulated = simulated_failures()
    for src in sources_of_kind(run_dir, "podcast"):
        sid = src["source_id"]
        if sid in simulated:
            log_error(errors_path, "SIMULATED FAILURE (deliberate, PIPELINE_SIMULATE_FAILURE): podcast feed not fetched", sid)
            failed += 1
            continue
        try:
            parsed = feedparser.parse(http_get(src["url"]))
            if not parsed.entries:
                raise ValueError(f"no entries ({parsed.get('bozo_exception', 'empty feed')})")
        except Exception as exc:  # noqa: BLE001
            log_error(errors_path, f"podcast feed fetch failed: {exc}", sid)
            failed += 1
            continue
        retrieved = now_iso()
        episodes = []
        for e in parsed.entries:
            audio = next((l.get("href") for l in e.get("links", [])
                          if l.get("rel") == "enclosure" and str(l.get("type", "")).startswith("audio")), None)
            if not audio:
                continue
            if not keyword_match(f"{e.get('title', '')} {e.get('summary', '')[:3000]}", src.get("include_keywords")):
                continue
            pub = struct_to_iso(e.get("published_parsed"))
            episodes.append((pub or "", e, audio, pub))
        episodes.sort(key=lambda t: t[0], reverse=True)
        for _, e, audio, pub in episodes[: int(src.get("max_items", 3))]:
            key = e.get("id") or audio
            print(json.dumps({
                "item_id": f"podcast:{src['publisher_id']}:{sha256(key)[:12]}",
                "source_id": sid,
                "publisher_id": src["publisher_id"],
                "kind": "podcast",
                "title": (e.get("title") or "").strip(),
                "url": e.get("link") or audio,
                "published_at": pub,
                "retrieved_at": retrieved,
                "media_url": audio,
                "episode_guid": e.get("id"),
                "duration_seconds": duration_seconds(e.get("itunes_duration")),
                "source_name": src.get("name", sid),
                "perspective": src.get("perspective"),
                "description_excerpt": (e.get("summary") or "")[:600],
            }))
        print(f"fetch_podcasts: {sid}: {len(episodes)} matching episodes with audio, emitted {min(len(episodes), int(src.get('max_items', 3)))}",
              file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
