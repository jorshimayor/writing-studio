# X Thread Template

**1/ Hook** (self-contained, specific, no "A thread 🧵"):
<The most surprising finding or the problem, with a number if you have one.>

**2/** <One idea, readable on its own. Attach a chart, code image or screenshot.>

**3/** <One idea.>

**4/** <One idea.>

**5/** <One idea or the honest caveat.>

**6/ Takeaway + link:**
<What the reader should do with this.> <one link: article, video or repo>

Checklist:
- [ ] No antithesis cadence, no em dashes, no padding
- [ ] No price calls, "alpha" or engagement bait
- [ ] Every number traceable to the source piece
- [ ] Projects tagged only with accurate claims

---

## Filled example (AI, from the few-shot experiments)

**1/** I ran 140 few-shot prompting experiments on a small open model. The prompt template moved accuracy by up to 41 points. Whether the example labels were correct moved it by about 1.

**2/** Same task, same 150 test reviews, one change at a time: number of examples, order, template, label words, label correctness, label balance.

**3/** One example was worse than none: 74% average against 87% with zero examples. Two or more balanced examples fixed it.

**4/** A template ending in "positive or negative?" answered "negative" 97% of the time. The last word mentioned pulled every answer.

**5/** Caveat: one 0.5B model, one easy task. Order effects were smaller than published results on bigger models.

**6/** Test 3 to 5 templates before tuning examples. Full write-up, charts and code: <link>
