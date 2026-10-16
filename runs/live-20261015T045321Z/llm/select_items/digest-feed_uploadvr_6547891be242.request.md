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

ITEM feed:uploadvr:6547891be242
version_id: 11ad3c82a89da1a53920f617f7e534a0b64f30903de41120eaeb80c8291e9e7a
kind: feed | publisher: UploadVR (uploadvr) | perspective: journalism (XR/smart-glasses trade press)
title: Meta's Smart Glasses Are Getting Its 'Muse' AI Agent
published_at: 2026-09-29T01:26:21Z | url: https://www.uploadvr.com/meta-smart-glasses-getting-muse-ai-agent/
---
Meta's Muse AI agent is coming to its smart glasses "soon", letting it take actions at your request while your phone stays in your pocket.
If you're unfamiliar with the idea of an AI agent, it differs from a simple chatbot in that it can take actions, not just provide a response.
Meta launched Muse, its AI agent, earlier this month on smartphones and the web in the US, and it quickly rose up to the top of iPhone App Store downloads, with strong reviews from both journalists and regular users.
Powered by its Muse Spark AI model, Meta says the agent runs on a private persistent Linux virtual machine in the cloud, with its own web browser, filesystem, and terminal that continue to run regardless of whether your app is open. To achieve your goals, Muse can decide to write and run code, delegate work to multiple subagents, and create scheduled jobs. Muse can also produce documents, PDFs, websites and interactive tools such as spending trackers or dashboards.
Compared to other AI agents that primarily target developers and professionals, Muse is highly consumer-oriented, with a simplified instant messaging style interface and a friendly avatar character, alongside marketing focused on solving tasks related to daily life.
Meta says Muse can book travel, send emails, fill out forms and purchase products through websites. Meta also describes more involved tasks, such as negotiating a bill or helping sell a car, and it can even make phone calls.
To make payments, Muse uses Stripe’s Link, which provides virtual single-use per-payment cards so that the AI never sees your personal card or bank details. Meta says Shop Pay and 1Password support are coming.
For smart glasses specifically, Meta gives examples including booking appointments, checking flight prices, finding replacement parts, logging meals, providing workout guidance and helping buy products the wearer sees. You'll activate Muse by saying "Hey Muse", or the name of your Muse, and then making a request. It will then work in the background and check back when the task is finished.
Meta says it doesn't use Muse data for advertising, though will use it to train future models unless you opt out. Muse's current cloud Linux VM is isolated, but Meta can still access it if it wants. The company says it will launch a Confidential VM option later this year, which even it won't be able to access.
As for when Muse will arrive on smart glasses, Meta officially states "in the coming months", though on-stage at Connect 2026, Mark Zuckerberg said "in the coming weeks", while CTO Andrew Bosworth separately said "soon".
=== END ITEM ===

