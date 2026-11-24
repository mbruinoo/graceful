"""Independent exhaustive check on all trees with n vertices (networkx generator, rsolve solver).
Every vertex is queried (no orbit reduction, so counts are per vertex).
Reports: non-anchor vertices, non-anchors by degree, trees with no anchor of maximum degree.
Usage: python3 exh.py n"""
import sys, subprocess, networkx as nx
from collections import Counter
n = int(sys.argv[1])
trees = list(nx.nonisomorphic_trees(n))
lines, meta = [], []
for t, T in enumerate(trees):
    E = " ".join(f"{u} {v}" for u, v in T.edges())
    for r in T.nodes():
        lines.append(f"{n} {r} {E}"); meta.append((t, r, T.degree(r)))
out = subprocess.run(["./rsolve", "d", "200000000"], input="\n".join(lines) + "\n", capture_output=True, text=True).stdout.split("\n")
res = Counter(); bydeg = Counter(); cap = 0; bad = 0
maxdeg_ok = [False] * len(trees)
for (t, r, dg), o in zip(meta, out):
    st = o.split()[0]
    if st == "BADWITNESS": bad += 1
    if st == "CAP": cap += 1
    if st == "NOT": res["not"] += 1; bydeg[dg] += 1
    if st == "ANCHOR" and dg == max(dict(trees[t].degree()).values()): maxdeg_ok[t] = True
print(f"n={n} trees={len(trees)} vertices={len(meta)} nonanchor_vertices={res['not']} by_degree={dict(sorted(bydeg.items()))} "
      f"trees_without_maxdeg_anchor={maxdeg_ok.count(False)} CAP={cap} BADWITNESS={bad}")
