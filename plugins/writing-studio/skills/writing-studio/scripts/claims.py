#!/usr/bin/env python3
"""Fact-check ledger for a draft: every statement gets a source or a decision.

Standard library only.

    python3 claims.py extract draft.md > draft.claims.md   # one row per sentence
    python3 claims.py check draft.claims.md --draft draft.md # gate: exit 1 if anything is open

Ledger format (Markdown table, one row per sentence):

| id | priority | tags | claim | status | source | note |

priority  high = contains something checkable (number, date, version, name,
          comparison, attribution, technical behaviour); low = framing or transition
status    one of:
  verified   the claim matches the source. Needs a source.
  corrected  the draft was changed to match the source. Needs a source and a note.
  softened   reworded to the certainty the evidence supports ("can", "usually"). Needs a note.
  removed    cut from the draft because it couldn't be verified.
  opinion    the author's view, written so it reads as opinion ("I think", "in my tests").
  framing    a transition or setup sentence with no factual content (low priority only).
  author     only the author can confirm (their own results, experience, plans). Blocks
             the gate unless --allow-author is passed.
  TODO       not checked yet. Always blocks the gate.
source    a URL (https://...), or for things checked another way:
          test:<file or command>, computed:<script or formula>, doc:<file path>, author:<who>
"""
import argparse
import hashlib
import re
import sys

STATUSES = {"verified", "corrected", "softened", "removed", "opinion", "framing", "author", "todo"}
NEEDS_SOURCE = {"verified", "corrected"}
NEEDS_NOTE = {"corrected", "softened"}
SOURCE_RE = re.compile(r"^(https?://\S+|test:\S.*|computed:\S.*|doc:\S.*|author:\S.*)$")

TAGS = [
    ("number", r"\b\d[\d,.]*\b"),
    ("percent", r"\d\s?%|\bper ?cent\b"),
    ("money", r"[$€£¥]\s?\d|\b\d[\d,.]*\s?(?:USD|EUR|GBP|ETH|BTC|SOL|USDC|USDT)\b"),
    ("date", r"\b(?:19|20)\d{2}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\b|\b(?:yesterday|today|last (?:week|month|year))\b"),
    ("version", r"\bv?\d+\.\d+(?:\.\d+)?\b|\b(?:EIP|ERC|BIP|RFC)-?\d+\b"),
    ("comparison", r"\b(?:fastest|slowest|cheapest|largest|biggest|smallest|first|only|most|least|best|worst|more|less|faster|slower|cheaper|higher|lower|better|worse|leading|popular|widely|majority|minority)\b"),
    ("absolute", r"\b(?:always|never|all|none|every|guaranteed|impossible|completely|entirely|no one|nobody)\b"),
    ("attribution", r"\b(?:according to|reported|announced|said|says|stated|claims?|found that|showed that|estimates?)\b"),
    ("quote", r"[\"“][^\"”]{12,}[\"”]"),
    ("causal", r"\b(?:because|causes?|caused|leads? to|led to|results? in|due to|so that|which means|therefore)\b"),
    ("behaviour", r"\b(?:returns?|reverts?|defaults? to|by default|requires?|supports?|deprecated|introduced|removed|added|uses|runs on|compatible|audited)\b"),
    ("entity", r"(?<=[a-z,;:] )[A-Z][a-zA-Z0-9]+(?:[ -][A-Z][a-zA-Z0-9]+)*"),
]


def strip_markdown(text):
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)          # front matter
    text = re.sub(r"```.*?```", "", text, flags=re.S)                  # code blocks are checked by running them
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", "", text)                 # images: alt text is checked with the figure
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)               # keep link text
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"[*_]{1,2}([^*_]+)[*_]{1,2}", r"\1", text)
    return text


def sentences(text):
    out = []
    for block in re.split(r"\n\s*\n", strip_markdown(text)):
        block = block.strip()
        if not block or set(block) <= set("-|: "):
            continue
        if block.startswith("|"):                                       # table: one claim per row
            for row in block.splitlines():
                cells = [c.strip() for c in row.strip("|").split("|")]
                if cells and not set("".join(cells)) <= set("-: "):
                    out.append(" | ".join(c for c in cells if c))
            continue
        for line in block.splitlines():
            line = re.sub(r"^\s*(?:#{1,6}|[-*+]|\d+[.)]|>)\s*", "", line).strip()
            if not line:
                continue
            for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"“(])", line):
                s = s.strip()
                if len(s) > 2:
                    out.append(s)
    return out


def sid(s):
    return hashlib.sha1(re.sub(r"\s+", " ", s).strip().encode()).hexdigest()[:8]


def tag(s):
    found = [name for name, pat in TAGS if re.search(pat, s, re.I if name not in ("entity",) else 0)]
    if found == ["entity"] and len(s.split()) < 4:
        found = []
    return found


def cell(s):
    return s.replace("|", "\\|").replace("\n", " ")


def extract(path):
    rows, seen = [], set()
    for s in sentences(open(path, encoding="utf-8").read()):
        i = sid(s)
        if i in seen:
            continue
        seen.add(i)
        t = tag(s)
        rows.append((i, "high" if t else "low", ",".join(t), s))
    print(f"<!-- claims ledger for {path}. Fill status, source and note for every row, then run: "
          f"python3 claims.py check <this file> --draft {path} -->")
    print()
    print("| id | priority | tags | claim | status | source | note |")
    print("|---|---|---|---|---|---|---|")
    for i, p, t, s in rows:
        print(f"| {i} | {p} | {t} | {cell(s)} | TODO |  |  |")
    hi = sum(1 for r in rows if r[1] == "high")
    print(f"\n<!-- {len(rows)} statements, {hi} high priority -->")


def parse_ledger(path):
    rows = []
    for line in open(path, encoding="utf-8"):
        if not line.startswith("| ") or line.startswith("| id ") or line.startswith("|---"):
            continue
        cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
        if len(cells) < 7:
            cells += [""] * (7 - len(cells))
        rows.append(dict(zip(["id", "priority", "tags", "claim", "status", "source", "note"], cells)))
    return rows


def check(path, draft=None, allow_author=False):
    rows = parse_ledger(path)
    problems, counts = [], {}
    for r in rows:
        st = r["status"].lower()
        counts[st] = counts.get(st, 0) + 1
        ref = f'{r["id"]} "{r["claim"][:70]}"'
        if st not in STATUSES:
            problems.append(f"unknown status '{r['status']}': {ref}")
        elif st == "todo":
            problems.append(f"not checked: {ref}")
        elif st == "author" and not allow_author:
            problems.append(f"needs the author to confirm: {ref}")
        if st in NEEDS_SOURCE and not SOURCE_RE.match(r["source"]):
            problems.append(f"{st} without a valid source (URL, test:, computed:, doc:, author:): {ref}")
        if st in NEEDS_NOTE and not r["note"]:
            problems.append(f"{st} without a note saying what changed: {ref}")
        if st == "framing" and r["priority"] == "high":
            problems.append(f"marked framing but contains checkable content ({r['tags']}): {ref}")
    if draft:
        ledger = {r["id"]: r for r in rows}
        current = {sid(s): s for s in sentences(open(draft, encoding="utf-8").read())}
        for i, s in current.items():
            if i not in ledger:
                problems.append(f"sentence in the draft but not in the ledger (new or edited after checking): {i} \"{s[:70]}\"")
        for i, r in ledger.items():
            if i not in current and r["status"].lower() not in ("removed", "corrected", "softened"):
                problems.append(f"ledger row no longer in the draft but not marked removed/corrected/softened: {i} \"{r['claim'][:70]}\"")
    total = len(rows)
    print(f"{total} statements: " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
    for p in problems:
        print("  ✘ " + p)
    print("PASS: every statement is accounted for" if not problems else f"FAIL: {len(problems)} open item(s)")
    return not problems


def main():
    ap = argparse.ArgumentParser(description="Fact-check ledger for a draft")
    sub = ap.add_subparsers(dest="cmd", required=True)
    e = sub.add_parser("extract"); e.add_argument("draft")
    c = sub.add_parser("check"); c.add_argument("ledger"); c.add_argument("--draft")
    c.add_argument("--allow-author", action="store_true", help="don't block on rows the author must confirm")
    a = ap.parse_args()
    if a.cmd == "extract":
        extract(a.draft)
    else:
        sys.exit(0 if check(a.ledger, a.draft, a.allow_author) else 1)


if __name__ == "__main__":
    main()
