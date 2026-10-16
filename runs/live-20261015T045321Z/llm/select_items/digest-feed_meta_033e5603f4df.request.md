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

ITEM feed:meta:033e5603f4df
version_id: 1923223e2258ab48b526fdc74abbbad79d8d67e63599403e466262ddf5c701e3
kind: feed | publisher: Meta Newsroom (meta) | perspective: vendor
title: Introducing Muse Wonder and Muse Wonder Full: Frontier Models for Agents
published_at: 2026-10-12T17:08:05Z | url: https://about.fb.com/news/2026/10/introducing-muse-wonder-models/
---
Fourteen months ago, we began an overhaul of our AI efforts, and in that time we’ve gone from rebuilding our foundations to pushing the frontier. Today, Meta is introducing the Muse Wonder series with Muse Wonder and Muse Wonder Full, our most capable models to date, built on the groundwork we laid with Muse Spark. The models deliver state-of-the-art performance on personal and professional agentic tasks.
Built for Real World Needs
Whether the job is navigating an insurance claim, understanding a lease, or making sense of someone’s finances, a model has to interpret the information in front of it and work through the problem. Muse Wonder and Muse Wonder Full bring that capability to expert domains including law, finance, and health, along with frontier coding performance for people building everything from a game to an app for a new business.
Real work also unfolds over time. That’s why we’ve built our new models to have Active Memory, the ability to carry what matters to you across conversations and bring back the details that are relevant to the task at hand. They’re also equipped with Active Focus, the ability to keep working toward your goal when a task gets hard, try other approaches, recover from errors, and follow through, asking for clarification when needed and checking in before following through on anything important.
How We Build for Safety
A personal agent can take on real tasks for you, which often means working across your messages, calendars, and documents. That’s why we trained the Muse Wonder family to avoid sharing private information without permission; turn down requests to assist in performing actually harmful acts; and work to improve security and strengthen defenses against cyber attacks. Developers and security teams can use models like Muse Wonder to find flaws in their own code and strengthen their systems, so we made sure the models can still do that work. We train, evaluate, and release our most capable AI models in line with the standards set out in our Meta Superintelligence Scaling Framework. A full report with additional safety evaluations will be available soon.
Muse Wonder is available today through the Meta Model API and Muse Code. It will soon power more of Muse, rolling out first to subscribers. This is a major step toward personal superintelligence for everyone, with much more to come.
For a closer look at how these models were built, how they were tested and what they can do, head to our research blog.
The post Introducing Muse Wonder and Muse Wonder Full: Frontier Models for Agents appeared first on Meta Newsroom.
=== END ITEM ===

