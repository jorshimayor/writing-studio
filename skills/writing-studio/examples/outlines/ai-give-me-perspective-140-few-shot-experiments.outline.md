---
topic: What actually moves few-shot accuracy, from 140 controlled experiments
user_need: Give Me Perspective
domain: AI
channel: blog
profile: jorshimayor
reader: developers who write few-shot prompts and have never measured what helps
level: intermediate
primary_keyword: few-shot prompting
secondary_keywords: [in-context learning, prompt format, few-shot examples]
title: I Ran 140 Few-Shot Experiments: Here's What Actually Matters
seo_title: Few-Shot Prompting: What 140 Experiments Show Matters
meta_description: I changed one thing at a time across 140 few-shot prompting runs. Prompt format moved accuracy up to 41 points, while correct labels barely mattered.
slug: few-shot-prompting-experiments
cta: Clone the notebook and rerun the experiments on your own model
target_length: 1,600 to 2,000 words
keyword_source: autocomplete + SERP
status: example
---

# I Ran 140 Few-Shot Experiments: Here's What Actually Matters

## Title options
| # | Title | Characters | Hook | Why it could win |
|---|---|---|---|---|
| 1 | I Ran 140 Few-Shot Experiments: Here's What Actually Matters | 58 | First-person proof | Original data, curiosity |
| 2 | Few-Shot Prompting: What 140 Experiments Show Matters | 52 | Keyword: payoff | Keyword first |
| 3 | Your Prompt Template Matters 5x More Than Your Examples | 53 | Surprise | Counter-intuitive number |
| 4 | One Example Made My Model Worse Than None | 41 | Surprise | Strong social hook |
| 5 | I Flipped Every Label In My Prompt. Accuracy Barely Moved | 56 | Result | Memorable experiment |
| 6 | Few-Shot Examples: Count, Order Or Format? I Tested All Three | 59 | Comparison | Answers a real question |
| 7 | What Moves Few-Shot Accuracy? A Controlled Study | 47 | Question | Research framing |
| 8 | Few-Shot Prompting Mistakes I Measured On A Small LLM | 51 | Mistake | Practical angle |

## Reader desires
- I want a clear point of view backed by evidence.
- I want honesty about the limits of the result.
- I want something I can apply to my own prompts.

## Search intent
- Format that ranks: prompt engineering guides with tips, few with original data.
- Questions to answer: how many examples should I use, does order matter, do labels need to be correct.
- Gap: almost nobody publishes controlled, reproducible results. This piece does.

## Intro plan
- Setup: "add a few examples" is standard advice, but nobody says which choices matter.
- Why it matters now: every prompt template ships into production and nobody measures it.
- Implied roadmap: the headline finding, the setup, the surprising results, the caveats, what to do.
- Transition: the biggest effect came from the part people tweak least.

## Outline
### H2: Few-Shot Prompting Format Matters More Than Your Examples
- Purpose: the headline finding with evidence.
- Key points: template changes moved accuracy 36 to 41 points and label words 31, while order moved it 8 to 9 and label correctness 6. One template collapsed to "negative" 97% of the time (49% accuracy).
- Keywords: few-shot prompting; prompt format
- Visual: the effect-size bar chart, alt "what moves few-shot prompting accuracy, ranked".
- Links: [the experiment notebook](https://github.com/jorshimayor/AI-Engineering-Flow_Research)

### H2: How I Tested Few-Shot Prompting
- Purpose: method, enough to trust and reproduce.
- Key points: Qwen2.5-0.5B base, SST-2 sentiment, the same 150 test reviews, label log-prob scoring, 140 configurations varying one factor at a time.
- Keywords: in-context learning

### H2: Why One Example Was Worse Than None
- Purpose: supporting finding 2.
- Key points: 1-shot averaged 74% (as low as 59%) against 87% zero-shot; more shots mostly cut variance (std 0.10 to 0.01); label mass rose from 0.62 to 0.99.
- Keywords: few-shot examples

### H2: Wrong Labels Barely Changed Few-Shot Accuracy
- Purpose: supporting finding 3.
- Key points: random labels cost about 1 point; fully flipped labels still gave 84%. Small models follow their prior, matching published work.
- Links: [Rethinking the Role of Demonstrations (Min et al.)](https://arxiv.org/abs/2202.12837)

### H2: What I Got Wrong and the Limits
- Purpose: honest caveats.
- Key points: one small model and one easy task; order effects were smaller than the literature reports; calibration helped some prompts and broke others (72% to 44% with arbitrary labels).

### H2: What This Means for Your Few-Shot Prompts
- Purpose: takeaways and how to reproduce.
- Key points: test 3 to 5 templates first, use natural label words, use 4 or more balanced examples or none, build a 100-example eval before tuning.
- Links: [the newsletter](https://jorshimayor.substack.com), [the video breakdown](https://www.youtube.com/@jorshimayor)

## Internal links
| Anchor text | URL | Section |
|---|---|---|
| the experiment notebook | https://github.com/jorshimayor/AI-Engineering-Flow_Research | Headline finding |
| the newsletter | https://jorshimayor.substack.com | What This Means |
| the video breakdown | https://www.youtube.com/@jorshimayor | What This Means |

## Sources
- https://arxiv.org/abs/2202.12837 (random labels finding)
- My own results: results/week2/icl_runs.jsonl in the notebook repo

## Repurposing plan
- Newsletter hook: "Adding one example made my model worse than adding none."
- Video chapters: one per finding, with the summary chart.

## Open questions
- Optional stretch: rerun on a 1.5B model to see whether format sensitivity shrinks with scale.
