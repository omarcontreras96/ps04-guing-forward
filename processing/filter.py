"""Mechanical eligibility check (no editorial judgment).

Window: for as-of date D (run.json), eligible publication dates are D-29 .. D inclusive (UTC).
Reasons: unknown_date, invalid_date, future_date, outside_window, and duplicate_recording
(a YouTube upload and a podcast episode from the same publisher with near-identical titles are
one underlying recording; the podcast copy is kept as canonical).
"""
import difflib
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone


def parse_date(value):
    s = value.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return date.fromisoformat(s)
    dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).date()


def norm_title(t):
    t = re.sub(r"\(.*?\)|\[.*?\]|#\d+|ep(isode)?\.?\s*\d+", " ", (t or "").lower())
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


def main(run_dir, exclusions_path):
    with open(f"{run_dir}/run.json", encoding="utf-8") as fh:
        as_of = date.fromisoformat(json.load(fh)["as_of_date"])
    start = as_of - timedelta(days=29)
    window = f"{start.isoformat()}..{as_of.isoformat()}"

    items, exclusions = [], []
    for n, line in enumerate(sys.stdin, 1):
        if not line.strip():
            continue
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError:
            print(f"filter: line {n} is not valid JSON", file=sys.stderr)
            sys.exit(2)

    def exclude(item, reason, detail):
        exclusions.append({"item_id": item.get("item_id"), "version_id": item.get("version_id"),
                           "reason": reason, "detail": detail,
                           "published_at": item.get("published_at"), "window": window})

    dated = []
    for item in items:
        pub = item.get("published_at")
        if pub is None or (isinstance(pub, str) and not pub.strip()):
            exclude(item, "unknown_date", "No publication date; undated material cannot support claims.")
            continue
        try:
            d = parse_date(str(pub))
        except (ValueError, TypeError):
            exclude(item, "invalid_date", f"Unparseable publication date {pub!r}.")
            continue
        if d > as_of:
            exclude(item, "future_date", f"Published {d} is after the as-of date {as_of}.")
        elif d < start:
            exclude(item, "outside_window", f"Published {d}, before window start {start} ({(as_of - d).days} days old).")
        else:
            dated.append(item)

    # Reconcile the same recording published as both podcast audio and a YouTube upload.
    podcasts = [i for i in dated if i.get("kind") == "podcast"]
    eligible = []
    for item in dated:
        if item.get("kind") == "youtube":
            twin = next((p for p in podcasts if p.get("publisher_id") == item.get("publisher_id") and
                         difflib.SequenceMatcher(None, norm_title(p.get("title")), norm_title(item.get("title"))).ratio() >= 0.85),
                        None)
            if twin:
                exclude(item, "duplicate_recording",
                        f"Same recording as podcast item {twin['item_id']}; counted once via the podcast copy.")
                continue
        eligible.append(item)

    with open(exclusions_path, "w", encoding="utf-8") as fh:
        for e in exclusions:
            fh.write(json.dumps(e) + "\n")
    for item in eligible:
        print(json.dumps(item))
    print(f"filter: window {window}: {len(eligible)} eligible, {len(exclusions)} excluded", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
