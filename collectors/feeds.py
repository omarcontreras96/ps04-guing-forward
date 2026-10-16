"""Discover written items from configured RSS/Atom feeds and emit candidate JSONL.

Identity: item_id = "feed:<publisher_id>:" + first 12 hex of sha256(canonical article URL).
Dates come from the entry's published (else updated) timestamp; missing -> null (never invented).
Optional per-source settings: max_items (most recent N after keyword filtering),
include_keywords (discovery filter for broad feeds), name, perspective.
Full entry content shipped inside the feed is kept as an original download in data/media/feeds/.
"""
import html
import json
import os
import sys

import feedparser

from util import (canonical_url, http_get, keyword_match, log_error, now_iso, safe_id, sha256,
                  simulated_failures, sources_of_kind, struct_to_iso)

MEDIA_DIR = os.path.join("data", "media", "feeds")


def entry_html(entry):
    if entry.get("content"):
        return max((c.get("value", "") for c in entry["content"]), key=len)
    return entry.get("summary", "") or ""


def main(run_dir, errors_path):
    failed = 0
    simulated = simulated_failures()
    os.makedirs(MEDIA_DIR, exist_ok=True)
    for src in sources_of_kind(run_dir, "feed"):
        sid = src["source_id"]
        if sid in simulated:
            log_error(errors_path, "SIMULATED FAILURE (deliberate, PIPELINE_SIMULATE_FAILURE): feed not fetched", sid)
            failed += 1
            continue
        try:
            raw = http_get(src["url"])
            parsed = feedparser.parse(raw)
            if parsed.bozo and not parsed.entries:
                raise ValueError(f"unparseable feed: {parsed.bozo_exception}")
        except Exception as exc:  # noqa: BLE001 - report every source failure
            log_error(errors_path, f"feed fetch failed: {exc}", sid)
            failed += 1
            continue

        retrieved = now_iso()
        entries = []
        for e in parsed.entries:
            link = e.get("link")
            if not link:
                continue
            text_for_filter = " ".join([e.get("title", ""), e.get("summary", "")[:2000],
                                        " ".join(t.get("term", "") for t in e.get("tags", []))])
            if not keyword_match(text_for_filter, src.get("include_keywords")):
                continue
            published = struct_to_iso(e.get("published_parsed")) or struct_to_iso(e.get("updated_parsed"))
            entries.append((published or "", e, link, published))
        entries.sort(key=lambda t: t[0], reverse=True)

        for _, e, link, published in entries[: int(src.get("max_items", 8))]:
            url = canonical_url(link)
            item_id = f"feed:{src['publisher_id']}:{sha256(url)[:12]}"
            content_html = entry_html(e)
            content_path = None
            if content_html.strip():
                content_path = os.path.join(MEDIA_DIR, f"{safe_id(item_id)}-{sha256(content_html)[:12]}.html")
                if not os.path.exists(content_path):
                    with open(content_path, "w", encoding="utf-8") as fh:
                        fh.write(content_html)
            print(json.dumps({
                "item_id": item_id,
                "source_id": sid,
                "publisher_id": src["publisher_id"],
                "kind": "feed",
                "title": html.unescape((e.get("title") or "").strip()),
                "url": url,
                "published_at": published,
                "retrieved_at": retrieved,
                "media_url": None,
                "updated_at": struct_to_iso(e.get("updated_parsed")),
                "source_name": src.get("name", sid),
                "perspective": src.get("perspective"),
                "author": e.get("author"),
                "feed_content_path": content_path,
            }))
        print(f"fetch_feeds: {sid}: {len(entries)} matching entries, emitted {min(len(entries), int(src.get('max_items', 8)))}",
              file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
