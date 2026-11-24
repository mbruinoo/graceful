"""Small extra checks for REPORT.txt:
 (1) Lemma B1 (t = 2): growth placements on 2p-1 vertices in which every odd label is a leaf
     are exactly the Rule B products of valid designs  (counts compared, and each product re-derived).
 (2) Rule N: j = 1 forces a staircase; every cut of a staircase is clean; Lemma N1: g <= j forces U' to be a star.
usage: python3 check_misc.py [PMAX=7]"""
import sys
from gp import *
PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
def band(j, v): return j - v if v <= j else v - j - 1
for p in range(2, PMAX + 1):
    m = p - 1; M = 2 * m
    # products
    prods = set()
    for P in all_growth(m):
        new, old, ell = info(P, m)
        own = [None] * m; usedb = [False] * m
        def rec(j):
            if j == m:
                Q = [None] * (M + 1)
                for i in range(1, m + 1): Q[2 * i] = 2 * P[i]
                for jj, v in enumerate(own):
                    a, b = sorted((2 * v, 2 * jj + 1)); Q[b - a] = a
                prods.add(tuple(Q[1:])); return
            for v in range(p):
                b = band(j, v)
                if usedb[b] or (v != 0 and b >= ell[v]): continue
                usedb[b] = True; own[j] = v; rec(j + 1); usedb[b] = False
        rec(0)
    oddleaf = set()
    for Q in all_growth(M):
        deg = [0] * (M + 1)
        for k in range(1, M + 1): deg[Q[k]] += 1; deg[Q[k] + k] += 1
        if all(deg[x] == 1 for x in range(1, M, 2)): oddleaf.add(tuple(Q[1:]))
    print('p=%d: valid designs (products, t=2): %d; growth placements on %d vertices with every odd label a leaf: %d; equal sets: %s' % (p, len(prods), M + 1, len(oddleaf), prods == oddleaf))
    sys.stdout.flush()
# (2)
cnt1 = bad1 = 0; cuts = badcuts = 0; stars = nonstars = 0
for m in range(1, 8):
    for f in all_growth(m):
        st = is_staircase(f, m)
        for L in range(1, m + 1):
            jump = sorted(i for i in range(1, m + 1) if f[i] <= L - 1 and f[i] + i >= L)
            clean = jump == list(range(m - len(jump) + 1, m + 1))
            if st: cuts += 1; badcuts += not clean
            if clean and len(jump) == m: cnt1 += 1; bad1 += not st
for mh in range(1, 9):
    for h in all_growth(mh):
        new, old, ell = info(h, mh)
        for j in range(1, mh + 1):
            g = mh + 1 - j
            if sorted(new[i] for i in range(1, j)) != list(range(1, j)): continue
            if g <= j:
                U = [(h[i], h[i] + i) for i in range(j, mh + 1)]
                if all(0 in e for e in U): stars += 1
                else: nonstars += 1
print('Rule N: clean cuts jumped by every bracket: %d, of which f not a staircase: %d' % (cnt1, bad1))
print('staircases: cuts %d, not clean %d' % (cuts, badcuts))
print('Lemma N1: truncations with g <= j (h on <= 9 vertices): %d stars centred at 0, %d others' % (stars, nonstars))
