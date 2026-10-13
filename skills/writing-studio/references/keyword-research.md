# Keyword Research

Pick keywords from evidence. Three layers, from free to paid. Use the best layer available, and say which one the numbers came from.

| Layer | Tool | Gives you | Cost |
|---|---|---|---|
| 1. Free, built in | `scripts/keyword_ideas.py` (Google and YouTube autocomplete) | Real phrasings, questions, comparisons, long-tail variants | Free |
| 1. Free, built in | Web search (when available) | What ranks now, "People also ask", competitor titles | Free |
| 2. Open-source SEO suite | [OpenSEO](https://github.com/every-app/open-seo) with a [DataForSEO](https://dataforseo.com/) API key | Search volume, keyword difficulty, CPC, SERP results, competitor keywords, backlinks, rank tracking | Software is free (MIT). DataForSEO data is pay-as-you-go |
| 3. Your own data | [Google Search Console](https://search.google.com/search-console) | The queries your site already appears for, with clicks, impressions and position | Free, needs a verified site |

Optional extras:
- [trendspyg](https://github.com/flack0x/trendspyg): a maintained Python library for Google Trends (interest over time, rising related queries). The older `pytrends` was archived in 2025.
- [SerpBear](https://github.com/towfiqi/serpbear): self-hosted rank tracker to watch positions after publishing.

**Never invent volumes, difficulty scores or trends.** If only layer 1 is available, say that the keyword choice is based on autocomplete and SERP evidence, not volume data.

## Layer 1: autocomplete ideas

```bash
python3 scripts/keyword_ideas.py "<seed>" --source both --expand questions
python3 scripts/keyword_ideas.py "<seed 1>" "<seed 2>" --expand full --json
```

- The **score** combines how often and how high a phrase was suggested. It's a popularity signal, not a search volume.
- Phrases suggested by **both Google and YouTube** are strong candidates for a cross-channel piece (article plus video).
- **Questions** become H2s and FAQ entries. **Comparisons** suggest a "Compare For Me" piece. **Problems** suggest "Fix It".
- Add `--gl gb --hl en-GB` (or another market) to see a specific country's phrasing.

## Layer 2: OpenSEO

OpenSEO is an open-source alternative to Ahrefs and Semrush. It's self-hosted with Docker or Cloudflare, and it pulls live data from DataForSEO, which you pay for per request. It also exposes an **MCP server**. When it's connected to Claude, use its tools directly for keyword volume, difficulty, SERP analysis and competitor research. Setup: [self-hosting docs](https://github.com/every-app/open-seo#self-hosting) and [MCP docs](https://openseo.so/docs/mcp).

If OpenSEO's MCP tools are available in the session, use them in Step 2 to:
1. Get **volume and difficulty** for the candidate keywords from layer 1.
2. Pull the **current SERP** for the top candidate: which pages rank, their titles, and the SERP features (featured snippet, "People also ask", videos).
3. Find **keywords competitors rank for** that you don't cover yet (content gaps).

## Choosing the primary keyword

Score each candidate on:

| Factor | Look for |
|---|---|
| Intent match | The SERP shows the format you plan (explainer, guide, comparison). If it doesn't, change the format or the keyword |
| Relevance | You can genuinely answer it with your experience, code or data |
| Volume | Enough demand to matter. For a small or new site, low-volume specific phrases are fine |
| Difficulty | A new site should target low difficulty and long-tail phrases first. Build authority, then aim higher |
| Freshness | Rising interest (Trends) or recent changes the top results haven't covered |
| Cross-channel | Also suggested on YouTube, so one piece can feed the video too |

Then pick:
- **1 primary keyword**: the phrase the piece is built around (goes in the title, the first 50 words, the H2s and the slug).
- **2 to 5 secondary keywords**: variants, synonyms and sub-questions (go in H2s, H3s and the body).
- **3 to 8 questions**: these become headings or an FAQ.

## Reading the competition (titles that rank)

For the primary keyword, look at the top 10 results (web search or OpenSEO's SERP data) and note:
- **Format**: list, guide, comparison, opinion, video carousel.
- **Title patterns**: numbers, years, "vs", "how to", brackets.
- **Gaps**: outdated versions, missing code or data, no real experiments, nothing for your audience.
- **SERP features**: a featured snippet means a crisp 40 to 60 word definition under an H2 can win it, and a video carousel means a YouTube version of the piece has a slot.

Feed this into `titles.md`: match the winning format, then beat the titles on specificity and evidence.
