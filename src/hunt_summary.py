#!/usr/bin/env python3
"""Tally the existence logs hunt_exist_*.log (written by hunt_exist.sh) into a markdown table."""
import glob, re, collections
rows = collections.OrderedDict()
for f in sorted(glob.glob("hunt_exist_*.log")):
    cls = f[len("hunt_exist_"):].split(".")[0]
    r = rows.setdefault(cls, dict(trees=0, found=0, none=0, unres=0, nmin=10**9, nmax=0, runs=collections.Counter(), maxnodes=0, bad=0, hardest=""))
    for line in open(f):
        m = re.match(r"(\S+) n=(\d+) (\S+)", line)
        if not m: continue
        n = int(m.group(2)); r["trees"] += 1; r["nmin"] = min(r["nmin"], n); r["nmax"] = max(r["nmax"], n)
        nodes = int(re.search(r"nodes=(\d+)", line).group(1))
        if nodes > r["maxnodes"]: r["maxnodes"] = nodes; r["hardest"] = m.group(1)
        if m.group(3) == "FOUND":
            r["found"] += 1; r["runs"][re.search(r"runs<=(\S+)", line).group(1)] += 1
            if "verified=yes" not in line: r["bad"] += 1
        elif m.group(3) == "NONE" and "unrestricted" in line: r["none"] += 1; print("NONE:", line.strip())
        else: r["unres"] += 1; print("UNRESOLVED:", line.strip())
print("| class | trees | n | growth placement found and verified | none (complete search) | unresolved | found within <=1 / 2 / 3 / 4 runs / unrestricted attempt | most nodes (tree) |")
print("|---|---|---|---|---|---|---|---|")
tot = collections.Counter()
for cls, r in rows.items():
    ru = r["runs"]; print(f"| {cls} | {r['trees']:,} | {r['nmin']}..{r['nmax']} | {r['found'] - r['bad']:,} | {r['none']} | {r['unres']} | {ru['1']:,} / {ru['2']:,} / {ru['3']:,} / {ru['4']:,} / {ru['inf']:,} | {r['maxnodes']:,} ({r['hardest']}) |")
    for k in ("trees", "found", "none", "unres"): tot[k] += r[k]
print(f"| **total** | {tot['trees']:,} | | {tot['found']:,} | {tot['none']} | {tot['unres']} | | |")
