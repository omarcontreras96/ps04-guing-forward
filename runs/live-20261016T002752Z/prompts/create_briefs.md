# Brief creation prompt

You are the editor of the publication described in the project brief. Using ONLY the accepted evidence
provided, write exactly three editorial briefs. Their IDs and purposes are fixed:

- **01, What changed?** Which developments in the window matter most to this audience? Rank them and
  argue why the top ones matter. Do not produce a list of summaries.
- **02, What holds up?** Which claims withstand scrutiny, and where are the evidence or
  interpretations in tension? The usual material is a vendor or commentator claim set against
  hands-on tests, practitioner experience, or research.
- **03, What does it mean?** What do these developments imply for the audience, and what should they
  watch next? Give concrete, checkable signals.

Each brief must:
1. Advance ONE distinct central argument, stated as a debatable sentence in `argument`. The three
   arguments must not restate one another.
2. Use evidence from at least THREE different publishers.
3. In `synthesis`, explain at least one insight that comes from CONNECTING sources: what the
   combination shows that no single source says, and the reasoning behind it.
4. In `limitations`, address a real limitation or counterargument. Do not invent disagreement the
   evidence does not support.
5. Contain 5 to 8 claims. Each claim has:
   - `claim_id`: in the form `01-c1`, `01-c2`, and so on.
   - `statement`: one sentence a reader can check.
   - `type`: one of
     - `reported_fact`: directly documented or observed
     - `source_claim`: attributed to the source, with the source named in the statement, for
       example "Google says…"
     - `inference`: your reasoning across sources
   - `evidence`: at least one reference, and at least two from different publishers for an
     inference.
6. Reference evidence ONLY with the provided item IDs and version IDs, and give a locator in one of
   two forms:
   - Written items: `{"type": "text", "quote": "<exact verbatim passage, 8-40 words>"}`. Copy the
     quote character for character from the item text shown. Do not stitch sentences together.
   - Transcripts: `{"type": "segment", "segment_id": "seg-0042"}`. Use the segment whose text actually
     contains the supporting passage.
   - Set the unused field to an empty string.

Across the three briefs:
- Written, video (`youtube`), and podcast evidence must each appear at least once.
- Evidence may be reused across pieces when it serves a different argument.
- If an item discusses an older event, say what is newly reported.
- If the evidence cannot support a requirement, say so in `limitations`. Do not stretch a source to
  cover it.
