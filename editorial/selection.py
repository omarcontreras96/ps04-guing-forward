"""Editorial selection through the model, in two passes.

Pass 1 (digest model): one call per eligible item. Produces a neutral digest: claims, evidence basis,
verbatim locators, relevance and commercial interest. Digests are cached per (item version, digest prompt,
model) in data/assets/digests/ so unchanged items are not re-read on later runs.

Pass 2 (editorial model): one call over all digests, together with the snapshotted editorial policy,
the change status of each item, and any previous run's decision. It decides accept/reject/defer for every
eligible item and assigns piece IDs.

Outputs: decision JSONL on stdout, RUN_DIR/digests.jsonl, RUN_DIR/selection_notes.json.
"""
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

import llm
from evidence import project_brief, read_text_file, render_item
from util import load_json, log_error, read_jsonl, safe_id, sha256

PIECES = ["01", "02", "03"]

DIGEST_SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "speakers_or_authors": {"type": "string"},
        "relevance": {"type": "integer", "enum": [0, 1, 2, 3]},
        "relevance_reason": {"type": "string"},
        "themes": {"type": "array", "items": {"type": "string"}},
        "claims": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "claim": {"type": "string"},
                "basis": {"type": "string", "enum": ["observation", "experience", "announcement", "assertion", "secondhand"]},
                "locator_type": {"type": "string", "enum": ["text", "segment"]},
                "quote": {"type": "string"},
                "segment_id": {"type": "string"},
            },
            "required": ["claim", "basis", "locator_type", "quote", "segment_id"],
            "additionalProperties": False,
        }},
        "commercial_interest": {"type": "string"},
        "older_event": {"type": "string"},
    },
    "required": ["summary", "speakers_or_authors", "relevance", "relevance_reason", "themes", "claims",
                 "commercial_interest", "older_event"],
    "additionalProperties": False,
}

DECISION_SCHEMA = {
    "type": "object",
    "properties": {
        "decisions": {"type": "array", "items": {
            "type": "object",
            "properties": {
                "item_id": {"type": "string"},
                "decision": {"type": "string", "enum": ["accept", "reject", "defer"]},
                "reason": {"type": "string"},
                "piece_ids": {"type": "array", "items": {"type": "string", "enum": PIECES}},
                "claim_cluster": {"type": "string"},
                "credibility": {"type": "string"},
                "change_from_previous_run": {"type": "string"},
            },
            "required": ["item_id", "decision", "reason", "piece_ids", "claim_cluster", "credibility",
                         "change_from_previous_run"],
            "additionalProperties": False,
        }},
        "developments": {"type": "string"},
        "missing_perspectives": {"type": "string"},
        "balance": {"type": "string"},
    },
    "required": ["decisions", "developments", "missing_perspectives", "balance"],
    "additionalProperties": False,
}


def prompt_section(path, heading):
    text = read_text_file(path)
    parts = text.split("\n## ")
    for p in parts:
        if p.startswith(heading):
            return "## " + p.strip()
    raise SystemExit(f"select: section '{heading}' not found in {path}")


def digest_item(run_dir, item, system, model, prompt_hash):
    cache_dir = os.path.join("data", "assets", "digests")
    os.makedirs(cache_dir, exist_ok=True)
    path = os.path.join(cache_dir, f"{safe_id(item['item_id'])}-{item['version_id'][:12]}-{prompt_hash}.json")
    if os.path.exists(path):
        return load_json(path), True, path
    user = ("Digest this item for the editor. Return JSON only.\n\n"
            + render_item(item, max_chars=200000))
    digest = llm.call(run_dir, "select_items", f"digest-{item['item_id']}", "digest", system, user,
                      schema=DIGEST_SCHEMA, max_tokens=16000, effort="medium")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(digest, fh, indent=1, ensure_ascii=False)
    return digest, False, path


def main(run_dir, errors_path):
    items = [json.loads(l) for l in sys.stdin if l.strip()]
    if not items:
        print("select: no eligible items on stdin", file=sys.stderr)
        return 1
    cfg = load_json(os.path.join(run_dir, "config", "project.json"))
    run = load_json(os.path.join(run_dir, "run.json"))
    policy = read_text_file(os.path.join(run_dir, "config", "editorial_policy.md"))
    prompt_file = os.path.join(run_dir, "prompts", "select_items.md")
    p1 = prompt_section(prompt_file, "Pass 1")
    p2 = prompt_section(prompt_file, "Pass 2")
    brief = project_brief(run_dir)

    # ---- pass 1: digests
    digest_system = brief + "\n\n" + p1
    digest_model = llm.model_for(run_dir, "digest")
    prompt_hash = sha256(digest_system + digest_model)[:8]

    def work(item):
        try:
            return item, *digest_item(run_dir, item, digest_system, digest_model, prompt_hash)
        except Exception as exc:  # noqa: BLE001
            log_error(errors_path, f"digest failed: {exc}", item["item_id"])
            return item, None, False, None

    with ThreadPoolExecutor(max_workers=int(cfg.get("pipeline", {}).get("digest_concurrency", 6))) as pool:
        results = list(pool.map(work, items))
    with open(os.path.join(run_dir, "digests.jsonl"), "w", encoding="utf-8") as fh:
        for item, digest, cached, path in results:
            fh.write(json.dumps({"item_id": item["item_id"], "version_id": item["version_id"], "cached": cached,
                                 "digest_path": path, "digest": digest}, ensure_ascii=False) + "\n")
    n_cached = sum(1 for r in results if r[2])
    print(f"select: digests ready ({n_cached} reused from cache, {len(results) - n_cached} new)", file=sys.stderr)

    # ---- pass 2: decisions over all digests
    changes = {c["item_id"]: c["change"] for c in read_jsonl(os.path.join(run_dir, "changes.jsonl"))}
    prev = {}
    if run.get("previous_run_id"):
        for d in read_jsonl(os.path.join("runs", run["previous_run_id"], "decisions.jsonl")):
            prev[d["item_id"]] = d
    blocks = []
    for item, digest, _, _ in results:
        p = prev.get(item["item_id"])
        meta = {
            "item_id": item["item_id"], "version_id": item["version_id"], "kind": item["kind"],
            "publisher_id": item["publisher_id"], "source_name": item.get("source_name"),
            "perspective": item.get("perspective"), "title": item["title"], "published_at": item["published_at"],
            "duration_seconds": item.get("duration_seconds"),
            "status_in_this_run": changes.get(item["item_id"], "not_collected_this_run (retained from earlier run)"),
            "previous_run_decision": ({"decision": p["decision"], "reason": p["reason"], "version_id": p["version_id"]}
                                      if p else None),
            "digest": digest if digest is not None else "DIGEST FAILED - decide defer and say evidence could not be read",
        }
        blocks.append(json.dumps(meta, ensure_ascii=False))
    window = f"as-of {run['as_of_date']} (30-day window ending that date)"
    user = (f"Run {run['run_id']}, {window}. {len(items)} eligible items follow, one JSON object per line.\n"
            "Decide every item exactly once.\n\n" + "\n".join(blocks))
    system = brief + "\n\n# Editorial policy\n" + policy + "\n\n# Instructions\n" + p2
    out = llm.call(run_dir, "select_items", "decisions", "editorial", system, user,
                   schema=DECISION_SCHEMA, max_tokens=64000, effort="high")

    by_id = {}
    for d in out["decisions"]:
        by_id.setdefault(d["item_id"], d)  # first decision wins if the model repeated an item
    decisions, problems = [], 0
    for item, digest, _, _ in results:
        d = by_id.get(item["item_id"])
        if d is None:
            problems += 1
            log_error(errors_path, "model returned no decision; recorded as defer for human decision", item["item_id"])
            d = {"decision": "defer", "reason": "No model decision returned; needs human decision.", "piece_ids": [],
                 "claim_cluster": "", "credibility": "", "change_from_previous_run": ""}
        piece_ids = sorted(set(d["piece_ids"])) if d["decision"] == "accept" else []
        decision = d["decision"]
        reason = d["reason"]
        if decision == "accept" and not piece_ids:
            decision, reason = "defer", reason + " [Pipeline: accepted without a piece assignment; recorded as defer.]"
        decisions.append({
            "item_id": item["item_id"], "version_id": item["version_id"], "decision": decision, "reason": reason,
            "piece_ids": piece_ids, "claim_cluster": d.get("claim_cluster"), "credibility": d.get("credibility"),
            "change_from_previous_run": d.get("change_from_previous_run") or None,
            "kind": item["kind"], "publisher_id": item["publisher_id"], "title": item["title"],
            "relevance": (digest or {}).get("relevance"),
        })
    extra = set(by_id) - {i["item_id"] for i in items}
    for x in extra:
        log_error(errors_path, "model decided an item that is not eligible; ignored", x)

    with open(os.path.join(run_dir, "selection_notes.json"), "w", encoding="utf-8") as fh:
        json.dump({"developments": out["developments"], "missing_perspectives": out["missing_perspectives"],
                   "balance": out["balance"], "digests_cached": n_cached, "digests_new": len(results) - n_cached},
                  fh, indent=2, ensure_ascii=False)
    for d in decisions:
        print(json.dumps(d, ensure_ascii=False))
    failed_digests = sum(1 for r in results if r[1] is None)
    return 1 if (problems or failed_digests) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
