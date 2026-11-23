#!/usr/bin/env python3
"""Whole classes of structured trees with nmin <= n <= nmax, for the exhaustive existence search
(growfam exist).  Usage: huntsets.py CLASS [nmin nmax [bmax]]     (defaults 26 70)

  kbranch   centre joined to the roots of k >= 3 copies of B, for EVERY rooted tree B on 2..bmax vertices
            (bmax default 9)                                   name kbranch(k,b,#i)
  kbranch+  the same plus one extra pendant path of 1, 2 or 3 edges at the centre     kbranch+(k,b,#i,L)
  sph       every spherically symmetric tree: all branching sequences d_1..d_h (h >= 2, d_i >= 1, d_h >= 2)
  corona    every tree S on 3..bmax vertices (default 9); m leaves on every vertex     corona(s,#i,m)
            and a pendant path of L=2..4 edges on every vertex                         combs(s,#i,L)
  leafhubs  every tree S on 4..bmax vertices; m further leaves on every LEAF of S      leafhubs(s,#i,m)
  dbl       the relatives of the 22-vertex tree of README s.11: two hubs of m leaves joined by a path of
            P edges, pendant path of r edges at distance t from the second hub; 2<=m, 2<=P<=10, 1<=r<=4
  spider2   spiders with i legs of length a and j legs of length b  (i+j >= 3, a < b)
  spider1   spiders with k >= 3 equal legs
Caterpillars are skipped.
"""
import sys
from hubscan_lib import rooted, parents, adjOf, caterpillar, canon
def emit(name, E): print(f"{name}: " + " ".join(f"{a} {b}" for a, b in E))
def copies(B_E, b, k, extra=0):
    E = []; n = 1
    for _ in range(k):
        E.append((0, n)); E += [(n + x, n + y) for x, y in B_E]; n += b
    p = 0
    for _ in range(extra): E.append((p, n)); p = n; n += 1
    return n, E
def freeTrees(s):
    seen = set()
    for L in rooted(s):
        par = parents(L); E = [(par[i], i) for i in range(1, s)]; c = canon(adjOf(s, E))
        if c in seen: continue
        seen.add(c); yield E
cls = sys.argv[1]; nmin = int(sys.argv[2]) if len(sys.argv) > 2 else 26; nmax = int(sys.argv[3]) if len(sys.argv) > 3 else 70
bmax = int(sys.argv[4]) if len(sys.argv) > 4 else 9
def out(name, n, E):
    if nmin <= n <= nmax and not caterpillar(adjOf(n, E)): emit(name, E)
if cls in ("kbranch", "kbranch+"):
    for b in range(1, bmax + 1):
        for i, L in enumerate(rooted(b)):
            par = parents(L); BE = [(par[j], j) for j in range(1, b)]
            for k in range(3, (nmax - 1) // b + 1):
                if cls == "kbranch": n, E = copies(BE, b, k); out(f"kbranch({k},{b},#{i})", n, E)
                else:
                    for ex in (1, 2, 3): n, E = copies(BE, b, k, ex); out(f"kbranch+({k},{b},#{i},{ex})", n, E)
elif cls == "sph":
    def rec(seq, width, n):
        if len(seq) >= 2 and seq[-1] >= 2 and n >= nmin:
            E = []; level = [0]; c = 1
            for d in seq:
                nl = []
                for v in level:
                    for _ in range(d): E.append((v, c)); nl.append(c); c += 1
                level = nl
            out("sph(" + ",".join(map(str, seq)) + ")", n, E)
        d = 1
        while n + width * d <= nmax: rec(seq + [d], width * d, n + width * d); d += 1
    rec([], 1, 1)
elif cls in ("corona", "leafhubs"):
    for s in range(3, bmax + 1):
        for i, SE in enumerate(freeTrees(s)):
            adj = adjOf(s, SE)
            if cls == "corona":
                for m in range(1, nmax // s):
                    E = SE[:]; c = s
                    for v in range(s):
                        for _ in range(m): E.append((v, c)); c += 1
                    out(f"corona({s},#{i},{m})", c, E)
                for Lp in (2, 3, 4):
                    E = SE[:]; c = s
                    for v in range(s):
                        p = v
                        for _ in range(Lp): E.append((p, c)); p = c; c += 1
                    out(f"combs({s},#{i},{Lp})", c, E)
            else:
                lv = [v for v in range(s) if len(adj[v]) == 1]
                for m in range(1, nmax // len(lv) + 1):
                    E = SE[:]; c = s
                    for v in lv:
                        for _ in range(m): E.append((v, c)); c += 1
                    out(f"leafhubs({s},#{i},{m})", c, E)
elif cls == "dbl":
    for m in range(2, 35):
        for P in range(2, 11):
            for t in range(1, P):
                for r in range(1, 5):
                    n = 2 * m + P + 1 + r
                    if not (nmin <= n <= nmax): continue
                    E = [(0, 1 + j) for j in range(m)]; c = m + 1; p = [0]
                    for _ in range(P): E.append((p[-1], c)); p.append(c); c += 1
                    for _ in range(m): E.append((p[-1], c)); c += 1
                    q = p[P - t]
                    for _ in range(r): E.append((q, c)); q = c; c += 1
                    out(f"dbl({m},{P},{t},{r})", c, E)
elif cls in ("spider1", "spider2"):
    def spider(legs):
        E = []; c = 1
        for Lg in legs:
            p = 0
            for _ in range(Lg): E.append((p, c)); p = c; c += 1
        return c, E
    if cls == "spider1":
        for k in range(3, nmax):
            for Lg in range(2, nmax):
                if nmin <= 1 + k * Lg <= nmax: n, E = spider([Lg] * k); out(f"spider({k}x{Lg})", n, E)
    else:
        for a in range(1, nmax):
            for b in range(a + 1, nmax):
                for i in range(1, nmax):
                    if 1 + i * a + b > nmax: break
                    for j in range(1, nmax):
                        n = 1 + i * a + j * b
                        if n > nmax: break
                        if i + j >= 3 and n >= nmin: n, E = spider([a] * i + [b] * j); out(f"spider({i}x{a},{j}x{b})", n, E)
