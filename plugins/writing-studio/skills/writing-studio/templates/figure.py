#!/usr/bin/env python3
"""Starter for an illustrated article figure with the figure kit. Copy it, change the content.

    python3 templates/figure.py profiles/<name>.brand.json images/example.png

Every number, line of code and label must come from the article's sources (references/fact-check.md).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import figure_kit as k  # noqa: E402

brand = sys.argv[1] if len(sys.argv) > 1 else None
out = sys.argv[2] if len(sys.argv) > 2 else "example-figure.png"
k.use_brand(brand)

# Two cards side by side: the normal case and the odd one, with one circle and one note.
body = (
    '<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">'
    f'<div class="card" style="padding:22px;display:flex;flex-direction:column;gap:12px;align-items:center">'
    f'<span class="pill vic">normal case</span>{k.vault([k.coins(6, "vic", w=40, step=8)], w=150, h=200)}'
    f'{k.ticket("6 SHARES", "vic", w=130)}</div>'
    f'<div class="card" style="padding:22px;display:flex;flex-direction:column;gap:12px;align-items:center">'
    f'<span class="pill att">odd case</span>{k.vault([k.coins(6, "att", w=40, step=8)], w=150, h=200)}'
    f'<span class="circ">{k.ticket("0 SHARES", "ghost", w=130, empty=True)}</span>'
    f'<span class="note">the one thing to see</span></div></div>'
)
page = k.figure("Series label", "A title that says what this is",
                "One sentence of context. <strong>The finding, stated plainly.</strong>",
                body, "Source: the run, version or document every value came from.")
k.render(page, out)
print("wrote", out)
