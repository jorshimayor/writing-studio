# Writing Studio

The all-in-one Claude writing skill for **Web3 technical writers**, covering the AI, zero-knowledge (ZK) and Web2 topics Web3 writers work across. I use it for everything I publish.

One skill handles three kinds of work:

| Work | Examples | What you get |
|---|---|---|
| **Content that ranks** | Articles, blog and Substack posts, newsletters, YouTube videos | Reader-need outlines, keyword research, stretch titles, SEO audits, repurposing across channels |
| **Web3 documents** | Developer docs, READMEs, protocol explainers, whitepapers, governance proposals, EIP drafts, audit summaries, post-mortems, release notes, grant proposals, X threads | The right structure for each document type, a template, and safety and voice checks |
| **Rewrites** | Drafts, emails, tweets, docs that sound AI-written or padded | A human, specific, concise version, with a list of what changed and why |

## What it enforces everywhere

**Voice** (these used to be the separate How Not to Write skill, and are now built in):
1. No "it's not X, it's Y" cadence or its relatives. State the claim, then prove it with specifics.
2. No em dashes, ever.
3. Conversational, never verbose.

**Web3 safety:**
- No private keys, seed phrases or API keys, in text, code, screenshots or video.
- No financial advice, price talk or yield promises. Explain mechanisms instead.
- Testnet-first examples, with example contracts and circuits labelled as unaudited.
- Addresses and chain IDs verified against official sources.
- Vulnerabilities written up by class and fix, never as live exploits.

**Accuracy:** no invented statistics, quotes, search volumes, benchmarks or sources.

## Five modes

| Mode | Ask for |
|---|---|
| **Outline** | "Outline these 5 topics for my blog" (one checked outline file per topic, plus an index) |
| **From outline** | "Write the article from `outlines/what-is-a-zero-knowledge-proof.outline.md`" |
| **End to end** | "Write a post about my rollup experiments" (outline for approval, then the piece) |
| **Web3 document** | "Write a post-mortem for this incident", "Draft a governance proposal", "Write the README" |
| **Edit and rewrite** | "Make this thread sound less AI", "Tighten this doc" |

## What's inside

All paths are inside `plugins/writing-studio/skills/writing-studio/`.

| Path | Contents |
|---|---|
| `SKILL.md` | The workflow, the five modes and the hard rules |
| `references/voice.md` | The voice rules in full, with the reasoning, the one exception, and before/after examples for Web3, AI, ZK and Web2 |
| `references/domains.md` | Per domain: primary sources, where readers ask questions, terminology, accuracy and safety rules, example topics |
| `references/doc-types.md` | Web3 document types: the four kinds of developer docs (Diátaxis), README, protocol explainer, whitepaper, governance proposal, EIP draft, audit summary, post-mortem, release notes, grant proposal, X thread |
| `references/youtube.md` | A full YouTube playbook for technical creators: strategy, packaging and "stretch" titles, scripting, the 1/3/6-minute retention beats, editing, publishing and repackaging, plus Web3 safety on screen. Distilled from [howtoyoutube.dev](https://howtoyoutube.dev/) |
| `references/reader-needs.md`, `outline-template.md`, `structure.md` | The 8 reader needs, outline format and skeletons, and structure rules |
| `references/keyword-research.md`, `titles.md`, `seo.md`, `channels.md` | Keywords, titles, on-page SEO, and blog, Substack, newsletter and YouTube formats |
| `examples/outlines/` | 8 complete outlines (one per reader need, two each for Web3, AI, ZK and Web2), each passing the checker with no warnings |
| `templates/` | 13 templates: article, Substack post, newsletter issue, YouTube package, README, reference doc, whitepaper, governance proposal, audit summary, post-mortem, release notes, grant proposal, X thread |
| `profiles/` | Your brand, channels, links and house style (`jorshimayor.md` is mine, `_template.md` is for yours) |
| `scripts/` | `keyword_ideas.py`, `outline_check.py`, `seo_check.py` (plain Python 3, no dependencies) |

## Install

### Claude Code

```
/plugin marketplace add jorshimayor/writing-studio
/plugin install writing-studio@writing-studio
```

Or copy the folder manually:

```bash
git clone https://github.com/jorshimayor/writing-studio.git
cp -r writing-studio/plugins/writing-studio/skills/writing-studio ~/.claude/skills/
```

### Claude.ai and the Claude desktop app

Download `writing-studio.zip` from the [latest release](https://github.com/jorshimayor/writing-studio/releases/latest) and upload it under **Settings → Capabilities → Skills**.

> **Used How Not to Write before?** It's now part of Writing Studio. Uninstall `how-not-to-write` (Claude Code: `/plugin uninstall how-not-to-write@writing-studio`; claude.ai: remove it in Settings) so you don't have two skills applying the same rules.

## Set up your profile

Copy `profiles/_template.md` to `profiles/<your-name>.md` and fill in your brand, channels, domains and house style, then ask for it by name:

> Write a Substack post about my ZK experiments using the acme profile.

## The scripts

Run these from inside the skill folder.

**Keyword ideas** from Google and YouTube autocomplete, free and with no API key. For volume and difficulty, connect [OpenSEO](https://github.com/every-app/open-seo) (see `references/keyword-research.md`):

```bash
python3 scripts/keyword_ideas.py "account abstraction" --source both
```

**Outline checks** against each reader need's rules, and drafts against their outline:

```bash
python3 scripts/outline_check.py outlines/*.outline.md --site yourdomain.com --strict
python3 scripts/outline_check.py outlines/<slug>.outline.md --article drafts/<slug>.md
```

**SEO, voice and Web3 safety audit.** Leave out `--keyword` for docs and edits:

```bash
python3 scripts/seo_check.py draft.md --keyword "zero-knowledge proof" \
  --site "yourdomain.com, you.substack.com" --meta "Your meta description" --spelling british --strict
python3 scripts/seo_check.py README.md --spelling british
```

It flags private keys and seed phrases (fail), financial-advice phrasing, unchecked addresses, contract code without an "unaudited" note and mainnet-only deploy commands, alongside the voice and SEO checks. It exits with code 1 if anything fails, so it can gate a publishing script.

## License

MIT
