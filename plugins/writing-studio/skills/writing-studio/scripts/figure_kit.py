#!/usr/bin/env python3
"""Figure kit: editorial, illustrated article figures as HTML + inline SVG, rendered to PNG
with headless Chrome. Brand-driven: palette, fonts, wordmark and logo come from a brand file
(profiles/<name>.brand.json), so every profile gets its own look from the same parts.

    import figure_kit as k
    k.use_brand("profiles/jorshimayor.brand.json")
    page = k.figure("Series label", "Title", "Dek with <strong>the finding</strong>", body_html, "Source line")
    k.render(page, "images/my-figure.png")          # 2x PNG plus my-figure.html, its editable source

Parts: figure() frame (kicker, display title, dek, body, source, logo + wordmark), card / pill /
stamp / hl / circ / note CSS classes, and drawn objects: coins(), vault(), mini_vault(),
ticket(), avatar(), keycap(), arrow(), hand_arrow(), logo(). Rules: references/visuals.md.

Needs Google Chrome or Chromium (set CHROME=/path) and network access for the fonts. Pillow
is optional (crops the PNG to the figure).
"""
import html as _h
import json
import os
import re
import shutil
import subprocess
import tempfile

E = _h.escape
WIDTH = 1200                      # CSS px; rendered at 2x

DEFAULT_BRAND = {
    "wordmark": "", "logo": "", "logo_dark": "",
    "paper": "#fcfcfb", "ink": "#0b0b0b", "ink2": "#52514e", "ink3": "#8a8984",
    "blue": "#2a78d6", "blue_side": "#1d5fae", "blue_tint": "#eef3fb",
    "orange": "#eb6834", "orange_side": "#c4501f", "orange_tint": "#fdeee8",
    "ghost": "#b9b8b1", "highlight": "#ffe45c", "marker": "#d1203f",
    "font_display": '"Bricolage Grotesque",Inter,sans-serif', "font_head": '"Geist",Inter,Helvetica,sans-serif',
    "font_text": '"Newsreader","Times New Roman",Times,serif', "font_mono": '"JetBrains Mono",Menlo,monospace',
    "font_hand": '"Caveat",cursive',
    "google_fonts": ("https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..800"
                     "&family=Caveat:wght@600..700&family=Geist:wght@400..800&family=JetBrains+Mono:wght@400..700"
                     "&family=Newsreader:ital,opsz,wght@0,6..72,400..700;1,6..72,400..700&display=block"),
}
B = dict(DEFAULT_BRAND)
ATT = ATT_SIDE = ATT_TINT = VIC = VIC_SIDE = VIC_TINT = GHOST = FONTS = CSS = ""


def use_brand(path=None):
    """Load a brand file (JSON with any DEFAULT_BRAND keys). "logo" and "logo_dark" are paths
    to SVGs, relative to the brand file. Without a path, WRITING_STUDIO_BRAND is used if set."""
    global B, ATT, ATT_SIDE, ATT_TINT, VIC, VIC_SIDE, VIC_TINT, GHOST, FONTS, CSS
    path = path or os.environ.get("WRITING_STUDIO_BRAND")
    B = dict(DEFAULT_BRAND)
    if path:
        with open(path, encoding="utf-8") as fh:
            B.update(json.load(fh))
        for key in ("logo", "logo_dark"):
            if B.get(key):
                with open(os.path.join(os.path.dirname(os.path.abspath(path)), B[key]), encoding="utf-8") as fh:
                    B[f"_{key}_svg"] = re.sub(r"<\?xml[^>]*>|<title>.*?</title>", "", fh.read()).strip()
    # Owner colours inside illustrations: orange = the attacker / odd one, blue = victim / normal.
    ATT, ATT_SIDE, ATT_TINT = B["orange"], B["orange_side"], B["orange_tint"]
    VIC, VIC_SIDE, VIC_TINT = B["blue"], B["blue_side"], B["blue_tint"]
    GHOST = B["ghost"]
    FONTS = B["google_fonts"]
    CSS = _build_css()
    return B


def _chrome():
    for c in [os.environ.get("CHROME", ""), "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium", shutil.which("google-chrome") or "",
              shutil.which("chromium") or "", shutil.which("chromium-browser") or ""]:
        if c and os.path.exists(c):
            return c
    raise SystemExit("Chrome or Chromium not found. Set CHROME=/path/to/chrome.")


def shoot(html_path, png_path, w, h, scale=1):
    """Screenshot a local HTML file at w x h CSS pixels with headless Chrome."""
    with tempfile.TemporaryDirectory() as prof:
        subprocess.run([_chrome(), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                        "--no-default-browser-check", f"--user-data-dir={prof}", f"--force-device-scale-factor={scale}",
                        f"--window-size={w},{h}", "--virtual-time-budget=8000",
                        f"--screenshot={os.path.abspath(png_path)}", "file://" + os.path.abspath(html_path)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, timeout=180)
    return png_path


def _build_css():
    return f"""
:root{{--paper:{B["paper"]};--ink:{B["ink"]};--ink2:{B["ink2"]};--ink3:{B["ink3"]};--line:#e4e3dd;--card:#ffffff;
--blue:{B["blue"]};--orange:{B["orange"]};--hl:{B["highlight"]};--red:{B["marker"]};--btint:{VIC_TINT};--otint:{ATT_TINT};
--display:{B["font_display"]};--head:{B["font_head"]};--ui:{B["font_text"]};--mono:{B["font_mono"]};--hand:{B["font_hand"]}}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{WIDTH}px;background:#ff00ff}}
body{{font-family:var(--ui);color:var(--ink);-webkit-font-smoothing:antialiased}}
.fig{{width:{WIDTH}px;padding:44px 52px 30px;background:var(--paper);
  background-image:radial-gradient(#e6e5df 1.1px,transparent 1.3px);background-size:22px 22px;background-position:11px 11px}}
.kicker{{display:flex;align-items:center;gap:10px;font:600 13px/1 var(--mono);letter-spacing:.12em;text-transform:uppercase;color:var(--ink2)}}
.kicker i{{width:9px;height:9px;border-radius:50%;border:2.5px solid var(--blue);display:inline-block}}
.kicker b{{flex:none;width:28px;height:2px;background:#c3c2b7}}
h1{{font:800 44px/1.02 var(--display);letter-spacing:-.035em;margin-top:14px;max-width:1000px;text-wrap:balance}}
.dek{{font:400 21px/1.42 var(--ui);color:var(--ink2);margin-top:12px;max-width:900px;text-wrap:pretty}}
.dek strong{{color:var(--ink);font-weight:600}}
.body{{margin-top:30px}}
.foot{{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;margin-top:28px;padding-top:14px;border-top:1px solid var(--line)}}
.src{{font:400 15px/1.45 var(--ui);color:var(--ink3);max-width:900px}}
.wm{{font:800 17px/1 var(--display);letter-spacing:-.03em;color:var(--ink)}}
.wm span{{background:linear-gradient(transparent 58%,var(--hl) 58%,var(--hl) 92%,transparent 92%)}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:18px;box-shadow:0 1px 0 var(--line),0 12px 28px -22px rgba(11,11,11,.35)}}
.mono{{font-family:var(--mono)}}
.hl{{background:linear-gradient(100deg,transparent 1%,var(--hl) 3%,var(--hl) 97%,transparent 99%) 0 70%/100% 42% no-repeat;padding:0 .08em;-webkit-box-decoration-break:clone}}
.circ{{position:relative;display:inline-block}}
.circ::before,.circ::after{{content:"";position:absolute;inset:-12px -14px;border:3px solid var(--red);border-radius:50%;transform:rotate(-4deg);pointer-events:none}}
.circ::after{{inset:-9px -17px;transform:rotate(3deg);opacity:.7}}
.note{{font:700 28px/1 var(--hand);color:var(--red);white-space:nowrap}}
.pill{{display:inline-flex;align-items:center;gap:6px;font:600 13px/1 var(--mono);padding:7px 10px;border-radius:999px;border:1.5px solid var(--line);background:#fff;white-space:nowrap}}
.pill.att{{border-color:var(--orange);background:var(--otint);color:#a8401a}}
.pill.vic{{border-color:var(--blue);background:var(--btint);color:#1d5fae}}
.pill.ok{{border-color:#1baf7a;background:#e8f7f1;color:#0f7a54}}
.stamp{{display:inline-block;font:800 15px/1 var(--display);letter-spacing:.06em;text-transform:uppercase;padding:8px 12px;border:2.5px solid currentColor;border-radius:8px;transform:rotate(-4deg)}}
"""


def logo(size=28, dark=False):
    """The brand's logo from the brand file (an SVG with a square viewBox), or nothing.
    dark=True uses "logo_dark" (for ink backgrounds) when the brand has one."""
    svg = (B.get("_logo_dark_svg") if dark else "") or B.get("_logo_svg", "")
    if not svg:
        return ""
    return re.sub(r"<svg\b", f'<svg width="{size}" height="{size}" style="display:block" aria-hidden="true"', svg, count=1)


def figure(kicker, title, dek, body, source, extra_css=""):
    return (f'<!doctype html><html lang="en-GB"><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}">'
            f'<style>{CSS}{extra_css}</style><div class="fig" id="fig">'
            f'<div class="kicker"><i></i><b></b>{E(kicker)}</div><h1>{title}</h1><p class="dek">{dek}</p>'
            f'<div class="body">{body}</div>'
            f'<div class="foot"><p class="src">{source}</p><div class="wm" style="display:flex;align-items:center;gap:8px">{logo(30)}<span>{E(B["wordmark"])}</span></div></div></div></html>')


def render(page, png, height=1600):
    """Write the page next to the PNG (as <name>.html, the editable source), screenshot it at 2x
    on a magenta page, and crop to where the figure ends (needs Pillow; without it the PNG keeps
    the full height)."""
    src = os.path.splitext(png)[0] + ".html"
    os.makedirs(os.path.dirname(png) or ".", exist_ok=True)
    with open(src, "w", encoding="utf-8") as fh:
        fh.write(page)
    shoot(src, png, WIDTH, height, scale=2)
    try:
        from PIL import Image
    except ImportError:
        return png
    im = Image.open(png).convert("RGB")
    w, h = im.size
    px = im.load()
    bottom = h
    for y in range(h - 1, 0, -1):
        r, g, b = px[w // 2, y]
        if not (r > 240 and g < 20 and b > 240):
            bottom = y + 1
            break
    im.crop((0, 0, w, bottom)).save(png, optimize=True)
    return png


# ---------------------------------------------------------------- illustrations (inline SVG)

def coins(n, color="vic", w=54, step=10, ghost=False):
    """A stack of n coins, bottom-up. n can be fractional for a sliver (1 wei)."""
    face, side = (VIC, VIC_SIDE) if color == "vic" else (ATT, ATT_SIDE)
    if ghost:
        face, side = "#fff", GHOST
    count = max(1, round(n)) if n >= 0.5 else 0
    h = step * count + 18 if count else 14
    out = [f'<svg width="{w + 4}" height="{h}" viewBox="0 0 {w + 4} {h}" style="display:block">']
    if not count:                                   # a single sliver, for 1 wei
        out.append(f'<ellipse cx="{w / 2 + 2}" cy="{h - 6}" rx="{w / 2 - 14}" ry="3.5" fill="{face}" stroke="{side}" stroke-width="1.5"/>')
    for i in range(count):
        y = h - 10 - i * step
        dash = ' stroke-dasharray="3 3"' if ghost else ""
        out.append(f'<path d="M2 {y - 4} v{step - 3} a{w / 2} 5 0 0 0 {w} 0 v-{step - 3}" fill="{side}"{dash} stroke="{B["ink"]}" stroke-width="1.2"/>')
        out.append(f'<ellipse cx="{w / 2 + 2}" cy="{y - 4}" rx="{w / 2}" ry="5" fill="{face}" stroke="{B["ink"]}" stroke-width="1.2"{dash}/>')
        out.append(f'<ellipse cx="{w / 2 + 2}" cy="{y - 4}" rx="{w / 2 - 8}" ry="2.6" fill="none" stroke="rgba(255,255,255,.6)" stroke-width="1.2"/>')
    out.append("</svg>")
    return "".join(out)


def vault(stacks, label="VAULT", w=230, h=210, note_html="", outside=""):
    """A safe seen from the front, with a glass window showing coin stacks.
    stacks: list of coins() SVG strings; outside: HTML placed to the right of the safe."""
    inner = "".join(f'<div style="display:flex;flex-direction:column;justify-content:flex-end">{s}</div>' for s in stacks)
    return (f'<div style="display:flex;align-items:flex-end;gap:14px">'
            f'<div style="position:relative;width:{w}px;height:{h}px">'
            f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="position:absolute;inset:0">'
            f'<rect x="3" y="3" width="{w - 6}" height="{h - 16}" rx="18" fill="#fff" stroke="{B["ink"]}" stroke-width="3"/>'
            f'<rect x="16" y="34" width="{w - 62}" height="{h - 62}" rx="10" fill="#f3f2ee" stroke="{B["ink"]}" stroke-width="2"/>'
            f'<circle cx="{w - 24}" cy="{h / 2 + 4}" r="11" fill="#fff" stroke="{B["ink"]}" stroke-width="2.5"/>'
            f'<path d="M{w - 24} {h / 2 + 4} l6 -6" stroke="{B["ink"]}" stroke-width="2.5" stroke-linecap="round"/>'
            f'<circle cx="{w - 24}" cy="{h / 2 + 4}" r="2.5" fill="{B["ink"]}"/>'
            f'<rect x="20" y="{h - 14}" width="26" height="10" rx="3" fill="{B["ink"]}"/><rect x="{w - 46}" y="{h - 14}" width="26" height="10" rx="3" fill="{B["ink"]}"/>'
            f'<text x="18" y="24" font-family="JetBrains Mono" font-weight="700" font-size="11" letter-spacing="2" fill="{B["ink"]}">{E(label)}</text>'
            f'</svg>'
            f'<div style="position:absolute;left:22px;bottom:34px;width:{w - 74}px;height:{h - 74}px;display:flex;align-items:flex-end;justify-content:center;gap:4px;overflow:hidden">{inner}</div>'
            f'{note_html}</div>{outside}</div>')


def ticket(text, kind="vic", w=128, empty=False, sub=""):
    """A share ticket with notched ends. kind: vic, att, ghost. empty draws a dashed, torn ticket."""
    stroke, fill, col = {"vic": (VIC, VIC_TINT, "#1d5fae"), "att": (ATT, ATT_TINT, "#a8401a"),
                         "ghost": (GHOST, "#fff", B["ink3"])}[kind]
    dash = ' stroke-dasharray="6 5"' if empty else ""
    h = 58
    path = f"M4 2 H{w - 4} V{h / 2 - 9} a9 9 0 0 0 0 18 V{h - 2} H4 V{h / 2 + 9} a9 9 0 0 0 0 -18 Z"
    s = (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="display:block">'
         f'<path d="{path}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"{dash}/>'
         f'<line x1="{w - 22}" y1="8" x2="{w - 22}" y2="{h - 8}" stroke="{stroke}" stroke-width="1.5" stroke-dasharray="3 4"/>'
         f'<text x="{(w - 22) / 2 + 6}" y="{h / 2 + 5}" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="14" fill="{col}">{E(text)}</text>'
         f'</svg>')
    if sub:
        s += f'<div style="font:500 12px var(--ui);color:var(--ink3);margin-top:4px;text-align:center">{E(sub)}</div>'
    return f'<div style="display:inline-block">{s}</div>'


def avatar(kind, label=None, size=46):
    """Attacker (hood and eye mask, orange ring) or victim (plain, blue ring)."""
    ring = ATT if kind == "att" else VIC
    if kind == "att":
        face = (f'<path d="M9 40 C9 18 17 9 23 9 C29 9 37 18 37 40 Z" fill="{B["ink"]}"/>'
                f'<circle cx="23" cy="24" r="9.5" fill="#f1d3bf"/>'
                f'<rect x="13" y="20" width="20" height="6" rx="3" fill="{B["ink"]}"/>'
                f'<circle cx="19" cy="23" r="1.6" fill="#fff"/><circle cx="27" cy="23" r="1.6" fill="#fff"/>')
    else:
        face = (f'<circle cx="23" cy="19" r="8.5" fill="#f1d3bf"/><path d="M18 14 q5 -6 11 0" stroke="{B["ink"]}" stroke-width="3" fill="none"/>'
                f'<path d="M8 42 C9 30 16 28 23 28 C30 28 37 30 38 42 Z" fill="{VIC}"/>')
    svg = (f'<svg width="{size}" height="{size}" viewBox="0 0 46 46" style="display:block">'
           f'<clipPath id="c{kind}"><circle cx="23" cy="23" r="21"/></clipPath>'
           f'<circle cx="23" cy="23" r="21.5" fill="#fff" stroke="{ring}" stroke-width="3"/>'
           f'<g clip-path="url(#c{kind})">{face}</g></svg>')
    if label is None:
        return svg
    return (f'<div style="display:inline-flex;align-items:center;gap:8px">{svg}'
            f'<span style="font:600 14px var(--ui);color:var(--ink)">{E(label)}</span></div>')


def keycap(label, w=86, h=56, marked=False):
    col = B["orange"] if marked else B["ink"]
    return (f'<svg width="{w}" height="{h + 6}" viewBox="0 0 {w} {h + 6}" style="display:block">'
            f'<rect x="2" y="6" width="{w - 4}" height="{h - 2}" rx="10" fill="#d9d8d3"/>'
            f'<rect x="2" y="2" width="{w - 4}" height="{h - 6}" rx="10" fill="#fff" stroke="{col}" stroke-width="2.5"/>'
            f'<text x="{w / 2}" y="{h / 2 + 4}" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="18" fill="{col}">{E(label)}</text></svg>')


def arrow(w=60, h=24, color=None, label=""):
    color = color or B["ink"]
    lab = f'<div style="font:600 12px var(--mono);color:var(--ink3);text-align:center;margin-bottom:4px">{E(label)}</div>' if label else ""
    return (f'<div style="display:flex;flex-direction:column;align-items:center">{lab}<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<path d="M2 {h / 2} H{w - 6}" stroke="{color}" stroke-width="2.5" stroke-linecap="round"/>'
            f'<path d="M{w - 14} {h / 2 - 7} L{w - 4} {h / 2} L{w - 14} {h / 2 + 7}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')


def hand_arrow(w=70, h=50, flip=False, up=False):
    """A curved marker-red arrow; default goes from bottom-right to top-left."""
    d = f"M{w - 4} {h - 4} C {w * 0.6} {h - 6}, {w * 0.25} {h * 0.6}, 8 10"
    head = "M8 10 l3 14 M8 10 l14 2"
    tf = ' transform="scale(-1,1)" transform-origin="center"' if flip else ""
    tf += ' style="transform:scaleY(-1)"' if up else ""
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"{tf}><path d="{d} {head}" fill="none" stroke="{B["marker"]}" '
            f'stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def mini_vault(size=34, color=None):  # noqa: D401
    """A small safe icon for tables and lists."""
    c = color or B["ink"]
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 34 34" style="display:block">'
            f'<rect x="3" y="3" width="28" height="24" rx="5" fill="#fff" stroke="{c}" stroke-width="2.5"/>'
            f'<rect x="7" y="8" width="13" height="14" rx="2.5" fill="#f3f2ee" stroke="{c}" stroke-width="1.8"/>'
            f'<circle cx="25.5" cy="15" r="3" fill="none" stroke="{c}" stroke-width="1.8"/>'
            f'<rect x="6" y="27" width="6" height="4" rx="1.5" fill="{c}"/><rect x="22" y="27" width="6" height="4" rx="1.5" fill="{c}"/></svg>')


use_brand()
