---
name: writing-studio
description: End-to-end content system for writing and publishing across a blog, Substack, email newsletters and YouTube. Use it whenever the user wants to plan, title, outline, write, edit, SEO-optimize, or repurpose an article, blog post, Substack post, newsletter issue, YouTube script or video description, or asks for catchy or trending titles, keyword placement, internal linking, or a content brief. It decides what the reader needs from the piece, researches search intent, writes ranking-friendly titles, drafts in a human voice, runs an automated SEO and style audit, and adapts one piece into every channel.
---

# Writing Studio

Turn a topic into a finished piece for any channel: a search-optimized article, a Substack post, a newsletter issue or a YouTube video. Every piece is shaped by **what the reader needs from it**, written in a plain human voice, and checked before it ships.

## Reference files

| File | Contains | Read at |
|---|---|---|
| `profiles/<name>.md` | Brand, audience, channels, links, calls to action, spelling and capitalization | Step 0 |
| `references/reader-needs.md` | The 8 reader needs, how to pick one, and how each shapes the piece | Step 1, Step 4 |
| `references/titles.md` | Titles, subject lines and YouTube titles that rank and get clicked; finding trending angles | Step 3 |
| `references/structure.md` | Intros, ordering, headings, transitions, lists, tables, length | Step 4, Step 5 |
| `references/voice.md` | Voice and style rules, including the hard bans | Step 5, Step 6 |
| `references/seo.md` | On-page SEO checklist, linking and metadata | Step 2, Step 4, Step 6 |
| `references/channels.md` | Format rules for blog, Substack, newsletter and YouTube, plus repurposing | Step 0, Step 5, Step 7 |
| `scripts/seo_check.py` | Automated SEO and voice audit for Markdown drafts | Step 6 |

## Workflow

### Step 0: Load the profile and the brief

1. **Profile.** Use the profile the user names. Otherwise use the default profile (`profiles/jorshimayor.md`), or the only one that exists. If its required fields are empty, ask for them once, and in Claude Code offer to save the answers into the profile file. To create a new profile, copy `profiles/_template.md`.
2. **Channel.** Blog article, Substack post, newsletter issue, YouTube video, or "all of them" (see Step 7). Read the channel's section in `references/channels.md`.
3. **Brief.** Ask only for what's missing, in one message:
   - Topic, and for search channels the **primary keyword** plus 2 to 5 **secondary keywords**.
   - The **reader**: who they are and their level.
   - Source material: notes, data, results, code, a transcript or an earlier piece to adapt.
   - The **call to action (CTA)**: subscribe, watch, read the deep dive, try a product. Default to the profile's.

If the user only gives a topic, propose the keywords and reader need yourself, say why, and continue.

### Step 1: Choose the reader need

Read `references/reader-needs.md` and pick the need that matches the reader's question:

| Reader's question | Need |
|---|---|
| "What is X?" | Educate Me |
| "How does X actually work?" / "Why does X behave like this?" | Explain It |
| "Which option should I pick?" | Compare For Me |
| "How do I do X?" | Guide Me |
| "Why isn't X working?" | Fix It |
| "What do you think about X? What did you find?" | Give Me Perspective |
| "What changed and does it affect me?" | Update Me |
| "Show me it's possible / tell me the story" | Inspire Me |

State the need, the reader desires it must satisfy, and the reader's level. The need sets the intro, the order of sections and how the piece closes.

### Step 2: Research

Use web search when available. Never invent data, statistics, search volumes or quotes. If you can't verify something, say so or ask the user.

1. **Intent:** search the primary keyword and read what ranks. Match the format that wins (explainer, comparison, tutorial, opinion).
2. **Questions:** collect "People also ask", forum and community questions. The best become headings.
3. **Gap:** find what the top results miss. That's the angle.
4. **Sources:** gather facts from primary sources (official docs, papers, standards, original data). Choose 1 to 3 as external links.
5. **Internal links:** search `"<keyword>" site:<profile domain>` or use the profile's link list. Aim for 3 to 5 per 1,000 words. Follow the anchor rules in `references/seo.md`.

### Step 3: Titles and hooks

Read `references/titles.md`. For the chosen channel produce 8 to 10 options across different hook patterns, recommend one, and give the channel's metadata:
- **Blog / Substack:** SEO title (50 to 60 characters), meta description (140 to 160), slug; Substack also gets a subtitle.
- **Newsletter:** subject line (under 50 characters) and preview text (40 to 90).
- **YouTube:** title (under 70 characters, ideally under 60), 3 thumbnail text options (2 to 4 words each).

### Step 4: Outline

Build the outline from the reader need (`references/reader-needs.md`), the structure rules (`references/structure.md`) and the channel format (`references/channels.md`):
- An **intro plan** that sets up the problem and stakes without giving the answer away, and never says "In this article, we will".
- The **core answer first**: the first H2 (or the first beat of a video) delivers what the title promised, using a keyword variation.
- Headings phrased as the reader's questions where natural.
- A **keyword map**, **link map**, **image or visual plan** (with alt text), and **CTA placement**.

Show the titles and outline to the user and wait for approval before drafting, unless they asked for a one-shot draft.

### Step 5: Draft

Write the piece following the reader need, the structure rules, the channel format, `references/voice.md` and the profile's style settings. For search channels, place keywords as `references/seo.md` describes: in the first 50 words, the first H2 and its first paragraph, spread through the body, and in the closing section, at a density of about 1% to 2% (primary) and 0.5% to 1% (secondary). Readability always wins over keyword count.

### Step 6: Audit and fix

For any Markdown draft (blog, Substack, newsletter), save it and run:

```bash
python3 scripts/seo_check.py draft.md --keyword "<primary>" --secondary "<s1>, <s2>" \
  --site <profile domain> --meta "<meta description>" [--strict] [--check-links]
```

Use `--strict` when the profile sets `strict_style: true`. `--check-links` needs network access. Fix every ✘. Fix each ⚠ unless there's a clear reason not to, and report the ones you kept. Re-run until nothing fails.

Then run the manual checks:
- The reader need's desires: does the piece satisfy at least two?
- `references/voice.md` final checklist.
- Read it aloud. Does it sound like an expert explaining something clearly, or like someone performing expertise?

For YouTube, use the checklist in `references/channels.md` instead of the script.

### Step 7: Deliver (and repurpose)

Return:
1. Title options with the recommendation and the channel metadata.
2. The finished piece.
3. Link table (anchor, URL, internal or external), image or visual list with alt text.
4. Audit summary and any warnings kept, with reasons.
5. Open questions and claims that need the author's verification.

If the user wants the piece on more channels, follow **Repurposing** in `references/channels.md`. The long-form article is the source of truth, and the newsletter and video are overviews that link back to it.

## Hard rules (always apply)

1. **No antithesis cadence.** Never write "it's not X, it's Y", "not just X, but Y", "this wasn't a product. It was a movement." or any short-negation-then-grander-claim pattern. State the point plainly and back it with specifics.
2. **No em dashes, ever.** Use a full stop, comma, colon or parentheses. Write ranges with "to" ("3 to 5").
3. **Conversational, never verbose.** Cut throat-clearing, doubled phrasing and sentences that repeat the last one.
4. **No invented facts.** No made-up statistics, quotes, search volumes, benchmarks or sources. Mark anything unverified.
5. **Deliver the title's promise early.** Never bury the answer.
