#!/usr/bin/env python3
"""Score a Markdown draft against on-page SEO, linking and style rules.

Standard library only. Usage:

    python3 seo_check.py article.md --keyword "bare metal server" \
        --secondary "dedicated server, single-tenant" --site example.com

Options:
    --keyword     primary keyword (required)
    --secondary   comma-separated secondary keywords
    --site        your domain(s), comma-separated, used to tell internal links
                  from external ones (e.g. "example.com, example.substack.com")
    --spelling    american | british: flag words spelled the other way
                  (defaults to american when --strict is set)
    --strict      apply the strict house style (spelling, title case, unit
                  spacing, no bold emphasis, no "Conclusion" heading)
    --meta        meta description to check
    --seo-title   SEO title tag to check (defaults to the H1)
    --check-links send a request to every link and report broken ones
    --json        machine-readable output

Exit code is 1 when any check fails, so it can gate a publish step.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import struct
import subprocess
import sys
from collections import defaultdict
from urllib.parse import urlparse

PASS, WARN, FAIL, INFO = "pass", "warn", "fail", "info"
ICON = {PASS: "✔", WARN: "⚠", FAIL: "✘", INFO: "•"}

GENERIC_ANCHORS = {"click here", "here", "read more", "this", "this link", "link", "more",
                   "learn more", "this article", "this page", "find out more", "see more"}
FILLER = ["it is important to note", "it's important to note", "it is worth noting", "it's worth noting",
          "basically", "essentially", "in simple terms", "in other words", "at the end of the day",
          "in order to", "in today's", "ever-evolving", "ever-changing", "fast-paced world",
          "dynamic world", "evolving world", "digital age", "let's dive", "dive into", "delve",
          "unlock the power", "harness the power", "look no further", "without further ado",
          "needless to say", "due to the fact that", "in the event that", "prior to", "subsequent to"]
HYPE = ["robust", "seamless", "seamlessly", "cutting-edge", "revolutionary", "game-changing", "game changer",
        "game-changer", "world-class", "next-generation", "unparalleled", "best-in-class",
        "state-of-the-art", "supercharge", "skyrocket", "unleash", "elevate your"]
SUPERLATIVES = ["fastest", "cheapest", "most powerful", "most secure", "easiest", "superior"]
ABSOLUTES = ["always", "never", "guaranteed", "impossible", "completely", "entirely"]
BRITISH = {"organisation": "organization", "organisations": "organizations", "optimise": "optimize",
           "optimised": "optimized", "optimising": "optimizing", "optimisation": "optimization",
           "virtualisation": "virtualization", "analyse": "analyze", "analysed": "analyzed",
           "analysing": "analyzing", "defence": "defense", "licence": "license", "centre": "center",
           "centres": "centers", "modelling": "modeling", "labelling": "labeling", "colour": "color",
           "behaviour": "behavior", "favour": "favor", "favourite": "favorite", "utilise": "utilize",
           "prioritise": "prioritize", "customise": "customize", "minimise": "minimize",
           "maximise": "maximize", "realise": "realize", "recognise": "recognize", "summarise": "summarize",
           "standardise": "standardize", "initialise": "initialize", "authorise": "authorize",
           "catalogue": "catalog", "travelling": "traveling", "cancelled": "canceled"}
# Words whose British form is also valid in American text (or vice versa) are left out.
AMERICAN = {v: k for k, v in BRITISH.items() if v not in {"license", "program"}}
SMALL_WORDS = {"a", "an", "the", "and", "but", "or", "nor", "for", "so", "yet", "as", "at", "by",
               "in", "of", "on", "to", "up", "via", "vs", "vs.", "with", "from", "into", "onto", "per"}
# Terms that are spelled more than one way. Mixing forms in one piece looks careless.
VARIANTS = [("onchain", "on-chain", "on chain"), ("offchain", "off-chain", "off chain"),
            ("zk-snark", "zksnark", "zk snark"), ("zk-stark", "zkstark", "zk stark"),
            ("zkevm", "zk-evm"), ("rollup", "roll-up"), ("fine-tuning", "fine tuning", "finetuning"),
            ("dataset", "data set"), ("email", "e-mail"), ("frontend", "front-end"), ("backend", "back-end"),
            ("codebase", "code base"), ("blockchain", "block chain")]
CASE_VARIANTS = [("Web3", "web3"), ("Web2", "web2"), ("dApp", "dapp", "Dapp", "DApp")]


def proper_term(w):
    """Mixed-case or numbered technical terms (zk-SNARK, zkVM, dApp, ERC-20) keep their own casing."""
    return any(c.isupper() for c in w[1:]) or bool(re.search(r"\d", w))


def uncapitalized(text):
    """Words (or halves of hyphenated words) that start lowercase, ignoring proper technical terms."""
    out = []
    for w in re.findall(r"[A-Za-z][\w'’\-]*(?:\.[A-Za-z]\w*)*", text):
        if proper_term(w):
            continue
        if any(part and part[0].islower() for part in w.split("-")):
            out.append(w)
    return out


UNITS = r"(?:KB|MB|GB|TB|PB|Kbps|Mbps|Gbps|Tbps|MHz|GHz|ms|GiB|TiB|MiB)"


# --------------------------------------------------------------------------- parsing
def strip_front_matter(text):
    meta = {}
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            for line in text[4:end].splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip().lower()] = v.strip().strip('"\'')
            text = text[end + 4:]
    return meta, text


def remove_code(text):
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "CODE", text)


def parse(text):
    meta, body = strip_front_matter(text)
    body_nocode = remove_code(body)
    headings = [(len(m.group(1)), m.group(2).strip(), m.start())
                for m in re.finditer(r"^(#{1,6})\s+(.+?)\s*#*\s*$", body_nocode, flags=re.M)]
    images = [(m.group(1), m.group(2)) for m in re.finditer(r"!\[([^\]]*)\]\(([^)\s]+)[^)]*\)", body_nocode)]
    images += [(alt, src) for src, alt in re.findall(r'<img[^>]*src="([^"]+)"[^>]*alt="([^"]*)"', body_nocode)]
    links = [(m.group(1).strip(), m.group(2)) for m in re.finditer(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)[^)]*\)", body_nocode)]

    blocks = [b.strip() for b in re.split(r"\n\s*\n", body_nocode) if b.strip()]
    paragraphs = []
    for b in blocks:
        first = b.lstrip()
        if first.startswith(("#", "|", "!", ">", "<", "- ", "* ", "+ ")) or re.match(r"^\d+[.)]\s", first):
            continue
        paragraphs.append(b)

    prose = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", body_nocode)
    prose = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", prose)
    prose = re.sub(r"<[^>]+>", " ", prose)
    prose = re.sub(r"^#{1,6}\s+", "", prose, flags=re.M)
    prose = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", prose, flags=re.M)
    prose = re.sub(r"[*_|>]", " ", prose)
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-.]*[A-Za-z0-9]|[A-Za-z0-9]", prose)
    h1 = next((t for lvl, t, _ in headings if lvl == 1), meta.get("title"))
    body_only = re.sub(r"^#{1,6}\s+.*$", " ", body_nocode, flags=re.M)
    body_only = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", body_only)
    lead_words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-.]*[A-Za-z0-9]|[A-Za-z0-9]", body_only)
    return dict(meta=meta, body=body_nocode, headings=headings, images=images, links=links,
                paragraphs=paragraphs, prose=prose, words=words, lead_words=lead_words, h1=h1)


def kw_pattern(phrase):
    toks = [re.escape(t) for t in re.split(r"[\s\-]+", phrase.lower().strip()) if t]
    return re.compile(r"\b" + r"[\s\-]+".join(t + r"(?:s|es)?" for t in toks) + r"\b", re.I)


def is_variation(text, phrase):
    """All keyword tokens present (any order, simple plural/stem tolerance)."""
    low = text.lower()
    return all(re.search(r"\b" + re.escape(t[:max(4, len(t) - 2)]), low)
               for t in re.split(r"[\s\-]+", phrase.lower()) if t)


def sentences(text):
    flat = re.sub(r"\s+", " ", text)
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z\"“(])", flat) if s.strip()]


def section_text(doc, index):
    """Body text from heading `index` to the next heading of the same or higher level."""
    hs = doc["headings"]
    lvl, _, start = hs[index]
    end = next((p for l, _, p in hs[index + 1:] if l <= lvl), len(doc["body"]))
    return doc["body"][start:end]


def image_info(path):
    try:
        with open(path, "rb") as f:
            head = f.read(64 * 1024)
        size = os.path.getsize(path)
        if head[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = struct.unpack(">II", head[16:24]); return size, w, h
        if head[:2] == b"\xff\xd8":
            i = 2
            while i < len(head) - 9:
                if head[i] != 0xFF: i += 1; continue
                marker, seg = head[i + 1], struct.unpack(">H", head[i + 2:i + 4])[0]
                if marker in (0xC0, 0xC1, 0xC2):
                    h, w = struct.unpack(">HH", head[i + 5:i + 9]); return size, w, h
                i += 2 + seg
        return size, None, None
    except OSError:
        return None


def link_status(url):
    try:
        out = subprocess.run(["curl", "-s", "-o", "/dev/null", "-L", "-m", "15", "-A", "Mozilla/5.0",
                              "-w", "%{http_code}", url], capture_output=True, text=True, timeout=20)
        return int(out.stdout or 0)
    except Exception:
        return 0


# --------------------------------------------------------------------------- checks
def run(doc, a):
    R = []
    add = lambda group, status, msg: R.append((group, status, msg))
    kw = a.keyword
    kp = kw_pattern(kw)
    words = doc["words"]; n = len(words) or 1
    h2s = [(i, t) for i, (l, t, _) in enumerate(doc["headings"]) if l == 2]

    # ---- keyword placement
    G = "Keyword placement"
    first50 = " ".join(doc["lead_words"][:50])  # body text only: the H1 does not count
    add(G, PASS if kp.search(first50) else (WARN if doc["paragraphs"] and kp.search(doc["paragraphs"][0]) else FAIL),
        f'Primary keyword in the first 50 words ("{kw}")')
    if h2s:
        first_h2_var = is_variation(h2s[0][1], kw)
        add(G, PASS if first_h2_var else FAIL, f'Keyword or a close variation in the first H2: "{h2s[0][1]}"')
        others = sum(is_variation(t, kw) for _, t in h2s[1:])
        add(G, PASS if others >= 1 else FAIL, f"Keyword variation in other H2s: {others} (target 1 to 2)")
        sec = section_text(doc, h2s[0][0])
        paras = [p for p in re.split(r"\n\s*\n", sec)[1:] if p.strip() and not p.lstrip().startswith(("#", "!", "|"))]
        add(G, PASS if paras and (kp.search(paras[0]) or is_variation(paras[0], kw)) else FAIL,
            "Keyword in the first paragraph under the first H2")
        last = section_text(doc, h2s[-1][0])
        add(G, PASS if kp.search(last) or is_variation(last, kw) else FAIL,
            f'Keyword in the closing section ("{h2s[-1][1]}")')
    else:
        add(G, FAIL, "No H2 headings found")
    hits = [m.start() for m in kp.finditer(doc["prose"])]
    density = 100 * len(hits) / n
    status = PASS if 1 <= density <= 2 else (WARN if 0.6 <= density <= 2.6 else FAIL)
    add(G, status, f"Primary density {density:.2f}% ({len(hits)} uses in {n} words, target 1% to 2%)")
    if hits:
        L = len(doc["prose"])
        thirds = {min(2, int(3 * h / L)) for h in hits}
        add(G, PASS if len(thirds) == 3 else WARN, "Primary keyword spread through the start, middle and end"
            if len(thirds) == 3 else f"Primary keyword only appears in {len(thirds)} of 3 thirds of the article")
    for s in [x.strip() for x in (a.secondary or "").split(",") if x.strip()]:
        c = len(kw_pattern(s).findall(doc["prose"])); d = 100 * c / n
        in_heads = sum(is_variation(t, s) for l, t, _ in doc["headings"] if l in (2, 3))
        st = PASS if 0.5 <= d <= 1 and in_heads else WARN
        add(G, st, f'Secondary "{s}": {d:.2f}% ({c} uses, target 0.5% to 1%), in {in_heads} H2/H3')

    # ---- structure
    G = "Structure"
    h1s = [t for l, t, _ in doc["headings"] if l == 1]
    add(G, PASS if len(h1s) <= 1 else FAIL, f"Single H1 ({len(h1s)} found)")
    prev, skips = 1, []
    for l, t, _ in doc["headings"]:
        if l > prev + 1: skips.append(f'H{prev}→H{l} at "{t}"')
        prev = l
    add(G, PASS if not skips else FAIL, "Heading levels never skip" if not skips else "Skipped levels: " + "; ".join(skips))
    add(G, INFO, f"{n} words, {len(h2s)} H2s, {sum(l == 3 for l, _, _ in doc['headings'])} H3s")
    if h2s:
        q = sum(t.rstrip().endswith("?") for _, t in h2s)
        add(G, INFO, f"{q} of {len(h2s)} H2s are phrased as reader questions")
    long_paras = [p for p in doc["paragraphs"] if len(sentences(p)) > 4]
    add(G, PASS if not long_paras else WARN, f"Paragraphs over 4 sentences: {len(long_paras)}"
        + (f' (first: "{long_paras[0][:70]}...")' if long_paras else ""))
    long_sents = [s for p in doc["paragraphs"] for s in sentences(p) if len(s.split()) > 35]
    add(G, PASS if not long_sents else WARN, f"Sentences over 35 words: {len(long_sents)}"
        + (f' (first: "{long_sents[0][:70]}...")' if long_sents else ""))
    if re.search(r"\bin this (?:article|guide|post|piece),? (?:we|you|i)(?:'ll| will)\b", doc["prose"], re.I):
        add(G, WARN, 'Intro announces the structure ("In this article, we will..."). Imply the roadmap instead')

    # ---- links
    G = "Links"
    sites = [x.strip().lower().removeprefix("www.") for x in (a.site or "").split(",") if x.strip()]
    internal, external = [], []
    for text, url in doc["links"]:
        parsed = urlparse(url)
        host, path = parsed.netloc.lower().removeprefix("www."), parsed.path
        mine = any(host == s or host.endswith("." + s) or (s.startswith(host) and (host + path).startswith(s)) for s in sites if host)
        (internal if (not host and not url.startswith("#")) or mine else external).append((text, url))
    per_k = 1000 * len(internal) / n
    # Short articles: 3 to 5 links in total. Longer ones: 3 to 5 per 1,000 words.
    ok = 3 <= len(internal) <= 5 if n < 1000 else (3 <= len(internal) and 2.5 <= per_k <= 5.5)
    st = PASS if ok else (WARN if len(internal) >= 2 else FAIL)
    add(G, st, f"Internal links: {len(internal)} ({per_k:.1f} per 1,000 words, target 3 to 5)"
        + ("" if sites else ". Pass --site to classify links"))
    add(G, PASS if 1 <= len(external) <= 3 else WARN, f"External authoritative links: {len(external)} (target 1 to 3)")
    generic = [t for t, _ in doc["links"] if t.lower().strip(" .") in GENERIC_ANCHORS]
    add(G, PASS if not generic else FAIL, "Anchor text is descriptive" if not generic else f"Generic anchors: {generic}")
    by_anchor = defaultdict(set)
    for t, u in doc["links"]: by_anchor[t.lower()].add(u)
    dup = [t for t, us in by_anchor.items() if len(us) > 1]
    add(G, PASS if not dup else WARN, "No anchor text points to two different URLs" if not dup else f"Same anchor, different URLs: {dup}")
    cannibal = [t for t, _ in internal if kp.fullmatch(t.strip())]
    add(G, PASS if not cannibal else FAIL, "Primary keyword is not used as an internal anchor"
        if not cannibal else f"Primary keyword used as internal anchor (cannibalization risk): {cannibal}")
    if doc["links"]:
        first_pos = doc["prose"].find(doc["links"][0][0])
        add(G, INFO, f"First link appears {100 * first_pos / max(1, len(doc['prose'])):.0f}% into the article")
    if a.check_links:
        bad = [(u, c) for _, u in doc["links"] if u.startswith("http") for c in [link_status(u)] if not 200 <= c < 400]
        add(G, PASS if not bad else FAIL, "No broken links" if not bad else f"Broken or unreachable: {bad}")
    else:
        add(G, INFO, "Broken links not checked (add --check-links)")

    # ---- images
    G = "Images"
    if doc["images"]:
        no_alt = [s for alt, s in doc["images"] if not alt.strip()]
        add(G, PASS if not no_alt else FAIL, "Every image has alt text" if not no_alt else f"Missing alt text: {no_alt}")
        kw_alt = sum(bool(kp.search(alt) or is_variation(alt, kw)) for alt, _ in doc["images"])
        add(G, PASS if kw_alt else WARN, f"Images with the keyword in alt text: {kw_alt} of {len(doc['images'])}")
        base = os.path.dirname(os.path.abspath(a.file))
        for alt, src in doc["images"]:
            if src.startswith("http"): continue
            info = image_info(os.path.join(base, src))
            if not info: add(G, WARN, f"Image not found locally: {src}"); continue
            size, w, h = info
            add(G, PASS if size <= 300_000 else WARN, f"{src}: {size / 1024:.0f} KB" + (" (compress to under 300 KB)" if size > 300_000 else ""))
            if a.strict and w and w != 1440:
                add(G, WARN, f"{src}: {w}x{h} px. Screenshots should be 1440 px wide (900 px tall by default)")
    else:
        add(G, WARN, "No images. Add at least one with descriptive alt text")

    # ---- metadata
    G = "Title and meta"
    title = a.seo_title or doc["h1"] or ""
    if title:
        st = PASS if 30 <= len(title) <= 60 else WARN
        add(G, st, f'Title is {len(title)} characters (aim for 50 to 60 so it is not truncated): "{title}"')
        add(G, PASS if kp.search(title) or is_variation(title, kw) else FAIL, "Primary keyword in the title")
        if a.strict:
            low = uncapitalized(title)
            add(G, PASS if not low else FAIL, "Every title word is capitalized" if not low else f"Lowercase words in title: {low}")
    else:
        add(G, FAIL, "No H1 or title found")
    if a.meta:
        st = PASS if 140 <= len(a.meta) <= 160 else WARN
        add(G, st, f"Meta description is {len(a.meta)} characters (target 140 to 160)")
        add(G, PASS if kp.search(a.meta) or is_variation(a.meta, kw) else FAIL, "Primary keyword in the meta description")
    else:
        add(G, INFO, "Meta description not checked (add --meta)")

    # ---- voice
    G = "Voice"
    em = doc["body"].count("—"); en = doc["body"].count("–")
    add(G, PASS if not em else FAIL, f"Em dashes: {em}")
    add(G, PASS if not en else WARN, f'En dashes: {en} (write ranges as "3 to 5")')
    anti = []
    pats = [r"\b(?:it|this|that)(?:'s|’s| is| was)\s+not\s+(?:just|only|merely|simply)\b",
            r"\bnot just (?:a|an|the|about)\b", r"\bmore than (?:just )?(?:a|an) \w+[.!]",
            r"\b(?:isn['’]t|is not|wasn['’]t|was not|aren['’]t|are not)\b[^.;!?\n]{1,50},\s*(?:it['’]s|it is|they['’]re|it was)\b"]
    for p in pats:
        anti += [m.group(0) for m in re.finditer(p, doc["prose"], re.I)]
    sents = [s for p in doc["paragraphs"] for s in sentences(p)]
    for s1, s2 in zip(sents, sents[1:]):
        if re.search(r"\bnot\b|n['’]t\b", s1, re.I) and len(s1.split()) <= 10 and len(s2.split()) <= 10 \
                and re.match(r"(?:It|This|That|We|They)(?:['’]s| is| was| are|['’]re)\b", s2):
            anti.append(f"{s1} {s2}")
    add(G, PASS if not anti else FAIL, 'No "not X, it\'s Y" antithesis cadence' if not anti else f"Antithesis cadence: {anti[:4]}")
    low = doc["prose"].lower()
    fil = [f for f in FILLER if re.search(r"(?<![\w-])" + re.escape(f) + r"(?![\w-])", low)]
    add(G, PASS if not fil else WARN, "No filler phrases" if not fil else f"Filler: {fil}")
    hype = [h for h in HYPE + SUPERLATIVES if re.search(r"(?<![\w-])" + re.escape(h) + r"(?![\w-])", low)]
    add(G, PASS if not hype else WARN, "No hype words" if not hype else f"Hype or unsupported claims: {hype}")
    mixed = []
    for group in VARIANTS:
        used = {v: len(re.findall(r"(?<![\w-])" + re.escape(v) + r"(?![\w-])", low)) for v in group}
        used = {k: v for k, v in used.items() if v}
        if len(used) > 1: mixed.append(" and ".join(f'"{k}" ({v})' for k, v in used.items()))
    for group in CASE_VARIANTS:
        used = {v: len(re.findall(r"(?<![\w-])" + re.escape(v) + r"(?![\w-])", doc["prose"])) for v in group}
        used = {k: v for k, v in used.items() if v}
        if len(used) > 1: mixed.append(" and ".join(f'"{k}" ({v})' for k, v in used.items()))
    add(G, PASS if not mixed else WARN, "Terminology is consistent" if not mixed else "Mixed term forms: " + "; ".join(mixed))
    absl = {w: len(re.findall(r"\b" + w + r"\b", low)) for w in ABSOLUTES}
    absl = {k: v for k, v in absl.items() if v}
    if absl: add(G, INFO, f"Absolute words to double-check: {absl}")

    # ---- spelling
    spelling = a.spelling or ("american" if a.strict else None)
    if spelling:
        G = "House style"
        table = BRITISH if spelling == "american" else AMERICAN
        wrong = sorted({w for w in re.findall(r"[a-z]+", low) if w in table})
        other = "British" if spelling == "american" else "American"
        add(G, PASS if not wrong else FAIL, f"{spelling.title()} spelling" if not wrong
            else f"{other} spellings: " + ", ".join(f"{w}→{table[w]}" for w in wrong))

    # ---- house style (strict)
    if a.strict:
        G = "House style"
        units = re.findall(r"\b\d+(?:\.\d+)?" + UNITS + r"\b", doc["prose"])
        add(G, PASS if not units else FAIL, "Space between numbers and units" if not units else f"Missing space before unit: {sorted(set(units))}")
        ords = re.findall(r"\b\d+(?:st|nd|rd|th)\b", doc["prose"])
        add(G, PASS if not ords else WARN, "Ordinals written out" if not ords else f"Write ordinals in words: {sorted(set(ords))}")
        if re.search(r"\bbare-metal\b", low): add(G, WARN, '"bare-metal" should be "bare metal"')
        bold = [m.group(1) for p in doc["paragraphs"] for m in re.finditer(r"\*\*([^*]+)\*\*", p)]
        add(G, PASS if not bold else WARN, "No bold emphasis in prose" if not bold else f"Bold used for emphasis: {bold[:5]}")
        parens = [m.group(0) for m in re.finditer(r"\(([^)]+)\)", doc["prose"]) if not re.fullmatch(r"[A-Z][A-Za-z0-9]{1,9}s?", m.group(1))]
        add(G, PASS if not parens else WARN, "Parentheses only for acronyms" if not parens else f"Parenthetical asides (use a clause instead): {parens[:4]}")
        bad_heads = []
        for l, t, _ in doc["headings"]:
            if l < 2: continue
            for i, w in enumerate(re.findall(r"[A-Za-z][\w'’\-]*", t)):
                if w[0].islower() and not proper_term(w) and (len(w) >= 5 or w in {"is", "are", "be", "was", "were", "do", "does"}) and not (i and w in SMALL_WORDS):
                    bad_heads.append(f'"{w}" in "{t}"')
        add(G, PASS if not bad_heads else WARN, "Heading capitalization" if not bad_heads else f"Capitalize: {bad_heads[:5]}")
        if any(re.fullmatch(r"(?i)conclusions?|final thoughts|wrapping up|summary", t.strip()) for _, t, _ in doc["headings"]):
            add(G, WARN, 'Generic closing heading. Close with next steps instead of "Conclusion"')
    return R


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file"); ap.add_argument("--keyword", required=True); ap.add_argument("--secondary")
    ap.add_argument("--site"); ap.add_argument("--meta"); ap.add_argument("--seo-title")
    ap.add_argument("--strict", action="store_true"); ap.add_argument("--spelling", choices=["american", "british"]); ap.add_argument("--check-links", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    with open(a.file, encoding="utf-8") as f:
        doc = parse(f.read())
    results = run(doc, a)
    fails = sum(s == FAIL for _, s, _ in results); warns = sum(s == WARN for _, s, _ in results)
    passes = sum(s == PASS for _, s, _ in results)
    if a.json:
        print(json.dumps({"passed": passes, "warnings": warns, "failed": fails,
                          "checks": [dict(group=g, status=s, message=m) for g, s, m in results]}, indent=2))
    else:
        group = None
        for g, s, m in results:
            if g != group:
                print(f"\n{g}"); group = g
            print(f"  {ICON[s]} {m}")
        print(f"\n{passes} passed, {warns} warnings, {fails} failed")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
