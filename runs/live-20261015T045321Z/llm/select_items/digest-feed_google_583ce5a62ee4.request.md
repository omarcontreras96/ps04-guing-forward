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

ITEM feed:google:583ce5a62ee4
version_id: 60a93943da6c56d051a7ac409a858ba870c0868d3684b32cf59f32e3ddae99c7
kind: feed | publisher: Google Keyword: Gemini (google) | perspective: vendor
title: Introducing Gemini 3.8 Live with Live Avatar
published_at: 2026-09-24T15:30:00Z | url: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-8-live-with-live-avatar/
---
Introducing Gemini 3.8 Live with Live Avatar
Building on the momentum of last week's Gemini 3.8 Live launch, today we are excited to introduce Gemini 3.8 Live with Live Avatar — bringing near real-time visual presence to our native live dialogue models. By pairing near real-time video generation with speech, the Live Avatar feature creates an experience that listens, sees, and speaks with a dynamic visual persona.
With precise lip-syncing, natural expressions, and fluid turn-taking, Live Avatar enables enterprises to expand their virtual offerings more interactively. Whether providing engaging customer service or delivering interactive walkthroughs, it transforms digital exchanges into richer, more accessible experiences.
Starting today, Gemini 3.8 Live with Live Avatar is available in Gemini Enterprise.
See how Gemini 3.8 Live with Live Avatar supports a wide range of characters, each with a distinct look, voice, and expressive presence.
More natural and multimodal conversations
Conversation is inherently multimodal: we listen, look, speak, and use facial expressions to communicate. Live Avatar brings these capabilities to enterprise agents. By processing visual and audio inputs simultaneously, it generates enriching conversations for a more comprehensive experience.
Watch how Gemini 3.8 Live with Live Avatar takes in what it sees and hears in near real time, responding with expressive audio and video for a more natural conversation.
Asynchronous tool execution with continuous presence
Beyond visual presence, the feature is backed by Gemini’s advanced reasoning. With asynchronous tool calling, Live Avatar can trigger tool calls and fetch data in the background while continuing active dialogue, handling complex tasks while ensuring an uninterrupted conversational flow.
See how Gemini 3.8 Live with Live Avatar handles complex tasks like checking in a guest at a hotel. Calling tools in the background while the dialogue continues uninterrupted.
Conversational experiences built for global scale
Conversational presence should feel natural and not be limited by languages. Live Avatar features native multilingual speech-to-speech synchronization. The feature dynamically adapts its lip-sync and expressions and can seamlessly transition across 97 languages without degrading video fidelity or introducing visual drift.
Watch how Gemini 3.8 Live Avatar switches between languages mid-conversation, with lip-sync and expressions adapting seamlessly across 97 languages.
A Live Avatar to fit your brand needs
Organizations often need distinct visual identities to fit their brand. In addition to a library of diverse, preset avatars, organizations can customize their Live Avatars. From a high-quality reference image, developers can generate a fully animated, responsive avatar while preserving reference likeness, brand styling, or character identity. Custom avatar creation is currently available only through enterprise allowlisting.
Trust and transparency at its core
We built Live Avatar with strict safeguards designed to respect identity, and keep AI-generated content transparent. All output generated by our AI products is watermarked with SynthID. This imperceptible watermark is woven directly into the audio and video output, helping to ensure AI-generated content remains detectable to help minimise misinformation and misattribution. To explore our comprehensive approach to safety and responsible deployment, read our model card.
Get started with Gemini 3.8 Live with Live Avatar
Gemini 3.8 Live with Live Avatar is available in Gemini Enterprise. Explore the API documentation to get started.
=== END ITEM ===

