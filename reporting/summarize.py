"""Summarize a run from its saved artifacts and receipts only (works for incomplete runs).

Counts are null when the producing stage never ran (file absent) and 0 for a measured empty result.
Status: failed | awaiting_review | ready_for_production. Publication links are reported separately from
production readiness.
"""
import glob
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone

from util import load_json, read_jsonl


def jsonl_or_none(run_dir, name):
    p = os.path.join(run_dir, name)
    return read_jsonl(p) if os.path.exists(p) else None


def count(x):
    return None if x is None else len(x)


def parse(ts):
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def main(run_dir):
    run = load_json(os.path.join(run_dir, "run.json"))
    receipts = []
    for p in sorted(glob.glob(os.path.join(run_dir, "logs", "*.json"))):
        try:
            r = load_json(p)
            if "stage" in r and "status" in r:
                r["_file"] = p
                receipts.append(r)
        except (json.JSONDecodeError, OSError):
            pass
    receipts.sort(key=lambda r: r.get("finished_at", ""))

    candidates = jsonl_or_none(run_dir, "candidates.jsonl")
    items = jsonl_or_none(run_dir, "items.jsonl")
    changes = jsonl_or_none(run_dir, "changes.jsonl")
    eligible = jsonl_or_none(run_dir, "eligible.jsonl")
    exclusions = jsonl_or_none(run_dir, "exclusions.jsonl")
    decisions = jsonl_or_none(run_dir, "decisions.jsonl")
    briefs = jsonl_or_none(run_dir, "briefs.jsonl")
    art_manifest = jsonl_or_none(run_dir, "articles.jsonl")
    scr_manifest = jsonl_or_none(run_dir, "video_scripts.jsonl")
    review = load_json(os.path.join(run_dir, "review.json")) if os.path.exists(os.path.join(run_dir, "review.json")) else None
    approval = load_json(os.path.join(run_dir, "approval.json")) if os.path.exists(os.path.join(run_dir, "approval.json")) else None
    pkg_manifest_path = os.path.join(run_dir, "package", "manifest.json")
    pkg = load_json(pkg_manifest_path) if os.path.exists(pkg_manifest_path) else None
    collection = load_json(os.path.join(run_dir, "collection_status.json")) if os.path.exists(os.path.join(run_dir, "collection_status.json")) else None

    ch = Counter(c["change"] for c in changes) if changes is not None else None
    dc = Counter(d["decision"] for d in decisions) if decisions is not None else None
    raw_ids = [c["item_id"] for c in candidates] if candidates is not None else None
    articles = sorted(glob.glob(os.path.join(run_dir, "articles", "*.md")))
    scripts = sorted(glob.glob(os.path.join(run_dir, "video_scripts", "*.md")))

    def coverage(records):
        if records is None:
            return None
        return {"by_kind": dict(Counter(r["kind"] for r in records)),
                "independent_publishers": sorted({r["publisher_id"] for r in records}),
                "publisher_count": len({r["publisher_id"] for r in records})}

    elig_by_id = {e["item_id"]: e for e in (eligible or [])}
    accepted = [elig_by_id[d["item_id"]] for d in (decisions or []) if d["decision"] == "accept" and d["item_id"] in elig_by_id]
    cited_ids = {r["item_id"] for b in (briefs or []) for c in b["claims"] for r in c["evidence"]}
    cited = [elig_by_id[i] for i in cited_ids if i in elig_by_id]

    # Stage outcomes from receipts; the latest receipt per stage decides its current state.
    latest = {}
    for r in receipts:
        latest[r["stage"]] = r
    problem_stages = [{"stage": s, "status": r["status"], "exit_code": r["exit_code"], "errors": r.get("errors", [])[:10]}
                      for s, r in latest.items() if r["status"] != "completed"]

    known = [r["cost_usd"] for r in receipts if r.get("cost_usd") is not None]
    unknown = sorted({r["stage"] for r in receipts if r.get("cost_usd") is None})
    by_stage = Counter()
    for r in receipts:
        if r.get("cost_usd") is not None:
            by_stage[r["stage"]] += r["cost_usd"]
    models = sorted({m for r in receipts for m in r.get("models", [])})
    tools = sorted({t.split(" ")[0] for r in receipts for t in r.get("tools", [])})

    # Pipeline time ends with the first summary of the run; later receipts belong to review/packaging.
    first_summary = next((r["finished_at"] for r in receipts if r["stage"] == "summarize_run"), None)
    pipeline_receipts = [r for r in receipts if r["stage"] != "summarize_run"
                         and (first_summary is None or r["finished_at"] <= first_summary)]
    finished = max((r["finished_at"] for r in pipeline_receipts), default=None)
    elapsed = (parse(finished) - parse(run["started_at"])).total_seconds() if finished else None
    last_activity = receipts[-1]["finished_at"] if receipts else None

    # Status
    drafts_exist = len(articles) == 3 and len(scripts) == 3
    approval_matches = bool(approval and review and approval.get("review_id") == review.get("review_id"))
    if pkg and approval_matches and approval.get("decision") == "approve" and pkg.get("review_id") == review.get("review_id"):
        status = "ready_for_production"
    elif drafts_exist and review is not None:
        status = "awaiting_review"
    else:
        status = "failed"

    links_path = os.path.join(run_dir, "package", "publication_links.json")
    links = load_json(links_path) if os.path.exists(links_path) else None

    manual = []
    if status == "failed":
        manual.append("Inspect failed stages below, fix the cause, and start a new run (collection reuses stored evidence).")
    if status == "awaiting_review":
        if review and not review.get("passed"):
            manual.append("Content check has blocking errors: revise drafts or briefs, then rerun: bash run.sh --package " + run_dir)
        manual.append("Human editorial review: read articles/, video_scripts/, review.json and the evidence; record corrections; "
                      "create approval.json (review/record_approval.sh), then: bash run.sh --package " + run_dir)
    if status == "ready_for_production":
        manual += ["Produce three videos in Google Vids from package/video_scripts/ (manual)",
                   "Upload videos to YouTube with package/youtube/NN_description.txt (manual)",
                   "Publish package/articles/ on Substack, free access (manual)",
                   "Record URLs in package/publication_links.json and repackage to fill placeholders"]
    if collection and not collection.get("complete"):
        manual.append("Collection was incomplete; see coverage_limitations and decide whether to rerun after fixing sources.")

    summary = {
        "run_id": run["run_id"],
        "mode": run["mode"],
        "as_of_date": run["as_of_date"],
        "previous_run_id": run.get("previous_run_id"),
        "note": run.get("note"),
        "status": status,
        "started_at": run["started_at"],
        "pipeline_finished_at": finished,
        "elapsed_seconds": elapsed,
        "last_activity_at": last_activity,
        "counts": {
            "discovered": count(candidates),
            "discovered_distinct_items": None if raw_ids is None else len(set(raw_ids)),
            "duplicate_observations": None if raw_ids is None else len(raw_ids) - len(set(raw_ids)),
            "extracted": count(items),
            "new": None if ch is None else ch.get("new", 0),
            "changed": None if ch is None else ch.get("changed", 0),
            "unchanged": None if ch is None else ch.get("unchanged", 0),
            "corpus_items_in_store": count(jsonl_or_none(run_dir, "corpus.jsonl")),
            "eligible": count(eligible),
            "excluded": count(exclusions),
            "excluded_by_reason": None if exclusions is None else dict(Counter(e["reason"] for e in exclusions)),
            "accepted": None if dc is None else dc.get("accept", 0),
            "rejected": None if dc is None else dc.get("reject", 0),
            "deferred": None if dc is None else dc.get("defer", 0),
            "briefs": count(briefs),
            "articles": len(articles) if art_manifest is not None or articles else None,
            "video_scripts": len(scripts) if scr_manifest is not None or scripts else None,
        },
        "coverage": {
            "eligible": coverage(eligible),
            "accepted": coverage(accepted) if decisions is not None else None,
            "cited_in_briefs": coverage(cited) if briefs is not None else None,
        },
        "coverage_limitations": {
            "collection_complete": None if collection is None else collection.get("complete"),
            "collectors": None if collection is None else collection.get("collectors"),
            "simulated_failures": run.get("simulated_failures") or [],
            "items_failed_extraction": [e for r in receipts if r["stage"] == "extract_content" for e in r.get("errors", [])],
        },
        "stages": [{"stage": r["stage"], "status": r["status"], "exit_code": r["exit_code"], "input_count": r.get("input_count"),
                    "output_count": r.get("output_count"), "started_at": r["started_at"], "finished_at": r["finished_at"],
                    "cost_usd": r.get("cost_usd"), "note": r.get("note"), "receipt": r["_file"]} for r in receipts],
        "failed_or_incomplete_stages": problem_stages,
        "models": models,
        "tools": tools,
        "cost": {"known_usd": round(sum(known), 4), "by_stage_usd": {k: round(v, 4) for k, v in by_stage.items()},
                 "stages_with_unknown_cost": unknown,
                 "basis": "Model costs computed from API token usage x snapshotted price table (estimate; excludes taxes/credits). "
                          "Local tools (yt-dlp, whisper.cpp, ffmpeg) and public feeds are counted as $0 API cost."},
        "review": None if review is None else {"review_id": review["review_id"], "passed": review["passed"],
                                               "errors": review.get("error_count"), "warnings": review.get("warning_count")},
        "approval": None if approval is None else {"decision": approval.get("decision"), "reviewer": approval.get("reviewer"),
                                                   "matches_current_review": approval_matches},
        "package": None if pkg is None else {"path": os.path.join(run_dir, "package"), "packaged_at": pkg.get("packaged_at")},
        "publication_links": links,
        "published": None if links is None else all(l.get("substack_url") and l.get("youtube_url") for l in links),
        "remaining_manual_actions": manual,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
