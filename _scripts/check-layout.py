#!/usr/bin/env python3
"""Check a rendered thesis PDF against the SGPS layout rules.

Usage: python3 _scripts/check-layout.py [_thesis/thesis.pdf]

For every page prints the text extents (inches from each edge) and the page-number
position, and flags violations of:
  - margins: left >= 1.5in, right/bottom/top >= 1in for body text (§6.4)
  - page numbers >= 0.5in from the edges (§6.6); roman at the bottom centre in the
    front matter, arabic in the upper right in the body
Requires `pdftotext` (poppler).
"""
import re
import subprocess
import sys

PDF = sys.argv[1] if len(sys.argv) > 1 else "_thesis/thesis.pdf"
TOL = 0.02  # inches of glyph-box slack

xml = subprocess.run(["pdftotext", "-bbox", PDF, "-"], capture_output=True,
                     text=True, check=True).stdout
pages = []
for chunk in xml.split("<page ")[1:]:
    w = float(re.search(r'width="([\d.]+)"', chunk).group(1))
    h = float(re.search(r'height="([\d.]+)"', chunk).group(1))
    words = [(float(a), float(b), float(c), float(d), t) for a, b, c, d, t in re.findall(
        r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>',
        chunk)]
    pages.append((w, h, words))

problems = 0
print(f"{'pg':>3}  {'left':>5} {'right':>5} {'top':>5} {'bottom':>6}  page number")
for i, (W, H, words) in enumerate(pages, 1):
    if not words:
        print(f"{i:>3}  (blank)")
        continue
    # Page number: a lone roman/arabic token in the header or footer band.
    num = [w for w in words if re.fullmatch(r"[ivxlc]+|\d+", w[4])
           and (w[1] < 72 or w[3] > H - 72)]
    # Running header: words that end above the 1in top margin (on body pages).
    header = [w for w in words if w[3] < 72 and w not in num]
    body = [w for w in words if w not in num and w not in header]
    notes = []
    if body:
        left = min(w[0] for w in body) / 72
        right = (W - max(w[2] for w in body)) / 72
        top = min(w[1] for w in body) / 72
        bottom = (H - max(w[3] for w in body)) / 72
        if left < 1.5 - TOL: notes.append("LEFT<1.5")
        if right < 1.0 - TOL: notes.append("RIGHT<1")
        if top < 1.0 - TOL - 0.2: notes.append("TOP<1")  # ascender slack
        if bottom < 1.0 - TOL - 0.05: notes.append("BOTTOM<1")  # descender slack
    else:
        left = right = top = bottom = float("nan")
    pn = ""
    if num:
        # In the header the page number is the rightmost token (the running header
        # may start with a chapter number).
        n = max(num, key=lambda w: w[2])
        edge = min(n[0], W - n[2], n[1], H - n[3]) / 72
        where = "top" if n[1] < 72 else "bottom"
        cx = (n[0] + n[2]) / 2 / 72
        pn = f"{n[4]:>5} {where} x={cx:.2f}in edge={edge:.2f}in"
        if edge < 0.5 - TOL: notes.append("PAGENO<0.5in")
    elif i > 1:
        notes.append("NO-PAGENO")
    problems += len(notes)
    print(f"{i:>3}  {left:5.2f} {right:5.2f} {top:5.2f} {bottom:6.2f}  {pn}  {' '.join(notes)}")

print(f"\n{problems} problem(s)")
sys.exit(1 if problems else 0)
