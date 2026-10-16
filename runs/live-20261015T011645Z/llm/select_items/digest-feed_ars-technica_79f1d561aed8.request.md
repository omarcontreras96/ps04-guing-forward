<!-- model: claude-sonnet-5-5 | effort: medium | schema: yes -->
# SYSTEM

# Project brief
{
  "publication_name": "GUIng Forward",
  "topic": "How AI is changing the way people interact with computers: agents that operate software for you, AI that runs on personal context and new devices, and voice/conversational interfaces versus other modalities.",
  "audience": "Tech enthusiasts and early adopters who use ChatGPT, Claude or Gemini regularly and follow product launches, but do not read HCI research or vendor documentation. They know what an LLM and an 'agent' are; they do not know how well these interfaces work outside demos.",
  "central_question": "Which new ways of interacting with computers through AI are actually changing how people use them this month, and which are still demos?",
  "voice": "Curious, plain-spoken and skeptical of hype; concrete examples over abstractions; separates what was shown from what was shipped and what users report; short paragraphs; no breathless superlatives.",
  "themes": [
    "Computer-use, browser and desktop agents that operate software on the user's behalf",
    "Personal context: assistants that remember or perceive the user (memory, connected apps, glasses, wearables, always-on mics/cameras) and the privacy trade-off",
    "Voice and conversational interfaces versus screens, text and direct manipulation (the '2001: HAL' question)",
    "AI built into operating systems, browsers and devices; generative or adaptive interfaces"
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

ITEM feed:ars-technica:79f1d561aed8
version_id: e9ed6f87df9193e8f5219d2507bdb921c0189f8b2087f6de145a5e28d56a6396
kind: feed | publisher: Ars Technica AI (ars-technica) | perspective: journalism
title: Epic says its new vibe-coded Epic Games Launcher is faster than Steam
published_at: 2026-10-14T21:15:56Z | url: https://arstechnica.com/gaming/2026/10/programming-is-hard-epic-games-leans-on-vibe-coding-for-its-new-launcher-app/
---
Nearly eight years after Epic took on Steam with its own Game Store and launcher, the Fortnite maker is deploying a new tool to give it an edge over Valve: vibe coding.
In announcing the new publicly available “Preview” build of its Epic Games Launcher, Epic writes that “programming is hard. So, instead of doing that, we vibe coded a new Epic Games Launcher that’s way faster and more responsive than the current one, and has a new look.” And while that might sound a little tongue-in-cheek, Epic Games Store General Manager and VP Martin Keely told PC Gamer that the team “started from scratch” and used AI as “a tool to write and review new features and new capabilities from the ground up in a different tech stack than what we had previously.” The goal, Keely said, was to “look at functionality that existed [in the current Epic Games Launcher] and [say] we want to replicate that, but not the code itself.”
Speaking to IGN, Keely clarified that using AI to code the new Launcher “made us more efficient and allowed a small team to rewrite the code base and be able to launch it faster across platforms, support Windows and Mac, and we’re going to have a Linux version as well.”
We vibe coded the Epic Games Launcher to be faster than the other guy.
Don’t believe us? Test it out for yourself in Preview:
https://t.co/pdtAeEIri4 https://t.co/aMxojUUVPV
— Epic Games Store (@EpicGames) October 14, 2026
The focus on startup speed extends to Epic’s social media announcement, which once again stresses that “we vibe coded the Epic Games Launcher to be faster than the other guy.” Ars’s own testing confirms that the new Launcher goes from a cold start to the store page a few seconds faster than Steam (assuming no login or update issues get in the way). Epic also claims the new Launcher can restore from the system tray to the Library screen slightly faster than Steam, though the claimed difference of 0.06 seconds in this seems so small as to be unnoticeable (and was in our testing).
=== END ITEM ===

