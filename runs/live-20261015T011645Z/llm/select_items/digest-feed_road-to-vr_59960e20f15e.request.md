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

ITEM feed:road-to-vr:59960e20f15e
version_id: 752f85378c32b9a1c0803fd0054e3ed790a261d19d5e460b2877672cf3e3904d
kind: feed | publisher: Road to VR (road-to-vr) | perspective: journalism (XR/wearables trade press)
title: Index Headset Goes on Sale for the First Time Ever as Valve Announces Discontinuation
published_at: 2026-10-14T05:55:15Z | url: https://roadtovr.com/valve-index-headset-discontinued-discount/
---
Index, Valve’s PC VR headset released in 2019, is officially on its way out. And to see it along, Valve has dropped the price of everything Index-related.
The News
Valve Index is no longer being produced, which means this could be your last chance to get new stock of the company’s landmark PC VR headset.
Everything is now 20 percent off on the Valve Index page, including:
- Valve Index Headset was $499.00, now $399.20
- Valve Index Replacement Left Controller was $149.00, now $119.20
- Valve Index Replacement Tether was $129.00, now $103.20
If you’re in the US, you’ll notice that Valve is only now selling left replacement controllers. If you’re in the UK or EU, you should still be able to buy both left and right.
Notably, the biggest missing piece is the required SteamVR 2.0 base stations, which give Valve Index six degrees of freedom (6DOF) by emitting lasers. You can find those direct from HTC, priced at $229 for a single unit.
While Index is being discontinued, Valve notes that nothing changes for prior owners, as it’s still supported on Steam and SteamVR.
This follows the release of Steam Frame last month, Valve’s first standalone VR headset that not only includes native VR and non-VR gameplay, but also the ability to wirelessly stream games from a much more powerful PC.
My Take
Valve Index might have been more expensive and less user-friendly than its biggest competitor at the time, Oculus Rift S, but became the choice for VR enthusiasts looking to maximize immersion for good reason. Excellent (for the time) optics, refresh rate, persistence, and resolution. Again, for the time.
And while Index was the leader in visual clarity, it was also one of the first to offer genuinely excellent audio quality too, as the headset’s off-ear speakers are still some of the best in the industry.
Ergonomically, Index was also much more comfortable than its bulk seems to suggest, as the built-in headstrap cradles the back of your head and helps balance out what otherwise might have been an excessively front-heavy weight distribution.
That said, Valve’s PC VR headset probably isn’t worth jumping in at this late date, as I’d consider the sale to be more appealing to existing owners hoping to get their hands on cheaper replacement parts than anyone looking to get into the ecosystem right now.
As it is, the SteamVR tracking ecosystem is on its way out, as most headsets now feature inside-out optical tracking, barring a few late entries, such as Bigscreen Beyond 2 and a number of Pimax headsets, the latter of which offer optional SteamVR tracking faceplates.
That, and the new discounted all-in price (if you can find a right controller in the US) of Index is somewhere around ~$1,200, which is only $100 less than Steam Frame’s top 1TB storage option—and $200 more than the actual all-in Index bundle initially offered in 2019.
It’s also significantly more complicated, as it requires mounting two base stations in your room, although if you’re dead set on getting an Index, check out our review to learn more.
The post Index Headset Goes on Sale for the First Time Ever as Valve Announces Discontinuation appeared first on Road to VR.
=== END ITEM ===

