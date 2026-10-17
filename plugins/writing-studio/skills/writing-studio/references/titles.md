# Titles, Subject Lines and Hooks

A title makes one promise and has to win against everything else on the screen. The best ones are specific, honest and impossible to misread. Catchy comes from **specificity and tension**, not hype.

## Principles

1. **Lead with the words people search or care about.** Put the keyword or the subject in the first half.
2. **Be concrete.** Numbers, names, versions, results and timeframes beat adjectives. "I Ran 140 Prompt Experiments" beats "Insights on Prompting".
3. **Create a gap the piece closes.** Hint at a surprising result, a mistake or a question without giving the answer away.
4. **Match the reader need.** The title should echo the question the reader is asking (see the table below).
5. **Keep the promise.** If it says "7 fixes", deliver 7 fixes, and put the core answer first. Clickbait that under-delivers kills watch time, read time and trust.
6. **No hype words, no em dashes, no antithesis hooks** ("Not X. Y."). Use a colon to join a subject to its payoff.
7. **Follow the profile's capitalization** (title case or sentence case) consistently.

## Patterns by reader need

| Need | Pattern | Web3 | AI | ZK | Web2 |
|---|---|---|---|---|---|
| Educate Me | "What Is X? A ... Guide" | What Is Account Abstraction (ERC-4337)? | What Is RAG? A Developer's Guide | What Is A Zero-Knowledge Proof? A Developer's Guide | What Is Connection Pooling? |
| Explain It | "How X Actually Works" | How Blobs Lower Rollup Fees | How Does A Context Window Work In LLMs? | How A zk-SNARK Proves Without Revealing | How Next.js Caching Actually Works |
| Compare For Me | "X Vs Y: Which Should You ...?" | Optimistic Vs ZK Rollups: Which Should You Build On? | Fine-Tuning Vs RAG: Which Fits Your App? | zk-SNARK Vs zk-STARK: Trade-Offs For Developers | REST Vs GraphQL: Which Fits Your API? |
| Guide Me | "How To X In N Steps / Minutes" | How To Deploy An ERC-20 Token With Foundry | How To Build A ReAct Agent In 100 Lines | How To Write Your First Noir Circuit | How To Add Rate Limiting To A Node.js API |
| Fix It | "X Not Working? N Fixes" | Transaction Stuck Pending? 5 Nonce Fixes | LLM Ignoring Instructions? 6 Prompt Fixes | Circom Constraint Errors: 5 Causes And Fixes | PostgreSQL Too Many Connections? 5 Fixes That Work |
| Give Me Perspective | "I Ran / Tested X: Here's What ..." | 30 Days Running A Solana Validator: The Numbers | I Ran 140 Few-Shot Experiments: Here's What Matters | I Benchmarked 3 zkVMs On The Same Program | I Moved From Serverless To A VPS: The Costs |
| Update Me | "X Is Out: What Changes For Y" | What The Latest Ethereum Upgrade Means For Developers | What MCP Means For Agent Builders | What The New zkVM Releases Mean For Rollups | Next.js 15 Caching Changes: What Breaks And How To Fix It |
| Inspire Me | "From X To Y: What Worked" | How A Reentrancy Bug Made Me A Safer Solidity Dev | From Solidity To AI Engineering In Three Weeks | Learning Zero-Knowledge Proofs: From Solidity To A ZK App | How A Weekend Script Became My Most-Used Tool |

More example titles and topics per domain are in `domains.md`.

## Hook toolkit

Mix these to generate options:
- **Number:** "5 Fixes", "140 Experiments", "In 100 Lines", "30 Days Running A Validator".
- **Result or surprise:** "...Was Worse Than A Coin Flip", "...Proved The Wrong Thing Perfectly".
- **Question the reader is asking:** "Do You Need A ZK Rollup?", "Is Fine-Tuning Worth It?"
- **Comparison:** "Optimistic Vs ZK Rollups", "REST Vs GraphQL".
- **Mistake or warning:** "The Private Key Mistake In Most Foundry Tutorials".
- **Audience callout:** "For Solidity Devs", "For Web2 Developers", "For Agent Builders".
- **Version or freshness:** "Next.js 15", "ERC-4337", "In 2026". Add the year only when freshness matters, and versions whenever the advice depends on them.
- **First-person proof:** "I Built", "I Tested", "I Benchmarked". Strong for creator channels.

**Domain cautions for titles:**
- Web3: never promise returns, prices or "the next 100x". Titles describe technology, not investment.
- AI: name the model size or setup when a result depends on it ("On A 0.5B Model").
- ZK: avoid "unbreakable", "100% private" or "trustless" unless the system genuinely has no trust assumptions.
- Web2: put the version in the title when the advice is version-specific.

## Channel limits

| Channel | Field | Limit | Notes |
|---|---|---|---|
| Blog | SEO title | 50 to 60 characters | Keyword in the first half |
| Blog | Meta description | 140 to 160 characters | Payoff plus a reason to click |
| Substack | Title | Under 60 characters | Also used as the email subject unless overridden |
| Substack | Subtitle | 1 sentence | Shown under the title and in previews. Adds the "why read" |
| Newsletter | Subject line | Under 50 characters | Front-load the hook. Most inboxes cut the rest on mobile |
| Newsletter | Preview text | 40 to 90 characters | Completes the subject line. Never repeat it |
| YouTube | Title | Under 70 characters, ideally under 60 | Keyword early. The title and thumbnail work as one unit |
| YouTube | Thumbnail text | 2 to 4 words | Complements the title instead of repeating it |

## Finding trending angles

"Trending" has to come from real signals. Never invent search volumes or trends. With web search available:
1. **Search the topic** and read the current top results and titles. Note which angles dominate, then find the one nobody covers (a newer version, a specific audience, an experiment, a cost angle).
2. **Read the questions:** "People also ask", Reddit, Hacker News, Stack Overflow, GitHub issues and YouTube comments. Use the reader's exact words.
3. **Check recency:** releases, announcements, papers and debates from the last few weeks make a timely angle.
4. **YouTube and search autocomplete:** type the topic and note the suggestions. They reflect real queries.
5. **Google Trends** (if the user shares data): rising and breakout related queries.

Without web access, ask the user for their keyword data, and label your angles as unverified.

## Delivering options

Give 8 to 10 options in a table:

| # | Title | Characters | Hook | Why it could win |
|---|---|---|---|---|

Recommend one, then give the channel metadata (SEO title, meta, slug, subtitle, subject line, preview text or thumbnail text).
