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

ITEM feed:uploadvr:12fbdd35a1ef
version_id: 97ab62f5c77eb8fd9e196219b88efd3f6f49437c194a65b4075ef39f4c79f9f3
kind: feed | publisher: UploadVR (uploadvr) | perspective: journalism (XR/smart-glasses trade press)
title: Body Proxy Is A Unique Meta Smart Glasses Game From Tender Claws
published_at: 2026-09-28T21:38:41Z | url: https://www.uploadvr.com/body-proxy-is-a-unique-ray-ban-meta-game-from-tender-claws/
---
Will you be able to prove your value to AI agents by completing challenges that they cannot yet perform? Body Proxy is a location-based immersive game that challenges players to impress the AI at a fictional startup, while wearing Ray-Ban Meta glasses to let them watch, listen and communicate with players. It’s the most fun I’ve had with AI glasses to date.
The experience is from Tender Claws, the award-winning studio behind projects like Stranger Things VR, Face Jumping, The Under Presents: Tempest, Virtual Virtual Reality and more. They are often celebrated for how they leverage the unique features of XR hardware to immerse audiences into story worlds, like with eye tracking to swap character perspectives, and interactive live theatre. This is their first time developing an experience that uses AI glasses.
Winner of the SXSW 2026 XR Experience Jury Award and official selection of TIFF: The Market 2026, Body Proxy is worth highlighting because of its incredibly unique and engaging approach to using Ray-Ban Meta glasses for an entertainment experience. Danny Cannizzaro, who co-founded the studio and co-directed Body Proxy with Samantha Gorman, shares that there are “versions of Body Proxy” being developed for “free-roaming across a variety of spaces” with plans to tour it at more events this and next year.
How AI Glasses Turn Your Reality Into Part Of The Immersive Experience
The AI agents in the game monitor how tasks are being completed through the Ray-Ban Meta glasses being worn by the players. Through the glasses, the system watches, speaks and listens to players throughout the experience. They can make sense of and judge what is happening in the real world. Because of this, the real world space, with physical objects that can be used to try to complete some of the tasks, becomes a part of the story. The features of the Ray-Ban Meta glasses create the bridge between the story and the physical space, transitioning players into the reality of the Body Proxy world but without any sort of digital visual immersion. It is like a form of mixed reality where just the physical space and objects are real, but the experience is driven by the story and immersion through its understanding of what players are doing and the mutual ability to see, speak and listen.
Onlookers can watch players attempt tasks and try to guess which they are attempting based on the list of challenges on a physical screen in the space. The screen includes elements like their digital avatar, and how well they are performing as well.
Tender Claws is used to leaning into available hardware features to create new experiences. Not being VR, Cannizzaro explains that they looked to immersive theatre as inspiration when designing the Ray-Ban Meta experience. “Something like Sleep No More is highly immersive with minimal technology. We’ve framed Body Proxy as a kind of narrative recruiting and onboarding process for this fictional company ... Everything the user does happens within the context of this narrative experience, in which they take on a role and become part of the story…You are still completely interacting with a digital system, but for a large part of the experience there is no screen at all.”
Challenges That Reward Natural Human Creativity
What I love most about Body Proxy is how the experience requires your character to reject any preconceived notions of how one should act and be as playful as possible in order to succeed. Human creativity under pressure is rewarded. There are no options for typical day-to-day actions that have a high probability of being correct. This feels like a nice nod to the value we bring to collaborating with AI agents. The random, unserious challenges also make the experience feel fun instead of too close to where we may be headed.
In the current version of Body Proxy, there are around 100 unusual randomized tasks and variations of them, and a large selection of peculiar physical objects for players to choose and interact with to try to get the AI to accept as many tasks as possible. Often, the objects are switched up between locations where Body Proxy is available.
“One of the joys of watching lots of people play Body Proxy is seeing the creative and innovative ways they approach the same task” shares Producer J Noland. “You may see the same task completed dozens of times over the course of a festival, and then someone approaches it in a completely new and surprising way.”
Proving Your Value To AI Is A Fun, Replayable Spectator Sport (For Now)
Proving your value to AI may seem like a reality in our not-so-distant future, but the playfulness of Body Proxy, its simple onboarding, clear challenge, unique format and wide range of tasks made this something that I caught many people trying to replay. Plus, the players and their choices become the entertainment for others. Cannizzaro shares that the “installation itself has a vaguely Taskmaster, game-show-esque vibe to it that always attracts a crowd.” There is intrigue in what each player will attempt and how. Both the player and audience get to view an entertaining generated video report at the end of each playthrough that analyzes performance and what the performance says about each proxy.
Unlocking New Immersive Experiences With Smart Glasses
There are different versions of Body Proxy in development, including “versions of the project running off phones and webcams as well.” shares Cannizzaro. Tasks in the current version are human-generated in advance, but a “roaming version of this project that takes place in a less controlled environment could incorporate a step where we have AI generate tasks based on the objects it sees around you.”
I hope that this experience inspires more game content for smart glasses. Story IP across genres could benefit from Tender Claws’ location-based entertainment concept.
=== END ITEM ===

