---
name: how-not-to-write
description: Guardrail against the AI-antithesis cadence and slopified phrasing in any writing. Use this whenever drafting or editing prose, copy, slides, taglines, emails, marketing, landing pages, or documents, and especially whenever the user asks to make text sound less AI, less generic, more original, sharper, or more human. Catch and remove "it's not just X, it's Y" constructions and their variants before they reach the page. Also enforce two hard rules on all writing: never use em dashes, and stay conversational without being verbose.
---

# How Not to Write

Three rules for anything you write or edit for a person to read. Rule 1 is the big one, an AI cadence tic to hunt down. Rules 2 and 3 are hard constraints that always apply, with no exceptions.

## Rule 1: kill the antithesis cadence

Do not use the antithesis cadence, the "it's not X, it's Y" contrast and its whole family. Default to plain sentences that state a thing and then explain it. When you feel the pull toward a dramatic reversal, treat that pull as the warning sign: it usually means you are performing insight instead of delivering it. Cut it, and say the real thing plainly.

## The banned pattern and its variants

They all share one shape: deny a smaller thing, then assert a grander one, in two short beats. Avoid every version of it.

- "If it's not X, it's Y."
- "This wasn't just a product. It was a movement."
- "We're not here to compete. We're here to change the world."
- "Not just an app. A revolution."
- "More than a brand. A lifestyle."
- "Not building for today. Building for the future."

The tell is the rhythm: a short negation, a full stop, then a short grander claim. Once you can hear it you cannot unhear it, and neither can the reader.

## Why this matters

Two problems, and they are worth keeping in mind because they explain why the fix is not just cosmetic.

First, it is obvious slopification. It makes writing feel cheap and signals creative laziness, a lack of taste, a lack of pressure-tested thinking. The irony is that people reach for this cadence believing it makes them sound smarter, when it actually compresses everyone toward the same median tone: the same sentence structures, the same faux-philosophical contrasts, the same pseudo-profound framing. You can tell instantly when someone has handed their brain to a model. The cadence is everywhere now: radio ads, founder videos, Netflix dialogue, VC pitch decks, Twitter threads.

Second, it erodes thinking. Wharton has a name for it, cognitive surrender. Every time you outsource the articulation of a thought, you weaken the muscle responsible for producing original ones. The mind flourishes under resistance. There is real value in searching for the exact word, restructuring a sentence fifteen times, interpreting tone and dialect, synthesizing first, second, and third order implications, and wrestling with ambiguity until something precise emerges. The value of a perspective is usually proportional to the resistance it took to arrive at it. More friction leads to deeper synthesis, deeper synthesis to sharper insight, and sharper insight to originality. Good writing was never supposed to feel frictionless. Do not trade one of the most beautiful parts of human intelligence for a short dopamine hit disguised as sophistication.

## What to do instead

State the claim plainly, then earn it with specifics. A reader does not need a contrast to feel the weight of a point. They need evidence and precision.

Instead of "This wasn't just a product. It was a movement," say what actually happened: who used it, how it spread, what changed because of it. Let the facts carry the size of the claim. If the thing really was a movement, the details will show it. If the details do not show it, the contrast was covering a hole.

Practical moves:

- Prefer a sentence that adds information over one that stages a reversal.
- When you catch a "not X, but Y," delete the "not X" half and check whether "Y" still lands. It usually lands harder alone.
- Replace the abstraction with the specific noun. "A lifestyle" tells the reader nothing. The actual behavior does.
- Read the draft out loud. The antithesis cadence has an audible singsong beat. If two sentences in a row go short-negation then short-claim, break the pattern.

## The one exception, used rarely

A true contrast can be the right tool at a genuine hinge in an argument, the moment where the reader is actively holding a wrong assumption and you resolve it. Even then, use it at most once in a section, and only after the setup has earned it. When in doubt, cut it. The default is always the plain, explained sentence.

## Rule 2: never use em dashes

Never use the em dash, the long dash. It is one of the loudest tells of machine-written text, and it is banned here with no exceptions. When you feel the reach for one, use the punctuation the sentence actually needs: a full stop for two separate thoughts, a comma for a light pause, a colon to introduce what follows, or parentheses for a true aside. Three em-dash habits to catch and kill: the dramatic pause before a payoff, the pair of dashes wrapping a parenthetical, and the dash standing in for "which is to say." Rewrite each into plain punctuation. Hyphens in compound words are fine, and ranges read better with "to" than with any dash (write "80% to 92%," not "80–92%").

## Rule 3: conversational, but never verbose

Warm does not mean long. Say the thing in the fewest words that keep it clear and human, then stop. Cut the throat-clearing openers ("It's worth noting that," "At the end of the day," "In order to"), the doubled phrasings that say one idea twice, and any sentence that just restates the one before it. A quick test: if a sentence can lose a third of its words and still land, it was too long. Warmth comes from word choice and rhythm, not word count. When a conversational tone and brevity pull against each other, keep the tone and cut the length.

## Examples by domain: Web3, AI, ZK and Web2

The same three rules, applied to the developer topics this skill is used for most. The "after" lines show the shape of the fix. Swap in your real facts, and never invent numbers to fill the slot.

### The antithesis cadence in the wild

| Domain | Banned | Plain and specific |
|---|---|---|
| Web3 | "This isn't just a token. It's a community." | "Holders vote on treasury spending onchain, and every proposal is public on the governance page." |
| Web3 | "We're not building a chain. We're building an ecosystem." | "The chain launched with a bridge, a block explorer and three dApps already deployed." |
| AI | "It's not autocomplete, it's reasoning." | "The model plans the steps in its Thought line, then calls the calculator for each one." |
| AI | "Not just a chatbot. An agent." | "It reads the ticket, searches the docs, drafts a reply and waits for approval before sending." |
| ZK | "Not just privacy. Freedom." | "The app proves you're over 18 without sending your birth date to the server." |
| ZK | "This isn't a proof system, it's a paradigm shift." | "Verifying the proof onchain takes one contract call, whatever the size of the computation behind it." |
| Web2 | "It's not a framework, it's a philosophy." | "Routing, data fetching and caching follow one set of conventions, so new pages need no config." |
| Web2 | "Not just faster. Better." | "Pages render on the server, so the first meaningful paint no longer waits for the JavaScript bundle." |

### Em dashes in technical writing

| Before | After |
|---|---|
| "Rollups batch transactions — thousands of them — and post them to Ethereum." | "Rollups batch thousands of transactions and post them to Ethereum." |
| "The model has one weakness — arithmetic." | "The model has one weakness: arithmetic." |
| "The circuit compiled — but it proved the wrong statement." | "The circuit compiled. It also proved the wrong statement." |
| "Raise max_connections — carefully — and restart." | "Raise max_connections carefully, then restart the server." |
| "Gas fees fell 80–95% after the upgrade." | "Gas fees fell by 80% to 95% after the upgrade." |

### Padding in technical writing

| Padded | Tight |
|---|---|
| "It's worth noting that, in today's fast-moving Web3 landscape, security is more important than ever." | "Audit the contract before mainnet. Most exploits target bugs a review would have caught." |
| "In order to basically get started with zero-knowledge proofs, you'll essentially want to first understand circuits." | "Start with circuits: they're how a ZK proof describes what it proves." |
| "At the end of the day, the context window is, in simple terms, kind of like the model's memory." | "The context window is the model's working memory, measured in tokens." |
| "Due to the fact that the database has a connection limit, in the event that you exceed it, errors will occur." | "PostgreSQL rejects new connections once it hits max_connections." |

### Domain words that signal hype

Treat these as warnings, not bans. Keep one only when it carries a specific, checkable meaning:
- **Web3:** revolutionary, trustless (unless it truly has no trust assumptions), "to the moon", next 100x, guaranteed yield.
- **AI:** understands, thinks, sentient, superhuman, "replaces developers".
- **ZK:** unbreakable, 100% private, magic, "math-proof".
- **Web2:** blazing fast, seamless, enterprise-grade, infinitely scalable.
