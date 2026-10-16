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

ITEM feed:nngroup:ac65fc287798
version_id: ce7126cb18c61286c3941acd07fc9eb0940d5727d091fbde4e4d57df23cb006a
kind: feed | publisher: Nielsen Norman Group (nngroup) | perspective: practitioner (UX research)
title: How AI Works and How Users Think About It: Study Guide
published_at: 2026-09-25T17:00:00Z | url: https://www.nngroup.com/articles/ai-functionality-study-guide/
---
Let’s not pretend we all completely understand the inner workings of artificial intelligence models. Neither do your users. Thankfully, you don’t need to fully understand them to use them. The same has always been true of a computer.
However, the better you understand some of the basics, the more accurate your mental model is. Accurate mental models make you more efficient and help you avoid problems.
These resources can strengthen your mental model of how AI functions and illuminate the mental models your users have for these systems, which dictate their usage of them.
How Artificial Intelligence Functions
Neural networks, unsupervised learning, hallucinations, and sycophancy? There is an entire vocabulary around large language models (LLMs) that suddenly gets thrown around like we all know what they are and why they matter. The resources below break these (and other) relevant AI concepts down into normal language.
| Number | Link | Format | Description | 
| 1 | Artificial Intelligence: Glossary | article | This is a collection of fundamental AI terms and definitions. | 
| 2 | AI: First New UI Paradigm in 60 Years | article | AI introduces a third UI paradigm called intent-based interaction, where users state goals rather than specific commands. | 
| 3 | How Do Generative AI Systems Work? | article | This is a non-technical explanation of how large-language models (LLMs) process user inputs and create their responses. | 
| 4 | How AI Models Are Trained | article | Large-language models (LLMs) learn language and develop their individual styles through multiple phases of training. | 
| 5 | AI Hallucinations: What Designers Need to Know | article | This article explains why AI tends to hallucinate, why that is hard to change, and how it should affect AI product design decisions. | 
| 6 | Sycophancy in Generative-AI Chatbots | article | Large-language models (LLMs) are built to prioritize pleasing users over validating the accuracy of their responses. | 
| 7 | A Concrete Definition of an AI Agent | article | An AI agent pursues a goal by iteratively taking actions, evaluating progress, and deciding next steps; useful agents must be reliable, adaptive, and accurate. | 
| 8 | GenUI vs. Vibe Coding: Who’s Designing? | article | With generative UI, the system decides to generate an interactive element or product in response to a user need; with vibe coding, the user asks the AI to build it. | 
Conversational and Prompt Authoring Patterns
Users' interactions with prompt-based AI tools follow clear, predictable patterns. These resources document and describe the partners we’ve observed in our research since the early days of ChatGPT.
| Number | Link | Format | Description | 
| 1 | Response Outlining with Generative-AI Chatbots | article | Users often include format or structure specifications in prompts to ensure that the chatbot’s response satisfies those requirements. | 
| 2 | Prompt Structure in Conversations with Generative AI | article | Users tend to follow common patterns and structural elements while prompting LLMs. | 
| 3 | The 6 Types of Conversations with Generative AI | article | Research shows six types of AI conversations: search queries, funneling, exploring, chiseling, expanding, and pinpointing. | 
| 4 | Accordion Editing and Apple Picking: Early Generative-AI User Behaviors | article | Two patterns describing the shifting and complex ways in which users carry on task-related conversations with genAI chatbots. | 
| 5 | The 4 Stages of AI Image Generation: An Experience Map | article | AI-image-generation users often follow a similar creative process: ideate, generate, refine, and export. | 
Trust and Anthropomorphism
People inherently seek interactions with people (or systems) that seem to listen to them and understand their needs. The better the AI is at seeming as though it understands a user, the more they trust it and project human-like attributes on it.
| Number | Link | Format | Description | 
| 1 | Prioritize Smarts over Sentience to Increase Trust with AI | article | People trust AI more when it seems smart rather than sentient. AI emotions can reduce trust in factual, task-oriented work. | 
| 2 | The ELIZA Effect - Why We Love AI | article | Users quickly attribute human-like characteristics to artificial systems, which reflect their personality back to them. | 
| 3 | ELIZA Effect: Why We Fall in Love With AI | video |  | 
| 4 | When Should We Trust AI? Magic-8-Ball Thinking and AI Hallucinations | article | It’s easy to place too much trust in genAI tools. Use only information you can verify or recognize to be true. | 
| 5 | The 4 Degrees of Anthropomorphism of Generative AI | article | Users tend to anthropomorphize AI at four different levels: courtesy, reinforcement, roleplay, and companionship. | 
| 6 | Humanizing AI Is a Trap | article | Large-language models (LLMs) humanize by design, and adding personality or emotion amplifies the risk of misplaced user trust. | 
Information Seeking and Search Behaviors
LLMs have introduced a new way for users to seek answers to their questions — a role search engines have dominated for years. While AI has made certain aspects of information seeking easier, it is far from perfect. It remains difficult to know whether its answers are true and trustworthy.
| Number | Link | Format | Description | 
| 1 | How AI Succeeds (and Fails) to Help People Find Information | article | AI can help people who don’t know the words for what they are looking for, but many users still don’t use it effectively. | 
| 2 | How AI Is Changing Search Behaviors | article | Generative AI is reshaping search, but long-standing habits persist. | 
| 3 | AI Chatbots Discourage Error Checking | article | The polish of AI outputs and the high interaction cost make it difficult to check for errors. | 
| 4 | Information Foraging with Generative AI: A Study of 3 Chatbots | article | Users expect AI chatbots to aggregate information in a concise and specific manner, while fully considering contextual cues. | 
| 5 | Information Seeking in China: A Different Ecosystem, Familiar Behavior | article | Information seeking in China is driven by mobile social-media apps, but how users prompt and engage with genAI mirrors Western behavior. | 
| 6 | GenAI for Complex Questions, Search for Critical Facts | article | Users choose AI to explore and synthesize information but rely on traditional search when accuracy and trust are critical. | 
Understanding and Adoption of AI UIs
While there has been an incredible adoption rate of AI across many different user groups, the learning curve can be steep. When users have inaccurate mental models of how the system functions or lack a larger vision of its potential, their usage of it can be underwhelming.
| Number | Link | Format | Description | 
| 1 | AI Adoption in the Workplace Still Low, 2 Years Later | article | Out of ~5,000 working Americans, 81% reported they did not use AI at work. | 
| 2 | Can Users Control and Understand a UI Driven by Machine Learning? | article | Users struggle to understand how complex personalization systems turn their actions into recommendations. | 
| 3 | New Users Need Support with Generative-AI Tools | article | First-time users of Chinese gen-AI chatbots struggled to understand the tools’ functionality. | 
| 4 | ChatGPT, Bard, or Bing Chat? Differences Among 3 Generative-AI Bots | article | Users preferred ChatGPT and Bard over Bing and shared opinions about all three. | 
| 5 | How AI Literacy Shapes GenAI Use | article | AI literacy requires both prompt fluency and the ability to critically assess outputs; frequent use does not imply skilled use. | 
| 6 | AI Literacy | video |  | 
Podcast Episodes
| Number | Link | Format | Description | 
| 1 | 24. Artificial Intelligence: What Is It? What Is It Not? (ft. Susan Farrell) | podcast | Susan Farrell shares some early insights into the potential benefits and drawbacks of AI systems. |
=== END ITEM ===

