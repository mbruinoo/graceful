"""Try to get 'd equal branches and nothing else' from Rule B.
Skeleton T = spider with d legs of length 2 (centre c, mids, tips), any growth placement of it.
Patterns of owners:  A: every mid owns 2 blocks -> d hubs with 2(t-1)+1 = 2t-1 leaves  (D((2t-1)^d))
                     M: every mid owns 1, every tip owns 1 -> branch = c - a(t-1 leaves) - b(t-1 leaves)
                     L: every tip owns 2 -> branch = c - a - b(2(t-1) leaves)
usage: python3 symdesign.py DMAX"""
import sys
from gp import *
def band(j, v): return j - v if v <= j else v - j - 1
def find_design(p, ell, quota):
    """quota[v] = number of blocks vertex v must own. Returns a valid design or None."""
    m = p - 1; own = [None] * m; q = dict(quota)
    def rec(b):
        if b < 0: return True
        for v in range(p):
            if q.get(v, 0) == 0: continue
            if v != 0 and b >= ell[v]: continue
            for j in ((v + b) if v + b <= m - 1 else None, v - b - 1):
                if j is None or j < 0 or own[j] is not None: continue
                own[j] = v; q[v] -= 1
                if rec(b - 1): return True
                own[j] = None; q[v] += 1
        return False
    return own[:] if rec(m - 1) else None
for d in range(2, int(sys.argv[1]) + 1):
    m = 2 * d; p = m + 1
    target = tree_canon([(0, i) for i in range(1, d + 1)] + [(i, i + d) for i in range(1, d + 1)])
    cnt = 0; found = {'A': None, 'M': None, 'L': None}; nA = nM = nL = 0
    for P in all_growth(m):
        E = edges(P, m)
        if tree_canon(E) != target: continue
        cnt += 1
        adj = adj_of(E); new, old, ell = info(P, m)
        centre = [v for v in adj if len(adj[v]) == d][0] if d > 2 else [v for v in adj if len(adj[v]) == 2 and all(len(adj[w]) == 2 for w in adj[v])][0]
        mids = adj[centre]; tips = [v for v in adj if v != centre and v not in mids]
        for name, quota in (('A', {v: 2 for v in mids}), ('M', {v: 1 for v in mids + tips}), ('L', {v: 2 for v in tips})):
            des = find_design(p, ell, quota)
            if des:
                if name == 'A': nA += 1
                if name == 'M': nM += 1
                if name == 'L': nL += 1
                if found[name] is None: found[name] = (fmt(P, m), des)
    print('d=%d: growth placements of S(2^%d): %d; with design A: %d, M: %d, L: %d' % (d, d, cnt, nA, nM, nL))
    for k, v in found.items():
        if v: print('    ', k, v)
    sys.stdout.flush()
