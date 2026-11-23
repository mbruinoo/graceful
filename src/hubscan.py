#!/usr/bin/env python3
"""Trees made of one or two giant hubs plus a small core, for the counterexample hunt.

  hubscan.py one a m       every rooted tree A on a vertices whose root has no leaf child, with m extra
                           leaves hung on the root (so: every tree with a vertex carrying exactly m leaves
                           and a-1 other vertices).  Name: one(a,m,#index)
  hubscan.py two s m1 m2   every tree S on s vertices and every pair of distinct leafless-after-marking
                           vertices u,v of S (up to isomorphism of the result): m1 leaves on u, m2 on v.
Caterpillars are skipped (they have staircases, Theorem 2).  Output lines are for growfam.
"""
import sys
from hubscan_lib import rooted, parents, adjOf, caterpillar, canon
def emit(name, n, E): print(f"{name}: " + " ".join(f"{a} {b}" for a, b in E))
mode = sys.argv[1]
if mode == "one":
    a, m = int(sys.argv[2]), int(sys.argv[3]); idx = 0
    for L in rooted(a):
        par = parents(L); E = [(par[i], i) for i in range(1, a)]; adj = adjOf(a, E)
        if any(len(adj[c]) == 1 for c in adj[0]): continue
        E2 = E + [(0, a + j) for j in range(m)]; idx += 1
        if caterpillar(adjOf(a + m, E2)): continue
        emit(f"one({a},{m},#{idx})", a + m, E2)
else:
    s, m1, m2 = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); seen = set(); idx = 0
    for L in rooted(s):
        par = parents(L); E = [(par[i], i) for i in range(1, s)]; adj = adjOf(s, E)
        for u in range(s):
            for v in range(s):
                if u == v or (m1 == m2 and v < u): continue
                E2 = E + [(u, s + j) for j in range(m1)] + [(v, s + m1 + j) for j in range(m2)]; adj2 = adjOf(s + m1 + m2, E2)
                # the core must carry no further leaves on u or v, so that (S,u,v) is determined by the tree
                if any(len(adj[c]) == 1 for c in adj[u]) or any(len(adj[c]) == 1 for c in adj[v]): continue
                c = canon(adj2)
                if c in seen: continue
                seen.add(c); idx += 1
                if caterpillar(adj2): continue
                emit(f"two({s},{m1},{m2},#{idx})", s + m1 + m2, E2)
