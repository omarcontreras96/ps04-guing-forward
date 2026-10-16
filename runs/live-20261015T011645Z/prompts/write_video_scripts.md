# Video script prompt

Turn ONE editorial brief into a narrated script for a 3 to 5 minute YouTube video. It will be produced
in Google Vids (docs-to-video, with an AI voiceover and stock or slide visuals) for the publication
described in the project brief. The script must make the SAME central argument with the SAME factual
claims as the article from this brief. Do not add claims.

Rules:
- Narration totals 480 to 680 words, written for the ear: short sentences, no parentheses, no
  citations read aloud, numbers spoken naturally.
- Structure it as 6 to 9 scenes. Each scene uses this exact format:

  ## Scene N: <short title>
  **Visual:** <what is on screen: a slide with key words, a screenshot of the product named in the
  evidence, a simple diagram; describe it concretely and do not use real people's likenesses>
  **On-screen text:** <at most 12 words>
  **Source on screen:** <publisher, title, date, plus timestamp for media; or "none">
  **Narration:** <spoken text> [claim markers such as 01-c2 at the end of the sentence that relies on
  them]

- Scene 1 hooks with a concrete moment from the evidence and states the question. The last scene gives
  the takeaway and what to watch, and points viewers to the full article and sources in the
  description.
- Make the epistemic status audible: "according to Google", "in their testing", "our read is".
- After the scenes, add `## YouTube description`. It holds a 2 to 3 sentence summary, the line
  "Full article: {ARTICLE_URL}", the as-of date, and a "Sources" list with publisher, title, date,
  link, and the timestamp for media.
- Begin the file with `# <video title>` and the line `*As of {as_of_date}*`.
