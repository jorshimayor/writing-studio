# SEO Checklist

Applies to blog articles and Substack posts (Substack posts are indexed and have their own SEO title and description settings). Newsletters and YouTube have their own discovery rules in `channels.md`.

Search engines reward pages that answer the query clearly and are easy to navigate. Every rule below serves that, so when a rule and readability conflict, readability wins.

`scripts/seo_check.py` checks the items marked *(auto)*.

## Keywords

**Primary keyword** (the main phrase you want to rank for):
- [ ] In the first paragraph, ideally the first 50 words. *(auto)*
- [ ] In the first H2, or a close variation of it. *(auto)*
- [ ] In at least 1 or 2 other H2s, as a variation if needed. *(auto)*
- [ ] In the first paragraph under the first H2. *(auto)*
- [ ] Spread naturally from start to end, never stuffed. *(auto)*
- [ ] In the closing section. *(auto)*
- [ ] Roughly 1% to 2% of words. *(auto)*
- [ ] In the title, the meta description and the URL slug. *(auto for title and meta)*

**Secondary keywords** (related phrases and synonyms):
- [ ] In some H2s and H3s. *(auto)*
- [ ] Used naturally in the body, roughly 0.5% to 1%. *(auto)*

Variations count. Plurals, reordered words and close synonyms all help, because search engines match meaning, not exact strings.

## Structure

- [ ] One H1 (the title). *(auto)*
- [ ] Headings go H2 → H3 with no skipped levels. *(auto)*
- [ ] The search intent is answered at the top, under an H2 that uses a variation of the topic.

## Links

**Internal links** (to your own pages):
- [ ] 3 to 5 per 1,000 words, or 3 to 5 total in short pieces. *(auto with `--site`)*
- [ ] Point to related deep dives, tutorials, case studies, your newsletter or product pages. Favor the pages that matter most to you.
- [ ] Place important links early in the piece.
- [ ] Find candidates with a search like `"topic" site:yourdomain.com`.

**Anchor text:**
- [ ] Descriptive and natural, never "click here" or "read more". *(auto)*
- [ ] Varied, using long-tail phrases rather than the same exact-match phrase every time.
- [ ] One anchor text, one destination: never send the same anchor to two URLs. *(auto)*
- [ ] Never use this page's own primary keyword as an anchor to another page. Both pages would compete for the same search (cannibalization). *(auto)*

**External links:**
- [ ] 1 to 3 links to authoritative primary sources: official docs, papers, standards, original data. *(auto)*
- [ ] No broken links. *(auto with `--check-links`)*

## Media

- [ ] Every image has descriptive alt text, with the keyword where it fits naturally. *(auto)*
- [ ] Images compressed for the web, ideally under 300 KB. *(auto for local files)*
- [ ] Screenshots captured at a consistent size (e.g. 1440 × 900 px).
- [ ] Descriptive file names (`attention-heatmap.png`, not `IMG_2041.png`).

## Metadata

- **SEO title:** 50 to 60 characters, primary keyword near the front.
- **Meta description:** 140 to 160 characters. Include the keyword, state the concrete payoff, and end with a reason to click.
- **Slug:** lowercase words joined by hyphens, built from the keyword, no stop words, no year (so the piece can be refreshed later).

## Conversion

- [ ] A clear CTA that fits the reader need: subscribe, watch the video, read the next piece, try the tool.

## Keyword placement tips

- Write for the reader first, then place keywords. If a sentence exists only to hold a keyword, rewrite it until you'd keep it anyway.
- Density too low: replace a vague "it" or "this" with the keyword or a variation.
- Density too high: swap some uses for secondary keywords or synonyms.
