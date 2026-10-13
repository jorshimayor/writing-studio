#!/usr/bin/env python3
"""Check an outline file against its User Need rules, and (optionally) check that
an article followed the outline.

Standard library only. The User Need rules live in `need_rules.json` next to this
script, so each skill can define its own set of needs.

Usage:
    python3 outline_check.py outlines/what-is-x.outline.md --site example.com
    python3 outline_check.py outlines/what-is-x.outline.md --article drafts/what-is-x.md
    python3 outline_check.py outlines/*.outline.md          # several outlines at once

Options:
    --site     your domain(s), comma-separated, to classify planned links
    --article  a drafted article to compare against the outline's section plan
    --strict   house style: titles must capitalize every word
    --json     machine-readable output

Exit code is 1 if any check fails.

Outline format (see references/outline-template.md):
    YAML-style front matter (topic, user_need, reader, level, primary_keyword,
    secondary_keywords, title, seo_title, meta_description, slug, cta), then
    planned article headings written as `### H2: ...` and `#### H3: ...`, each
    followed by bullets such as `- Purpose:`, `- Key points:`, `- Links:`.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from urllib.parse import urlparse

PASS, WARN, FAIL, INFO = "pass", "warn", "fail", "info"
ICON = {PASS: "✔", WARN: "⚠", FAIL: "✘", INFO: "•"}
REQUIRED = ["topic", "user_need", "reader", "level", "primary_keyword", "title", "slug", "cta"]
RECOMMENDED = ["secondary_keywords", "seo_title", "meta_description"]
STOP = {"a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "with", "is", "are", "do", "does",
        "how", "what", "why", "when", "which", "your", "you", "it", "its", "vs", "vs."}


def load_rules():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "need_rules.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def front_matter(text):
    meta = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                if ":" in line and not line.startswith((" ", "\t", "-")):
                    k, v = line.split(":", 1)
                    v = v.strip().strip('"\'')
                    if v.startswith("[") and v.endswith("]"):
                        v = [x.strip().strip('"\'') for x in v[1:-1].split(",") if x.strip()]
                    meta[k.strip().lower()] = v
            text = text[end + 4:]
    return meta, text


def parse_outline(text):
    meta, body = front_matter(text)
    sections, current = [], None
    for line in body.splitlines():
        m = re.match(r"^#{2,6}\s*H([23])\s*[:.]\s*(.+?)\s*$", line)
        if m:
            current = dict(level=int(m.group(1)), title=m.group(2), lines=[])
            sections.append(current)
            continue
        if re.match(r"^#{1,3}\s", line) and not re.match(r"^#{2,6}\s*H[23]", line):
            current = None          # a non-plan heading (e.g. "## Sources") ends the plan block
            continue
        if current is not None:
            current["lines"].append(line)
    blocks = {m.group(1).strip().lower(): m.group(2) for m in
              re.finditer(r"^##\s+(.+?)\s*\n(.*?)(?=^##\s|\Z)", body, flags=re.M | re.S)}
    return meta, body, sections, blocks


def words(s):
    return [w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in STOP]


def variation(text, phrase):
    low = text.lower()
    return all(re.search(r"\b" + re.escape(t[:max(4, len(t) - 2)]), low) for t in re.split(r"[\s\-]+", phrase.lower()) if t)


def field(sec, name):
    pat = re.compile(r"^\s*[-*]\s*" + name + r"\s*:\s*(.*)$", re.I)
    for line in sec["lines"]:
        m = pat.match(line)
        if m:
            return m.group(1).strip() or "(sub-bullets)"
    return None


def similarity(a, b, ignore=frozenset()):
    """Word overlap between two headings, ignoring words every heading shares (the keyword)."""
    wa, wb = set(words(a)) - ignore, set(words(b)) - ignore
    if not wa or not wb:
        wa, wb = set(words(a)), set(words(b))
    return len(wa & wb) / max(1, min(len(wa), len(wb))) if wa and wb else 0.0


def check(path, a, rules):
    R = []
    add = lambda g, s, m: R.append((g, s, m))
    with open(path, encoding="utf-8") as f:
        meta, body, sections, blocks = parse_outline(f.read())

    # ---- brief
    G = "Brief"
    for k in REQUIRED:
        add(G, PASS if meta.get(k) else FAIL, f"{k}: {meta.get(k) or 'missing'}")
    for k in RECOMMENDED:
        if not meta.get(k):
            add(G, WARN, f"{k} missing")
    need_name = str(meta.get("user_need", "")).strip()
    rule = next((v | {"name": n} for n, v in rules["needs"].items() if n.lower() == need_name.lower()), None)
    add(G, PASS if rule else FAIL, f'User Need "{need_name}" ' + ("is valid" if rule else
        "is not one of: " + ", ".join(rules["needs"])))
    kw = str(meta.get("primary_keyword", ""))
    sec_kws = meta.get("secondary_keywords") or []
    if isinstance(sec_kws, str):
        sec_kws = [x.strip() for x in sec_kws.split(",") if x.strip()]

    # ---- title and meta
    G = "Title and meta"
    title = str(meta.get("seo_title") or meta.get("title") or "")
    if title:
        add(G, PASS if 30 <= len(title) <= 60 else WARN, f'SEO title is {len(title)} characters (50 to 60): "{title}"')
        add(G, PASS if kw and variation(title, kw) else FAIL, "Primary keyword in the title")
        if a.strict:
            low = [w for w in re.findall(r"[A-Za-z][\w'’]*", str(meta.get("title", ""))) if w[0].islower()]
            add(G, PASS if not low else FAIL, "Every title word capitalized" if not low else f"Lowercase title words: {low}")
    md = str(meta.get("meta_description", ""))
    if md:
        add(G, PASS if 140 <= len(md) <= 160 else WARN, f"Meta description is {len(md)} characters (140 to 160)")
        add(G, PASS if variation(md, kw) else WARN, "Primary keyword in the meta description")
    opts = blocks.get("title options", "")
    n_opts = len(re.findall(r"^\|\s*\d+\s*\|", opts, flags=re.M)) or len(re.findall(r"^\s*\d+[.)]\s", opts, flags=re.M))
    add(G, PASS if n_opts >= 8 else WARN, f"Title options listed: {n_opts} (target 8 to 10)")

    # ---- reader need
    G = "User Need"
    desires = blocks.get("reader desires", "") or blocks.get("reader and intent", "")
    n_des = len(re.findall(r"^\s*[-*]\s+\S", desires, flags=re.M))
    add(G, PASS if n_des >= 2 else FAIL, f"Reader desires to satisfy: {n_des} (at least 2)")
    intro = blocks.get("intro plan", "")
    add(G, PASS if intro.strip() else FAIL, "Intro plan present")
    if intro and re.search(r"in this (article|guide|post),? (we|you|i)(\s|'ll)", intro, re.I):
        add(G, FAIL, 'Intro plan announces the structure ("In this article, we will"). Imply the roadmap instead')

    # ---- section plan
    G = "Section plan"
    h2 = [s for s in sections if s["level"] == 2]
    h3 = [s for s in sections if s["level"] == 3]
    if not h2:
        add(G, FAIL, "No planned sections found. Write them as '### H2: ...' and '#### H3: ...'")
        return R, meta, sections
    lo, hi = (rule or {}).get("min_h2", 3), (rule or {}).get("max_h2", 10)
    add(G, PASS if lo <= len(h2) <= hi else WARN, f"{len(h2)} H2s and {len(h3)} H3s planned (this need: {lo} to {hi} H2s)")
    add(G, PASS if variation(h2[0]["title"], kw) else FAIL, f'First H2 uses a keyword variation: "{h2[0]["title"]}"')
    others = sum(variation(s["title"], kw) for s in h2[1:])
    add(G, PASS if others >= 1 else FAIL, f"Other H2s with a keyword variation: {others} (target 1 to 2)")
    if sec_kws:
        used = [k for k in sec_kws if any(variation(s["title"], k) for s in sections)]
        add(G, PASS if used else WARN, f"Secondary keywords in H2/H3s: {len(used)} of {len(sec_kws)}")
    q = sum(s["title"].rstrip().endswith("?") for s in h2)
    add(G, INFO, f"{q} of {len(h2)} H2s phrased as reader questions")
    missing = [s["title"] for s in h2 if not field(s, "purpose")]
    add(G, PASS if not missing else WARN, "Every H2 states its purpose" if not missing else f"H2s without '- Purpose:': {missing[:4]}")
    thin = [s["title"] for s in h2 if not field(s, "key points") and len([l for l in s["lines"] if l.strip()]) < 2]
    add(G, PASS if not thin else WARN, "Every H2 has key points" if not thin else f"H2s without key points: {thin[:4]}")

    # ---- need-specific rules
    if rule:
        G = f"{rule['name']} rules"
        titles = [s["title"].lower() for s in h2]
        for req in rule.get("required_sections", []):
            pat = re.compile(req["match"], re.I)
            pos = req.get("position", "any")
            idx = [i for i, t in enumerate(titles) if pat.search(t)]
            if pos == "first":
                ok = bool(idx) and idx[0] <= req.get("within", 0)
            elif pos == "last":
                ok = bool(idx) and idx[-1] >= len(titles) - req.get("within", 2)
            else:
                ok = bool(idx)
            where = {"first": "at the start", "last": "at the end", "any": ""}[pos]
            add(G, PASS if ok else req.get("severity", FAIL), f"{req['label']} section {where}".strip()
                + ("" if ok else f" (no H2 matching /{req['match']}/)"))
        for bad in rule.get("forbidden_sections", []):
            hit = [s["title"] for s in h2 if re.search(bad["match"], s["title"], re.I)]
            add(G, FAIL if hit and bad.get("severity", FAIL) == FAIL else (WARN if hit else PASS),
                bad["label"] if not hit else f"{bad['label']}: {hit}")
        alltext = body.lower()
        if rule.get("needs_table"):
            add(G, PASS if re.search(r"\btable\b", alltext) else FAIL, "Comparison table planned")
        if rule.get("needs_steps"):
            add(G, PASS if re.search(r"\bsteps?\b|numbered", alltext) else FAIL, "Numbered steps planned")
        if rule.get("needs_visuals"):
            add(G, PASS if re.search(r"\b(screenshot|image|diagram|visual)\b", alltext) else WARN, "Visuals or screenshots planned for the steps")
        if rule.get("section_summary"):
            no_sum = [s["title"] for s in h2 if not re.search(r"summary", "\n".join(s["lines"]), re.I)
                      and not re.search(rule.get("summary_exempt", "^$"), s["title"], re.I)]
            add(G, PASS if not no_sum else WARN, "Each section plans a closing summary" if not no_sum
                else f"Sections without a planned summary: {no_sum[:4]}")
        for tip in rule.get("reminders", []):
            add(G, INFO, tip)

    # ---- links
    G = "Planned links"
    urls = re.findall(r"\]\((https?://[^)\s]+|/[^)\s]*)\)|(?<![(\w])(https?://[^\s)|>]+)", body)
    urls = list(dict.fromkeys(u1 or u2 for u1, u2 in urls))   # each planned URL counts once
    sites = [x.strip().lower().removeprefix("www.") for x in (a.site or "").split(",") if x.strip()]
    def internal(u):
        p = urlparse(u); host = p.netloc.lower().removeprefix("www.")
        return (not host) or any(host == s or host.endswith("." + s) or (host + p.path).startswith(s) for s in sites)
    links_block = blocks.get("internal links", "") + blocks.get("links", "")
    n_int = sum(internal(u) for u in urls) if sites else len(re.findall(r"^\s*[-*|]", links_block, flags=re.M))
    n_ext = sum(not internal(u) for u in urls) if sites else None
    add(G, PASS if n_int >= 3 else WARN, f"Internal links planned: {n_int} (3 to 5 per 1,000 words)")
    if n_ext is not None:
        add(G, PASS if 1 <= n_ext <= 3 else WARN, f"External sources planned: {n_ext} (1 to 3)")

    # ---- article vs outline
    if a.article:
        G = "Article follows outline"
        with open(a.article, encoding="utf-8") as f:
            art = f.read()
        art_h2 = [m.group(1).strip() for m in re.finditer(r"^##\s+(.+?)\s*#*\s*$", re.sub(r"```.*?```", "", art, flags=re.S), flags=re.M)]
        ignore = frozenset(words(kw))
        matched, last_idx, order_ok = [], -1, True
        for s in h2:
            free = [i for i in range(len(art_h2)) if i not in matched]      # one article heading per planned heading
            best = max(free, key=lambda i: similarity(s["title"], art_h2[i], ignore), default=None)
            if best is not None and similarity(s["title"], art_h2[best], ignore) >= 0.6:
                matched.append(best)
                if best < last_idx: order_ok = False
                last_idx = best
            else:
                add(G, FAIL, f'Planned H2 missing from the article: "{s["title"]}"')
        add(G, PASS if len(matched) == len(h2) else WARN, f"{len(matched)} of {len(h2)} planned H2s found in the article")
        add(G, PASS if order_ok else FAIL, "Sections appear in the planned order" if order_ok else "Sections are out of the planned order")
        extra = [t for i, t in enumerate(art_h2) if i not in matched]
        if extra:
            add(G, WARN, f"H2s not in the outline (explain or add them to the outline): {extra[:4]}")
    return R, meta, sections


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("outlines", nargs="+"); ap.add_argument("--site"); ap.add_argument("--article")
    ap.add_argument("--strict", action="store_true"); ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if a.article and len(a.outlines) > 1:
        ap.error("--article works with a single outline")
    rules, any_fail, report = load_rules(), False, []
    for path in a.outlines:
        R, meta, _ = check(path, a, rules)
        fails = sum(s == FAIL for _, s, _ in R); any_fail |= bool(fails)
        report.append(dict(outline=path, user_need=meta.get("user_need"), title=meta.get("title"),
                           passed=sum(s == PASS for _, s, _ in R), warnings=sum(s == WARN for _, s, _ in R),
                           failed=fails, checks=[dict(group=g, status=s, message=m) for g, s, m in R]))
        if not a.json:
            print(f"\n=== {path}")
            group = None
            for g, s, m in R:
                if g != group:
                    print(f"\n{g}"); group = g
                print(f"  {ICON[s]} {m}")
            print(f"\n{report[-1]['passed']} passed, {report[-1]['warnings']} warnings, {fails} failed")
    if a.json:
        print(json.dumps(report, indent=2))
    elif len(report) > 1:
        print("\n=== Summary")
        for r in report:
            print(f"  {'✘' if r['failed'] else '✔'} {r['outline']}: {r['user_need']} | {r['failed']} failed, {r['warnings']} warnings")
    sys.exit(1 if any_fail else 0)


if __name__ == "__main__":
    main()
