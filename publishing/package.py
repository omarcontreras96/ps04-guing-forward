"""Assemble the production package after human approval.

Preconditions, all verified here even when invoked directly:
  * review/check_content.sh run now yields passed=true,
  * its review_id equals review.json's and approval.json's (so nothing changed since review),
  * approval.json says decision=approve.
Otherwise list what is missing or stale and exit 1.

Package contents (RUN_DIR/package/):
  articles/NN.md               reader-facing article: claim markers become numbered sources, AI disclosure added
  video_scripts/NN.md          Google Vids script: narration without markers, sources kept on screen
  youtube/NN_description.txt   YouTube description: article link, as-of date, timestamped sources, disclosure
  sources/NN.md                source notes: every claim -> item/version -> exact passage or timestamp
  MANUAL_STEPS.md              remaining human steps (Google Vids, YouTube, Substack)
  publication_links.json       {piece_id, substack_url, youtube_url}; existing entries are preserved
  manifest.json                asset list by piece (also printed on stdout)
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

from evidence import claim_sources
from util import load_json, read_jsonl

PIECES = ["01", "02", "03"]
MARKER = re.compile(r"\[(\d{2}-c\d+)\]")


def fail(problems):
    for p in problems:
        print(f"prepare_package: {p}", file=sys.stderr)
    sys.exit(1)


def source_line(s):
    when = f", at {s['timestamp'].split('-')[0]}" if s.get("timestamp") else ""
    return f"{s['publisher']}, “{s['title']}” ({s['date']}{when}): {s['link']}"


def main(run_dir):
    problems = []
    for f in ("review.json", "approval.json"):
        if not os.path.exists(os.path.join(run_dir, f)):
            problems.append(f"missing {f}" + (" (create it after reviewing: review/record_approval.sh)" if f == "approval.json" else ""))
    if problems:
        fail(problems)
    review = load_json(os.path.join(run_dir, "review.json"))
    approval = load_json(os.path.join(run_dir, "approval.json"))
    res = subprocess.run(["bash", "review/check_content.sh", run_dir], capture_output=True, text=True)
    if res.returncode != 0:
        fail(["content check could not run: " + res.stderr.strip()[-300:]])
    current = json.loads(res.stdout)
    if current["review_id"] != review["review_id"]:
        problems.append("review.json is stale: drafts, briefs or evidence changed since it was produced; rerun checks")
    if approval.get("review_id") != current["review_id"]:
        problems.append("approval.json does not match the current review_id; the reviewed material changed or was never approved")
    if not current["passed"]:
        problems.append(f"current content check does not pass ({current['error_count']} errors)")
    if approval.get("decision") != "approve":
        problems.append(f"approval decision is {approval.get('decision')!r}, not 'approve'")
    for f in ("reviewer", "reviewed_at"):
        if not approval.get(f):
            problems.append(f"approval.json has no {f}")
    if problems:
        fail(problems)

    run = load_json(os.path.join(run_dir, "run.json"))
    cfg = load_json(os.path.join(run_dir, "config", "project.json"))
    briefs = {b["piece_id"]: b for b in read_jsonl(os.path.join(run_dir, "briefs.jsonl"))}
    pkg = os.path.join(run_dir, "package")
    for d in ("articles", "video_scripts", "youtube", "sources"):
        os.makedirs(os.path.join(pkg, d), exist_ok=True)

    links_path = os.path.join(pkg, "publication_links.json")
    links = {l["piece_id"]: l for l in load_json(links_path)} if os.path.exists(links_path) else {}
    links = [links.get(p, {"piece_id": p, "substack_url": None, "youtube_url": None}) for p in PIECES]
    with open(links_path, "w", encoding="utf-8") as fh:
        json.dump(links, fh, indent=2)
        fh.write("\n")
    link_of = {l["piece_id"]: l for l in links}

    disclosure = (f"*How this was made: {cfg['publication_name']} uses an AI-assisted research pipeline. Sources published "
                  f"in the 30 days before {run['as_of_date']} were collected automatically; an AI model (Anthropic Claude) "
                  "helped select evidence and draft this piece under a published editorial policy, and a human editor "
                  f"({approval['reviewer']}) reviewed the claims and sources before publication.*")
    pieces = []
    for pid in PIECES:
        b = briefs[pid]
        sources = claim_sources(b)
        statements = {c["claim_id"]: c for c in b["claims"]}
        yt = link_of[pid]["youtube_url"] or "{YOUTUBE_URL}"
        sub = link_of[pid]["substack_url"] or "{ARTICLE_URL}"

        # Article: markers -> [n] in order of first use; model reference list replaced by verified sources.
        md = open(os.path.join(run_dir, "articles", f"{pid}.md"), encoding="utf-8").read()
        body = re.split(r"\n##\s+References", md, maxsplit=1)[0].rstrip()
        order = []
        for m in MARKER.findall(body):
            if m not in order:
                order.append(m)
        num = {cid: i + 1 for i, cid in enumerate(order)}
        body = MARKER.sub(lambda m: f"[{num[m.group(1)]}]" if m.group(1) in num else "", body)
        refs = ["## Sources", ""]
        for cid in order:
            refs.append(f"**[{num[cid]}]** {statements[cid]['statement']}  ")
            for s in sources.get(cid, []):
                refs.append(f"- {source_line(s)}")
            refs.append("")
        article = (body + f"\n\n*Watch the video version: {yt}*\n\n" + "\n".join(refs) + "\n---\n\n" + disclosure + "\n")
        a_path = os.path.join(pkg, "articles", f"{pid}.md")
        open(a_path, "w", encoding="utf-8").write(article)

        # Script: strip markers from narration, separate the YouTube description.
        sc = open(os.path.join(run_dir, "video_scripts", f"{pid}.md"), encoding="utf-8").read()
        parts = re.split(r"\n##\s+YouTube description", sc, maxsplit=1)
        script = MARKER.sub("", parts[0]).replace(" .", ".").rstrip() + "\n"
        s_path = os.path.join(pkg, "video_scripts", f"{pid}.md")
        open(s_path, "w", encoding="utf-8").write(script)
        summary = ""
        if len(parts) > 1:
            summary = re.split(r"\n\s*(?:\*\*)?Sources", parts[1], maxsplit=1)[0]
            summary = MARKER.sub("", summary).replace("{ARTICLE_URL}", sub).strip()
        desc = [summary or b["argument"], "", f"Full article: {sub}", f"As of {run['as_of_date']}.", "", "Sources (timestamps link to the cited passage):"]
        seen = set()
        for cid in [c["claim_id"] for c in b["claims"]]:
            for s in sources.get(cid, []):
                key = (s["link"], s.get("timestamp"))
                if key not in seen:
                    seen.add(key)
                    desc.append(f"- {source_line(s)}")
        desc += ["", "Made with an AI-assisted pipeline: script drafted with Anthropic Claude from human-reviewed evidence; "
                     "voiceover and visuals produced in Google Vids. Claims and sources were checked by a human editor."]
        d_path = os.path.join(pkg, "youtube", f"{pid}_description.txt")
        open(d_path, "w", encoding="utf-8").write("\n".join(desc) + "\n")

        # Source notes for reviewers and graders.
        notes = [f"# Source notes: piece {pid}: {b['title']}", "", f"**Argument:** {b['argument']}", "",
                 f"**Synthesis:** {b['synthesis']}", "", f"**Limitations:** {b['limitations']}", ""]
        for c in b["claims"]:
            notes.append(f"## {c['claim_id']} ({c['type']})")
            notes.append(c["statement"])
            for s in sources.get(c["claim_id"], []):
                loc = (f"segment {s['locator']['segment_id']} ({s['timestamp']})" if s["locator"]["type"] == "segment"
                       else "exact quote")
                notes.append(f"- {source_line(s)}  \n  item `{s['item_id']}` version `{s['version_id'][:16]}…`, {loc}:  \n"
                             f"  > {s['passage']}")
            notes.append("")
        n_path = os.path.join(pkg, "sources", f"{pid}.md")
        open(n_path, "w", encoding="utf-8").write("\n".join(notes))
        pieces.append({"piece_id": pid, "title": b["title"], "article": a_path, "video_script": s_path,
                       "youtube_description": d_path, "source_notes": n_path})

    steps = f"""# Manual steps remaining for run {run['run_id']}

Preparing this package does not mean anything has been rendered or published.

1. **Google Vids (one video per piece):** open `video_scripts/NN.md`. Paste it into a Google Doc and use
   Vids "docs to video" (or paste it into Vids' script panel). Keep each scene's on-screen source line
   visible and use an AI voiceover. Target 3-5 minutes. Export or publish to YouTube.
2. **YouTube:** upload as public or unlisted. Use the brief title. Paste `youtube/NN_description.txt` as
   the description, replacing {{ARTICLE_URL}} once the article is live. Mark AI-generated presentation
   where YouTube asks.
3. **Substack:** create a free (not paywalled) post from `articles/NN.md`. Paste the rendered Markdown
   and check that the links survive. Replace {{YOUTUBE_URL}} with the video link.
4. **Links:** record both URLs in `publication_links.json` and rerun `bash run.sh --package {run_dir}`.
   Existing links are preserved, and placeholders in the package files are filled in.
5. Verify each link opens in a private browser window.
"""
    open(os.path.join(pkg, "MANUAL_STEPS.md"), "w", encoding="utf-8").write(steps)
    manifest = {"run_id": run["run_id"], "as_of_date": run["as_of_date"], "review_id": current["review_id"],
                "approved_by": approval["reviewer"], "approved_at": approval["reviewed_at"],
                "packaged_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "pieces": pieces, "publication_links": os.path.join(pkg, "publication_links.json"),
                "manual_steps": os.path.join(pkg, "MANUAL_STEPS.md"),
                "published": {l["piece_id"]: bool(l["substack_url"] and l["youtube_url"]) for l in links}}
    with open(os.path.join(pkg, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
        fh.write("\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
