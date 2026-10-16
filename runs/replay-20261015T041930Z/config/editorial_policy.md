# GUIng Forward: Editorial Policy (v2)

This policy is given to the model during item selection, brief creation, and drafting. It states what
the publication counts as evidence and how it decides. When the policy and a source disagree, the
policy wins.

## 1. Audience relevance
Accept material only when it helps an enthusiastic, non-specialist reader answer the recurring question:
*which new ways of interacting with computers through AI are actually changing how people use them, and
which are still demos?*

- **Relevant:** something a reader could use, buy, or try, or something that changes how a person
  operates a computer, phone, browser or device. Examples are agents acting in software, assistants
  using personal context, voice or multimodal interaction, AI in the OS or browser, and new AI devices.
  Evidence about how well these work for real people also counts: reliability, failures, privacy,
  learning curve, and accessibility.
- **Not relevant on its own:** model benchmarks, funding, valuations, chips, data centres, enterprise
  sales, or policy debates with no interface consequence. A relevant item may *mention* these.
- A long podcast or video is relevant when a substantial, identifiable passage addresses the themes,
  even if most of the episode is about something else. Evidence must come from that passage. A passing
  news recap inside an otherwise off-topic episode is not a substantial passage (see 3, relayed
  statements).

## 2. Freshness
- Only material published within the run's 30-day window can support claims. The pipeline enforces
  this mechanically before selection.
- A recent source discussing an older event is admissible only for what is **new**: new data, new
  user experience, a new interpretation. The decision and brief must say which older event is
  discussed and what is newly reported.
- Re-uploads and reposts of older material are not new developments.

## 3. Credibility: judge the claim, not the brand
Rate the support for each claim, not the outlet's reputation, popularity, or the model's own confidence.
Credibility is strongest to weakest in this order:
1. **Direct observation or measurement:** hands-on testing, a study with described method and
   participants, reproducible demonstrations, logs.
2. **Specific first-hand experience** from a named practitioner, with concrete details.
3. **Vendor statements of what shipped:** availability, price, features. These are reliable for *what
   exists* and unreliable for *how well it works*.
4. **Vendor or commentator claims about impact, adoption, or the future.** Treat these as claims to
   attribute, never as facts.
5. **Anonymous, second-hand, or unsourced assertions.** Do not use them as support.

Several outlets repeating one announcement count as **one** underlying claim, not corroboration.
Independent corroboration means separate observation by different parties.

**Relayed statements.** A source that reports what someone else said is relaying it. Examples: podcast
hosts recounting a CEO's remarks, or a news item read on air. If the original statement is not itself in
the evidence, the relayed version is second-hand (level 5). It may appear only as an attributed
`source_claim` that names both the relayer and the original speaker, for example "The Vergecast reported
that Jamie Dimon said…". It can never be the only support for a claim. An item whose only relevant
passage is relayed news is **deferred**, not accepted, unless the primary source is also in the
evidence.

## 4. Commercial incentives
Identify when the source benefits from the claim: a vendor about its own product, a creator with
sponsorships, an investor about a portfolio company. Such material is accepted for what it
documents (what shipped, how it is supposed to work). Its performance claims must be attributed
("Google says…") and, where possible, checked against an independent source.

## 5. Novelty
Prefer items that add something the selected set does not already have: a new development, a
first-hand test, contrary evidence, or a research finding. When two items carry the same claim, accept
the one with the more direct evidence and **defer** the other.

**Partial duplicates.** Independent coverage of an announcement is a duplicate only if it adds nothing
to the vendor's own account. Added details are new information: availability, price, who can actually
use it, restrictions, or the reporter's own testing. Such an item may be accepted for that added detail,
while the vendor's post stays the source for the vendor's own claims. A pure duplicate is
**deferred**. Duplication alone is never a reason to reject.

## 6. Diversity of perspectives
The selected set should include vendor announcements, independent journalism or reviews, practitioner
experience, and research. Accept a weaker item from an under-represented perspective over a stronger
duplicate from an over-represented one. Name the perspectives that remain missing; for example, users
outside tech, accessibility users, non-US users, privacy advocates.

**Theme coverage.** The series must engage each recurring theme in the project brief, not only the theme
with the most news that month. During selection, before accepting another item on a theme that is
already well covered, check whether an eligible item addresses an under-covered theme, and prefer it
when its evidence is usable. If no eligible item gives usable evidence for a theme, say so explicitly:
in the selection summary, and in the limitations of the piece where that theme belongs. Never
substitute an adjacent topic and present it as coverage of the theme. Coverage must come from evidence,
not from stretching a weak source.

## 7. Uncertainty, conflict, and unsupported claims
- Label every claim as one of three types:
  - **reported_fact:** directly observed or documented.
  - **source_claim:** asserted by a source and attributed to it.
  - **inference:** our reasoning across sources, with the reasoning stated.
- When sources conflict, report both and explain the likely reason for the difference: a different
  product version, different task, different user, or different incentive. Do not pick a winner
  without evidence.
- Do not manufacture disagreement. If the evidence agrees, say so.
- Say plainly when the evidence is too thin to support a conclusion.
- Never fill a gap with outside knowledge or invented sources. If something is not in the evidence,
  it does not appear as a claim.

## 8. Decisions
- **accept:** relevant, in-window, and contributes evidence to at least one of the three pieces.
  State which piece and why.
- **defer:** relevant but redundant (a pure duplicate, see 5), weaker than an accepted item carrying
  the same claim, relevant only through a relayed statement (see 3), or useful only if a later edition
  follows that thread.
- **reject:** off-topic for this audience, not substantive (too thin, promotional fluff), or with no
  usable evidence passage. Do not reject an item only because it duplicates another.

Every decision states its reason in one or two sentences, naming the specific evidence. "Seems
relevant" is not a reason.

## 9. The three pieces
- **01 What changed:** which developments in the window matter most to this audience, and why. Rank
  them; do not list them.
- **02 What holds up:** which claims withstand scrutiny, and where the evidence or interpretations are
  in tension. The usual pattern is a vendor claim set against independent tests or practitioner
  experience.
- **03 What it means:** the implications for the audience, and what they should watch next, with
  concrete signals that would confirm or overturn the analysis.

Each piece needs at least three independent publishers. Across the series, written, video, and podcast
evidence must all contribute.
