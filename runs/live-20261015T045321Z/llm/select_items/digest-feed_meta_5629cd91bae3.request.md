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

ITEM feed:meta:5629cd91bae3
version_id: 0dc74b59b64d6633f1968dbb1911fe5a4bb9a4f8bff9140b3dbd5f6c8a68723e
kind: feed | publisher: Meta Newsroom (meta) | perspective: vendor
title: More Than Three Quarters of Small Business Owners Say AI Makes Them More Productive, But Most Need More Guidance
published_at: 2026-10-15T00:50:50Z | url: https://about.fb.com/news/2026/10/more-than-three-quarters-of-small-business-owners-say-ai-makes-them-more-productive-but-most-need-more-guidance/
---
Today, we’re releasing findings from a new YouGov study we commissioned of almost 4,000 small business owners across nine APAC markets: Australia, Singapore, Vietnam, Indonesia, Taiwan, India, Thailand, Japan and Hong Kong, on how AI is helping them grow, compete with larger businesses and reach customers beyond their borders.
AI adoption is already broad, with 84% of surveyed small business owners currently using AI, 76% reporting a positive impact on productivity and 71% reporting a positive impact on revenue or sales over the past 12 months. Small business owners also report AI helps tackle two significant challenges facing small businesses: limited resources and limited time.
- Owners say AI is helping small businesses compete. Across the nine markets, four in five (80%) owners agree AI helps small businesses compete more effectively with larger companies, and the same proportion say it makes starting a business easier. 83% agree AI enables small businesses to do things that previously required significantly more money or resources.
- And, they say the time saved is going back into the business. Among those reporting a positive productivity impact from using AI, 58% are using the time to improve the quality of their existing work, 50% are putting it into growth and business planning, and 46% are getting more done with the team they already have.
- The everyday uses are practical. Among surveyed owners whose business has used AI in the past 12 months, 51% have used it to create or edit content, 43% for local advertising and marketing, 38% for translation, and 37% for customer support and communications.
From Adoption to Advantage
More than four in five owners surveyed (86%) say small businesses need more guidance to gain the full benefits of AI. Cost is the leading barrier to training, cited by 51%. When asked what support they would value most, owners pointed to clearer information on cost and return on investment, and guidance on data privacy and security.
In other words, small businesses have adopted AI – what they’re asking for now is help using it well. To make the most of AI, they need free training, clearer information on costs and returns, and policies that support access and investment in AI and digital skills.
Helping Small Businesses Get More From AI
That’s why we’ve been partnering with governments and industry associations to help businesses use AI effectively, so more entrepreneurs can compete and contribute to economic growth. This research follows the launch of the Meta Small Business Growth Academy across Asia-Pacific earlier this year – a programme built to help small businesses move from small to scale using digital and AI-enabled tools to find customers, improve productivity and grow across borders. Delivered with governments, chambers of commerce and local programme partners, it offers practical training in AI-enabled advertising, Reels, WhatsApp for Business and cross-border commerce.
Small businesses can get started with AI-enabled tools from Meta today, including Advantage+ to create and run high-performing ads, ads that click to WhatsApp to turn conversations into customers, and Meta Business Agent to handle customer enquiries automatically.
In Indonesia, Husnul Khotimah, founder of modest fashion brand Zayya, used Small Business Growth Academy training to expand into Malaysia on a daily ad budget of just Rp30,000 [approx USD 1.68]. Using business tools from Meta, she generated 50 enquiries , while reducing customer response times from 30 to 60 minutes to under two minutes. This helped to increase sales – she reported more than eight times return on ad spend for this campaign.
Ms Khotimah says, “Meta has helped me see what is possible for a small business like Zayya. I used to think AI was mainly for writing captions and creating content, but I’ve learned that it can also help me understand new markets and reach the right customers. Using tools like Advantage+, we’ve been able to reach customers beyond Indonesia with a small advertising budget, while giving me more time to grow the business and connect with more women who share the same needs that inspired Zayya in the first place.”
At Meta, we believe the future is for everyone, and that includes small businesses. We’ll keep working with governments, partners and entrepreneurs across APAC so more small businesses have the skills, tools and confidence to grow with AI.
About the research
The research was commissioned by Meta and conducted online by YouGov among 3,983 small business owners across Australia, Singapore, Vietnam, Indonesia, Taiwan, India, Thailand, Japan and Hong Kong. Data was collected between 6 August and 2 September 2026.
Within each market, quotas were applied by business size to achieve a broad and balanced spread across businesses with 1–9, 10–19 and 20–49 employees. The findings provide insights across a diverse cross-section of small businesses in each market, rather than being nationally representative of the small business population. Reported adoption and impact differ across the nine markets surveyed. These differences may partly reflect how owners in each market interpret the questions, as well as translation and local survey response norms.
The post More Than Three Quarters of Small Business Owners Say AI Makes Them More Productive, But Most Need More Guidance appeared first on Meta Newsroom.
=== END ITEM ===

