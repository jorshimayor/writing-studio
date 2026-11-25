"""LLM tokenisation figures, v2 (illustrated). Numbers come from the author's GPT-2 notebook
(week 1 of AI-Engineering-Flow_Research) as used in drafts/llm-tokenisation-quirks.md.

    python3 design/figures/tokenisation_v2.py drafts/images/png [figure ...]
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from figures.kit import E, figure, render, keycap, arrow  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else "."
ONLY = set(sys.argv[2:])
KICK = "LLM tokenisation"

TOK_CSS = """
.tok{display:inline-flex;align-items:center;height:40px;padding:0 12px;border-radius:10px;border:2px solid var(--blue);background:var(--btint);font:600 18px var(--mono);white-space:pre;color:var(--ink)}
.tok.odd{border-color:var(--orange);background:var(--otint);color:#a8401a}
.tok.n{border-color:#d6d5cf;background:#fff;color:var(--ink2)}
.sp{color:var(--ink3)}
.lab{font:700 12px var(--mono);letter-spacing:.1em;color:var(--ink3);text-transform:uppercase}
.big{font:800 54px/1 var(--display);letter-spacing:-.04em}
"""


def chip_icon():
    pins = "".join(f'<rect x="{14 + i * 12}" y="2" width="4" height="9" rx="1" fill="#0b0b0b"/>'
                   f'<rect x="{14 + i * 12}" y="69" width="4" height="9" rx="1" fill="#0b0b0b"/>'
                   f'<rect x="2" y="{14 + i * 12}" width="9" height="4" rx="1" fill="#0b0b0b"/>'
                   f'<rect x="69" y="{14 + i * 12}" width="9" height="4" rx="1" fill="#0b0b0b"/>' for i in range(5))
    return (f'<svg width="80" height="80" viewBox="0 0 80 80">{pins}<rect x="10" y="10" width="60" height="60" rx="10" fill="#0b0b0b"/>'
            f'<rect x="20" y="20" width="40" height="40" rx="6" fill="none" stroke="#fcfcfb" stroke-width="1.5" stroke-dasharray="3 3"/>'
            f'<text x="40" y="45" text-anchor="middle" font-family="Bricolage Grotesque" font-weight="800" font-size="13" fill="#fcfcfb">GPT-2</text></svg>')


def bpe_pipeline():
    css = TOK_CSS + """
.pipe{display:grid;grid-template-columns:1fr 36px 1.45fr 36px 1.1fr 36px 1fr;align-items:stretch}
.st{padding:18px;display:flex;flex-direction:column;gap:14px}
.st h3{font:700 18px/1.2 var(--head)}
.belt{display:flex;align-items:center;justify-content:center}
.belt svg{display:block}
.input{border:2px solid var(--ink);border-radius:12px;padding:14px;font:600 20px var(--mono);background:#fff;white-space:nowrap}
.input i{display:inline-block;width:2px;height:24px;background:var(--blue);vertical-align:-4px;margin-left:2px}
.bytes{display:grid;grid-template-columns:repeat(6,1fr);gap:6px}
.byte{border:1.5px solid #d6d5cf;border-radius:8px;background:#fff;text-align:center;padding:6px 0 4px;font:700 15px var(--mono)}
.byte small{display:block;font:500 12px var(--mono);color:var(--ink3);margin-top:2px}
.merge{display:flex;gap:8px;flex-wrap:wrap}
.grp{border:2px solid var(--blue);border-radius:10px;padding:6px 8px;display:flex;gap:3px;background:var(--btint)}
.grp span{font:600 14px var(--mono);color:#1d5fae}
.ids{display:flex;gap:8px}
.id{font:800 26px var(--display);border:2px solid var(--ink);border-radius:10px;padding:8px 12px;background:#fff}
"""
    arrow = ('<div class="belt"><svg width="36" height="24" viewBox="0 0 36 24"><path d="M2 12H30M22 4l9 8-9 8" fill="none" '
             'stroke="#0b0b0b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')
    word = "tokenization"
    hexes = [f"{ord(c):02x}" for c in word]
    bytes_html = "".join(f'<div class="byte">{h}<small>{c}</small></div>' for h, c in zip(hexes, word))
    g1 = "".join(f"<span>{c}</span>" for c in "token")
    g2 = "".join(f"<span>{c}</span>" for c in "ization")
    s1 = (f'<div class="card st"><span class="lab">1 · you type</span><h3>A word, in plain text</h3>'
          f'<div class="input">tokenization<i></i></div><p style="font:16px var(--ui);color:var(--ink2)">12 characters</p></div>')
    s2 = (f'<div class="card st"><span class="lab">2 · UTF-8 bytes</span><h3>Every character becomes bytes</h3>'
          f'<div class="bytes">{bytes_html}</div><p style="font:16px var(--ui);color:var(--ink2)">256 possible values, so nothing is ever unknown</p></div>')
    s3 = (f'<div class="card st" style="position:relative"><span class="lab">3 · BPE merges</span><h3>Learned merges glue frequent pairs</h3>'
          f'<div class="merge"><div class="grp">{g1}</div><div class="grp">{g2}</div></div>'
          f'<div style="font:600 13px var(--mono);color:var(--ink3);text-align:center">↓ 12 bytes become 2 tokens</div>'
          f'<div style="display:flex;gap:8px"><span class="circ" style="display:flex;gap:8px"><span class="tok">token</span><span class="tok">ization</span></span></div>'
          f'<div class="note" style="margin-top:14px;transform:rotate(-2deg)">2 tokens, not 12 letters</div></div>')
    s4 = (f'<div class="card st"><span class="lab">4 · IDs</span><h3>What the model actually sees</h3>'
          f'<div class="ids"><span class="id">30001</span><span class="id">1634</span></div>'
          f'<div style="display:flex;align-items:center;gap:12px">{chip_icon()}<span style="font:500 16px var(--ui);color:var(--ink2)">a list of integers, never the letters</span></div></div>')
    body = f'<div class="pipe">{s1}{arrow}{s2}{arrow}{s3}{arrow}{s4}</div>'
    page = figure(KICK, "What the model receives",
                  "Before GPT-2 reads anything, your text goes through four steps. "
                  "<strong>It never sees “tokenization”, only two integer IDs.</strong>",
                  body, "GPT-2 tokeniser. IDs shown for illustration; check them in the notebook.", css)
    render(page, f"{OUT}/bpe-pipeline.png")


def trailing_space():
    css = TOK_CSS + """
.lane{display:grid;grid-template-columns:44px 1fr 50px 300px;align-items:center;gap:16px;padding:22px 24px}
.lane + .lane{margin-top:16px}
.tag{width:44px;height:44px;border-radius:50%;display:grid;place-items:center;font:800 20px var(--display);color:#fff}
.prompt{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.cur{width:3px;height:30px;background:var(--ink);margin-left:4px;border-radius:2px}
.res{border-radius:14px;padding:14px 18px;display:grid;grid-template-columns:1fr auto;align-items:end;gap:4px 14px}
.res .lab{grid-column:1/-1}
.res .p{font:600 15px var(--mono);color:var(--ink2)}
"""
    toks = "".join(f'<span class="tok">{E(t)}</span>' for t in ["The", "␣capital", "␣of", "␣France", "␣is"])
    arrow = ('<svg width="50" height="24" viewBox="0 0 50 24"><path d="M2 12H44M36 4l9 8-9 8" fill="none" stroke="#0b0b0b" '
             'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    a = (f'<div class="card lane"><span class="tag" style="background:var(--blue)">A</span>'
         f'<div class="prompt">{toks}<span class="cur"></span></div>{arrow}'
         f'<div class="res" style="background:var(--btint);border:2px solid var(--blue)"><span class="lab">most likely next token</span>'
         f'<span class="tok">␣Paris</span><span class="big" style="color:#1d5fae">#5</span><span class="p">P = 3.2%</span><span class="p">rank</span></div></div>')
    b = (f'<div class="card lane" style="position:relative"><span class="tag" style="background:var(--orange)">B</span>'
         f'<div class="prompt">{toks}<span class="circ" style="margin-left:6px">{keycap("␣", w=60, h=44, marked=True)}</span><span class="cur"></span></div>{arrow}'
         f'<div class="res" style="background:var(--otint);border:2px solid var(--orange)"><span class="lab">the right answer now sits at</span>'
         f'<span class="tok odd">Paris</span><span class="big" style="color:#a8401a">#1,472</span><span class="p">P ≈ 0%</span><span class="p">rank</span></div>'
         f'<div class="note" style="position:absolute;left:470px;bottom:-30px;transform:rotate(-3deg)">one extra space</div></div>')
    body = a + b + '<div style="height:24px"></div>'
    page = figure(KICK, "One trailing space, two different questions",
                  "In GPT-2 the space belongs to the next word. Type it yourself and the model must predict a rare "
                  "no-space “Paris”. <strong>Rank 5 drops to rank 1,472.</strong>",
                  body, "GPT-2 (124M), next-token probabilities from the week 1 notebook. ␣ marks a space.", css)
    render(page, f"{OUT}/trailing-space.png")


def token_tax():
    css = TOK_CSS + """
.wrap2{display:grid;grid-template-columns:780px 1fr;gap:28px;align-items:center}
.receipt{background:#fff;padding:28px 30px 40px;font-family:var(--mono);position:relative;
  box-shadow:0 1px 0 var(--line),0 18px 30px -24px rgba(11,11,11,.45);
  -webkit-mask:linear-gradient(#000,#000) top/100% calc(100% - 14px) no-repeat,
  conic-gradient(from -45deg at bottom,#0000,#000 1deg 89deg,#0000 90deg) bottom/20px 14px repeat-x}
.rh{text-align:center;border-bottom:2px dashed #cfcec8;padding-bottom:14px;margin-bottom:10px}
.rh b{font:800 26px var(--display);letter-spacing:.02em}
.rh p{font:500 13px var(--mono);color:var(--ink2);margin-top:6px}
.li{display:grid;grid-template-columns:86px 1fr 52px 58px;align-items:center;gap:12px;padding:9px 0;border-bottom:1px dotted #dcdbd5;font-size:15px}
.li .n{font-weight:700;text-align:right}
.li .m{text-align:right;color:var(--ink2)}
.tiles{display:flex;flex-wrap:nowrap;gap:1px}
.tiles i{width:4px;height:16px;border-radius:1px;background:var(--blue)}
.li.base .tiles i{background:#c3c2b7}
.li.top .tiles i{background:var(--orange)}
.rf{display:flex;justify-content:space-between;padding-top:14px;font:600 13px var(--mono);color:var(--ink2)}
.call{display:flex;flex-direction:column;gap:12px}
.call .huge{font:800 120px/0.9 var(--display);letter-spacing:-.05em}
.call p{font:400 21px/1.4 var(--ui);color:var(--ink2)}
"""
    data = [("Hindi", 91, 5.4), ("Russian", 57, 3.4), ("Arabic", 50, 2.9), ("French", 30, 1.8),
            ("German", 28, 1.6), ("Chinese", 28, 1.6), ("English", 17, 1.0)]
    lines = "".join(
        f'<div class="li{" top" if l == "Hindi" else " base" if l == "English" else ""}"><span>{l}</span>'
        f'<span class="tiles">{"<i></i>" * n}</span><span class="n">{n}</span><span class="m">{m:.1f}×</span></div>'
        for l, n, m in data)
    receipt = (f'<div class="receipt"><div class="rh"><b>TOKEN RECEIPT</b><p>GPT-2 tokeniser · one sentence · seven languages</p></div>'
               f'{lines}<div class="rf"><span>1 tile = 1 token</span><span>× = cost vs English</span></div></div>')
    call = ('<div class="call"><span class="lab">same sentence, in Hindi</span>'
            '<span class="huge"><span class="circ">5.4×</span></span>'
            '<p>the tokens English needs. On a per-token API that means a bigger bill, and it fills the context window faster.</p>'
            '<div class="note" style="transform:rotate(-3deg)">same meaning, bigger bill</div></div>')
    page = figure(KICK, "The token tax",
                  "One sentence, translated into seven languages and run through GPT-2's tokeniser. "
                  "<strong>English costs 17 tokens; Hindi costs 91.</strong>",
                  f'<div class="wrap2">{receipt}{call}</div>',
                  "Same sentence in each language (the English one is 71 characters), GPT-2 tokeniser. From my notebook.", css)
    render(page, f"{OUT}/token-tax.png")


def _bar_row(tok, v, maxv=40, col="var(--blue)", circ=False):
    pill = f'<span class="tok" style="height:34px;font-size:15px">{tok}</span>'
    pct = f'<span class="circ">{v:.1f}%</span>' if circ else f"{v:.1f}%"
    return (f'<div style="display:grid;grid-template-columns:120px 1fr 70px;align-items:center;gap:12px;padding:6px 0">'
            f'<span style="justify-self:end">{pill}</span><div style="height:16px;border-radius:8px;background:#efeee9;overflow:hidden">'
            f'<i style="display:block;height:100%;width:{v / maxv * 100}%;background:{col};border-radius:8px"></i></div>'
            f'<span style="font:700 15px var(--mono);text-align:right">{pct}</span></div>')


def next_token_after_space():
    css = TOK_CSS + """
.two{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.pc{padding:22px;display:flex;flex-direction:column;gap:14px;position:relative}
.prompt{font:600 20px var(--mono);background:#f6f5f1;border-radius:12px;padding:12px 14px}
.gauge{display:grid;grid-template-columns:auto 1fr auto;gap:12px;align-items:center;font:400 16px var(--ui);color:var(--ink2)}
.gauge .t{height:10px;border-radius:5px;background:#efeee9;position:relative}
.gauge .t i{position:absolute;left:0;top:0;bottom:0;border-radius:5px}
.gauge b{font:700 15px var(--mono);color:var(--ink)}
"""
    sp = '<span class="sp">␣</span>'
    clean = [(f"{sp}the", 8.5), (f"{sp}now", 4.8), (f"{sp}a", 4.6), (f"{sp}France", 3.2), (f"{sp}Paris", 3.2), (f"{sp}in", 2.7)]
    trail = [("NBSP", 39.8), ("ét", 34.2), ("Â", 9.1), ("vern", 6.8), ("iced", 1.2), ("Ã", 0.7)]
    a = (f'<div class="card pc"><span class="lab">A · clean prompt</span><div class="prompt">The capital of France is</div>'
         f'<div class="gauge"><span>uncertainty</span><span class="t"><i style="width:{8.65 / 16 * 100}%;background:var(--blue)"></i></span><b>8.65 bits</b></div>'
         + "".join(_bar_row(t, v, col="var(--orange)" if "Paris" in t else "var(--blue)", circ="Paris" in t) for t, v in clean) +
         '<p style="font:400 16px var(--ui);color:var(--ink2)">Sensible English. “␣Paris” sits at rank 5.</p></div>')
    b = (f'<div class="card pc"><span class="lab">B · same prompt + trailing space</span><div class="prompt">The capital of France is<span style="color:var(--orange)">␣</span></div>'
         f'<div class="gauge"><span>uncertainty</span><span class="t"><i style="width:{2.55 / 16 * 100}%;background:var(--orange)"></i></span><b>2.55 bits</b></div>'
         + "".join(_bar_row(t, v, col="#c3c2b7") for t, v in trail) +
         '<p style="font:400 16px var(--ui);color:var(--ink2)">NBSP is a non-breaking space; “ét” follows a space inside French words.</p>'
         '<div class="note" style="position:absolute;right:26px;top:12px;transform:rotate(-3deg)">confident and wrong</div></div>')
    page = figure(KICK, "What GPT-2 expects next",
                  "The top six next tokens for each prompt, on the same scale. "
                  "<strong>After the trailing space the model is far more certain, and none of its guesses is Paris.</strong>",
                  f'<div class="two">{a}{b}</div>', "GPT-2 small (124M), softmax over the last position's logits, from the week 1 notebook. Uncertainty is entropy on a 0 to 16 bit scale.", css)
    render(page, f"{OUT}/next-token-after-space.png")


def token_splits():
    css = TOK_CSS + """
.rows{padding:10px 26px}
.r{display:grid;grid-template-columns:220px 50px minmax(0,1fr) 120px;align-items:center;gap:16px;padding:14px 0;border-bottom:1px solid var(--line)}
.r:last-child{border-bottom:0}
.typed{font:600 22px var(--mono);border:2px solid var(--ink);border-radius:10px;padding:8px 12px;background:#fff;white-space:pre}
.ts{display:flex;gap:6px;flex-wrap:wrap}
.cnt{font:800 28px var(--display);text-align:right}
.cnt small{font:400 15px var(--ui);color:var(--ink3);margin-left:4px}
"""
    rows = [("Hello", ["Hello"], 1), ("HELLO", ["HE", "LL", "O"], 3), ("1234567", ["123", "45", "67"], 3),
            ("2026", ["20", "26"], 2), ("········", ["␣"] * 8, 8)]
    out = []
    for typed, parts, n in rows:
        pills = "".join(f'<span class="tok">{E(x)}</span>' for x in parts)
        if typed == "1234567":
            pills = f'<span class="circ" style="display:flex;gap:6px">{pills}</span><span class="note" style="margin-left:34px;transform:rotate(-3deg)">chopped by frequency</span>'
        label = "8 spaces" if typed.startswith("·") else typed
        out.append(f'<div class="r"><span class="typed">{E(label)}</span>{arrow(44, 22)}<div class="ts" style="align-items:center">{pills}</div>'
                   f'<span class="cnt">{n}<small>{"token" if n == 1 else "tokens"}</small></span></div>')
    page = figure(KICK, "How GPT-2 splits what you type",
                  "Merges follow frequency in web text. <strong>Common forms become one token; everything else is chopped.</strong>",
                  f'<div class="card rows">{"".join(out)}</div>', "GPT-2 tokeniser, from the week 1 notebook. ␣ marks a space.", css)
    render(page, f"{OUT}/token-splits.png")


def emoji_bytes():
    css = TOK_CSS + """
.flow{display:grid;grid-template-columns:1fr 40px 1.2fr 40px 1.2fr 40px 1.3fr;align-items:stretch}
.s{padding:18px;display:flex;flex-direction:column;gap:12px;align-items:center;text-align:center;position:relative}
.s h3{font:700 17px/1.2 var(--head)}
.emo{font-size:84px;line-height:1}
.by{display:grid;grid-template-columns:repeat(2,1fr);gap:6px}
.b{border:1.5px solid #d6d5cf;border-radius:8px;background:#fff;padding:8px 12px;font:700 18px var(--mono)}
.pair{display:flex;gap:6px;border:2.5px solid var(--blue);background:var(--btint);border-radius:12px;padding:6px}
.pair .b{border-color:#a9c6ee}
.rep{font:700 30px var(--mono);border:2.5px solid var(--orange);background:var(--otint);border-radius:12px;width:62px;height:62px;display:grid;place-items:center;color:#a8401a}
.ar{display:flex;align-items:center;justify-content:center}
.p{font:400 16px/1.35 var(--ui);color:var(--ink2)}
"""
    ar = f'<div class="ar">{arrow(36, 22)}</div>'
    s1 = '<div class="card s"><span class="lab">you type</span><span class="emo">🙂</span><p class="p">one character</p></div>'
    s2 = ('<div class="card s"><span class="lab">UTF-8</span><h3>4 bytes</h3><div class="by">'
          + "".join(f'<span class="b">{b}</span>' for b in ["f0", "9f", "99", "82"]) + '</div></div>')
    s3 = ('<div class="card s"><span class="lab">GPT-2 tokens</span><h3>2 tokens of 2 bytes each</h3>'
          '<div style="display:flex;flex-direction:column;gap:10px"><div class="pair"><span class="b">f0</span><span class="b">9f</span></div>'
          '<div class="pair"><span class="b">99</span><span class="b">82</span></div></div><p class="p">no merge ever joined all four</p></div>')
    s4 = ('<div class="card s"><span class="lab">decode</span><h3>One token alone</h3>'
          '<span class="circ" style="display:flex;gap:8px"><span class="rep">�</span><span class="rep">�</span></span>'
          '<div class="note" style="transform:rotate(-3deg);margin-top:6px">half a character</div>'
          '<h3 style="margin-top:4px">Both together</h3><span class="emo" style="font-size:54px">🙂</span></div>')
    page = figure(KICK, "One emoji, four bytes, two tokens",
                  "GPT-2 holds 🙂 as two tokens of two bytes each. <strong>Half an emoji isn't a character, so decoding one token shows �.</strong> "
                  "The family emoji is 18 bytes and ten tokens the same way.",
                  f'<div class="flow">{s1}{ar}{s2}{ar}{s3}{ar}{s4}</div>', "GPT-2 tokeniser, from the week 1 notebook.", css)
    render(page, f"{OUT}/emoji-bytes.png")


def token_tax_evolution():
    css = TOK_CSS + """
.chart{padding:24px 30px 18px;position:relative}
.leg{display:flex;gap:24px;font:400 17px var(--ui);color:var(--ink2);margin-bottom:14px}
.leg span{display:flex;align-items:center;gap:8px}
.leg i{width:16px;height:16px;border-radius:50%}
.plot{position:relative;margin-left:110px;margin-right:30px}
.rw{position:relative;height:66px;border-bottom:1px dashed #e4e3dd}
.rw .lang{position:absolute;left:-110px;top:18px;font:600 18px var(--ui)}
.seg{position:absolute;top:27px;height:4px;background:#d6d5cf;border-radius:2px}
.d{position:absolute;top:18px;width:22px;height:22px;border-radius:50%;margin-left:-11px;border:2.5px solid #fff;box-shadow:0 0 0 1px rgba(0,0,0,.08)}
.v{position:absolute;top:-2px;font:700 12px var(--mono);color:var(--ink2);transform:translateX(-50%)}
.base{position:absolute;top:0;bottom:0;width:0;border-left:2px dashed var(--ink3)}
.axis{display:flex;justify-content:space-between;font:500 13px var(--mono);color:var(--ink3);margin-top:8px}
"""
    rows = [("Hindi", [91, 62, 16]), ("Russian", [57, 27, 16]), ("Arabic", [50, 35, 17]), ("French", [30, 18, 17]),
            ("German", [28, 19, 15]), ("Chinese", [28, 20, 12]), ("English", [17, 17, 17])]
    cols = ["#b9cff0", "#5b98e2", "#1d5fae"]
    X = lambda v: f"{v / 100 * 100}%"
    out = []
    for lang, vs in rows:
        lo, hi = min(vs), max(vs)
        dots = ""
        for i, v in enumerate(vs):
            circ = lang == "Hindi" and i == 2
            inner = f'<span class="d" style="left:{X(v)};background:{cols[i]}"></span>'
            if circ:
                inner += (f'<span style="position:absolute;left:{X(v)};top:9px;width:46px;height:40px;margin-left:-23px;border:3px solid var(--red);'
                          f'border-radius:50%;transform:rotate(-8deg)"></span>')
            if lang != "English" or i == 0:
                dots += inner + f'<span class="v" style="left:{X(v)};top:{44 if i == 2 else -2}px">{v}</span>'
            else:
                dots += inner
        out.append(f'<div class="rw"><span class="lang">{lang}</span><span class="seg" style="left:{X(lo)};width:{(hi - lo)}%"></span>{dots}</div>')
    legend = ('<div class="leg">' + "".join(f'<span><i style="background:{c}"></i>{n}</span>' for c, n in
              zip(cols, ["GPT-2 · 50k vocab", "GPT-4 · cl100k_base", "GPT-4o · o200k_base"])) + '</div>')
    plot = (f'<div class="plot"><span class="base" style="left:17%"></span>{"".join(out)}'
            f'<div class="axis"><span>0</span><span>25</span><span>50</span><span>75</span><span>100 tokens</span></div>'
            f'<div class="note" style="position:absolute;left:21%;top:-6px;transform:rotate(-3deg)">now below English</div></div>')
    page = figure(KICK, "Did newer tokenisers fix the token tax?",
                  "Same sentence, three vocabularies. English costs 17 tokens under all three (dashed line). "
                  "<strong>Hindi fell from 5.4× English to 3.6× to 0.9×.</strong>",
                  f'<div class="card chart">{legend}{plot}</div>',
                  "One sentence per language, token counts from tiktoken 0.8.0. Multipliers are against the same tokeniser's English count.", css)
    render(page, f"{OUT}/token-tax-evolution.png")


def data_gap():
    css = TOK_CSS + """
.venn{position:relative;height:440px}
.ring{position:absolute;top:30px;width:440px;height:400px;border-radius:50%}
.vec{display:flex;gap:3px}
.vec i{width:14px;height:22px;border-radius:3px}
.cap{font:400 17px/1.35 var(--ui);color:var(--ink2)}
"""
    vec = lambda cols: '<span class="vec">' + "".join(f'<i style="background:{c}"></i>' for c in cols) + "</span>"
    trained = vec(["#1d5fae", "#5b98e2", "#2a78d6", "#b9cff0", "#1d5fae", "#5b98e2"])
    untrained = vec(["#e4e3dd"] * 6)
    body = (f'<div class="venn">'
            f'<div class="ring" style="left:120px;background:rgba(42,120,214,.08);border:3px solid var(--blue)"></div>'
            f'<div class="ring" style="left:440px;background:rgba(11,11,11,.04);border:3px solid var(--ink2)"></div>'
            f'<div style="position:absolute;left:150px;top:0;font:700 16px var(--head);color:#1d5fae">Text the tokeniser was trained on</div>'
            f'<div style="position:absolute;left:660px;top:0;font:700 16px var(--head);color:var(--ink2)">Text the model was trained on</div>'
            f'<div style="position:absolute;left:175px;top:170px;display:flex;flex-direction:column;gap:10px;align-items:flex-start">'
            f'<span class="circ"><span class="tok odd">␣SolidGoldMagikarp</span></span>'
            f'<span class="cap">has an ID and an embedding row…</span>{untrained}<span class="cap">…that training never updated</span>'
            f'<div class="note" style="transform:rotate(-3deg)">a token with no meaning</div></div>'
            f'<div style="position:absolute;left:590px;top:185px;display:flex;flex-direction:column;gap:10px;align-items:center">'
            f'<span class="tok">␣Paris</span>{trained}<span class="cap">normal tokens,<br>seen by both</span></div></div>')
    page = figure(KICK, "Where glitch tokens come from",
                  "A tokeniser can learn a token from text the model never trains on. "
                  "<strong>The token gets an ID and an embedding, but nothing ever trains it.</strong>",
                  body, "Schematic. SolidGoldMagikarp is the best-known GPT-2 and GPT-3 glitch token.", css)
    render(page, f"{OUT}/data-gap.png")


def embedding_neighbours():
    css = TOK_CSS + """
.map{position:relative;height:420px;overflow:hidden;
 background-image:linear-gradient(#efeee9 1px,transparent 1px),linear-gradient(90deg,#efeee9 1px,transparent 1px);background-size:40px 40px}
.blob{position:absolute;border-radius:50%;background:rgba(42,120,214,.09);border:2px dashed #a9c6ee}
.pt{position:absolute;display:flex;flex-direction:column;align-items:center;gap:4px;transform:translate(-50%,-50%)}
.pt i{width:16px;height:16px;border-radius:50%;background:#fff;border:3px solid var(--blue)}
.pt.c i{background:var(--blue);width:20px;height:20px}
.pt.o i{background:var(--orange);border-color:var(--orange);width:20px;height:20px}
.pt span{font:600 17px var(--mono)}
.side{padding:20px;display:flex;flex-direction:column;gap:14px}
.tr{display:grid;grid-template-columns:100px 1fr;align-items:center;gap:10px;font:600 16px var(--mono)}
.tr .vec{display:flex;gap:3px}.tr .vec i{width:16px;height:24px;border-radius:3px}
"""
    def pt(x, y, label, kind=""):
        return f'<div class="pt {kind}" style="left:{x}px;top:{y}px"><i></i><span>{E(label)}</span></div>'
    m = (f'<div class="blob" style="left:40px;top:70px;width:300px;height:240px"></div>'
         f'<div class="blob" style="left:330px;top:150px;width:240px;height:200px"></div>'
         + pt(190, 180, "king", "c") + pt(105, 125, "queen") + pt(260, 120, "prince") + pt(250, 255, "monarch")
         + pt(450, 250, "7", "c") + pt(395, 200, "6") + pt(510, 205, "8") + pt(420, 310, "5")
         + pt(640, 110, "␣Paris", "o") + pt(700, 330, "Paris", "o")
         + '<svg style="position:absolute;left:0;top:0" width="800" height="420"><path d="M642 128 L698 312" stroke="#eb6834" stroke-width="2.5" stroke-dasharray="6 6"/></svg>'
         + '<div class="note" style="position:absolute;left:470px;top:60px;transform:rotate(-3deg)">two separate rows</div>')
    vec = lambda cols: '<span class="vec">' + "".join(f'<i style="background:{c}"></i>' for c in cols) + "</span>"
    side = (f'<div class="card side"><span class="lab">embedding table (excerpt)</span>'
            f'<div class="tr"><span>␣Paris</span>{vec(["#1d5fae", "#b9cff0", "#5b98e2", "#2a78d6", "#b9cff0", "#1d5fae", "#5b98e2"])}</div>'
            f'<div class="tr"><span>Paris</span>{vec(["#b9cff0", "#2a78d6", "#1d5fae", "#b9cff0", "#5b98e2", "#2a78d6", "#b9cff0"])}</div>'
            f'<p style="font:400 16px/1.4 var(--ui);color:var(--ink2)">Each of the 50,257 IDs maps to its own 768-number vector. '
            f'The model had to learn on its own that these two rows mean the same city.</p></div>')
    page = figure(KICK, "Where tokens become meaning",
                  "Nearest neighbours in GPT-2's embeddings: similar tokens end up close together. "
                  "<strong>“␣Paris” and “Paris” are two separate points.</strong>",
                  f'<div style="display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:20px"><div class="card map">{m}</div>{side}</div>',
                  "GPT-2 small token embeddings. Positions and vector colours are schematic.", css)
    render(page, f"{OUT}/embedding-neighbours.png")


FIGS = {"bpe-pipeline": bpe_pipeline, "trailing-space": trailing_space, "token-tax": token_tax,
        "next-token-after-space": next_token_after_space, "token-splits": token_splits, "emoji-bytes": emoji_bytes,
        "token-tax-evolution": token_tax_evolution, "data-gap": data_gap, "embedding-neighbours": embedding_neighbours}

if __name__ == "__main__":
    for name, fn in FIGS.items():
        if not ONLY or name in ONLY:
            fn()
            print("wrote", f"{OUT}/{name}.png")
