---
topic: How an LLM's context window works, and why "fits in context" doesn't mean "remembered"
user_need: Explain It
domain: AI
channel: blog
profile: jorshimayor
reader: developers building LLM apps who know what a prompt is but not what happens to it
level: intermediate
primary_keyword: context window
secondary_keywords: [tokens, long context, lost in the middle]
title: How Does A Context Window Work In LLMs?
seo_title: How Does a Context Window Work in LLMs? Tokens Explained
meta_description: A context window is the model's working memory, measured in tokens. See how it fills up, why long context isn't perfect recall, and what it means for prompts.
slug: how-does-a-context-window-work
cta: Clone the experiments and run the passkey test yourself
target_length: 1,800 to 2,400 words
keyword_source: autocomplete + SERP
status: example
---

# How Does A Context Window Work In LLMs?

## Title options
| # | Title | Characters | Hook | Why it could win |
|---|---|---|---|---|
| 1 | How Does A Context Window Work In LLMs? | 38 | Direct question | Exact autocomplete phrasing |
| 2 | Context Windows Explained: Tokens, Limits And Recall | 51 | Keyword: payoff | Covers three sub-queries |
| 3 | Your LLM's Context Window Is Smaller Than It Looks | 50 | Surprise | Challenges an assumption |
| 4 | I Hid A Passkey In 8,192 Tokens: What The Context Window Did | 59 | First-person proof | Original experiment |
| 5 | What Fills An LLM Context Window (And What Gets Lost) | 52 | Curiosity | Practical framing |
| 6 | Context Window Vs Memory: Why Long Prompts Still Fail | 53 | Comparison | Common confusion |
| 7 | How LLM Context Windows Work: A Developer's Guide | 48 | Audience | Clear promise |
| 8 | Context Window Limits Every Prompt Engineer Should Know | 55 | Audience callout | Skimmable list angle |

## Reader desires
- I want the mechanism, not just "it's the model's memory".
- I want concrete numbers and an example I can reproduce.
- I want to know what this changes about how I write prompts.

## Search intent
- Format that ranks: explainers from model providers plus a few blog deep dives.
- Questions to answer: how does context window work in LLM, what fills it, what happens when it's full, does a bigger window mean better recall.
- Gap: few pieces show a reproducible test. Mine has one (passkey retrieval from 512 to 8,192 tokens on Qwen2.5-0.5B).

## Intro plan
- Setup: model pages advertise ever-larger windows, yet long prompts still produce answers that ignore key details.
- Why it matters now: agents and RAG pipelines stuff more into context every month.
- Implied roadmap: what a window is in tokens, what fills it, the gap between capacity and recall, what to do about it.
- Transition: start with what the model actually receives.

## Outline
### H2: How Does a Context Window Work Under the Hood?
- Purpose: the central mechanism.
- Key points: text becomes tokens; attention reads every token in the window on each step; past the limit there's no position for new tokens. Show GPT-2 failing at token 1,025 as the hard limit.
- Keywords: context window; tokens
- Links: [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- Visual: diagram of a window filling with system prompt, history, documents and output, alt "context window filled with tokens".
- Transition: so what is competing for those slots?

### H2: What Fills a Context Window? Tokens, Prompts and History
- Purpose: show the budget.
- Key points: system prompt, chat history, retrieved documents, tool results and the output all share one budget. Token counts differ by language (link my tokeniser piece).
- Keywords: tokens
- Links: [my AI engineering notebooks](https://github.com/jorshimayor/AI-Engineering-Flow_Research)

### H2: Why a Long Context Window Isn't Perfect Recall
- Purpose: correct the main misconception.
- Key points: capacity is not use. My passkey test found the key 50 of 50 times up to 8,192 tokens, but that's an easy copy task. Harder multi-document tasks show the "lost in the middle" effect.
- Keywords: long context; lost in the middle
- Links: [Lost in the Middle (Liu et al.)](https://arxiv.org/abs/2307.03172)
- Visual: my passkey heatmap, alt "passkey retrieval accuracy by context length and depth".

### H2: What a Context Window Means for Your Prompts in Practice
- Purpose: apply the mechanism.
- Key points: put instructions and key facts at the start or end; trim history; retrieve fewer, better documents; measure instead of assuming.
- Links: [Anthropic's guide to context windows](https://docs.anthropic.com/en/docs/build-with-claude/context-windows)

### H2: Going Deeper Into Context Windows
- Purpose: next step and CTA.
- Key points: run the notebook; read the follow-up on few-shot examples, which also spend context.
- Links: [the newsletter](https://jorshimayor.substack.com), [the video walkthrough](https://www.youtube.com/@jorshimayor)

## Internal links
| Anchor text | URL | Section |
|---|---|---|
| my AI engineering notebooks | https://github.com/jorshimayor/AI-Engineering-Flow_Research | What Fills a Context Window |
| the newsletter | https://jorshimayor.substack.com | Going Deeper |
| the video walkthrough | https://www.youtube.com/@jorshimayor | Going Deeper |

## Sources
- https://arxiv.org/abs/1706.03762 (attention mechanism)
- https://arxiv.org/abs/2307.03172 (position effects in long contexts)

## Repurposing plan
- Newsletter hook: "The model found my passkey 50 of 50 times, and that's exactly why the test proves less than it looks."
- Video chapters: one per H2, with the passkey demo as the visual.

## Open questions
- Add the context sizes of 2 to 3 current models, dated, from their official docs.
