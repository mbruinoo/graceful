#!/usr/bin/env python3
"""Census of Rule B (block designs): for every tree T on p <= PMAX vertices, every growth placement f of T and every
valid design, record the leaf distribution (how many blocks each vertex owns).  Each distinct (T, distribution) is an
infinite family: for every t >= 2, T with (t-1)*blocks(v) extra leaves on v has a growth placement on (p-1)t+1 vertices.
   python3 families.py [PMAX=6] [show=4]
"""
import sys
from collections import defaultdict
PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6
SHOW = int(sys.argv[2]) if len(sys.argv) > 2 else 4
def all_gp(n):
    m = n - 1; out = []
    def rec(k, used, p):
        if k == 0: out.append(dict(p)); return
        for a in range(0, m - k + 1):
            if (a in used) != (a + k in used):
                p[k] = a; rec(k - 1, used | {a, a + k}, p)
        p.pop(k, None)
    rec(m - 1, {0, m}, {m: 0}); return out
def plen_of(n, p):
    m = n - 1; plen = {0: 10**9, m: m}; used = {0, m}
    for k in range(m - 1, 0, -1):
        a, b = p[k], p[k] + k
        plen[b if a in used else a] = k; used |= {a, b}
    return plen
def designs(p, plen):
    out = []
    def rec(beta, vert):
        if beta < 0: out.append([vert[j] for j in range(p - 1)]); return
        for j in range(p - 1):
            if j in vert: continue
            for v in (j - beta, j + beta + 1):
                if 0 <= v <= p - 1 and (v == 0 or beta < plen[v]):
                    vert[j] = v; rec(beta - 1, vert); del vert[j]
    rec(p - 2, {}); return out
def mirror(p, plen):
    out = []
    for w in range(1, p + 1):
        vert = [0 if j >= w - 1 else w - 1 - j for j in range(p - 1)]
        if all(v == 0 or (j - v if v <= j else v - j - 1) < plen[v] for j, v in enumerate(vert)): out.append(vert)
    return out
def canon_weighted(n, p, w):
    adj = defaultdict(list)
    for k, a in p.items(): adj[a].append(a + k); adj[a + k].append(a)
    def enc(v, pa): return "(" + (str(w[v]) if w[v] else "") + "".join(sorted(enc(u, v) for u in adj[v] if u != pa)) + ")"
    return min(enc(v, None) for v in range(n))
def base_tree(s): return "".join(ch for ch in s if ch in "()")
def is_cat_after(n, p, w):
    """is T plus leaves (on vertices with w>0) a caterpillar?"""
    adj = defaultdict(set)
    for k, a in p.items(): adj[a].add(a + k); adj[a + k].add(a)
    nonleaf = lambda v: len(adj[v]) + (1 if w[v] else 0) > 1
    return all(sum(1 for u in adj[v] if nonleaf(u)) <= 2 for v in range(n))
print("p  trees  families(all designs)  non-caterpillar  families(mirror windows)  non-caterpillar")
for p in range(2, PMAX + 1):
    fam = {}; famD = {}; trees = set()
    for f in all_gp(p):
        plen = plen_of(p, f)
        trees.add(canon_weighted(p, f, [0] * p))
        for src, store in ((designs(p, plen), fam), (mirror(p, plen), famD)):
            for vert in src:
                w = [0] * p
                for v in vert: w[v] += 1
                c = canon_weighted(p, f, w)
                if c not in store: store[c] = (is_cat_after(p, f, w), dict(f), list(vert))
    print("%d  %5d  %21d  %15d  %24d  %15d" % (p, len(trees), len(fam), sum(1 for c in fam.values() if not c[0]), len(famD), sum(1 for c in famD.values() if not c[0])))
    if p <= SHOW:
        for c in sorted(fam, key=lambda c: (base_tree(c), c)):
            cat, f, vert = fam[c]
            print("     %-28s %s  %s   e.g. T = %s, blocks owned by labels %s" % (c, "caterpillar    " if cat else "NOT caterpillar", "mirror" if c in famD else "      ",
                  " ".join("%d-%d" % (f[k], f[k] + k) for k in sorted(f, reverse=True)), vert))
print("notation: nested parentheses = T rooted somewhere; a number after '(' = number of blocks that vertex owns")
