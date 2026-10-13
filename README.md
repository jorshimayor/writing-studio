# Writing Studio

A Claude skill that takes a topic from idea to published piece: a search-ranked article, a Substack post, a newsletter issue or a YouTube video. I use it for everything I publish.

It works in seven steps:

1. **Load a profile and brief.** Your brand, audience, channels, links and house style live in a profile file.
2. **Pick the reader need.** One of 8 needs (Educate Me, Explain It, Compare For Me, Guide Me, Fix It, Give Me Perspective, Update Me, Inspire Me) decides the intro, section order and ending.
3. **Research.** Keywords from free Google and YouTube autocomplete (bundled script), plus volume and difficulty from [OpenSEO](https://github.com/every-app/open-seo), the open-source Ahrefs alternative, if you connect it. Also search intent, real reader questions, gaps in what ranks, primary sources and internal links. It never invents data.
4. **Titles.** 8 to 10 options across hook patterns, using real trending signals, with SEO title, meta, slug, subject line or thumbnail text for the channel.
5. **Outline**, which you approve before drafting.
6. **Draft and audit.** A bundled checker scores the draft on keyword placement, density, headings, links, anchors, alt text and voice, and the draft gets fixed until nothing fails.
7. **Deliver and repurpose.** The article becomes the source of truth, and the newsletter and video become overviews that link back to it.

It also enforces the [How Not to Write](https://github.com/jorshimayor/how-not-to-write) rules: no "it's not X, it's Y" cadence, no em dashes, no padding.

## Install

### Claude Code

```
/plugin marketplace add jorshimayor/writing-studio
/plugin install writing-studio@writing-studio
```

Or copy the folder manually:

```bash
git clone https://github.com/jorshimayor/writing-studio.git
cp -r writing-studio/skills/writing-studio ~/.claude/skills/
```

### Claude.ai and the Claude desktop app

Download `writing-studio.zip` from the [latest release](https://github.com/jorshimayor/writing-studio/releases/latest) and upload it under **Settings → Capabilities → Skills**.

## Set up your profile

Copy `skills/writing-studio/profiles/_template.md` to `profiles/<your-name>.md` and fill in your brand, channels, domain and style. Then ask for it by name:

> Write a Substack post about my RAG experiments using the acme profile.

The bundled `jorshimayor` profile is mine and shows a filled-in example.

## Use

> Write an SEO article on "how does a context window work" for my blog.

> Turn this article into a newsletter issue and a YouTube script.

> Give me 10 catchy titles for a post about my ReAct agent results.

## Keyword ideas (free)

`scripts/keyword_ideas.py` pulls real search phrasings, questions and comparisons from Google and YouTube autocomplete. It needs no API key:

```bash
python3 skills/writing-studio/scripts/keyword_ideas.py "react agent" --source both
```

For search volume and keyword difficulty, self-host [OpenSEO](https://github.com/every-app/open-seo) with a pay-as-you-go [DataForSEO](https://dataforseo.com/) key and connect its MCP server to Claude. The skill uses it automatically when it's available. See `references/keyword-research.md`.

## The checker

`scripts/seo_check.py` runs on any Markdown draft with plain Python 3 and no dependencies:

```bash
python3 skills/writing-studio/scripts/seo_check.py draft.md \
  --keyword "context window" --secondary "token limit, long context" \
  --site "yourdomain.com, you.substack.com" --meta "Your meta description" \
  --spelling british --strict
```

It returns ✔, ⚠ or ✘ for each check, and exits with code 1 if anything fails, so it can gate a publishing script.

## License

MIT
