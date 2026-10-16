"""Small shared helpers (no stage logic): hashing, IDs, dates, HTTP, JSONL."""
import calendar
import hashlib
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/129.0 Safari/537.36 GUIngForward-pipeline/1.0")


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def safe_id(item_id):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", item_id)


def struct_to_iso(st):
    """feedparser time.struct_time (UTC) -> ISO 8601 UTC string."""
    if not st:
        return None
    return datetime.fromtimestamp(calendar.timegm(st), tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def canonical_url(url):
    parts = urlsplit(url.strip())
    query = [(k, v) for k, v in parse_qsl(parts.query) if not k.lower().startswith(("utm_", "ref", "source"))]
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path, urlencode(query), ""))


def http_get(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def download(url, dest, timeout=120):
    tmp = dest + ".part"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp, open(tmp, "wb") as fh:
        while True:
            chunk = resp.read(1 << 20)
            if not chunk:
                break
            fh.write(chunk)
    os.replace(tmp, dest)


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def read_jsonl(path):
    out = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    out.append(json.loads(line))
    return out


def sources_of_kind(run_dir, kind):
    return [s for s in load_json(os.path.join(run_dir, "config", "sources.json")) if s.get("kind") == kind]


def simulated_failures():
    """Deliberately simulated collection failures (labelled), from PIPELINE_SIMULATE_FAILURE=src1,src2."""
    return {s.strip() for s in os.environ.get("PIPELINE_SIMULATE_FAILURE", "").split(",") if s.strip()}


def log_error(errors_path, message, subject=None):
    with open(errors_path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"message": message, "subject": subject, "at": now_iso()}) + "\n")


def keyword_match(text, keywords):
    if not keywords:
        return True
    low = text.lower()
    return any(re.search(r"(?<![a-z])" + re.escape(k.lower()) + r"(?![a-z])", low) for k in keywords)
