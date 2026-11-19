# Fact-checking

Everything this skill produces is for public readers, so every statement is checked before it ships. A statement either has a source, is reworded to what the evidence supports, is clearly the author's opinion, or comes out. "I'm fairly sure" isn't a source.

## Contents
- The rule
- The procedure
- What counts as a source
- What to check, claim by claim
- Domain checks (Web3, AI, ZK, Web2)
- When you can't verify something
- The ledger statuses
- The fact-check report

## The rule

No statement reaches the reader unverified. This covers the body, headings, tables, captions, alt text, titles, meta descriptions, thumbnails, video scripts, threads and newsletter blurbs. Repurposed pieces inherit the source article's checks only for sentences copied word for word. Anything reworded is checked again.

## The procedure

1. **Gather sources first.** In Step 2, collect primary sources for each fact you plan to use, and keep the URLs. It's much easier than hunting for a source after the sentence is written.
2. **Write the draft**, keeping a note of where each fact came from.
3. **Extract the ledger.** Save the draft and run:

   ```bash
   python3 scripts/claims.py extract draft.md > draft.claims.md
   ```

   Every sentence, table row and list item becomes a row. Rows marked `high` contain something checkable: a number, date, version, name, comparison, absolute ("always", "never"), attribution, quote, cause, or technical behaviour.
4. **Check every row.** Open each source and confirm the claim says exactly what the source says: the same number, unit, version, date, scope and certainty. Fill in `status`, `source` and `note` (statuses below).
5. **Fix the draft** where a check fails: correct it, soften it, or cut it. Then re-extract any changed sentences into the ledger.
6. **Run the gate:**

   ```bash
   python3 scripts/claims.py check draft.claims.md --draft draft.md
   ```

   It fails on any unchecked row, any verified row without a source, any high-priority row marked as framing, and any sentence added or edited since it was checked. Fix and re-run until it passes. Use `--allow-author` only when you hand the piece to the author with the `author` rows listed for them to confirm.
7. **Re-run the gate after every edit**, including edits made after the SEO and voice audits. A small rewording can change a claim.

## What counts as a source

Use the highest level available. Go lower only when nothing higher exists, and say so in the note.

1. **Primary:** the specification (EIP, RFC, ERC), the source code at a tagged release, official docs for the version you name, the paper itself, the audit report itself, the on-chain transaction or contract on a block explorer, official release notes and changelogs, the original dataset, and your own tests or computations (record the command).
2. **Secondary, reputable:** post-mortems by the affected team, well-known security firms' write-ups, peer-reviewed surveys, established technical publications.
3. **Last resort:** blog posts, forum threads, social posts. Only for what someone said (cite them for the quote), never as proof of a technical fact.

Never use as a source: AI-generated text (including your own earlier output), content farms, undated pages for time-sensitive facts, or a page that only repeats a claim without its own source. If a secondary source cites a primary one, open the primary one.

Record sources as:
- a URL, ideally a permalink (a tagged commit, a block explorer transaction, a versioned docs page, an archived copy)
- `test:<file or command>` for something you ran (a Foundry test, a notebook cell, a benchmark)
- `computed:<script or formula>` for arithmetic you redid
- `doc:<path>` for a file in the project (the author's own data, notes or repo)
- `author:<name>` for something only the author knows, once they've confirmed it

## What to check, claim by claim

- **Numbers and statistics:** match the source exactly, with the same unit, date range and population. Recompute any derived figure (percentages, ratios, totals, "3× faster"). Round the way the source does or say you've rounded.
- **Money and losses:** the amount, the currency or token, and the date of the valuation. Token losses quoted in dollars change with the price, so say "worth about $X at the time".
- **Dates and versions:** the exact version where a feature landed or changed, and the release date from the changelog. Say which version your instructions and code were tested on.
- **Names and attributions:** spelling and capitalisation of people, projects, companies and products. Who said, built, found or published what, and when.
- **Quotes:** word for word from the original, linked. If you shorten one, mark the cut with an ellipsis and keep the meaning. Never paraphrase inside quotation marks.
- **Comparisons and superlatives** ("fastest", "first", "only", "most popular"): need a source that makes the same comparison, on the same measure, recently. Otherwise reword ("one of the first", "faster in our test on X").
- **Absolutes** ("always", "never", "all", "impossible"): almost always too strong. Check for exceptions, then keep the absolute only if the source supports it.
- **Cause and effect** ("because", "leads to", "so"): the source must show that one causes the other. Two true facts side by side aren't enough.
- **Technical behaviour** (what a function returns, a default value, a revert, a gas cost, an API limit): confirm it in the code, the docs for that version, or by running it. Note the version.
- **Code and commands:** run every snippet and command, on the versions you state, and paste real output. Never hand-write output.
- **Figures, tables and captions:** every number in a chart or table traces to its data, and every caption's claim is true of the chart.
- **Links:** each link works and says what the sentence says it does (`seo_check.py --check-links` covers the first half).
- **Time-sensitive facts** (prices, TVL, fees, rankings, team members, "currently", "the latest"): give an "as of" date, or rephrase so it doesn't go stale.

## Domain checks

- **Web3:** contract addresses and transactions on the chain's official explorer, with the chain named. Chain IDs from the network's own docs. Exploit amounts from the team's post-mortem or the transactions themselves, not from social posts. Audit status from the audit report, with the firm, date and commit. EIP and ERC status (draft, final) from eips.ethereum.org on the day you publish. Gas figures from a run you can repeat.
- **AI:** benchmark scores from the paper or the official model card, with the benchmark version, number of shots and setting. Model names, sizes, context windows and licences from the official model card. Your own results with the run, seed and hardware recorded. Don't turn one run into a general claim.
- **ZK:** proof sizes, prover times and security levels from the paper or the library's benchmarks, with the hardware and parameters. Say which proving system and curve. Distinguish "zero-knowledge" from "succinct" when the source does.
- **Web2:** versions, defaults and limits from the official docs for the version you name. Browser and runtime support from the official compatibility tables. Performance numbers from a benchmark you ran, with the setup.

## When you can't verify something

In this order of preference:
1. **Find a primary source,** or run the code and record the result.
2. **Soften it** to what you can support: "can", "often", "in our test", "according to X". Record what changed in the note.
3. **Turn it into clearly marked opinion** if it's a judgement: "I think", "in my experience". Opinion is never dressed up as fact.
4. **Ask the author** if only they can know (their results, plans, experience). Mark it `author` and list it in the report.
5. **Cut it.** A piece with one fewer claim is better than a piece with one wrong claim.

Never leave a placeholder like "[citation needed]" or "studies show" in delivered text.

## The ledger statuses

| Status | Meaning | Needs |
|---|---|---|
| `verified` | The claim matches the source exactly | A source |
| `corrected` | The draft was changed to match the source | A source and a note saying what changed |
| `softened` | Reworded to the certainty the evidence supports | A note |
| `removed` | Cut because it couldn't be verified | Nothing |
| `opinion` | The author's view, written so it reads as one | Nothing |
| `framing` | A transition or setup with nothing to check (low priority rows only) | Nothing |
| `author` | Only the author can confirm | Their confirmation before publishing |
| `TODO` | Not checked yet | Blocks delivery |

## The fact-check report

Deliver it with the piece:
1. The gate's summary line (for example "42 statements: verified 25, framing 12, opinion 3, softened 2").
2. Every `corrected`, `softened` and `removed` row: what the draft said, what it says now, and why.
3. Every `author` row, as a checklist for the author to confirm before publishing.
4. Time-sensitive facts with their "as of" dates, so the author knows when to refresh the piece.
5. The ledger file itself (`draft.claims.md`), so the author or an editor can audit any claim.
