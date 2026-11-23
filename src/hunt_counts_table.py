#!/usr/bin/env python3
"""Markdown table of results/counterexample-hunt/counts/*.txt: per family, the range counted and how the count moves."""
import glob, re, os
print("| file | members counted | n | first counts | last count | least count at n >= 26 | drops (count smaller than the previous member) | most non-anchor vertices |")
print("|---|---|---|---|---|---|---|---|")
for f in sorted(glob.glob("../results/counterexample-hunt/counts/*.txt")):
    rows = []
    for line in open(f):
        m = re.match(r"(\S+) n=(\d+) count=(\d+)", line)
        if not m: continue
        na = re.search(r"non_anchors=(\d+)/(\d+)", line)
        rows.append((m.group(1), int(m.group(2)), int(m.group(3)), int(na.group(1)) if na else 0))
    if not rows: continue
    drops = sum(1 for a, b in zip(rows, rows[1:]) if b[2] < a[2]); big = [r for r in rows if r[1] >= 26]
    least = min(big, key=lambda r: r[2]) if big else None; wn = max(rows, key=lambda r: r[3] / r[1])
    print(f"| {os.path.basename(f)[:-4]} | {len(rows)} | {rows[0][1]}..{rows[-1][1]} | {', '.join(str(r[2]) for r in rows[:6])} | {rows[-1][2]:,} | {(str(least[2]) + ' (n=' + str(least[1]) + ')') if least else '-'} | {drops} | {wn[3]} of {wn[1]} |")
