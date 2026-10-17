# YouTube Package Template

Fill this in **before recording**. The full reasoning is in `references/youtube.md`.

## 1. The promise
- **What the viewer clicked for:** <one sentence>
- **What they get (the thing the video owes them):** <one sentence>
- **Audience:** <growth video for new viewers | deep dive for existing followers>

## 2. Packaging

**Title (stretch level, Title Case, under 70 characters, ideally under 60):**
| Level | Title |
|---|---|
| Truth (literal) | <what the video is> |
| Stretch option 1 | <one step past the truth, still delivered early> |
| Stretch option 2 | <...> |
| Stretch option 3 | <...> |

Test: does it make someone think "huh?" rather than "I don't believe that"? Can the video pay it off in the first few minutes?

**Thumbnail concept** (design comes from the designer's brand kit):
- Idea: <the reason to stop scrolling>
- Enemy or saviour: <recognisable secondary subject, e.g. a failed-transaction toast, a gas spike, a passing test>
- Face: <expression matching the promise; position consistent with the channel>
- Text: <none, or 1 to 2 big words>
- Magnified detail: <the one line, button or number that matters>
- Squint test passed: <yes or no>

## 3. Script in four layers

**Intro (15 to 20 seconds, word for word, read aloud):**
> <What changed. Why you should care. What you'll get. Straight into the first point. Words tie back to the thumbnail.>

**Framework (2 to 3 sentences on how the video delivers the promise):**
> <e.g. "I'll deploy a token on a testnet and show the exact step where most tutorials leak your key.">

**Macro points (bullets):**
1. <point 1, lands by ~1:00>
2. <point 2, lands by ~3:00>
3. <point 3, lands by ~6:00>
4. <back-half depth: stories, context, edge cases>

Only one or two points? Make it a Short or an X post instead.

## 4. Beat sheet

| Time | Beat | On screen | Re-engagement line |
|---|---|---|---|
| 0:00 to 0:15 | Intro: re-confirm the click, show the promised thing | <demo or result> | |
| ~1:00 | Finish a small first unit | | <"That's the first change, but it doesn't explain..."> |
| ~3:00 | Second payoff | | <next reason to keep watching> |
| ~6:00 | Third payoff, then the back half | | <bigger promise reminder> |
| 6:00+ | Back half: depth and personality | | |
| End | Fold the ending into the last point, closing line, cut | | |

Length: over 8 minutes. 15 to 20 minutes is fine if every section earns its place.

## 5. Recording notes
- [ ] 2 to 3 intro takes
- [ ] Ending recorded so it doesn't refer to the previous section
- [ ] Optional back-half sections shot standalone
- [ ] 20-second versions of long explanations
- [ ] Spoken notes for the editor
- [ ] Testnet only. No real keys, seed phrases or API keys on screen

## 6. Description
<One or two plain, search-friendly sentences with the keyword.>

Full article: <url>
Code: <repo url>
Newsletter: <url>

<Chapters only for reference-style tutorials where viewers jump between steps.>

## 7. Launch and follow-up
- [ ] Share unlisted with engaged community members for a day
- [ ] Post to X and Discord at go-live
- [ ] Pinned comment: <a question that invites replies>
- [ ] Day 2 to 3: if packaged for core fans, test broader packaging
- [ ] Week 1: read retention for the first six minutes and the ending
- [ ] Later: repackage if an evergreen video flatlines

---

## Filled example (Web3)

**The promise:** viewers clicked to deploy their first token safely, and they get a working testnet ERC-20 plus the one habit that keeps keys out of shell history.

| Level | Title |
|---|---|
| Truth | How To Deploy An ERC-20 Token With Foundry |
| Stretch 1 | Most Token Tutorials Leak Your Private Key |
| Stretch 2 | Deploy Your First Token Without Leaking Your Key |
| Stretch 3 | The Foundry Command That Exposes Your Wallet |

**Thumbnail concept:** a terminal command with the private key flag magnified and circled in red (enemy), a shocked expression on the right, one word: "LEAKED". Designer applies the brand kit.

**Intro:** "Most ERC-20 tutorials have you paste your private key straight into the terminal, where it sits in your shell history. In the next ten minutes we'll deploy a real token to a testnet with Foundry, and your key will never touch the command line. Here's the token we're about to ship."

**Framework:** "I'll build and deploy the token live on Sepolia, and stop at the exact step where most guides leak the key."

**Macro points:**
1. The leak: what goes wrong in typical tutorials (by ~1:00)
2. Project setup and the OpenZeppelin contract (by ~3:00)
3. Safe deployment with environment variables and a burner wallet (by ~6:00)
4. Back half: testing, verifying on a block explorer, common errors

**Description:** Deploy an ERC-20 token to a testnet with Foundry and OpenZeppelin, without ever putting your private key on the command line.
Full article: https://jorshimayor.is-a.dev/work · Code: https://github.com/jorshimayor
