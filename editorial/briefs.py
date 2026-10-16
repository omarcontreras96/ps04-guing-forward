"""Create exactly three editorial briefs (01, 02, 03) from accepted evidence.

Refuses (exit 1, no briefs) when accepted evidence cannot meet the structural requirements
(>= 3 publishers available, all three media kinds accepted).

Every evidence reference is then checked against the stored item version. A near-miss quote is replaced
with the verbatim passage it matches (>= 0.88 similarity), and the correction is logged. Any remaining
problems go back to the model for one repair round. If problems persist, the briefs are written to
RUN_DIR/briefs.rejected.jsonl rather than stdout, and the stage exits 1.
Validation details: RUN_DIR/briefs_validation.json.
"""
import json
import os
import sys
from datetime import date, timedelta

import llm
from evidence import closest_passage, load_segments, load_text, project_brief, read_text_file, render_item, resolve_ref, store_get
from util import load_json, log_error, read_jsonl

PIECES = ["01", "02", "03"]

REF_SCHEMA = {
    "type": "object",
    "properties": {
        "item_id": {"type": "string"},
        "version_id": {"type": "string"},
        "locator": {"type": "object", "properties": {
            "type": {"type": "string", "enum": ["text", "segment"]},
            "quote": {"type": "string"},
            "segment_id": {"type": "string"},
        }, "required": ["type", "quote", "segment_id"], "additionalProperties": False},
    },
    "required": ["item_id", "version_id", "locator"],
    "additionalProperties": False,
}
BRIEF_SCHEMA = {
    "type": "object",
    "properties": {"briefs": {"type": "array", "items": {
        "type": "object",
        "properties": {
            "piece_id": {"type": "string", "enum": PIECES},
            "title": {"type": "string"},
            "question": {"type": "string"},
            "argument": {"type": "string"},
            "synthesis": {"type": "string"},
            "limitations": {"type": "string"},
            "claims": {"type": "array", "items": {
                "type": "object",
                "properties": {
                    "claim_id": {"type": "string"},
                    "statement": {"type": "string"},
                    "type": {"type": "string", "enum": ["reported_fact", "source_claim", "inference"]},
                    "evidence": {"type": "array", "items": REF_SCHEMA},
                },
                "required": ["claim_id", "statement", "type", "evidence"],
                "additionalProperties": False,
            }},
        },
        "required": ["piece_id", "title", "question", "argument", "synthesis", "limitations", "claims"],
        "additionalProperties": False,
    }}},
    "required": ["briefs"],
    "additionalProperties": False,
}


def clean_locator(loc):
    if loc.get("type") == "text":
        return {"type": "text", "quote": loc.get("quote", "")}
    return {"type": "segment", "segment_id": loc.get("segment_id", "")}


def validate(briefs, accepted, window, corrections):
    """Fix near-miss quotes in place; return a list of remaining problems."""
    problems = []
    if sorted(b["piece_id"] for b in briefs) != PIECES:
        problems.append(f"piece ids must be exactly 01, 02, 03 (got {[b['piece_id'] for b in briefs]})")
    kinds_used = set()
    for b in briefs:
        pubs = set()
        if not b["claims"]:
            problems.append(f"{b['piece_id']}: no claims")
        for c in b["claims"]:
            c["evidence"] = [{"item_id": r["item_id"], "version_id": r["version_id"], "locator": clean_locator(r["locator"])}
                             for r in c["evidence"]]
            if not c["claim_id"].startswith(b["piece_id"] + "-c"):
                problems.append(f"{c['claim_id']}: claim id must look like {b['piece_id']}-c1")
            if not c["evidence"]:
                problems.append(f"{c['claim_id']}: claim has no evidence")
            for r in c["evidence"]:
                if r["item_id"] not in accepted:
                    problems.append(f"{c['claim_id']}: {r['item_id']} is not an accepted item")
                    continue
                item = accepted[r["item_id"]]
                if r["version_id"] != item["version_id"]:
                    r["version_id"] = item["version_id"]  # accepted version is authoritative
                res = resolve_ref(r)
                if not res["ok"] and r["locator"]["type"] == "text":
                    fixed = closest_passage(r["locator"]["quote"], load_text(item))
                    if fixed:
                        corrections.append({"claim_id": c["claim_id"], "item_id": r["item_id"],
                                            "model_quote": r["locator"]["quote"], "verbatim_quote": fixed})
                        r["locator"]["quote"] = fixed
                        res = resolve_ref(r)
                if not res["ok"]:
                    problems.append(f"{c['claim_id']}: {res['error']}")
                    continue
                pub = res["item"]["published_at"][:10]
                if not (window[0] <= pub <= window[1]):
                    problems.append(f"{c['claim_id']}: evidence {r['item_id']} published {pub} outside window")
                pubs.add(res["item"]["publisher_id"])
                kinds_used.add(res["item"]["kind"])
            if c["type"] == "inference" and len({accepted[r["item_id"]]["publisher_id"] for r in c["evidence"]
                                                 if r["item_id"] in accepted}) < 2:
                problems.append(f"{c['claim_id']}: an inference needs evidence from at least two publishers")
        if len(pubs) < 3:
            problems.append(f"{b['piece_id']}: evidence from only {len(pubs)} publisher(s); needs >= 3")
    missing_kinds = {"feed", "youtube", "podcast"} - kinds_used
    if missing_kinds:
        problems.append(f"series: no evidence from {sorted(missing_kinds)}")
    return problems


def main(run_dir, errors_path):
    decisions = [json.loads(l) for l in sys.stdin if l.strip()]
    run = load_json(os.path.join(run_dir, "run.json"))
    as_of = date.fromisoformat(run["as_of_date"])
    window = ((as_of - timedelta(days=29)).isoformat(), as_of.isoformat())
    eligible = {i["item_id"]: i for i in read_jsonl(os.path.join(run_dir, "eligible.jsonl"))}
    digests = {d["item_id"]: d.get("digest") for d in read_jsonl(os.path.join(run_dir, "digests.jsonl"))}

    accepted = {}
    for d in decisions:
        if d["decision"] == "accept":
            item = store_get(d["item_id"], d["version_id"]) or eligible.get(d["item_id"])
            if item:
                accepted[d["item_id"]] = item
    pubs = {i["publisher_id"] for i in accepted.values()}
    kinds = {i["kind"] for i in accepted.values()}
    gate = []
    if len(pubs) < 3:
        gate.append(f"only {len(pubs)} accepted publishers (need >= 3 per piece)")
    if {"feed", "youtube", "podcast"} - kinds:
        gate.append(f"no accepted items of kind {sorted({'feed', 'youtube', 'podcast'} - kinds)}")
    if gate:
        for g in gate:
            log_error(errors_path, "insufficient evidence: " + g)
        with open(os.path.join(run_dir, "briefs_validation.json"), "w") as fh:
            json.dump({"status": "blocked_insufficient_evidence", "problems": gate}, fh, indent=2)
        print("create_briefs: insufficient accepted evidence; no briefs created: " + "; ".join(gate), file=sys.stderr)
        return 1

    # Evidence pack: accepted items, long transcripts narrowed to the digest's cited passages (+/- context).
    reasons = {d["item_id"]: d for d in decisions}
    blocks = []
    for item_id, item in accepted.items():
        d = reasons[item_id]
        dg = digests.get(item_id) or {}
        seg_ids = [c["segment_id"] for c in dg.get("claims", []) if c.get("segment_id")]
        segs = load_segments(item)
        narrow = seg_ids if (segs and len(segs) > 60 and seg_ids) else None
        blocks.append(f"EDITOR DECISION for {item_id}: accept for pieces {d['piece_ids']}: {d['reason']}\n"
                      f"DIGEST SUMMARY: {dg.get('summary', '')}\nCOMMERCIAL INTEREST: {dg.get('commercial_interest', '')}\n"
                      f"OLDER EVENT: {dg.get('older_event', '')}\n"
                      + render_item(item, max_chars=60000, segment_ids=narrow, context=8))
    notes_path = os.path.join(run_dir, "selection_notes.json")
    notes = load_json(notes_path) if os.path.exists(notes_path) else {}
    policy = read_text_file(os.path.join(run_dir, "config", "editorial_policy.md"))
    prompt = read_text_file(os.path.join(run_dir, "prompts", "create_briefs.md"))
    system = project_brief(run_dir) + "\n\n# Editorial policy\n" + policy + "\n\n# Instructions\n" + prompt
    user = (f"As-of date {run['as_of_date']}; evidence window {window[0]} to {window[1]}.\n"
            f"Selection notes from the editor: {json.dumps(notes, ensure_ascii=False)}\n\n"
            f"ACCEPTED EVIDENCE ({len(accepted)} items):\n\n" + "\n".join(blocks))

    corrections = []
    out = llm.call(run_dir, "create_briefs", "briefs", "editorial", system, user, schema=BRIEF_SCHEMA,
                   max_tokens=64000, effort="high")
    briefs = out["briefs"]
    problems = validate(briefs, accepted, window, corrections)
    rounds = [{"round": 1, "problems": problems}]
    if problems:
        print(f"create_briefs: {len(problems)} problems, asking the model to repair", file=sys.stderr)
        repair_user = (user + "\n\nYOUR PREVIOUS BRIEFS:\n" + json.dumps({"briefs": briefs}, ensure_ascii=False)
                       + "\n\nAUTOMATED VALIDATION FOUND THESE PROBLEMS. Return the full corrected set of three briefs; "
                         "fix only what is needed (exact verbatim quotes, valid segment IDs, accepted items only, "
                         ">= 3 publishers per piece, all three media kinds across the series):\n- "
                       + "\n- ".join(problems))
        out = llm.call(run_dir, "create_briefs", "briefs-repair", "editorial", system, repair_user,
                       schema=BRIEF_SCHEMA, max_tokens=64000, effort="high")
        briefs = out["briefs"]
        problems = validate(briefs, accepted, window, corrections)
        rounds.append({"round": 2, "problems": problems})

    briefs.sort(key=lambda b: b["piece_id"])
    with open(os.path.join(run_dir, "briefs_validation.json"), "w", encoding="utf-8") as fh:
        json.dump({"status": "valid" if not problems else "invalid", "rounds": rounds,
                   "quote_corrections": corrections}, fh, indent=2, ensure_ascii=False)
    if problems:
        with open(os.path.join(run_dir, "briefs.rejected.jsonl"), "w", encoding="utf-8") as fh:
            for b in briefs:
                fh.write(json.dumps(b, ensure_ascii=False) + "\n")
        for p in problems:
            log_error(errors_path, "brief validation: " + p)
        print("create_briefs: briefs failed validation; see briefs_validation.json and briefs.rejected.jsonl", file=sys.stderr)
        return 1
    for b in briefs:
        print(json.dumps(b, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
