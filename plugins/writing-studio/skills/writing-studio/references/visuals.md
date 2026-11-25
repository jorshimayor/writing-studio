# Visuals: figures, annotated code and pictures, headers and thumbnails

Every piece ships with its pictures: the figures inside it and the brand assets around it (article header, YouTube thumbnail, social card). This file is the process. The look comes from the profile.

## Contents
- Where the look comes from
- Plan visuals in the outline
- Figures inside the piece
- The figure kit
- The annotation layer: pointing at the one thing
- Brand assets around the piece
- Checks before delivery

## Where the look comes from

Read the profile's **Visual branding** section in Step 0.

- **It points to a brand guide or tooling** (tokens, figure components, an asset renderer): follow it exactly and build every image with that tooling. Never hard-code a colour, font or size the guide defines.
- **It names a designer or brand kit you can't use**: deliver the concept, the exact text for each image, and the alt text, and leave the design to them.
- **It's empty**: deliver concepts and text only, and suggest the author sets up a brand guide.

## Plan visuals in the outline

In Step 4, the outline's image or visual plan lists, for each figure: what it shows, the one thing to notice (that becomes the caption), the data or code it uses and where that comes from, whether it needs the annotation layer, and the alt text. Add the brand assets: the header title and highlighted phrase, and for video the thumbnail hook.

A figure earns its place when it shows something words can't do as quickly: a flow, a comparison, a state change, the exact line of code. Don't add a figure that repeats a paragraph.

## Figures inside the piece

- One figure, one point. Title (what you're looking at), caption (what to notice), footnote (source, version, caveat).
- Real numbers only. Every value comes from a run, a source or a computation you can name; if a value is illustrative, the footnote says so.
- Code in a figure is real code from a tagged release or the author's repo. Name the file and lines; say if it was reflowed.
- Screenshots: crop to the part that matters, blur anything private, use testnets and burner wallets, and never show a key, seed phrase or token.
- Alt text states the finding in numbers and says what is marked.

## The figure kit

`scripts/figure_kit.py` builds illustrated figures as HTML and inline SVG and renders them to 2x PNG with headless Chrome. Use it for any figure that explains a mechanism, a flow, a comparison or a result. A plain chart from a plotting library is fine for dense data, but give it the same title, dek and source.

**Brand.** The kit reads `profiles/<name>.brand.json`: palette, wordmark and an optional logo SVG. Copy `profiles/_template.brand.json` for a new profile. Fonts default to Bricolage Grotesque (titles), Geist (small headings), Newsreader (text), JetBrains Mono (code and numbers) and Caveat (the one marker note); a brand file can override any of them.

**Frame.** `figure(kicker, title, dek, body, source)` gives every figure the same anatomy: a series label, a display title saying what it shows, a dek stating the finding (bold the one sentence that matters), the body, and a source line with the logo and wordmark. `render(page, "images/name.png")` writes the PNG and `name.html` beside it, the editable source.

**Parts.**

| Part | Call or class | Use it for |
|---|---|---|
| Card | `class="card"` | A panel, a step, an option |
| Pill | `class="pill"`, `pill vic`, `pill att`, `pill ok` | State, a value, a tag |
| Stamp | `class="stamp"` | A verdict: holds, leaks, broken, reverts |
| Highlight | `class="hl"` | The word or term that matters |
| Circle and note | `class="circ"`, `class="note"` | The annotation layer below |
| Coins and vault | `coins(n, "vic" or "att")`, `vault([stacks])`, `mini_vault()` | Balances, deposits, who owns what (state the scale, such as one coin per 1,000 tokens) |
| Ticket | `ticket(text, kind, empty=)` | Shares, receipts, claims; `empty=True` for one that wasn't minted |
| Avatar | `avatar("att" or "vic", label)` | The actors in a flow |
| Keycap, arrow | `keycap(label)`, `arrow()`, `hand_arrow()` | Input, steps, direction |

**Layouts that work.** A storyboard of numbered step cards along a trace line for a sequence; side-by-side cards for a comparison; a scoreboard (rows with a bar, a value and a stamp) for results; a station pipeline for transformations; a receipt or ledger for costs; a dot chart for one value changing across versions. `templates/figure.py` is a starter.

**Rules.** Draw the thing the reader is imagining (a vault, a token, a key), not a generic box. Keep the same scale across panels and say what a unit means. Owner colours keep their meaning across a piece: blue is normal or the victim, orange is the odd one or the attacker. One circle and one note per figure. Check the render, because overlaps don't show up in code.

## The annotation layer: pointing at the one thing

When the reader must look at one exact place (a token in a line of code, a value in a chart, a field on an explorer page), annotate it the way someone would with a pen:

- **Highlight** the word or expression that matters.
- **Circle** the exact thing.
- **One short note**, five words or fewer, saying why ("rounds down to 0").

Rules: at most one circle and one note per figure (a second point is a second figure); annotation colours never encode data, so the figure's data colours keep their meaning underneath; the caption still states the finding. Leave it off overview diagrams and charts whose caption already lands. If the profile's brand guide defines this layer (colours, fonts, components), use its version.

## Brand assets around the piece

Produce these when the profile has the tooling, otherwise as concepts and text:

| Asset | Usual size | Content |
|---|---|---|
| Article header and link preview | 1200 × 630 | Series label, the title with one phrase highlighted, optional key value |
| YouTube thumbnail | 1280 × 720 | One number or one or two words, optional one line of real code with the annotation, optional face. Follows `references/youtube.md` |
| Social card | 1080 × 1350 | Three short lines that tell the story; the last one carries the hook |
| Newsletter or profile banner | wide | Name, tagline, topics |

The thumbnail adds to the title instead of repeating it. Record where every number and line of code on an asset came from, and fact-check asset text like any sentence: it goes in the claims ledger (add the asset text to the draft's ledger as extra rows, or run `claims.py extract` on a short file listing it).

## Checks before delivery

- [ ] Every figure has a title, caption, footnote and alt text, and every value traces to a source.
- [ ] Code and screenshots are real, cropped, and free of keys, seed phrases and private data; addresses are checked on an explorer with the network named.
- [ ] Annotation: at most one circle and one note per figure, and the note is five words or fewer.
- [ ] Asset text is in the fact-check ledger, and the gate passes.
- [ ] The thumbnail passes the shrink test: the hook reads at about 170 px wide.
- [ ] No money imagery (price charts, rockets, "100x"), in line with the no-financial-advice rule.
- [ ] Deliver the image files (or the concepts and text), each with its alt text, in the visual list.
