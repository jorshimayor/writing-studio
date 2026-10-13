#!/usr/bin/env python3
"""Free keyword ideas from Google and YouTube autocomplete.

Autocomplete reflects what people actually type, so it is a reliable source of
real phrasing, questions and long-tail variants. It does NOT give search volume
or difficulty. For those, use OpenSEO / DataForSEO (see references/keyword-research.md).

Standard library only. Usage:

    python3 keyword_ideas.py "react agent"
    python3 keyword_ideas.py "context window" "llm memory" --source both --expand full
    python3 keyword_ideas.py "solana node" --gl gb --hl en-GB --json

Options:
    --source   google | youtube | both            (default: both)
    --expand   none | questions | full           (default: questions)
               questions = seed + question/comparison modifiers
               full      = questions + "seed a" ... "seed z"
    --gl, --hl country and language for suggestions (default: us, en)
    --loose    keep every suggestion, even ones that drop the seed words
    --json     machine-readable output
"""
from __future__ import annotations

import argparse
import json
import re
import string
import time
import urllib.parse
import urllib.request
from collections import Counter, defaultdict

ENDPOINT = "https://suggestqueries.google.com/complete/search"
PREFIXES = ["what is", "how does", "how to", "why", "when to", "which", "can", "is", "best", "what are"]
SUFFIXES = ["vs", "for", "with", "without", "tutorial", "example", "explained", "from scratch",
            "not working", "error", "alternative", "pricing", "requirements", "2026"]
QUESTION = re.compile(r"^(what|how|why|when|where|which|who|can|is|are|does|do|should|will)\b")


def suggest(query: str, source: str, gl: str, hl: str) -> list[str]:
    params = {"client": "firefox", "q": query, "gl": gl, "hl": hl}
    if source == "youtube":
        params["ds"] = "yt"
    req = urllib.request.Request(f"{ENDPOINT}?{urllib.parse.urlencode(params)}",
                                 headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode("utf-8", "ignore"))
        return [s.strip().lower() for s in data[1] if isinstance(s, str)]
    except Exception:
        # Some Python builds lack CA certificates; fall back to curl.
        import subprocess
        url = f"{ENDPOINT}?{urllib.parse.urlencode(params)}"
        try:
            out = subprocess.run(["curl", "-s", "-m", "10", "-A", "Mozilla/5.0", url],
                                 capture_output=True, text=True, timeout=15).stdout
            return [s.strip().lower() for s in json.loads(out)[1] if isinstance(s, str)]
        except Exception:
            return []


def queries_for(seed: str, expand: str) -> list[str]:
    qs = [seed]
    if expand in ("questions", "full"):
        qs += [f"{p} {seed}" for p in PREFIXES] + [f"{seed} {s}" for s in SUFFIXES]
    if expand == "full":
        qs += [f"{seed} {c}" for c in string.ascii_lowercase]
    return qs


def relevant(phrase: str, seed: str) -> bool:
    """Seed words appear in order, allowing plurals, underscores and up to 2 words between them."""
    toks = [re.escape(t) for t in re.split(r"[\s_-]+", seed) if t]
    pat = r"[\s_-]+(?:\S+[\s_-]+){0,2}".join(t + r"s?" for t in toks)
    return re.search(r"(?<![a-z])" + pat + r"(?![a-z])", phrase) is not None


def classify(phrase: str) -> str:
    if QUESTION.match(phrase):
        return "questions"
    if re.search(r"\bvs\.?\b|\bversus\b|\bor\b|\balternatives?\b|\bcompared?\b", phrase):
        return "comparisons"
    if re.search(r"\b(not working|error|fix|issue|failed|problem)\b", phrase):
        return "problems"
    if re.search(r"\b(how to|tutorial|guide|setup|set up|install|from scratch|example|step)\b", phrase):
        return "how-to"
    return "long-tail"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("seeds", nargs="+")
    ap.add_argument("--source", choices=["google", "youtube", "both"], default="both")
    ap.add_argument("--expand", choices=["none", "questions", "full"], default="questions")
    ap.add_argument("--gl", default="us"); ap.add_argument("--hl", default="en")
    ap.add_argument("--loose", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    sources = ["google", "youtube"] if a.source == "both" else [a.source]
    hits, seen_in = Counter(), defaultdict(set)
    for seed in a.seeds:
        for q in queries_for(seed.lower().strip(), a.expand):
            for src in sources:
                for rank, s in enumerate(suggest(q, src, a.gl, a.hl)):
                    if not a.loose and not relevant(s, seed.lower().strip()):
                        continue
                    hits[s] += 10 - min(rank, 9)        # earlier suggestions are more popular
                    seen_in[s].add(src)
                time.sleep(0.15)                          # be polite to the endpoint

    rows = [dict(phrase=p, score=sc, sources=sorted(seen_in[p]), group=classify(p))
            for p, sc in hits.most_common()]
    if a.json:
        print(json.dumps({"seeds": a.seeds, "count": len(rows), "ideas": rows}, indent=2))
        return
    groups = defaultdict(list)
    for r in rows:
        groups[r["group"]].append(r)
    print(f"{len(rows)} ideas for {', '.join(a.seeds)} "
          f"(score = how often and how high a phrase was suggested; it is NOT search volume)\n")
    for g in ["questions", "comparisons", "how-to", "problems", "long-tail"]:
        if groups[g]:
            print(f"{g.upper()}")
            for r in groups[g][:25]:
                both = " [google+youtube]" if len(r["sources"]) == 2 else f" [{r['sources'][0]}]"
                print(f"  {r['score']:>4}  {r['phrase']}{both}")
            print()


if __name__ == "__main__":
    main()
