"""Does Rule B ever produce a tree made of k >= 3 equal branches at one vertex and nothing else?
Scan every growth placement of every tree T on p <= PMAX vertices and every valid design, t in TS (default 2,3).
A tree is 'equal-branch' if some vertex r has degree >= 3 and all components of T - r, rooted at the
neighbour of r, are isomorphic, and it is not a star.   usage: python3 bscan.py PMAX [t1,t2,..]"""
import sys
from collections import Counter
from gp import *
PMAX = int(sys.argv[1]); TS = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 else [2, 3]
def band(j, v): return j - v if v <= j else v - j - 1
def equal_branch(E):
    adj = adj_of(E)
    out = []
    for r in adj:
        if len(adj[r]) < 3: continue
        forms = {rooted_canon(adj, c, r) for c in adj[r]}
        if len(forms) == 1 and forms != {'()'}: out.append((len(adj[r]), forms.pop()))
    return out
hits = Counter(); ndes = 0; examples = {}
for m in range(2, PMAX):
    p = m + 1
    for P in all_growth(m):
        new, old, ell = info(P, m)
        own = [None] * m; usedb = [False] * m
        def rec(j):
            global ndes
            if j == m:
                ndes += 1
                for t in TS:
                    E = edges(P, m) + [(own[jj], ('l', jj, d)) for jj in range(m) for d in range(1, t)]
                    for k, form in equal_branch(E):
                        key = (p, t, k, form); hits[key] += 1
                        examples.setdefault(key, (fmt(P, m), own[:]))
                return
            for v in range(p):
                b = band(j, v)
                if usedb[b] or (v != 0 and b >= ell[v]): continue
                usedb[b] = True; own[j] = v; rec(j + 1); usedb[b] = False
        rec(0)
    print('p <= %d: valid designs so far %d; equal-branch products so far: %d kinds' % (p, ndes, len(hits))); sys.stdout.flush()
for key in sorted(hits):
    print('  p=%d t=%d: %d branches of shape %s   (%d designs)  e.g. %s' % (key[0], key[1], key[2], key[3], hits[key], examples[key]))
