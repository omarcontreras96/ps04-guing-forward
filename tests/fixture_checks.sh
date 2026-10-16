#!/usr/bin/env bash
# tests/fixture_checks.sh — the deterministic checks from examples/README.md, run against a disposable
# evidence store (PIPELINE_EVIDENCE_DIR) so the fictional fixtures never touch data/evidence/.
# Exit 0 when every check passes. Fixtures are fictional and are not assignment evidence.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
export PIPELINE_EVIDENCE_DIR="$T/evidence"
mkdir -p "$T/run"; cp examples/run.json "$T/run/"
fail=0
check() { if [[ "$2" == "$3" ]]; then echo "PASS  $1"; else echo "FAIL  $1"; echo "  expected: $3"; echo "  got:      $2"; fail=1; fi; }
norm() { jq -cS . "$@"; }

bash data/store.sh init
check "1. initial ingest: three new items" \
  "$(bash data/store.sh upsert "$T/run" < examples/items.jsonl 2>/dev/null | norm)" "$(norm examples/initial_changes_expected.jsonl)"
check "2. replay: 4 unchanged (incl. duplicate, refreshed retrieved_at) then 1 changed" \
  "$(bash data/store.sh upsert "$T/run" < examples/replay_items.jsonl 2>/dev/null | norm)" "$(norm examples/replay_changes_expected.jsonl)"
check "2b. store holds three logical items" "$(bash data/store.sh list | wc -l | tr -d ' ')" "3"
check "2c. podcast item has two versions" "$(bash data/store.sh history podcast:fictional-episode | wc -l | tr -d ' ')" "2"
check "2d. first podcast version still retrievable" \
  "$(bash data/store.sh get podcast:fictional-episode 8f4fc03210022af1be3798fa7355ae3fa40297873b3ed037420ded36c5849bd5 | jq -r .text_path)" "examples/text/podcast.txt"
check "2e. latest podcast version is the changed one" \
  "$(bash data/store.sh get podcast:fictional-episode | jq -r .version_id)" "ed221b9c9d6af72c61b3881e7ef697bf8c4a36bfe6fcffb8e6542953118979c5"

elig="$(bash processing/filter_items.sh "$T/run" < examples/filter_input.jsonl 2>/dev/null | jq -r .item_id | sort | tr '\n' ' ')"
check "3. date filter: eligible IDs" "$elig" "$(jq -r '.eligible_item_ids[]' examples/filter_expected.json | sort | tr '\n' ' ')"
check "3b. date filter: exclusion reasons" "$(jq -c '[.item_id,.reason]' "$T/run/exclusions.jsonl" | sort | tr '\n' ' ')" \
  "$(jq -c '.exclusions[] | [.item_id,.reason]' examples/filter_expected.json | sort | tr '\n' ' ')"

refs="$(PYTHONPATH=lib "${PIPELINE_PYTHON:-$(ls .venv.nosync/bin/python .venv/bin/python 2>/dev/null | head -1)}" -c '
import json, evidence
bad = [r for b in map(json.loads, open("examples/briefs.jsonl")) for c in b["claims"] for r in c["evidence"] if not evidence.resolve_ref(r)["ok"]]
print("all-resolve" if not bad else f"{len(bad)} unresolved")')"
check "4. every fixture brief reference resolves to its item version and retained file" "$refs" "all-resolve"

v="$(PYTHONPATH=lib "${PIPELINE_PYTHON:-$(ls .venv.nosync/bin/python .venv/bin/python 2>/dev/null | head -1)}" -c '
import json, sys; sys.path.insert(0, "processing"); import extract
ok = all(extract.version_id(i, open(i["text_path"]).read(), json.load(open(i["segments_path"])) if i["segments_path"] else None) == i["version_id"]
         for i in map(json.loads, open("examples/items.jsonl")))
print("match" if ok else "mismatch")')"
check "5. version_id computation reproduces the fixture version IDs" "$v" "match"
exit $fail
