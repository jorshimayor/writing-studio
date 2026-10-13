# Reader Needs

People open a piece of content with a question already in mind. A piece performs when it is built around that question, the reader's need, instead of around everything the writer knows. The same topic can produce eight different pieces depending on which need it serves.

This framework adapts the "user needs" idea from newsroom audience research (first popularized by Dmitry Shishkin at BBC World Service, later extended by smartocto) for creators who publish explainers, tutorials, research and opinion across blogs, newsletters and video.

## Contents

- [Picking the need](#picking-the-need)
- Learn: [Educate Me](#educate-me), [Explain It](#explain-it)
- Decide: [Compare For Me](#compare-for-me), [Give Me Perspective](#give-me-perspective)
- Do: [Guide Me](#guide-me), [Fix It](#fix-it)
- Stay current: [Update Me](#update-me)
- Be moved: [Inspire Me](#inspire-me)

## Picking the need

| Search or reader signal | Need |
|---|---|
| "what is X", "X explained", "X for beginners" | Educate Me |
| "how does X work", "why does X", "X under the hood", "X deep dive" | Explain It |
| "X vs Y", "best X for", "which X", "X alternatives", "X pricing" | Compare For Me |
| "how to X", "X tutorial", "set up / build / deploy X", "X step by step" | Guide Me |
| "X not working", "X error", "fix X", "X troubleshooting" | Fix It |
| opinion, results, lessons, experiments, "what I learned", "is X worth it" | Give Me Perspective |
| releases, announcements, "X 2.0", "what's new in X", news | Update Me |
| case studies, build logs, journeys, "how I went from X to Y" | Inspire Me |

If two fit, choose the one that matches what currently ranks or what the audience asked for, name the runner-up, and borrow one section from it at most. A piece that tries to serve every need serves none.

Reader needs also chain together. Someone who has been *educated* on a topic wants it *explained*, then *guided*, then helped to *fix* it. End each piece by pointing to the next need in the chain.

---

## Learn

### Educate Me

**Question:** "What is X?" The reader is new to the topic.

**They want:** a solid foundation, terms explained, bite-size sections, and the confidence to talk about it.

**Shape it like this:**
- **Intro:** describe the situation or problem the subject belongs to before naming it, then introduce it as the answer and hint at why it matters and who uses it. Don't open with the definition, because a definition up front makes the rest look like padding.
- **First section:** the core answer. What it is, in plain terms, with one concrete example.
- **Then:** how it works → why it exists or where it fits → who uses it and how → its limits.
- Explain every term and acronym the first time it appears, then use it freely.
- Short paragraphs (3 to 4 sentences), many headings, headings phrased as questions.
- **Close:** point to an "Explain It" or "Guide Me" piece as the next step.

### Explain It

**Question:** "How does X actually work?" or "Why does X behave like this?" The reader knows the basics and wants depth.

**They want:** their knowledge respected, mechanisms instead of summaries, concrete examples, and links to go deeper.

**Shape it like this:**
- **Intro:** start where the subject is used and why the reader would care about its internals now. Skip the 101.
- **First section:** the central mechanism, shown with a diagram, code, a worked example or real numbers.
- Give each important component its own section. Open each with one line reminding the reader where it fits.
- Show the subject in context (with the tools it connects to), not in a vacuum.
- Use subordinate clauses as reminders of terms, not full re-explanations.
- **Close:** what this explains about real-world behavior, plus a deeper resource.

---

## Decide

### Compare For Me

**Question:** "Which option should I pick?"

**They want:** transparency, differences at a glance, and an answer that fits *their* situation.

**Shape it like this:**
- **Intro:** the decision the reader faces and why it's not obvious. Don't give the verdict yet. Make clear it depends on their needs.
- **First section:** the one distinction that matters most.
- A comparison table, introduced before it and interpreted after it.
- Then the factors (cost, performance, effort, risk, scale) and **when each option wins, for whom**.
- Be fair. Never call one option universally better when it depends on circumstances. State trade-offs plainly.
- **Close:** a short "choose X if..., choose Y if..." guide.

### Give Me Perspective

**Question:** "What do you think?" or "What did you find?" This is where original research, experiments, results and lessons live.

**They want:** a clear point of view, evidence for it, honesty about limits, and something they can apply.

**Shape it like this:**
- **Intro:** the surprising result or tension, stated concretely. Example: "Adding one example made my model *worse* than adding none."
- **First section:** the headline finding, with the evidence (chart, table, numbers).
- Then the method in brief (enough to trust and reproduce), the supporting findings, and **what didn't work or what you got wrong**.
- Separate what the data shows from what you believe. Mark opinions as opinions.
- **Close:** what the reader should do differently, plus how to reproduce the result.

---

## Do

### Guide Me

**Question:** "How do I do X?"

**They want:** clear steps, follow-up questions answered before they ask them, and confidence it worked.

**Shape it like this:**
- **Intro:** what they'll have at the end, and roughly how long it takes.
- **Prerequisites** first (accounts, versions, tools), then steps in order from first to advanced.
- One heading per major step, with minor steps numbered. Commands and file names in code formatting.
- After key steps, show the expected result (output, screenshot) so the reader can check they're on track.
- Anticipate likely errors inline.
- **Close:** how to verify it works, and the next thing to try.

### Fix It

**Question:** "Why isn't X working?" The reader is frustrated.

**They want:** the likely causes, several actionable fixes, and a fallback if none work.

**Shape it like this:**
- **First section:** the most common causes, quickly.
- One section per fix, from most likely or easiest to rarest or hardest, each with numbered steps and the expected result.
- Plain, calm language. Explain any term you must use.
- **Close:** where to get help if nothing worked, and what information to bring.

---

## Stay current

### Update Me

**Question:** "What changed, and does it affect me?"

**They want:** the news in the first lines, what it means for them, and what to do about it.

**Shape it like this:**
- **First lines:** what happened, when, and who it affects.
- Then why it matters, what changes in practice, and any action needed (with dates and versions).
- Link to the primary source (release notes, announcement).
- Keep it short. Update Me pieces date quickly, so link to evergreen pieces for background.

---

## Be moved

### Inspire Me

**Question:** "Show me it's possible," or "Tell me the story."

**They want:** a real person or project, the obstacle, the turning point, and a takeaway they can use.

**Shape it like this:**
- **Intro:** start in the middle of the story at the moment of tension.
- Then the context, the attempts (including failures), the turning point, and the result in concrete numbers or outcomes.
- Keep the details specific: dates, tools, numbers, what was hard.
- **Close:** the transferable lesson and one first step the reader can take.
