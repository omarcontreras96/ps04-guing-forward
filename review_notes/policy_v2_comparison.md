# Policy v1 → v2 comparison on identical evidence

- **v1 run:** `runs/live-20261015T011645Z` (live, policy v1)
- **v2 replay:** `runs/replay-20261015T041930Z` (mode `replay`, `evidence_reused_from: live-20261015T011645Z`). It reuses the same 51 eligible items and the cached digests; only the policy and the drafting prompts changed.
- **What changed in the inputs:** `review_notes/policy_v1_to_v2.diff` (policy) and `review_notes/prompts_run1_to_v2.diff` (claim-marker rule in the article and script prompts).

## Decision changes (machine diff of the two decisions.jsonl files, reasons verbatim)

| Item | v1 | v2 | v2 reason (verbatim) |
| --- | --- | --- | --- |
| `podcast:the-verge:f1ce6b3ada73` The $8 million AI music scam | accept 03 | defer  | The only relevant passage is a 90-second news recap inside an off-topic AI-music-fraud episode. The Jamie Dimon agent-blocking remark is relayed, with no primary source in the evidence, so policy 3 requires deferral. It is worth following if the primary statement surfaces. |
| `podcast:the-verge:fe7f0906ff40` HomeView: Apple just got serious about the smart home | Livestream | defer  | accept 01,02 | Adds availability and restriction details that MKBHD's review lacks: Siri AI is not launching on HomePod mini and is beta-only on Apple TV, there is a new 'unrecognized user' guest tier, and the Apple TV gains far-field mics. It also adds a host's skepticism about face-based switching drawn from Echo Show experience. Accepted for that added detail under policy 5's partial-duplicate rule, for pieces 01 and 02. |
| `youtube:vKjnZAcimss` Holo4: A Model That Clicks, Codes and Calls Tools | accept 02 | accept 01,02 | A hands-on demo of open-weight Holo4. With MCP off it clicked the GUI and then wrote code; with MCP on it used only tools and code and needed fewer steps. This supports the argument that GUI clicking is the brittle last resort. The presenter says he is still not convinced browser agents beat a normal model with a custom harness, a key piece 02 tension, and it documents a new computer-use model for piece 01. |

## Items from the 3+3 review that did NOT change

- `feed:ars-technica:16810b93abf0` (Ars Technica, Gemini 4 Argon rollout): still **reject**. v2 reason (verbatim): "A paid model rollout story that restates Google's benchmark and internal-impact claims and contains no interface evidence. Model launches are excluded by the brief (policy 1)."

## Theme coverage (new rule) — selection summary, verbatim excerpt

> Users outside tech: almost all evidence comes from experts, reviewers, developers or professionals, and the voice study is the only general-public sample (UK). Missing as well are accessibility users, non-US and non-English users, and privacy advocates or regulators commenting on agents with account access and always-on home cameras. No eligible item gives usable evidence on smart glasses or wearables; the only glasses item is a storage accessory, so the personal-context theme lacks wearable coverage and this must be stated in that piece's limitations. There is no independent test of Gemini tasks mode, Gemini Spark on Windows or Copilot local actions (the last has not shipped). The Alexa Plus assessment and the JPMorgan agent-blocking remark are relayed only. No longitudinal or adoption data exists beyond vendor and commentator claims, and generative-UI evidence is limited to a vendor's design account and a brief widget note.

## Briefs: v1 vs v2

| Piece | v1 title / argument | v2 title / argument |
| --- | --- | --- |
| 01 | **The month agents started messaging you first** — The development that matters most this month is consumer agents that act on people's own accounts and reach out first. The OS-level AI from Microsoft, Google and Apple ranks below it, because most of that is still pre-order, beta, paid-tier or 'coming months'. | **The real change this month: assistants that hold your keys, not assistants that talk better** — The development that matters most this month is proactive agents like Meta's Muse acting on users' connected accounts. The OS-level assistants from Apple, Google and Microsoft rank lower: they are still beta, first-generation, or promised for 'the coming months'. |
| 02 | **The failures you don't see are the ones that count** — Vendor and practitioner tests show agents and context-aware assistants succeeding at bounded, well-specified tasks. The failures that hurt users are silent ones: a missing source, a dropped detail, a finished-looking result that is wrong. Vendors' headline safety numbers do not measure those failures. | **Agents pass the tests with an answer key and slip where the work only looks finished** — Claims that agents can act for you hold up on tasks with a checkable end state. Where the output merely looks complete, the documented failures go unnoticed by the user, so the weak point is how visible the agent's work is, not raw capability. |
| 03 | **Can you still check its work? The question to ask of every launch** — Whether these interfaces change everyday computing depends less on the modality (voice, chat, GUI or agent) than on whether the user can still check what the system did. Readers should judge the next launches by how much they expose sources, routing and failures, not by how much they automate. | **Your new job is auditor: what to look for, and what to watch next** — Adopting AI assistants now makes the user a context maintainer and auditor, so readers should choose tools by how clearly they show what the assistant accessed and did. Conversational and voice interfaces make that auditing harder, because they feel agreeable and effortless while they steer. |

## Interpretation (TODO: student, in your own words)

- Revision 1 (relayed statements):
- Revision 2 (partial duplicates):
- Theme coverage:
