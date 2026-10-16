"""Write one uniquely named stage receipt under RUN_DIR/logs/.

Cost accounting: model calls append usage lines (with cost computed from the
snapshotted price table) to the stage's LLM usage file. A stage with no model
calls reports cost_usd 0.0 with basis "no_paid_api_calls" (local tools and free
public endpoints only). A model call whose model has no configured price makes
the stage cost null (unknown) rather than a guessed number.
"""
import argparse
import json
import os
import secrets
from datetime import datetime, timezone


def read_jsonl(path):
    out = []
    if path and os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    try:
                        out.append(json.loads(line))
                    except json.JSONDecodeError:
                        out.append({"message": line})
    return out


def as_count(value):
    return None if value in (None, "", "null") else int(value)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-dir", required=True)
    ap.add_argument("--stage", required=True)
    ap.add_argument("--status", required=True)
    ap.add_argument("--exit-code", type=int, required=True)
    ap.add_argument("--started", required=True)
    ap.add_argument("--input-count")
    ap.add_argument("--output-count")
    ap.add_argument("--tools", default="")
    ap.add_argument("--note", default="")
    ap.add_argument("--errors-file")
    ap.add_argument("--usage-file")
    args = ap.parse_args()

    finished = datetime.now(timezone.utc)
    usage = read_jsonl(args.usage_file)
    errors = read_jsonl(args.errors_file)

    if not usage:
        cost, basis = 0.0, "no_paid_api_calls"
    elif any(u.get("cost_usd") is None for u in usage):
        cost, basis = None, "unknown_price_for_some_model"
    else:
        cost, basis = round(sum(u["cost_usd"] for u in usage), 4), "computed_from_token_usage_and_price_table"

    models = sorted({u["model"] for u in usage if u.get("model")})
    receipt = {
        "stage": args.stage,
        "status": args.status,
        "exit_code": args.exit_code,
        "started_at": args.started,
        "finished_at": finished.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "input_count": as_count(args.input_count),
        "output_count": as_count(args.output_count),
        "tools": [t for t in args.tools.split(",") if t],
        "models": models,
        "model_calls": len(usage),
        "tokens": {
            "input": sum(u.get("input_tokens", 0) for u in usage),
            "output": sum(u.get("output_tokens", 0) for u in usage),
        },
        "cost_usd": cost,
        "cost_basis": basis,
        "errors": errors,
        "note": args.note or None,
    }
    logs = os.path.join(args.run_dir, "logs")
    os.makedirs(logs, exist_ok=True)
    name = f"{args.stage}-{finished.strftime('%Y%m%dT%H%M%S')}-{secrets.token_hex(3)}.json"
    with open(os.path.join(logs, name), "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=2)
        fh.write("\n")
    if usage:
        with open(os.path.join(logs, "llm_usage.jsonl"), "a", encoding="utf-8") as fh:
            for u in usage:
                fh.write(json.dumps({"stage": args.stage, **u}) + "\n")
    print(os.path.join(logs, name))


if __name__ == "__main__":
    main()
