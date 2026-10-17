# How Not to Write

A writing skill for Claude. It cleans up the habits that make text read as machine-written, and it's the skill I use for every article I publish.

It enforces three rules:

1. **Kill the antithesis cadence.** No "it's not X, it's Y" and none of its relatives ("Not just an app. A revolution."). State the claim plainly, then back it with specifics.
2. **Never use em dashes.** Use the punctuation the sentence needs: a full stop, a comma, a colon or parentheses.
3. **Conversational, never verbose.** Cut throat-clearing openers, doubled phrasing and sentences that repeat the one before.

The full reasoning, examples and the one narrow exception are in [`skills/how-not-to-write/SKILL.md`](skills/how-not-to-write/SKILL.md).

## Install

### Claude Code (plugin)

```
/plugin marketplace add jorshimayor/how-not-to-write
/plugin install how-not-to-write@how-not-to-write
```

### Claude Code (manual)

Copy the skill folder into your personal skills directory:

```bash
git clone https://github.com/jorshimayor/how-not-to-write.git
cp -r how-not-to-write/skills/how-not-to-write ~/.claude/skills/
```

### Claude.ai and the Claude desktop app

Download `how-not-to-write.zip` from the [latest release](https://github.com/jorshimayor/how-not-to-write/releases/latest) and upload it under **Settings → Capabilities → Skills**.

## Use

Claude loads the skill on its own whenever it drafts or edits prose: articles, emails, landing pages, slides, taglines. You can also ask for it directly:

> Rewrite this intro using the how-not-to-write skill.

## Before and after

Examples from the topics I write about most:

| Domain | Before | After |
|---|---|---|
| Web3 | This isn't just a token. It's a community. | Holders vote on treasury spending onchain, and every proposal is public on the governance page. |
| AI | It's not autocomplete, it's reasoning. | The model plans the steps in its Thought line, then calls the calculator for each one. |
| ZK | Not just privacy. Freedom. | The app proves you're over 18 without sending your birth date to the server. |
| Web2 | The page has one bottleneck — the database. | The page has one bottleneck: the database. |

The "after" versions are shorter on drama and longer on facts. If the thing really matters, the details show it. More examples, including padding fixes and hype words to watch in each domain, are at the end of [`SKILL.md`](skills/how-not-to-write/SKILL.md).

## License

MIT
