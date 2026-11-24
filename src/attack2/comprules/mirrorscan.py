"""Which trees have a growth placement satisfying the FULL mirror condition of Rule D (w = p)?
For such a tree T, Rule D + Lemma 6 give a growth placement of T with t-1 new leaves on every vertex
(the generalised corona), for every t >= 2.      usage: python3 mirrorscan.py PMAX"""
import sys
from gp import *
for m in range(1, int(sys.argv[1])):
    p = m + 1; allt = set(); good = set(); cnt = 0
    for P in all_growth(m):
        c = tree_canon(edges(P, m)); allt.add(c)
        new, old, ell = info(P, m)
        if all((ell[i] >= p - 2 * i) if 2 * i <= p - 1 else (ell[i] >= 2 * i - p + 1) for i in range(1, p)):
            good.add(c); cnt += 1
    miss = sorted(allt - good, key=len)
    print('p=%2d: trees %4d, with a full-window mirror placement %4d (mirror placements: %d)   first missing: %s' % (p, len(allt), len(good), cnt, miss[:3]))
    sys.stdout.flush()
