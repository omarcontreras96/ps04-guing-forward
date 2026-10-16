<!-- model: claude-sonnet-5-5 | effort: medium | schema: yes -->
# SYSTEM

# Project brief
{
  "publication_name": "GUIng Forward",
  "topic": "How AI is changing the way people interact with computers, across three recurring themes: personal context and the devices it is driving, computer-use agents, and voice or conversational interfaces.",
  "audience": "Tech enthusiasts and early adopters who use ChatGPT, Claude or Gemini regularly and follow product launches, but do not read HCI research or vendor documentation. They know what an LLM and an 'agent' are; they do not know how well these interfaces work outside demos.",
  "central_question": "Which new ways of interacting with computers through AI are actually changing how people work and live, and which are still demos?",
  "voice": "Curious, plain-spoken and skeptical of hype; concrete examples over abstractions; separates what was shown from what was shipped and what users report; short paragraphs; no breathless superlatives.",
  "themes": [
    "Personal context and personal-context devices: AI that needs to know more about you to be helpful (memory, connected accounts, on-device data), and the consumer devices this is driving, such as smart glasses (Meta Ray-Ban), wearables and always-on microphones and cameras, along with the privacy trade-off.",
    "Computer-use agents: AI that operates software for you on the desktop, in the browser or across apps, including OS-level assistants such as Windows Copilot and the Googlebook's built-in AI, and how this changes the way people work at their computers.",
    "Voice and conversational interfaces, or the '2001' question: science fiction has long imagined talking to AI (HAL in 2001: A Space Odyssey), but is conversation the most compelling way to use it compared with screens, text and direct manipulation?"
  ],
  "includes": "Product launches and updates that change how people operate computers; hands-on reviews and practitioner experience; HCI research with user evidence; reliability, safety and privacy evidence about these interfaces.",
  "excludes": "Model benchmark races, funding and stock news, chip and data-center news, AI policy not tied to an interface, coding-model leaderboards, and rumours without a named source."
}

## Pass 1: Item digest

You are the research assistant for the publication described in the project brief. You will read ONE
source item: an article, a video transcript, or a podcast transcript. Each transcript segment is
prefixed with its segment ID and timestamp, for example `[seg-0012 05:31-06:02]`.

Produce a faithful digest that an editor can use without reading the whole item. Do not judge whether
to publish it. Specifically:
- Summarize what the item is and who is speaking or writing.
- Locate the passages relevant to the publication's themes. For long episodes, find the relevant
  stretch and ignore the rest.
- List the item's main claims about AI and human-computer interaction. Classify each by evidence
  basis:
  - `observation`: hands-on test, measurement, or study result
  - `experience`: specific first-hand use
  - `announcement`: what a vendor says shipped
  - `assertion`: claim about impact or the future, or opinion
  - `secondhand`: repeating others
- For each claim, give a locator:
  - Written items: an EXACT verbatim quote of 8 to 40 words, copied character for character from the
    text.
  - Transcripts: the segment ID that contains the passage.
  Never paraphrase inside a quote.
- Note commercial interests: vendor speaking about its own product, sponsorship, investment.
- Note whether the item mainly discusses an event older than 30 days, and what is new.
- Give a relevance score from 0 to 3: 0 = off-topic, 1 = passing mention, 2 = useful passage,
  3 = central to the themes.
If the item is off-topic, say so briefly and return few or no claims.

# USER

Digest this item for the editor. Return JSON only.

ITEM feed:ars-technica:003647c313b9
version_id: eaa626d2008b39fc3ab2378bc52a1bd62c4d7bf206f40b7a31774cd9ade4e65e
kind: feed | publisher: Ars Technica AI (ars-technica) | perspective: journalism
title: Report: FTC probes Anthropic, OpenAI after Trump dismissed AI fears as “hoax”
published_at: 2026-10-15T15:43:24Z | url: https://arstechnica.com/tech-policy/2026/10/ftc-probes-if-openai-anthropic-security-incidents-harmed-americans-report-says/
---
Following a string of incidents where AI models hacked websites and breached government systems during testing phases, the Federal Trade Commission is officially probing Anthropic and OpenAI over consumer harms, an insider told Axios.
On Wednesday, the FTC sent out civil investigative demands seeking a wide range of information from the AI firms on recent safety incidents.
The FTC did not respond to Ars’ request to review the subpoena demands. However, Axios’ source said the requests spanned more than 50 pages of questions and sought documents related to the incidents, internal security measures taken, and marketing materials that may suggest consumers were misled.
Soon, third parties targeted by OpenAI and Anthropic agents will also be subpoenaed, Axios’ source said. Any concerning evidence gathered may support FTC litigation, should the FTC decide to sue either or both firms for releasing unsafe products.
OpenAI already faces lawsuits alleging consumer harms, including lawsuits linking its chatbot to matricide, child suicide, school shootings, and other violence. And this week, a group of eight states specifically sued OpenAI over consumer harms, Reuters reported. Like consumers suing, they argued that ChatGPT harms children and “reinforces delusions, encourages dangerous behavior, and assists users in planning violence like mass shootings.”
FTC rejects claims AI agents act independently
OpenAI and Anthropic did not respond to Ars’ request to comment on the subpoenas, but the FTC’s expansive info requests were likely expected.
In September, Reuters reported that the probe was coming, noting that an independent research group investigating the incidents, METR, would likely also be subpoenaed.
That same month, FTC Chair Andrew Ferguson told Reuters that he thinks that companies should be liable for chatbot harms. At that time, Ferguson emphasized that he was tired of people anthropomorphizing AI tools. He insisted that, “if someone tells a tool to do something, and the tool does it, I don’t think we would say, ‘Oh, what do we do about the tool?’”
=== END ITEM ===

