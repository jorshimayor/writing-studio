# Outline Template and Skeletons

Every outline is a Markdown file named `<slug>.outline.md`. It's the contract between planning and writing: the piece must follow it, and `scripts/outline_check.py` checks the outline against its reader need, and the finished piece against the outline.

## File format

Planned headings are written as `### H2: ...` and `#### H3: ...` so the checker can read them. Every H2 gets `Purpose` and `Key points` bullets, plus `Keywords`, `Links`, `Visual` and `Transition` where relevant.

````markdown
---
topic: <one-line topic>
user_need: <Educate Me | Explain It | Compare For Me | Guide Me | Fix It | Give Me Perspective | Update Me | Inspire Me>
channel: <blog | substack | newsletter | youtube>
profile: <profile name>
reader: <who they are and why they're looking>
level: <beginner | intermediate | expert>
primary_keyword: <phrase>
secondary_keywords: [<phrase>, <phrase>, <phrase>]
title: <recommended title, in the profile's capitalization>
seo_title: <50 to 60 characters>
meta_description: <140 to 160 characters>
slug: <keyword-based-slug>
cta: <what the reader should do next>
target_length: <driven by the reader need>
keyword_source: <autocomplete + SERP | OpenSEO volume/KD | Search Console>
status: outline
---

# <Recommended title>

## Title options
| # | Title | Characters | Hook | Why it could win |
|---|---|---|---|---|
| 1 | ... | 54 | Number | ... |

## Reader desires
- <2 or more things this reader wants, from references/reader-needs.md>

## Search intent
- Format that ranks: <explainer / comparison / tutorial / opinion / video>
- Questions to answer: <from autocomplete, People also ask, forums>
- Gap: <what the current top results miss>

## Intro plan
- Setup: <the situation or problem>
- Why it matters now: <stakes for this reader>
- Implied roadmap: <ideas the body will cover, hinted, not listed>
- Transition: <the question that leads into the first H2>

## Outline
### H2: <Core answer, using a primary keyword variation>
- Purpose: <the question this section answers>
- Key points: <facts, explanation, example, evidence>
- Keywords: <primary variation; secondary keywords>
- Links: [<descriptive anchor>](<url>)
- Visual: <chart, diagram, screenshot, code or demo, with alt text idea>
- Transition: <how it leads into the next section>
#### H3: <sub-topic>
- Key points: ...

### H2: <next section>
...

### H2: <Closing section for this reader need: next step and CTA>

## Internal links
| Anchor text | URL | Section |
|---|---|---|

## Sources
- <primary source URL and the claim it supports>

## Repurposing plan (optional)
- Newsletter hook: <the most surprising point>
- Video chapters: <one per H2>

## Open questions
- <claims to verify, data still needed>
````

## Skeletons by reader need

Start from the skeleton, then adapt it to the topic and what currently ranks. **X stands for the primary keyword.** Keep it (or a natural variation) in the first H2 and in 1 to 2 other H2s, as the SEO checklist requires, even when the reader need dictates a fixed opening such as Prerequisites or causes.

### Educate Me ("What is X?")
```
Intro plan: set up the problem before naming X; introduce X as the answer; hint at why and for whom.
### H2: What Is X and How Does It Work?        (core answer plus one concrete example)
### H2: Why Does X Exist? / Where Does X Fit?
### H2: Who Uses X, and for What?               (use cases)
### H2: What Are the Limits of X?
### H2: Where To Go Next With X                 (point to an Explain It or Guide Me piece)
```

### Explain It ("How does X actually work?")
```
Intro plan: where X is used and why its internals matter now. Skip the 101.
### H2: How Does X Work Under the Hood?         (the central mechanism, shown with a diagram, code or numbers)
### H2: <Component 1>                           (each opens with one line on where it fits)
### H2: <Component 2>
### H2: What This Explains About X in Practice
### H2: Going Deeper                            (resources, next piece)
```

### Compare For Me ("Which should I pick?")
```
Intro plan: the decision and why it's not obvious. No verdict yet.
### H2: How Do X and Y Differ?                  (the one distinction that matters most)
### H2: X vs Y at a Glance                      (comparison table, introduced and interpreted)
### H2: What Factors Should Decide?             (cost, performance, effort, risk, scale)
### H2: When Should You Choose X or Y?          ("choose X if..., choose Y if...")
```

### Guide Me ("How do I do X?")
```
Intro plan: what the reader will have at the end, and roughly how long it takes.
### H2: Prerequisites for X                    (e.g. "Prerequisites for Deploying a ReAct Agent")
### H2: Step 1: <Instruction>                   (numbered sub-steps, expected output)
### H2: Step 2: <Instruction>
### H2: Step 3: <Instruction>
### H2: How To Verify X Works / Next Steps
```

### Fix It ("Why isn't X working?")
```
Intro plan: name the problem calmly.
### H2: Why Does X Happen?                     (likely causes; X is the problem phrase, e.g. "SSH Connection Refused")
### H2: Fix 1: <Most likely or easiest>         (numbered steps, expected result)
### H2: Fix 2: <...>
### H2: Fix 3: <...>
### H2: What To Do if X Still Happens          (where to get help, what to bring)
```

### Give Me Perspective ("What did you find?")
```
Intro plan: the surprising result or tension, stated concretely.
### H2: <The Headline Finding About X>         (evidence: chart, table, numbers)
### H2: How I Tested X                        (method in brief: enough to trust and reproduce)
### H2: <Supporting Finding 2>
### H2: <Supporting Finding 3>
### H2: What I Got Wrong / Limits               (honest caveats)
### H2: What This Means for You                 (takeaways, how to reproduce)
```

### Update Me ("What changed?")
```
Intro plan: one or two lines: what happened, when, and who it affects.
### H2: What Changed in X?                      (with versions and dates)
### H2: What X Means for <Reader>             (practical impact and action)
### H2: What To Do Next                         (steps, links to primary sources and evergreen pieces)
```

### Inspire Me ("Show me it's possible")
```
Intro plan: open in the middle of the story, at the moment of tension.
### H2: Where My X Journey Started             (context, the obstacle)
### H2: What I Tried (and What Failed)
### H2: The Turning Point
### H2: The Results                             (concrete numbers or outcomes)
### H2: Lessons From X You Can Apply           (transferable lesson and a first step)
```
