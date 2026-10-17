---
name: writing-studio
description: End-to-end content system for writing and publishing across a blog, Substack, email newsletters and YouTube, tuned for Web3, AI, zero-knowledge (ZK) and Web2 developer topics. Use it whenever the user wants to plan, title, outline, write, edit, SEO-optimize, or repurpose an article, blog post, Substack post, newsletter issue, YouTube script or video description, or asks for catchy or trending titles, keyword placement, internal linking, or a content brief. It works in three modes: topic(s) to reader-need outlines, outline to finished piece, or topic straight to a finished piece. It decides what the reader needs, researches keywords and search intent, writes ranking-friendly titles, builds a checked outline, drafts in a human voice, runs automated outline, SEO and style audits, and adapts one piece into every channel.
---

# Writing Studio

Turn a topic into a finished piece for any channel: a search-optimized article, a Substack post, a newsletter issue or a YouTube video. Every piece is shaped by **what the reader needs from it**, written in a plain human voice, and checked before it ships.

## Reference files

| File | Contains | Read at |
|---|---|---|
| `profiles/<name>.md` | Brand, audience, channels, links, calls to action, spelling and capitalization | Step 0 |
| `references/reader-needs.md` | The 8 reader needs, how to pick one, and how each shapes the piece | Step 1, Step 4 |
| `references/domains.md` | Web3, AI, ZK and Web2: sources, terminology, accuracy rules, example topics | Step 0, Step 2, Step 5 |
| `references/keyword-research.md` | Free autocomplete ideas, OpenSEO (open-source Ahrefs alternative) and Search Console; choosing keywords; reading competitor titles | Step 2 |
| `references/titles.md` | Titles, subject lines and YouTube titles that rank and get clicked; finding trending angles | Step 3 |
| `references/outline-template.md` | Outline file format and a skeleton for each reader need | Step 4 |
| `references/structure.md` | Intros, ordering, headings, transitions, lists, tables, length | Step 4, Step 5 |
| `references/voice.md` | Voice and style rules, including the hard bans | Step 5, Step 6 |
| `references/seo.md` | On-page SEO checklist, linking and metadata | Step 2, Step 4, Step 6 |
| `references/channels.md` | Format rules for blog, Substack, newsletter and YouTube, plus repurposing | Step 0, Step 5, Step 7 |
| `examples/outlines/` | 8 complete outlines, one per reader need, across Web3, AI, ZK and Web2 | Step 4 |
| `templates/` | Fill-in templates: article, Substack post, newsletter issue, YouTube package | Step 5, Step 7 |
| `scripts/keyword_ideas.py` | Free keyword and question ideas from Google and YouTube autocomplete | Step 2 |
| `scripts/outline_check.py` | Checks an outline against its reader-need rules, and a draft against its outline | Step 4, Step 6 |
| `scripts/seo_check.py` | Automated SEO and voice audit for Markdown drafts | Step 6 |

## Modes

Pick the mode from the request:

| Mode | Trigger | Steps |
|---|---|---|
| **A. Outline** | "Outline...", "plan these topics", a list of topics, "give me outlines" | 0 to 4, then stop and deliver the outline file(s) |
| **B. Piece from outline** | "Write it from this outline", an `.outline.md` file or a pasted outline | Load and check the outline, then 5 to 7 |
| **C. End to end** | "Write an article / post / script about..." | 0 to 7, pausing after Step 4 for approval unless asked for a one-shot draft |

**Batch outlines (Mode A with several topics).** Run Steps 0 to 4 for each topic. Save each as `outlines/<slug>.outline.md` (in the user's working folder when files can be written, otherwise return each outline in full). Then deliver an index:

| # | Topic | Reader need | Channel | Primary keyword | Recommended title | Outline file | Check result |
|---|---|---|---|---|---|---|---|

Flag topics that overlap or would compete for the same keyword, and suggest merging them or giving each a different reader need and keyword. Suggest an order that chains the needs (Educate Me, then Explain It, then Guide Me), so each piece links to the next.

**Piece from an outline (Mode B).**
1. Read the outline. Run `python3 scripts/outline_check.py <outline> --site "<profile domains>" --strict`. If anything fails, fix the outline first, tell the user what changed, and get approval if the change is substantive (a different reader need, keyword or section order).
2. Treat the outline as the contract: the same reader need, title, keywords, H2 order and links. Turn each `### H2:` and `#### H3:` into a real `##` / `###` heading, and cover every `Key points` bullet.
3. If writing shows a section should change, make the change, update the outline file to match, and say so in the delivery notes.
4. Continue with Steps 5 to 7. In Step 6, also run the alignment check (`--article`).

## Workflow

### Step 0: Load the profile and the brief

1. **Profile.** Use the profile the user names. Otherwise use the default profile (`profiles/jorshimayor.md`), or the only one that exists. If its required fields are empty, ask for them once, and in Claude Code offer to save the answers into the profile file. To create a new profile, copy `profiles/_template.md`.
2. **Channel.** Blog article, Substack post, newsletter issue, YouTube video, or "all of them" (see Step 7). Read the channel's section in `references/channels.md`.
3. **Domain.** Classify the topic as Web3, AI, ZK, Web2 or a bridge between two of them, and read its section in `references/domains.md`. Its accuracy rules apply to every later step.
4. **Brief.** Ask only for what's missing, in one message:
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

1. **Keywords:** follow `references/keyword-research.md`. Run `scripts/keyword_ideas.py` on 1 to 3 seed phrases. If OpenSEO's MCP tools are connected, add volume, difficulty and SERP data. Pick 1 primary keyword, 2 to 5 secondary keywords and 3 to 8 questions, and say which data source backed the choice.
2. **Intent:** search the primary keyword and read what ranks. Match the format that wins (explainer, comparison, tutorial, opinion).
3. **Questions:** collect "People also ask", forum and community questions. The best become headings.
4. **Gap:** find what the top results miss. That's the angle.
5. **Sources:** gather facts from primary sources (official docs, papers, standards, original data). Choose 1 to 3 as external links.
6. **Internal links:** search `"<keyword>" site:<profile domain>` or use the profile's link list. Aim for 3 to 5 per 1,000 words. Follow the anchor rules in `references/seo.md`.

### Step 3: Titles and hooks

Read `references/titles.md`. For the chosen channel produce 8 to 10 options across different hook patterns, recommend one, and give the channel's metadata:
- **Blog / Substack:** SEO title (50 to 60 characters), meta description (140 to 160), slug; Substack also gets a subtitle.
- **Newsletter:** subject line (under 50 characters) and preview text (40 to 90).
- **YouTube:** title (under 70 characters, ideally under 60), 3 thumbnail text options (2 to 4 words each).

### Step 4: Outline

Write the outline in the file format from `references/outline-template.md`, starting from the skeleton for the chosen reader need. Use the matching example in `examples/outlines/` as the quality bar (same need, ideally the same domain). Then adapt it with the reader need (`references/reader-needs.md`), the structure rules (`references/structure.md`) and the channel format (`references/channels.md`):
- An **intro plan** that sets up the problem and stakes without giving the answer away, and never says "In this article, we will".
- The **core answer first**: the first H2 (or the first beat of a video) delivers what the title promised, using a keyword variation.
- Headings phrased as the reader's questions where natural.
- A **keyword map**, **link map**, **image or visual plan** (with alt text), and **CTA placement**.

Run the outline check and fix every ✘:

```bash
python3 scripts/outline_check.py outlines/<slug>.outline.md --site "<profile domains>" [--strict]
```

It verifies the brief, the title and meta, at least 2 reader desires, the intro plan, the keyword placement in planned headings, the planned links, and the reader need's own rules (e.g. Guide Me starts with prerequisites, Fix It starts with causes and ends with where to get help, Compare For Me plans a table and ends with when to choose each, Give Me Perspective includes the method and the limits).

In Mode A, stop here and deliver. In Mode C, show the titles and outline and wait for approval before drafting, unless the user asked for a one-shot draft.

### Step 5: Draft

Start from the channel's template in `templates/`. Write the piece following the reader need, the structure rules, the channel format, `references/voice.md` and the profile's style settings. For search channels, place keywords as `references/seo.md` describes: in the first 50 words, the first H2 and its first paragraph, spread through the body, and in the closing section, at a density of about 1% to 2% (primary) and 0.5% to 1% (secondary). Readability always wins over keyword count.

### Step 6: Audit and fix

For any Markdown draft (blog, Substack, newsletter), save it and run:

```bash
python3 scripts/seo_check.py draft.md --keyword "<primary>" --secondary "<s1>, <s2>" \
  --site "<profile domains>" --meta "<meta description>" --spelling <profile spelling> [--strict] [--check-links]
```

Use `--strict` when the profile sets `strict_style: true`, and `--spelling` from the profile (british or american). `--check-links` needs network access. Fix every ✘. Fix each ⚠ unless there's a clear reason not to, and report the ones you kept. Re-run until nothing fails.

Then run the manual checks:
- The reader need's desires: does the piece satisfy at least two?
- `references/voice.md` final checklist.
- Read it aloud. Does it sound like an expert explaining something clearly, or like someone performing expertise?

If the piece was written from an outline, confirm it followed the plan:

```bash
python3 scripts/outline_check.py outlines/<slug>.outline.md --site "<profile domains>" --article draft.md
```

It reports planned sections missing from the draft, sections out of order, and sections that aren't in the outline.

For YouTube, use the checklist in `references/channels.md` instead of the scripts.

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
