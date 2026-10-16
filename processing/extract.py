"""Turn candidates into normalized evidence items with retained text and timestamped transcripts.

Per kind:
  feed     full article text: feed-supplied content if substantive, else the fetched page (trafilatura);
           arXiv abstract pages are swapped for the arXiv HTML full text when available.
  youtube  YouTube captions (manual preferred, else auto) via yt-dlp json3; if none, audio + whisper.cpp.
  podcast  enclosure audio downloaded to data/media/podcasts/, transcribed locally with whisper.cpp.
Transcripts are grouped into ~30-second segments: {segment_id, start_seconds, end_seconds, text}.

Reuse: before any download, the stored item is fetched through `data/store.sh get`. If title, URL,
publication date (and, for feeds, the feed's updated timestamp) are unchanged and the retained assets
exist, the stored version is reused without re-fetching or re-transcribing.

Assets are content-addressed (…-<sha12>.txt/.json) so an asset referenced by an earlier run is never
overwritten. version_id = sha256 of compact sorted JSON {title, url, published_at, text, segments}
(retrieved_at is deliberately excluded).
"""
import html as htmlmod
import json
import os
import re
import subprocess
import sys
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor

import trafilatura

from util import download, http_get, load_json, log_error, safe_id, sha256

TEXT_DIR = os.path.join("data", "assets", "text")
SEG_DIR = os.path.join("data", "assets", "segments")
YT_MEDIA = os.path.join("data", "media", "youtube")
POD_MEDIA = os.path.join("data", "media", "podcasts")
FEED_MEDIA = os.path.join("data", "media", "feeds")
WHISPER_MODEL = os.environ.get("WHISPER_MODEL", os.path.expanduser("~/.cache/whisper-cpp/ggml-base.en.bin"))
REQUIRED = ["item_id", "source_id", "publisher_id", "kind", "title", "url", "published_at", "retrieved_at", "media_url"]

whisper_lock = threading.Lock()


class ExtractionError(Exception):
    pass


def words(text):
    return len((text or "").split())


def html_to_text(fragment):
    txt = trafilatura.extract(f"<html><body><article>{fragment}</article></body></html>", favor_recall=True) or ""
    if words(txt) < 50:  # trafilatura drops short fragments; fall back to a plain tag strip
        txt = htmlmod.unescape(re.sub(r"<[^>]+>", " ", fragment))
    return re.sub(r"[ \t]+", " ", txt).strip()


def version_id(item, text, segments):
    payload = {"title": item["title"], "url": item["url"], "published_at": item["published_at"],
               "text": text, "segments": segments}
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False))


def write_asset(directory, item_id, content, ext):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, f"{safe_id(item_id)}-{sha256(content)[:12]}.{ext}")
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
    return path


def group_segments(pieces, target=30.0, hard_max=45.0):
    """pieces: [(start, end, text)] in order -> ~30 s segments with stable sequential IDs."""
    segs, cur, cur_start, cur_end = [], [], None, None
    for start, end, text in pieces:
        text = text.strip()
        if not text:
            continue
        if cur_start is None:
            cur_start = start
        cur.append(text)
        cur_end = max(end, start)
        span = cur_end - cur_start
        if span >= hard_max or (span >= target and re.search(r"[.?!]$", text)):
            segs.append((cur_start, cur_end, " ".join(cur)))
            cur, cur_start = [], None
    if cur:
        segs.append((cur_start, cur_end, " ".join(cur)))
    return [{"segment_id": f"seg-{i + 1:04d}", "start_seconds": round(s, 2), "end_seconds": round(e, 2),
             "text": re.sub(r"\s+", " ", t)} for i, (s, e, t) in enumerate(segs)]


# ---------------------------------------------------------------- written items
def extract_feed(c):
    feed_txt = ""
    if c.get("feed_content_path") and os.path.exists(c["feed_content_path"]):
        with open(c["feed_content_path"], encoding="utf-8") as fh:
            feed_txt = html_to_text(fh.read())
    if words(feed_txt) >= 300:
        return feed_txt, "feed_content"

    url = c["url"]
    m = re.match(r"https?://arxiv\.org/abs/([^?#]+)", url)
    fetch_urls = ([f"https://arxiv.org/html/{m.group(1)}"] if m else []) + [url]
    last_err = None
    for fu in fetch_urls:
        try:
            page = http_get(fu).decode("utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            continue
        txt = trafilatura.extract(page, url=fu, favor_recall=True, include_comments=False) or ""
        if words(txt) >= 150:
            os.makedirs(FEED_MEDIA, exist_ok=True)
            write_asset(FEED_MEDIA, c["item_id"] + "-page", page, "html")
            return txt.strip(), "fetched_page" if fu == url else "fetched_arxiv_html"
    if words(feed_txt) >= 120:
        return feed_txt, "feed_content_short"
    raise ExtractionError(f"no substantive text (feed {words(feed_txt)} words; page error: {last_err})")


# ---------------------------------------------------------------- transcripts
def whisper_pieces(audio_path, max_seconds):
    if not os.path.exists(WHISPER_MODEL):
        raise ExtractionError(f"whisper model not found at {WHISPER_MODEL} (set WHISPER_MODEL)")
    with tempfile.TemporaryDirectory() as tmp:
        wav = os.path.join(tmp, "audio.wav")
        cmd = ["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", audio_path]
        if max_seconds:
            cmd += ["-t", str(int(max_seconds))]
        subprocess.run(cmd + ["-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", wav], check=True, timeout=900)
        with whisper_lock:  # one transcription at a time; whisper.cpp already uses all cores / GPU
            res = subprocess.run(["whisper-cli", "-m", WHISPER_MODEL, "-f", wav, "-l", "en", "-t", "8", "-np",
                                  "-oj", "-of", os.path.join(tmp, "out")], capture_output=True, text=True, timeout=3600)
        if res.returncode != 0:
            raise ExtractionError(f"whisper-cli failed: {res.stderr.strip()[-300:]}")
        data = load_json(os.path.join(tmp, "out.json"))
    return [(t["offsets"]["from"] / 1000, t["offsets"]["to"] / 1000, t["text"]) for t in data.get("transcription", [])]


def caption_pieces(path):
    data = load_json(path)
    pieces = []
    for ev in data.get("events", []):
        if "segs" not in ev:
            continue
        text = "".join(s.get("utf8", "") for s in ev["segs"]).replace("\n", " ").strip()
        if text:
            start = ev.get("tStartMs", 0) / 1000
            pieces.append((start, start + ev.get("dDurationMs", 0) / 1000, text))
    return pieces


def extract_youtube(c, max_seconds):
    vid = c["item_id"].split(":", 1)[1]
    os.makedirs(YT_MEDIA, exist_ok=True)
    existing = sorted(f for f in os.listdir(YT_MEDIA) if f.startswith(vid + ".") and f.endswith(".json3"))
    if not existing:
        subprocess.run(["yt-dlp", "--no-warnings", "--ignore-config", "--skip-download", "--write-subs",
                        "--write-auto-subs", "--sub-langs", "en,en-US,en-GB,en-orig", "--sub-format", "json3",
                        "-o", os.path.join(YT_MEDIA, "%(id)s.%(ext)s"), c["url"]],
                       capture_output=True, text=True, timeout=300)
        existing = sorted(f for f in os.listdir(YT_MEDIA) if f.startswith(vid + ".") and f.endswith(".json3"))
    # Prefer human captions (en / en-US / en-GB) over auto-generated (en-orig is the ASR track).
    for f in sorted(existing, key=lambda n: (".en-orig." in n, n)):
        pieces = caption_pieces(os.path.join(YT_MEDIA, f))
        if pieces:
            if max_seconds:
                pieces = [p for p in pieces if p[0] < max_seconds]
            return pieces, f"youtube_captions:{f.split('.')[-2]}"
    # No captions: fall back to local transcription of the audio track.
    audio = os.path.join(YT_MEDIA, f"{vid}.m4a")
    if not os.path.exists(audio):
        res = subprocess.run(["yt-dlp", "--no-warnings", "--ignore-config", "-f", "bestaudio[ext=m4a]/bestaudio",
                              "-o", audio, c["url"]], capture_output=True, text=True, timeout=900)
        if res.returncode != 0:
            raise ExtractionError(f"no captions and audio download failed: {res.stderr.strip()[-300:]}")
    return whisper_pieces(audio, max_seconds), "whisper.cpp"


def extract_podcast(c, max_seconds):
    if not c.get("media_url"):
        raise ExtractionError("podcast candidate has no audio enclosure URL")
    os.makedirs(POD_MEDIA, exist_ok=True)
    ext = os.path.splitext(c["media_url"].split("?")[0])[1] or ".mp3"
    audio = os.path.join(POD_MEDIA, safe_id(c["item_id"]) + ext[:5])
    if not os.path.exists(audio):
        download(c["media_url"], audio)
    return whisper_pieces(audio, max_seconds), "whisper.cpp"


# ---------------------------------------------------------------- orchestration per item
def stored_item(item_id):
    res = subprocess.run(["bash", "data/store.sh", "get", item_id], capture_output=True, text=True)
    return json.loads(res.stdout) if res.returncode == 0 and res.stdout.strip() else None


def reusable(c, s):
    if not s:
        return False
    same = all(c.get(k) == s.get(k) for k in ("title", "url", "published_at"))
    if c["kind"] == "feed":
        same = same and c.get("updated_at") == s.get("updated_at")
    if c["kind"] == "podcast":
        same = same and c.get("media_url") == s.get("media_url")
    assets_ok = os.path.exists(s.get("text_path") or "") and (s.get("segments_path") is None or os.path.exists(s["segments_path"]))
    return same and assets_ok


def process(c, max_seconds):
    s = stored_item(c["item_id"])
    if reusable(c, s):
        item = dict(c)
        for k in ("version_id", "text_path", "segments_path", "word_count", "segment_count", "transcript_seconds",
                  "transcript_truncated", "extraction_method"):
            if k in s:
                item[k] = s[k]
        item["extraction"] = "reused_stored_version"
        return item

    if c["kind"] == "feed":
        text, method = extract_feed(c)
        segments = None
    else:
        pieces, method = extract_youtube(c, max_seconds) if c["kind"] == "youtube" else extract_podcast(c, max_seconds)
        segments = group_segments(pieces)
        if len(segments) < 3:
            raise ExtractionError(f"transcript too short ({len(segments)} segments)")
        text = "\n".join(s["text"] for s in segments)

    item = dict(c)
    item["version_id"] = version_id(c, text, segments)
    item["text_path"] = write_asset(TEXT_DIR, c["item_id"], text, "txt")
    item["segments_path"] = (write_asset(SEG_DIR, c["item_id"], json.dumps(segments, indent=1, ensure_ascii=False), "json")
                             if segments is not None else None)
    item["extraction_method"] = method
    item["extraction"] = "extracted"
    item["word_count"] = words(text)
    if segments is not None:
        item["segment_count"] = len(segments)
        item["transcript_seconds"] = segments[-1]["end_seconds"]
        dur = c.get("duration_seconds")
        item["transcript_truncated"] = bool(max_seconds and dur and dur > max_seconds + 5)
    return item


def main(run_dir, errors_path):
    max_minutes = load_json(os.path.join(run_dir, "config", "project.json")).get("pipeline", {}).get("max_transcribe_minutes", 90)
    max_seconds = int(max_minutes * 60) if max_minutes else None
    candidates = []
    for n, line in enumerate(sys.stdin, 1):
        if not line.strip():
            continue
        try:
            c = json.loads(line)
        except json.JSONDecodeError:
            print(f"extract: line {n} is not valid JSON", file=sys.stderr)
            return 2
        missing = [k for k in REQUIRED if k not in c]
        if missing:
            print(f"extract: line {n} missing {missing}", file=sys.stderr)
            return 2
        candidates.append(c)

    seen, unique = set(), []
    for c in candidates:  # the same candidate discovered twice is processed once
        if c["item_id"] not in seen:
            seen.add(c["item_id"])
            unique.append(c)

    def run(c):
        try:
            item = process(c, max_seconds)
            print(f"extract: {c['item_id']}: {item['extraction']} ({item.get('extraction_method')}, {item.get('word_count')} words)",
                  file=sys.stderr)
            return item
        except Exception as exc:  # noqa: BLE001 - every inaccessible item is reported, the rest continue
            log_error(errors_path, f"extraction failed: {type(exc).__name__}: {exc}", c["item_id"])
            print(f"extract: {c['item_id']}: FAILED {exc}", file=sys.stderr)
            return None

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run, unique))
    failed = 0
    for item in results:
        if item is None:
            failed += 1
        else:
            print(json.dumps(item, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
