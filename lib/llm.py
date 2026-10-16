"""Thin provider wrapper around the Anthropic Messages API.

Every model call in the pipeline goes through `call()`. It:
  * sends the exact system/user text it is given (callers assemble prompts from the
    run's snapshotted policy and prompt files),
  * saves the request and raw response under RUN_DIR/llm/<stage>/ for inspection,
  * appends token usage and computed cost to $LLM_USAGE_FILE for the stage receipt.

Model choice and prices come from the run snapshot (config/project.json -> pipeline).
"""
import json
import os
import re
import time
from datetime import datetime, timezone

import anthropic

API_BASE_URL = os.environ.get("PIPELINE_ANTHROPIC_BASE_URL", "https://api.anthropic.com")
FALLBACK_BETA = "server-side-fallback-2026-07-01"

_client = None


class LLMError(RuntimeError):
    pass


def client():
    global _client
    if _client is None:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            raise LLMError("ANTHROPIC_API_KEY is not set (put it in .env or the environment)")
        _client = anthropic.Anthropic(base_url=API_BASE_URL, max_retries=4, timeout=900)
    return _client


def pipeline_config(run_dir):
    with open(os.path.join(run_dir, "config", "project.json"), encoding="utf-8") as fh:
        return json.load(fh).get("pipeline", {})


def model_for(run_dir, role):
    models = pipeline_config(run_dir).get("models", {})
    if role not in models:
        raise LLMError(f"config/project.json pipeline.models.{role} is not set")
    return models[role]


def _cost(run_dir, model, usage):
    prices = pipeline_config(run_dir).get("pricing_usd_per_mtok", {})
    p = prices.get(model)
    if not p:
        return None
    cache_write = getattr(usage, "cache_creation_input_tokens", 0) or 0
    cache_read = getattr(usage, "cache_read_input_tokens", 0) or 0
    return round(
        usage.input_tokens * p["input"] / 1e6
        + cache_write * p["input"] * 1.25 / 1e6
        + cache_read * p["input"] * 0.1 / 1e6
        + usage.output_tokens * p["output"] / 1e6,
        6,
    )


def _safe(label):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", label)[:120]


def call(run_dir, stage, label, role, system, user, schema=None, max_tokens=32000, effort="high"):
    """Run one model request. Returns parsed JSON when `schema` is given, else text."""
    model = model_for(run_dir, role)
    out_dir = os.path.join(run_dir, "llm", stage)
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.join(out_dir, _safe(label))
    with open(base + ".request.md", "w", encoding="utf-8") as fh:
        fh.write(f"<!-- model: {model} | effort: {effort} | schema: {'yes' if schema else 'no'} -->\n")
        fh.write("# SYSTEM\n\n" + system + "\n\n# USER\n\n" + user + "\n")

    params = {
        "model": model,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user}],
        "output_config": {"effort": effort},
        "betas": [FALLBACK_BETA],
        "fallbacks": "default",
    }
    if schema:
        params["output_config"]["format"] = {"type": "json_schema", "schema": schema}

    started = time.time()
    with client().beta.messages.stream(**params) as stream:
        message = stream.get_final_message()
    elapsed = round(time.time() - started, 1)

    record = {
        "label": label,
        "role": role,
        "model": message.model,
        "requested_model": model,
        "input_tokens": message.usage.input_tokens,
        "output_tokens": message.usage.output_tokens,
        "cost_usd": _cost(run_dir, message.model, message.usage),
        "elapsed_seconds": elapsed,
        "stop_reason": message.stop_reason,
        "at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    usage_file = os.environ.get("LLM_USAGE_FILE")
    if usage_file:
        with open(usage_file, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(record) + "\n")

    text = "".join(b.text for b in message.content if getattr(b, "type", "") == "text")
    with open(base + ".response.txt", "w", encoding="utf-8") as fh:
        fh.write(text)

    if message.stop_reason == "refusal":
        raise LLMError(f"{label}: model declined the request")
    if message.stop_reason == "max_tokens":
        raise LLMError(f"{label}: response truncated at max_tokens={max_tokens}")
    if schema:
        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise LLMError(f"{label}: response was not valid JSON: {exc}") from exc
    return text
