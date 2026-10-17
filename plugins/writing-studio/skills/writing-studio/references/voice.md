# Voice and Style

The target sound: an expert friend explaining something clearly over coffee. Relaxed, precise and specific. The profile can tighten these defaults (spelling, capitalization, person).

## Hard bans

### 1. The antithesis cadence

Never use "it's not X, it's Y" or its relatives:
- "This isn't just a tool, it's a new way of working."
- "Not just an app. A revolution."
- "More than a newsletter. A community."
- "We're not here to compete. We're here to win."

They share one shape: a short denial of a smaller thing, then a grander claim, in two quick beats. Readers now recognize it instantly as machine-written or ad copy, and it signals that the writer performed insight instead of providing it.

**Fix:** delete the "not X" half and check whether "Y" still lands. Then replace the abstraction with evidence. "It was a movement" becomes who joined, how fast, and what changed.

The one exception: a real contrast at a genuine turning point in an argument, where the reader actually holds the wrong belief. At most once per section, and only after the setup has earned it.

### 2. Em dashes

Never use the em dash. Use the punctuation the sentence actually needs:
- A full stop for two separate thoughts.
- A comma for a light pause.
- A colon to introduce what follows.
- Parentheses for a true aside.

Write ranges with "to": "3 to 5 links", "80% to 92%".

### 3. Padding

Cut throat-clearing, doubled phrasing and sentences that restate the one before. If a sentence can lose a third of its words and still land, cut them. Warmth comes from word choice and rhythm, not length.

## Phrases to delete on sight

| Delete | Use instead |
|---|---|
| It's important to note that / It's worth noting that | (just say it) |
| In today's fast-paced / ever-evolving world | (say what actually changed) |
| Basically, essentially, in simple terms | (just say it) |
| In order to | to |
| Due to the fact that | because |
| Prior to / subsequent to | before / after |
| In the event that | if |
| Let's dive in / delve into | (start the section) |
| Unlock / harness the power of | use |
| Game-changing, revolutionary, cutting-edge, seamless, robust, world-class, best-in-class, next-generation | (describe the specific capability) |

## Defaults

- **Plain words over impressive ones**, but keep the precise technical term when it's the accurate one, and explain it on first use with a short clause.
- **Active voice.** "The model predicts the next token", not "the next token is predicted by the model". Passive is fine when the actor doesn't matter.
- **Acronyms:** write the full term first, acronym in parentheses: "retrieval-augmented generation (RAG)". Then use the acronym.
- **Contractions** in most content. They read naturally. Formal step-by-step docs may avoid them.
- **"You"** when talking about the reader's choices and actions. "I" is welcome for personal research, opinions and stories (Give Me Perspective, Inspire Me) and should be avoided in neutral explainers. Never present opinion as established fact.
- **Specific over general.** Numbers, names, versions, dates and examples beat adjectives.
- **Calibrated claims.** Avoid absolutes (always, never, guaranteed, impossible) unless they're literally true. Use "can", "may" and "usually" where the truth is conditional. No unsupported superlatives (fastest, best, cheapest).
- **Rhetorical questions** sparingly, only when they voice a question the reader really has.
- **Bold** sparingly. Clear sentences carry their own emphasis.
- **Numbers and units:** numerals for measurements with a space before the unit (16 GB, 10 ms). Keep formatting consistent through the piece.
- **Consistency:** once you choose a spelling, term, capitalization or format, keep it everywhere.

## Domain terminology

Each domain has its own spelling and capitalisation conventions (Web3, smart contract, ERC-20, zk-SNARK, zkVM, LLM, fine-tuning, Next.js, PostgreSQL). Use the forms in `domains.md`, and keep one form per piece. The checker warns when a piece mixes variants such as "on-chain" and "onchain", "Web3" and "web3", or "dataset" and "data set".

Write mixed-case technical names exactly as their owners do, even in title case: zk-SNARK, zkVM, dApp, iOS. The checker treats these as proper names.

## Final checklist

- [ ] No antithesis cadence, no em dashes, no padding phrases.
- [ ] Every claim is specific and either sourced or marked as opinion.
- [ ] Technical terms explained on first use, acronyms expanded.
- [ ] Active voice by default, sentence lengths varied.
- [ ] Consistent spelling, capitalization, terms and number formats.
- [ ] Reads naturally aloud, in one pass.
- [ ] The final test: does it sound like an expert explaining clearly, or someone trying to prove they're an expert?
