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

ITEM feed:uploadvr:62aa11e641a8
version_id: fb5049148cdb16842564281f47cb82f93d983ed0f88a96ad7a5b095550cfd3e1
kind: feed | publisher: UploadVR (uploadvr) | perspective: journalism (XR/smart-glasses trade press)
title: Liminal Uses Meta Glasses To Deliver Meditation Based On What You See
published_at: 2026-09-28T21:36:27Z | url: https://www.uploadvr.com/liminal-walking-meditation-uses-meta-ai-glasses-to-deliver-a-meditation-based-on-what-you-see/
---
Liminal, known for its VR app offering short experiences designed around emotional states like calm, focus, and energy, is now applying some of that experience to smartglasses.
Liminal: Walking Meditation is a new experience for Meta AI glasses which uses the camera to capture images as you walk and provides a spoken meditation experience based on what you see, in close to real time. The required smartphone app is slated for release in October on both iOS and Android.
The app is an example of what developers can build using Meta's Device Access Toolkit, which was just demonstrated during the Developer State of the Union at Meta Connect 2026.
I have been trying a prerelease version with my Ray-Ban Meta glasses ahead of Connect. After taking it for a walk around my neighborhood, I found that it feels quite different from simply listening to a meditation recording.
Your Surroundings Become Part Of The Meditation
To begin a Walking Meditation you launch the smartphone app which needs to be paired to your Meta AI glasses during the setup process, and select the theme, voice, and pacing that you would like. Once the walk begins you can pocket your phone and continue hands-free, listening through your glasses while the app uses images to describe what is around you and contextualize it for the meditation session.
On my first walk, I deliberately went outside at night to see how well it could make sense of a darker environment. At one point, it referred to my car sitting nearby and described it in the context of the scenery around me. Even though its vision was limited, it managed to call out details like the "amber streetlights" shining against the darkness.
Liminal co-founder and CEO Damian Moratti told me the company approached smartglasses by asking what they could actually add to the experience.
Moratti said Liminal has always used VR to create strong emotional responses through immersion. Smartglasses gave the team a chance to apply some of that thinking while keeping people engaged with the real world as well.
At launch the app will include twelve meditation themes. In my testing I utilized Presence, Wonder, and Gratitude. Each is guided differently to focus your thoughts in different ways. There are also eight voice and three pacing options.
Pacing does more than change the amount of silence between spoken sections. Liminal CTO Tin Nguyen told me the team is using the setting to shape how much narration you hear and the overall length of the experience. The shortest walks are expected to last around 10 to 13 minutes.
Deciding What Is Worth Talking About
It sounds simple enough, until you start thinking about everything a pair of glasses can see, even during a short walk.
A tree or a statue might be interesting. The garbage cans you have passed every Tuesday for the last ten years probably are not.
Moratti says figuring out that logic has become a major part of Liminal's testing.
During testing, an early version mentioned the garbage cans around eight times. Another noticed a glowing sign inside the window of an adult store and built an unintentionally enthusiastic narrative around it.
As funny as those examples are, they also show how difficult the problem is.
Nguyen says the app isn't constantly shooting and analyzing images. Instead, it periodically takes a look at the current scene as the walk progresses. In his description, it is more like single moments in time rather than a continuous photo stream.
In my testing the narration was very close to real time, with the app focusing on an object such as a particular tree as I would come up to it and pass by. It also would comment on the way the grass met the pavement or the bright sun against the blue sky. Somewhat general in certain ways, but also correctly observed.
The narration was separated by generous moments of silence, so I wasn't overwhelmed by a constant string of prompts. That also made the impact hit harder when a narration did arrive.
What Happens To The Images?
The obvious question with an app that repeatedly looks at your surroundings is where those images go.
Liminal says images captured for Walking Meditation use zero data retention. According to Nguyen, when the app needs context from the environment, an image from the glasses is sent through the phone for AI processing. Liminal is currently using Google Gemini for that processing with zero data retention enabled. Once the response is generated, the image is discarded.
The app also does not request access to the microphone, something Moratti said was a deliberate privacy decision. Users don't have to worry about their conversations being recorded or used a prompts for the meditation.
What About Safety?
Liminal says that the Walking Meditation app will not provide any navigation or route guidance, and that they purposely designed the experience to focus the user on what they see in their surroundings.
Moratti said that they considered whether to develop the ability alert the user to potential hazards, but the difficulty in building that reliably convinced them that the correct choice is to avoid navigation altogether, at least for now.
Liminal Is Moving Beyond The Headset
Walking Meditation is separate from the existing Liminal VR app on Meta Quest, but Moratti sees the two products as complementary, with the VR app providing escape from the real world, while Walking Meditation is built to focus attention on the real world as you walk through it.
I have listened to plenty of guided meditation through headphones, and this does feel different. The environment around you becomes part of the experience.
Adding wellness and meditation capability goes a long way toward improving the practical usefulness of Meta AI glasses. In my brief time testing the experience, I've found it pleasant and effective enough that I plan on continuing with it once it is fully released.
Launching in October
Liminal: Walking Meditation is planned to launch on iOS and Android in October for compatible Meta AI glasses. It will cost $9.99 per month or $99.99 per year, which includes 30 contextual walks per month, and unlimited access to offline scripted versions of each theme.
=== END ITEM ===

