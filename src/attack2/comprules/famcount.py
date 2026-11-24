"""Recount of the 'families' table of Rule B: pairs (tree T, numbers of blocks lambda(v) owned by each
vertex), up to isomorphism, that admit a valid design; and those coming from a mirror window (Rule D).
'not caterpillar' refers to the product tree for t = 3.     usage: python3 famcount.py PMAX"""
import sys
from collections import Counter
from gp import *
def band(j, v): return j - v if v <= j else v - j - 1
def wcanon(adj, lam, r, par=None):
    return '(' + str(lam.get(r, 0)) + ''.join(sorted(wcanon(adj, lam, c, r) for c in adj[r] if c != par)) + ')'
def wtree(E, lam):
    adj = adj_of(E); return min(wcanon(adj, lam, r) for r in adj)
for m in range(2, int(sys.argv[1])):
    p = m + 1; fams = {}; famsD = {}
    for P in all_growth(m):
        new, old, ell = info(P, m); E = edges(P, m)
        own = [None] * m; usedb = [False] * m
        def reg(store):
            lam = Counter(own); key = (tree_canon(E), wtree(E, lam))
            if key not in store:
                prod = E + [(own[j], ('l', j, d)) for j in range(m) for d in (1, 2)]
                store[key] = is_caterpillar(prod)
        def rec(j):
            if j == m: reg(fams); return
            for v in range(p):
                b = band(j, v)
                if usedb[b] or (v != 0 and b >= ell[v]): continue
                usedb[b] = True; own[j] = v; rec(j + 1); usedb[b] = False
        rec(0)
        for w in range(1, p + 1):
            if all((ell[i] >= w - 2 * i) if 2 * i <= w - 1 else (ell[i] >= 2 * i - w + 1) for i in range(1, w)):
                own = [w - 1 - j if j < w - 1 else 0 for j in range(m)]; reg(famsD)
    print('p=%d trees %d  families %d  not caterpillars %d   from windows %d  not caterpillars %d' % (
        p, len({k[0] for k in fams}), len(fams), sum(1 for v in fams.values() if not v), len(famsD), sum(1 for v in famsD.values() if not v)))
