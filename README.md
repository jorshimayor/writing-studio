# Writing Studio

Two Claude skills for developer content in **Web3, AI, zero-knowledge (ZK) and Web2**. I use them for everything I publish.

| Skill | What it does | Folder |
|---|---|---|
| **Writing Studio** | Takes a topic from idea to published piece: a search-ranked article, a Substack post, a newsletter issue or a YouTube video | [`plugins/writing-studio`](plugins/writing-studio) |
| **How Not to Write** | A prose guardrail for any writing: no "it's not X, it's Y" cadence, no em dashes, no padding | [`plugins/how-not-to-write`](plugins/how-not-to-write) |

Install either one or both (see [Install](#install)). Writing Studio already applies the How Not to Write rules, so install How Not to Write on its own when you want the guardrail for everyday writing too: emails, docs, posts.

## Writing Studio

It works in seven steps:

1. **Load a profile and brief.** Your brand, audience, channels, links and house style live in a profile file.
2. **Pick the reader need.** One of 8 needs (Educate Me, Explain It, Compare For Me, Guide Me, Fix It, Give Me Perspective, Update Me, Inspire Me) decides the intro, section order and ending.
3. **Research.** Keywords from free Google and YouTube autocomplete (bundled script), plus volume and difficulty from [OpenSEO](https://github.com/every-app/open-seo), the open-source Ahrefs alternative, if you connect it. Also search intent, real reader questions, gaps in what ranks, primary sources and internal links. It never invents data.
4. **Titles.** 8 to 10 options across hook patterns, using real trending signals, with SEO title, meta, slug, subject line or thumbnail text for the channel.
5. **Outline**, which you approve before drafting.
6. **Draft and audit.** A bundled checker scores the draft on keyword placement, density, headings, links, anchors, alt text and voice, and the draft gets fixed until nothing fails.
7. **Deliver and repurpose.** The article becomes the source of truth, and the newsletter and video become overviews that link back to it.

It also enforces the [How Not to Write](plugins/how-not-to-write) rules: no "it's not X, it's Y" cadence, no em dashes, no padding.

### Three ways to use it

| Mode | Ask for | You get |
|---|---|---|
| **Outline** | "Outline these 5 topics for my blog" | One `<slug>.outline.md` per topic (reader need, keywords, titles, intro plan and every planned section), checked against the reader need's rules, plus an index table |
| **From outline** | "Write the article from `outlines/what-is-rag.outline.md`" | The finished piece, built section by section from the approved outline, then checked for SEO and for sticking to the outline |
| **End to end** | "Write a post about my ReAct agent results" | Outline for your approval, then the finished piece |

Each reader need has its own outline skeleton and rules. For example, a Guide Me outline must open with prerequisites, a Fix It outline must start with causes and end with where to get help, and a Compare For Me outline must plan a comparison table. `scripts/outline_check.py` enforces them:

```bash
python3 plugins/writing-studio/skills/writing-studio/scripts/outline_check.py outlines/*.outline.md --site yourdomain.com
python3 plugins/writing-studio/skills/writing-studio/scripts/outline_check.py outlines/what-is-rag.outline.md --article drafts/what-is-rag.md
```

### Built for Web3, AI, ZK and Web2

All paths below are inside `plugins/writing-studio/skills/writing-studio/`.

- **Domain guide** (`references/domains.md`): primary sources to cite, where readers ask questions, terminology conventions and accuracy rules for each domain. For example: no financial advice in Web3, date every model fact in AI, state security assumptions in ZK, name the version in every Web2 fix.
- **8 example outlines** (`examples/outlines/`), one per reader need, two per domain: *What Is A Zero-Knowledge Proof?*, *How Does A Context Window Work In LLMs?*, *Optimistic Vs ZK Rollups*, *How To Deploy An ERC-20 Token With Foundry*, *PostgreSQL Too Many Connections?*, *I Ran 140 Few-Shot Experiments*, *Next.js 15 Caching Changes* and *Learning Zero-Knowledge Proofs*. Each passes the outline checker with no warnings.
- **Templates** (`templates/`): article, Substack post, newsletter issue (with a filled multi-domain example) and YouTube package (with a filled Web3 example).
- **Terminology checks**: the SEO checker warns on mixed forms ("on-chain" and "onchain", "Web3" and "web3") and accepts mixed-case names like zk-SNARK, zkVM and dApp in title case.

## Install

### Claude Code

```
/plugin marketplace add jorshimayor/writing-studio
/plugin install writing-studio@writing-studio
/plugin install how-not-to-write@writing-studio
```

Or copy the folders manually:

```bash
git clone https://github.com/jorshimayor/writing-studio.git
cp -r writing-studio/plugins/writing-studio/skills/writing-studio ~/.claude/skills/
cp -r writing-studio/plugins/how-not-to-write/skills/how-not-to-write ~/.claude/skills/
```

### Claude.ai and the Claude desktop app

Download `writing-studio.zip` and/or `how-not-to-write.zip` from the [latest release](https://github.com/jorshimayor/writing-studio/releases/latest) and upload each one under **Settings → Capabilities → Skills**.

> **Moved from jorshimayor/how-not-to-write?** That repo is archived. Re-add the marketplace with the commands above and install `how-not-to-write@writing-studio`.

### Set up your profile

Copy `plugins/writing-studio/skills/writing-studio/profiles/_template.md` to `profiles/<your-name>.md` and fill in your brand, channels, domain and style. Then ask for it by name:

> Write a Substack post about my RAG experiments using the acme profile.

The bundled `jorshimayor` profile is mine and shows a filled-in example.

### Use

> Write an SEO article on "how does a context window work" for my blog.

> Turn this article into a newsletter issue and a YouTube script.

> Give me 10 catchy titles for a post about my ReAct agent results.

### Keyword ideas (free)

`scripts/keyword_ideas.py` pulls real search phrasings, questions and comparisons from Google and YouTube autocomplete. It needs no API key:

```bash
python3 plugins/writing-studio/skills/writing-studio/scripts/keyword_ideas.py "react agent" --source both
```

For search volume and keyword difficulty, self-host [OpenSEO](https://github.com/every-app/open-seo) with a pay-as-you-go [DataForSEO](https://dataforseo.com/) key and connect its MCP server to Claude. The skill uses it automatically when it's available. See `references/keyword-research.md`.

### The checker

`scripts/seo_check.py` runs on any Markdown draft with plain Python 3 and no dependencies:

```bash
python3 plugins/writing-studio/skills/writing-studio/scripts/seo_check.py draft.md \
  --keyword "context window" --secondary "token limit, long context" \
  --site "yourdomain.com, you.substack.com" --meta "Your meta description" \
  --spelling british --strict
```

It returns ✔, ⚠ or ✘ for each check, and exits with code 1 if anything fails, so it can gate a publishing script.

## How Not to Write

Three rules for anything written for a person to read:

1. **Kill the antithesis cadence.** No "it's not X, it's Y" and none of its relatives. State the claim plainly, then back it with specifics.
2. **Never use em dashes.** Use a full stop, comma, colon or parentheses.
3. **Conversational, never verbose.** Cut throat-clearing openers, doubled phrasing and repeated sentences.

Before-and-after examples from Web3, AI, ZK and Web2, plus domain hype words to watch, are in [`plugins/how-not-to-write`](plugins/how-not-to-write).

## Repository layout

```
.claude-plugin/marketplace.json     lists both plugins
plugins/
├── writing-studio/                 the content system (skill, references, examples, templates, scripts)
└── how-not-to-write/               the prose guardrail
```

## License

MIT
