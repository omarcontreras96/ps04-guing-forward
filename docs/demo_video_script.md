# Technical demonstration video script: GUIng Forward pipeline (target 5:00, limit 4–6 min)

> Draft for Omar to rehearse and adapt. Narration is about 720 words, roughly 5 minutes at a natural
> pace. Every number below comes from the run artifacts in this repo.

**Before recording**
- Terminal at the repo root, font size 18 or larger, a dark theme, and a window about 110 columns wide.
- Browser tabs:
  1. The GitHub repo, with SUBMISSION.md scrolled to the architecture diagram.
  2. The Substack post for piece 03.
  3. `review_notes/policy_v2_comparison.md` on GitHub.
- Run the commands below once beforehand so nothing surprises you. All of them are read-only.
- Set this shortcut in the terminal: `R1=runs/live-20261015T011645Z; P=runs/live-20261015T045321Z; R2=runs/live-20261016T002752Z`

---

## Scene 1: What it is (0:00–0:20)
**Screen:** the GitHub repo front page.

> "This is GUIng Forward, a repeatable pipeline that collects the last 30 days of RSS, YouTube and
> podcast material about how AI is changing the way we use computers. AI makes the editorial decisions,
> under a policy I wrote. The output is three Substack articles and three videos. I'll show the
> architecture, trace one published claim back to its source, and show the second run."

## Scene 2: Architecture and entry point (0:20–1:05)
**Screen:** the SUBMISSION.md mermaid diagram, then the terminal.

```bash
sed -n '1,20p' run.sh
ls $P
```

> "One command, `bash run.sh`, creates a run folder. It snapshots the config, policy and prompts, then
> calls two workflows. The collection workflow runs the three collectors in parallel, extracts full text
> and transcripts (YouTube captions, or whisper.cpp locally for podcasts), stores everything, and
> applies the 30-day date filter. Only `data/store.sh` touches the evidence index, which is SQLite.
> Every other stage goes through its commands. The series workflow does AI selection, three briefs,
> articles and video scripts, then automated checks, and it stops for my review. Every stage writes a
> receipt with counts, timings and cost, and every artifact you see here is saved per run."

## Scene 3: Trace one claim (1:05–2:20)
**Screen:** the Substack piece 03, the paragraph about Alexa Plus. Then the terminal.

```bash
bash reporting/trace_claim.sh $P 03-c4
```

> "Here's a published claim: The Verge's smart-home reviewer calls setting up Alexa Plus routines by voice
> 'the game changer', but says agentic errands only occasionally work. That's source 5 in the published
> article. In the pipeline it's claim 03-c4 in the brief; published sources are simply renumbered in
> reading order. It's typed as a *source claim*, because it's the reviewer's opinion and not our fact. Its evidence points to a specific version of a Vergecast episode and to two transcript
> segments: seg-0017, at 08:51, and seg-0022, at 11:39. Those are whisper.cpp transcript segments
> stored in data/assets, and you can read the exact words here. The editorial decision record shows the
> AI accepted this episode as 'the strongest first-hand voice evidence', and it noted the Ring
> sponsorship. Discovery shows it came from the Vergecast feed. The store history shows the same
> version was observed in three runs and never duplicated."

## Scene 4: The second run (2:20–3:15)
**Screen:** the terminal.

```bash
jq -c '{run_id, as_of_date, previous_run_id}' $R2/run.json
jq -r .change $R2/changes.jsonl | sort | uniq -c
bash data/store.sh history podcast:big-technology:59d694e6df2c | jq -c '{v:.version_id[0:12], first_seen_run}'
cat $R2/exclusions.jsonl | jq -c '{item_id, reason, detail}'
```

> "Run 2 ran on a later day, with as-of date October 16. Of 66 items, 58 were unchanged. Those were
> reused from the store, with no re-download and no re-transcription, and no duplicate records. Seven
> were new, including a Vergecast episode called 'Everything's recording everybody', which the AI
> accepted for all three pieces. One was *changed*: Big Technology re-dated and then retitled the same
> episode. The store kept all three versions, and the evidence behind earlier briefs still points to
> the version it used. The window also moved forward a day, and a Mollick post from August 31 is
> re-checked and excluded as outside the window."

## Scene 5: Failure and recovery (3:15–3:55)
**Screen:** the terminal.

```bash
jq -c .collectors runs/live-20261015T043607Z/collection_status.json
jq -r '.errors[0].message' $R2/logs/write_articles-20261016T*.json | head -1
grep resume $R2/logs/run.console.log | head -4
```

> "Two real failures. In one run my RSS collector crashed on a bug. The workflow recorded it as
> incomplete, kept going with the YouTube and podcast evidence, and the summary reported the coverage
> gap. It didn't pretend the empty result was a success. In run 2, the API credit ran out halfway
> through writing piece 3. After adding credit, `run.sh --resume` reused the finished selection, briefs
> and drafts, generated only the missing piece, and the run then passed its checks."

## Scene 6: Human review and the policy revision (3:55–4:40)
**Screen:** `review_notes/run1_decision_review.md`, then `policy_v2_comparison.md`.

> "I reviewed three accepted and three rejected items from run 1. In one case the AI had accepted a
> podcast episode only for a CEO's statement that the hosts relayed second-hand, which my own policy
> said shouldn't count as support. So I added a 'relayed statements' rule and a 'partial duplicates'
> rule, and replayed selection on the identical evidence. The relayed item moved to *defer*. The
> duplicates rule changed a different decision, but the case that motivated it stayed rejected, because
> the AI simply found another reason. I also noticed the series had drifted to agents and dropped my
> glasses and voice themes. Policy could only make that gap explicit; fixing collection is what closed
> it."

## Scene 7: One architectural tradeoff, and the approval gate (4:40–5:15)
**Screen:** the terminal.

```bash
jq -c '{digests_cached, digests_new}' $R2/selection_notes.json
jq -c '{approval, review: .review.passed}' $P/summary.json
```

> "One tradeoff: selection runs in two passes. A cheaper model writes a digest per item, cached by
> version, and then one strong model decides on all items together, so it can spot duplicate
> announcements and missing perspectives. The cost is that the editor reads summaries, not full text.
> In exchange, run 2 reused 82 of 90 digests, and selection cost dropped from $2.34 to $1.28. Finally,
> nothing publishes without me. My approval is bound to a fingerprint of the drafts and evidence, and
> packaging refuses if anything changed after I approved. Thanks for watching."

---

**If you're running long:** shorten Scene 4 to the change counts and the Big Technology history, and in
Scene 6 drop the drift sentences.
