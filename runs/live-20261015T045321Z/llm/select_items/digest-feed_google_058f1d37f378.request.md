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

ITEM feed:google:058f1d37f378
version_id: 7f957a1892a7b40d03c1b7ce43629c1043769c1133331b3bed14253863340099
kind: feed | publisher: Google Keyword: Gemini (google) | perspective: vendor
title: Guided Vision in Gemini Live: built for accessibility
published_at: 2026-10-01T16:00:00Z | url: https://blog.google/innovation-and-ai/products/gemini-app/guided-vision-gemini-live/
---
Guided Vision in Gemini Live: built for accessibility
Today, we’re launching Guided Vision in Gemini Live across compatible Android devices — bringing voice-forward, real-time visual interpretation to people who are blind, have low vision, or want intuitive visual assistance.
Technology is most powerful when it opens up the world for everyone, and Guided Vision turns Gemini into a conversational visual partner. Guided Vision was developed through close collaboration with the accessibility community. We previewed it earlier this month, among other tools to expand digital and physical accessibility across Android.
To train Gemini Live for conversational, real-world context, we partnered with Aira to visually interpret data for a total of tens of thousands of hours. More than 1,000 members of Aira’s Trusted Tester network helped stress-test and refine the model across daily routines, while Aira specialists worked directly with our teams as subject-matter experts to help establish and evaluate our safety guardrails.
Now, you can simply share your camera during a Gemini Live session to hear clear descriptions of your surroundings, ask detailed follow-up questions, and receive proactive, spoken cues to center whatever you want to explore.
Real-time visual assistance designed for how you experience the world
When you share your camera in Gemini Live with Guided Vision turned on, Gemini acts as a conversational partner. If your camera is pointed too high, too close, or slightly off to the side, Gemini provides natural verbal prompts to help you reframe — asking you to pan slowly to the right, tilt downward, or step back so it can get the clear visual context needed to answer your questions.
Everyday moments made simple
Whether locating objects, preparing a meal, or picking an outfit, Guided Vision supports everyday tasks where quick visual verification matters most:
- Reading fine print and complex text: Read small nutrition labels on food packages, decipher appliance dials and washing machine cycles, or read printed menus in dimly lit restaurants.
- Finding and locating objects: Search your immediate area for everyday items, such as finding a dropped earbud on the floor or locating the black pepper inside a crowded spice cabinet.
- Describing objects and matching details: Ask about colors, patterns, and shapes — such as checking whether a striped shirt pairs with a pair of trousers or identifying the color of a specific jacket.
- Exploring your immediate environment: Get descriptive overviews of unfamiliar spaces, room layouts, or objects placed across a table.
- Conversing naturally in your preferred language: Guided Vision supports conversations across multiple languages. It reflects extensive testing and feedback from blind and low-vision communities across India, Brazil, Singapore, Indonesia, Japan, and more to make descriptions, reframing cues, and answers feel natural and helpful.
Like many accessibility innovations, Guided Vision also provides practical visual assistance for older adults, individuals with low literacy, or anyone trying to read fine print in low lighting.
Quick access across Android
Guided Vision is designed to fit seamlessly into daily routines with minimal friction:
- Gemini App: Open your profile settings in the Gemini mobile app and switch on Use Guided Vision in Live. From there, open Gemini Live and tap to share your camera.
- Accessibility Shortcuts: Under Android Settings > Accessibility > Vision assistance > Guided Vision, configure an Accessibility shortcut to launch Guided Vision using the floating accessibility button, a two-finger swipe gesture, or by pressing both volume keys.
- TalkBack Integration: Users running Google TalkBack can bring up the TalkBack menu with a three-finger tap and select Guided Vision directly.
As with any generative AI technology, Guided Vision is an assistive utility and can make mistakes. It is not a medical device, mobility aid, or white cane replacement, and it’s not intended for navigation, safe-travel guidance, or obstacle detection. Users should continue relying on established mobility aids and safe-travel practices in physical environments.
Guided Vision is now available on Android devices running Android 9 and above in regions and languages where Gemini Live is supported. Make sure your Gemini app and Android system software are updated to the latest versions to get started.
=== END ITEM ===

