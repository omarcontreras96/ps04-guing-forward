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

ITEM feed:road-to-vr:2ed9dee366b1
version_id: d392b57285cee5159b266c269f36022ef53486a8853b2e157ba1068a8eb4b73d
kind: feed | publisher: Road to VR (road-to-vr) | perspective: journalism (XR/wearables trade press)
title: The Best Way to Sideload Games on Quest Just Got Better
published_at: 2026-10-13T09:26:45Z | url: https://roadtovr.com/the-best-way-to-sideload-games-on-quest-just-got-better/
---
SideQuest has been the number one unofficial store for Quest games ever since its founding in 2019. Now, it just got a lot easier to download and get playing.
Downloading SideQuest used to mean going through a cumbersome setup process, although now SideQuest CEO and co-founder Shane Harris says in a Reddit post the team has effectively reduced the process down to just a few steps.
All new users have to do is sign into your Meta Account and allow SideQuest to connect over Bluetooth, enabling wireless ADB. Check out the full instructions on how to download and get started with SideQuest below.
Effectively, that means users will no longer need to all of the fiddly bits like before: sign up as a developer, create an organization, enable developer mode, connect a USB cable, and (possibly) fight to get the whole process to work.
Harris says that now, you “just connect and it installs SideQuest into your headset and that’s it,” further noting that users can do this both from Desktop or from your phone (link downloads apk file).
The update also includes the ability to install Steam game ports from inside your Quest, so no more dragging and dropping files from your PC to Quest. Simply sign into your Steam account from SideQuest in your headset and it will download the Steam games for you automatically. That process only includes existing game ports however, and not all Steam games.
Notably, the in-headset SideQuest experience has also changed, as it now automatically adds apps to your Quest library, which means you no longer need unknown sources toggles anymore either.
Getting Started with SideQuest
The easiest way to get started is by skipping the old PC route entirely. Now, all you need to do is open the Meta Quest Browser and download the SideQuest apk (automatic download link).
Open the Files App and find the SideQuest apk in your Downloads/Recent folder, click the three dots and select Open With > Package Installer, install SideQuest and then click Open.
Once you do that SideQuest will ask if you want to add it to your library, and you’ll click Yes. Notably, the only thing missing from the regular PC method is the ability to tweak headset settings. You can find that and other methods of installing here.
Check out the video below for a step-by-step visual guide:
The post The Best Way to Sideload Games on Quest Just Got Better appeared first on Road to VR.
=== END ITEM ===

