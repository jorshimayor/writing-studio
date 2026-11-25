# Profile: jorshimayor

Default profile. All links come from [jorshimayor.is-a.dev](https://jorshimayor.is-a.dev).

## Brand

- **Name:** jorshimayor (Josh)
- **Author:** Joshua Obafemi
- **Role:** technical writer and blockchain developer
- **What I publish:** four domains and the bridges between them:
  - **Web3:** smart contracts and dApps, rollups and L2s, validator nodes, security analysis.
  - **AI:** AI engineering, LLM internals, agents and tool use, evaluation, experiments with real results.
  - **ZK:** zero-knowledge proofs, circuits (Circom, Noir), zkVMs and ZK rollups.
  - **Web2:** backend and full-stack infrastructure, databases, frameworks, servers.
  Formats: technical articles, guides, research write-ups, tutorials and videos. Domain rules live in `references/domains.md`.
- **Audience:** developers and technical builders working across Web3, AI, ZK and Web2, from curious beginners to practising engineers. Assume programming literacy, not deep ML, cryptography or protocol background.
- **Positioning:** make complex systems simple, and back every piece with something I built, ran or measured. Show the code, the data and what broke.

## Channels

| Channel | URL | Default CTA |
|---|---|---|
| Website and portfolio | https://jorshimayor.is-a.dev | See more of my work |
| Blog (on my site) | https://jorshimayor.is-a.dev/blog | Read the next deep dive |
| Hashnode (current articles) | https://jorshimayor.hashnode.dev | Read the next deep dive |
| Substack (newsletter) | https://jorshimayor.substack.com | Subscribe for new deep dives and experiments |
| YouTube | https://www.youtube.com/@jorshimayor | Watch the full walkthrough |
| GitHub | https://github.com/jorshimayor | Clone the code |
| X | https://x.com/jorshimayor | Follow for shorter takes |
| LinkedIn | https://linkedin.com/in/jorshimayor | Connect |

**Site domains for internal links** (pass all of them to `--site`):

```
jorshimayor.is-a.dev, jorshimayor.hashnode.dev, jorshimayor.substack.com, youtube.com/@jorshimayor, github.com/jorshimayor
```

The /blog page on the website has no posts yet, and articles currently live on Hashnode. When a piece is published in both places, ask which URL is canonical.

## Linkable assets

Use these for internal links and next-step CTAs. Add new pieces as they're published.

- Portfolio of articles and videos by category: https://jorshimayor.is-a.dev/work
- Projects with code: https://jorshimayor.is-a.dev/projects
- AI engineering series code: https://github.com/jorshimayor/AI-Engineering-Flow_Research
- Writing Studio (my all-in-one Web3 writing skill): https://github.com/jorshimayor/writing-studio

## Visual branding

Brand guide: `design/BRAND_GUIDE.md` in the writing-studio repo. The look is **Paper Trace with a marker layer**: paper `#fcfcfb`, ink `#0b0b0b`, trace blue `#2a78d6`, Bricolage Grotesque 800 for titles and hooks, Inter for text, JetBrains Mono for code, and on top a marker layer (highlighter `#ffe45c`, marker red `#d1203f`, one Caveat note) that points at the exact line, value or spot that matters.

- **Per piece**, deliver a brand-asset spec (`design/brand/specs/<slug>.json`) and render it with `python3 design/brand/brand_assets.py <spec>`: YouTube thumbnail, article header, social card and banner, plus the shrink test. Record the source of every number and line of code in the spec's `sources`.
- **Illustrated figures** use the skill's figure kit (`scripts/figure_kit.py`) with `profiles/jorshimayor.brand.json` and the Marked j logo. The vector master is in `profiles/jorshimayor-brand/`: the mark for light and dark backgrounds (`mark-colour-on-paper.svg`, `mark-colour-on-ink.svg`, `mark-auto.svg`), single-colour versions, app tiles, outlined lockups (`lockup-horizontal-*`, `lockup-stacked-*`, `wordmark-*`) and favicons (`favicon.svg`, `favicon.ico`). Article scripts live in `design/figures/` (`erc4626_v2.py`, `tokenisation_v2.py`) and write to `drafts/images/v2/`.
- **Plain SVG figures**, build with `design/viz/components.py` and `design/viz/tokens.py` following `design/ILLUSTRATION_DESIGN_SYSTEM.md`. Use the marker layer (`highlight`, `marker_circle`, `note`, plus `code_block` and `image` for code and pictures) when the reader must look at one place: at most one circle and one note per figure. Never hard-code a colour or size.
- **Export** PNGs with `python3 design/viz/export.py`, which loads the brand fonts.
- Each figure gets a title, a caption, a footnote with the source, and alt text that states the finding in numbers and says what is marked.
- Logo: Marked j. Still open: the tagline "Built. Run. Measured." (proposed), and a library of cut-out photos.

## House style

These override the defaults in `references/voice.md`.

- `strict_style: true`. Run the checker with `--strict --spelling british`.
- **Spelling: British English** (organisation, optimise, analyse, behaviour, colour, centre, modelling, and licence as the noun with license as the verb). Product names, code, APIs and quotations keep their official spelling (`color` in CSS, "Optimizer" in a library name).
- **Titles:** capitalise every word, including short ones and both halves of hyphenated words: "How To Build A ReAct Agent In 100 Lines".
- **Headings:** capitalise nouns, verbs (including "Is" and "Are") and any word of 5 or more letters: "What Is a Context Window?"
- **Oxford comma** always.
- **Contractions** by default. Step-by-step guides may skip them.
- **Parentheses** only for acronyms on first use: "retrieval-augmented generation (RAG)". Put other asides in a clause.
- **No bold for emphasis** in prose.
- **Numbers:** words for small counts in prose ("two models"), numerals for measurements and technical values (0.5B parameters, 16 GB, 8,192 tokens), and a space before units.
- **Person:** "I" for my experiments, results and opinions. Neutral voice for explainers. "You" for the reader's choices and actions.
- **Dates:** "13 October 2026" (British day-month-year). **Times:** with a timezone, e.g. "14:00 UTC".
