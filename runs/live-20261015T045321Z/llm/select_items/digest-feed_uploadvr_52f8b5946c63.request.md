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

ITEM feed:uploadvr:52f8b5946c63
version_id: a889d57d544605414b333be5d32f56029ed1f1a6e3a39393dad3cc4b36d98075
kind: feed | publisher: UploadVR (uploadvr) | perspective: journalism (XR/smart-glasses trade press)
title: Meta Ray-Ban Display Gets New Features, Online Ordering & International Launch
published_at: 2026-09-28T01:07:44Z | url: https://www.uploadvr.com/meta-ray-ban-display-gets-new-features-online-ordering-international-launch/
---
At Connect 2026, Meta announced that Meta Ray-Ban Display is expanding beyond the US, can be ordered online without a fitting, and is getting third-party app discovery, major navigation improvements, and the Hologram avatar system.
Online Ordering & International Expansion
When launching Meta-Ray-Ban Display at Connect 2025 last year, Meta originally said that the HUD glasses would come to the UK, France, Italy, and Canada in early 2026. But following "unprecedented demand and limited inventory", back in January, the company announced it was pausing that plan.
To buy the product, you also needed to secure a demo spot at select physical retail stores, at which an attendant would measure your wrist size to get the optimal Meta Neural Band size, as well as tailor your order to your prescription.
Now, Meta-Ray-Ban Display can be purchased online without a store demo, and it's also available both online and in select stores in the UK and Canada.
It will also be available to buy in France, Italy & Germany on October 13.
In the UK it starts at £749, in Canada at CA$1149, and in Europe €899.
Select stores in London, Vancouver, Toronto, Paris, Milan, Rome, Frankfurt, Hamburg, and Munich will offer in-store demos for prospective buyers.
Major Navigation Improvements
Meta is making the voice of the navigation feature on Meta-Ray-Ban Display far more natural. It will reference the world in front of you instead of robotic street names, for example “turn left at the yellow house ahead”, instead of “turn left at Third Street.”
It's also adding two new navigation types, cycling and public transport, in addition to the current on-foot navigation.
However, Meta's navigation feature remains only available in select cities, a major limitation compared to Snap Specs and the upcoming Samsung HUD glasses powered by Google's software.
Selective Phone Notifications
At launch, Meta Ray-Ban Display could not mirror your phone notifications at all, something we harshly criticized in our review. It would show notifications for built-in applets and features like your text messages, WhatsApp, and Messenger, but not for your other phone apps.
A few months ago, Meta added an optional phone notification mirroring feature. But this was arguably even worse, as it shows all notifications, with no customization.
Now, Meta says you'll be able to "control your notifications and choose the ones you want to turn off".
Third-Party App Explorer
Earlier this year, Meta rolled out the ability to develop visual web apps for Meta Ray-Ban Display, controlled by Meta Neural Band, and developers have already built amazing things.
But discovering these web apps requires following the right developers on social media or knowing about the best third-party aggregators.
To make web apps for Meta Ray-Ban Display discoverable, "later this year" Meta is adding an Explore app on the glasses, which will surface and recommend what the company considers to be the best experiences to try out.
Eventually, it's possible that this could expand to become a full-fledged app store, but Meta hasn't said anything about that.
'Hologram' Avatars
Currently, when taking video calls on Meta Ray-Ban Display, the other person sees either nothing or your first-person view, if you choose to share it.
Later this year, Meta says it will roll out its new Hologram realistic avatar to US Meta Ray-Ban Display owners enrolled in the Early Access program, for use in WhatsApp video calls.
You set up your Hologram by scanning your face and providing a minute or so of sample speech to the Meta AI app. Then, once your Hologram is set up, when you make or receive a WhatsApp video call on Meta Ray-Ban Display glasses, the other person will see this synthetic version of you, with its facial expressions entirely derived from the device's microphones.
You can find more details about Hologram, including our hands-on impressions, in our full Hologram coverage here.
Calendar App On Display
Meta is adding a dedicated Calendar app to Meta Ray-Ban Display, which will let you "see who’s attending a meeting, accept or decline invites, and join meetings, all from your glasses".
It expands on the calendar integration Meta first launched for its displayless glasses last year.
For now, the Calendar app on Meta Ray-Ban Display will only be available in the US.
=== END ITEM ===

