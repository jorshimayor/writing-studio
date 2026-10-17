# Web3 Document Types

How to write the documents a Web3 technical writer produces beyond articles. Each type lists its purpose, structure and rules. Templates live in `templates/`. The voice rules (`voice.md`) and Web3 safety rules (`SKILL.md` hard rules and `domains.md`) apply to all of them.

## Contents

- [Developer documentation](#developer-documentation)
- [README](#readme)
- [Protocol explainer](#protocol-explainer)
- [Whitepaper or litepaper](#whitepaper-or-litepaper)
- [Governance proposal](#governance-proposal)
- [EIP or ERC draft](#eip-or-erc-draft)
- [Audit summary](#audit-summary)
- [Incident post-mortem](#incident-post-mortem)
- [Release notes and changelog](#release-notes-and-changelog)
- [Grant proposal](#grant-proposal)
- [X thread](#x-thread)

## Quick map

| Document | Reader's question | Closest reader need | Template |
|---|---|---|---|
| Tutorial | "Teach me by building something" | Guide Me | `article.md` |
| How-to guide | "How do I do this specific task?" | Guide Me / Fix It | `article.md` |
| Reference | "What exactly does this function, parameter or contract do?" | (lookup) | `reference.md` |
| Explanation / protocol explainer | "How and why does this work?" | Explain It | `article.md` |
| README | "What is this repo, is it safe, how do I start?" | Educate Me + Guide Me | `readme.md` |
| Whitepaper | "What is this protocol, and does the design hold up?" | Explain It | `whitepaper.md` |
| Governance proposal | "What are we voting on, and why?" | Compare For Me + Update Me | `governance-proposal.md` |
| EIP / ERC draft | "What is the standard, precisely?" | (specification) | the official EIP template |
| Audit summary | "Is it safe, and what was found?" | Update Me | `audit-summary.md` |
| Post-mortem | "What happened, and will it happen again?" | Update Me | `post-mortem.md` |
| Release notes | "What changed, and what do I need to do?" | Update Me | `release-notes.md` |
| Grant proposal | "Why should we fund this?" | Give Me Perspective | `grant-proposal.md` |
| X thread | "Give me the gist fast" | any (overview) | `x-thread.md` |

---

## Developer documentation

Use the [Diátaxis](https://diataxis.fr/) split: four kinds of docs with four different jobs. Mixing them is the most common reason docs feel confusing.

| Kind | Job | Rules |
|---|---|---|
| **Tutorial** | Learning by doing: the reader builds something small that works | One happy path, every step shown, no choices offered. Start from zero. End with a working result |
| **How-to guide** | Getting one task done | Assumes basic knowledge. Title is the task ("How To Verify A Contract On Etherscan"). Steps only, no teaching detours |
| **Reference** | Looking up exact facts | Complete, consistent and dry: signatures, parameters, return values, errors, events, gas notes. Same layout for every entry. No opinions |
| **Explanation** | Understanding why | Design decisions, trade-offs, alternatives, history. No steps |

Web3 specifics:
- State **network(s), chain IDs, contract versions and compiler versions** at the top of every page.
- Publish **deployed addresses** in one table per network, linked to a block explorer, and generated from deployment artifacts where possible rather than typed by hand.
- Document **errors and reverts** (custom error names and what triggers them) in the reference.
- Every code sample runs as written against a named testnet, pins versions, and reads secrets from environment variables.
- Mark **upgradeable contracts** and who controls upgrades (multisig, timelock, governance).
- Use the same term for the same thing everywhere. In docs, consistency matters more than variety.

## README

The front door of a repo. Answer, in order: what it is, whether it's safe to use, how to start.

Structure (`templates/readme.md`):
1. **Name and one-line description**, saying what it does, for whom.
2. **Status**: development stage, networks deployed, audit status (with link), licence.
3. **Quickstart**: the shortest path to a working result.
4. **Install** and **usage** with copy-paste commands.
5. **Contracts and addresses**: a table per network with explorer links.
6. **Architecture** (short), linking to fuller docs.
7. **Security**: audits, bug bounty, and how to report a vulnerability privately (a security contact or `SECURITY.md`; see [security.txt / RFC 9116](https://www.rfc-editor.org/rfc/rfc9116) for the web convention).
8. **Contributing** and **licence**.

Rules: no marketing copy at the top, no unverified "audited" claims, and badges only when they're true and current.

## Protocol explainer

An Explain It article about one protocol or mechanism (a rollup design, an AMM curve, a bridge, a staking system). Follow the Explain It shape in `reader-needs.md`, and add:
- The **actors** (users, validators, sequencers, relayers, keepers) and what each one can and can't do.
- The **trust and security assumptions**, stated plainly: who can pause, upgrade or censor, and what has to stay honest for funds to be safe.
- **Failure modes**: what happens when a component goes down or acts maliciously.
- A **diagram** of the flow of funds or messages.
- Link the spec, audits and code. Use [L2BEAT](https://l2beat.com/)-style risk framing for L2s.

## Whitepaper or litepaper

A technical case for a protocol design. A litepaper is the short, readable version.

Structure (`templates/whitepaper.md`):
1. Abstract (5 to 8 sentences: the problem, the design, the key result).
2. Problem and motivation, with evidence.
3. Background and related work: what exists and where it falls short.
4. Design: components, the mechanism, the protocol flow, with diagrams.
5. Security model: assumptions, threat model, mitigations, known limitations.
6. Economics, if there's a token: what the token does mechanically, supply and distribution facts, incentives. **No price or return claims.**
7. Implementation status and roadmap (dated, with what's live vs planned).
8. References.

Rules: separate what exists from what's planned; quantify claims with methods ("tested on X with Y"); state limitations openly; no "revolutionary" or "trustless" without proof.

## Governance proposal

A DAO or protocol proposal people vote on. It must let a voter decide without reading anything else.

Structure (`templates/governance-proposal.md`):
1. **Title** that names the change ("Lower The Liquidation Threshold For wstETH From 80% To 78%").
2. **Summary**: 2 to 3 sentences: the change, why, and the effect.
3. **Motivation**: the problem, with data and links.
4. **Specification**: exactly what changes: parameters (old and new values), contract addresses, function calls, code or calldata.
5. **Rationale**: alternatives considered and why this one.
6. **Risks and security considerations**, including what could go wrong and how it's monitored.
7. **Voting options** and what each one does.
8. **Timeline**: discussion, snapshot or onchain vote, execution, with dates in UTC.
9. **Disclosures**: conflicts of interest, who's paid by whom.

Rules: neutral tone, both sides of the trade-off, exact numbers, links to the forum discussion (e.g. [Optimism governance forum](https://gov.optimism.io/), [Tally](https://www.tally.xyz/), [Snapshot](https://snapshot.box/)).

## EIP or ERC draft

Follow the official process and format in [EIP-1](https://eips.ethereum.org/EIPS/eip-1) and the [EIP template](https://github.com/ethereum/EIPs/blob/master/eip-template.md). The template's sections (Abstract, Motivation, Specification, Rationale, Backwards Compatibility, Test Cases, Reference Implementation, Security Considerations) are required in its own order, so don't apply the article structure here. Use RFC 2119 keywords (MUST, SHOULD, MAY) exactly. Voice rules still apply to the prose.

## Audit summary

A plain-language summary of a security audit for users and the community. Not a replacement for the report.

Structure (`templates/audit-summary.md`):
1. What was audited: repo, **commit hash**, contracts in scope, dates, auditor.
2. Findings by severity (critical, high, medium, low, informational) in a table, with status: fixed, acknowledged or disputed.
3. What the fixes changed, in plain terms.
4. What was out of scope, and the limits of an audit (it reduces risk, it doesn't guarantee safety).
5. Link to the full report and the fixed commit.

Rules: never write "audited, so it's safe"; give the commit hash so readers can tell whether the deployed code matches.

## Incident post-mortem

Written after an exploit, outage or bug. Blameless, factual and timely.

Structure (`templates/post-mortem.md`):
1. **Summary**: what happened, impact, current status, in 3 to 5 sentences.
2. **Impact**: funds affected, users affected, downtime, with exact figures and how they were calculated.
3. **Timeline** in **UTC**: detection, response, mitigation, resolution, each with a time and a link (transaction hash, PR, announcement).
4. **Root cause**: the vulnerability class and how it was reachable. Technical detail after the fix is deployed.
5. **Response**: what was done, by whom, and why.
6. **Remediation**: fixes, compensation plan (if any) and process changes, with owners and dates.
7. **What we're changing**, and how anyone can verify it.
8. **Acknowledgements**: responders and whitehats.

Rules: publish facts quickly and update the document as more are confirmed; mark what's still under investigation; don't publish exploit reproduction steps while any funds or forks remain at risk; no blame on individuals.

## Release notes and changelog

Follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

Structure (`templates/release-notes.md`):
1. Version and date.
2. **Breaking changes first**, each with the migration step.
3. Added, Changed, Deprecated, Removed, Fixed, Security.
4. **Contract changes**: new addresses per network, upgrade transactions, storage layout changes.
5. Upgrade guide link.

Rules: write for the person upgrading ("Call `migrate()` before..."), not for the team; one line per change; link PRs.

## Grant proposal

For ecosystem grants (foundations, DAOs, L2 grant programmes).

Structure (`templates/grant-proposal.md`):
1. Project summary (3 sentences).
2. Problem and who has it, with evidence.
3. Solution and why it's different from what exists.
4. **Milestones**: each with deliverables, acceptance criteria, date and budget.
5. Budget breakdown.
6. Team and prior work (links to shipped code).
7. Success metrics you can actually measure.
8. Maintenance and sustainability after the grant ends.
9. Licence (most ecosystem grants expect open source).

Rules: match the programme's stated priorities and format exactly; concrete deliverables over vision; no inflated user numbers.

## X thread

An overview that points to the long piece. Follow the voice rules strictly: threads are where the antithesis cadence spreads fastest.

Structure (`templates/x-thread.md`):
1. **Post 1 (hook):** the most surprising finding or the problem, specific and self-contained. No "A thread 🧵" opener.
2. **Posts 2 to 6:** one idea per post, each one readable alone, with a number, a code snippet image or a chart.
3. **Final post:** the takeaway and one link (article, video or repo).

Rules: no price calls or "alpha"; no engagement bait ("like and RT"); tag projects only when you're accurate about them; keep the link out of post 1 if the platform suppresses link posts.
