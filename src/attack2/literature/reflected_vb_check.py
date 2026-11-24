#!/usr/bin/env python3
"""The level labelling f of Okechukwu, arXiv:2611.01340v1, eq. (3) (a 'cyclic reflection' of Van
Bussel's 2002 level labelling):  vertices in breadth-first order, v_{i,j} = j-th vertex of level i,
L_i = number of vertices on levels < i, M = 2m - h - t_h + 1,
     f(v_{i,j}) = L_i + j - i/2                 (i even),
     f(v_{i,j}) = M + 1 - L_i - j + (i-1)/2     (i odd).
Checked here from the definition, for random rooted trees: f is injective into [0, M], f(root) = 0,
edge differences are pairwise distinct, and they strictly DECREASE along every path away from the
root (the property README section 16 calls a relaxed growth labelling).
Usage: reflected_vb_check.py TRIALS MAXN
"""
import random, sys
T, MAXN = int(sys.argv[1]), int(sys.argv[2])
random.seed(1)
bad = 0; worst = 0.0
for _ in range(T):
    n = random.randint(2, MAXN)
    par = [None] + [random.randrange(i) if random.random() < .7 else max(0, i - random.randint(1, 3))
                    for i in range(1, n)]
    ch = [[] for _ in range(n)]
    for v in range(1, n): ch[par[v]].append(v)
    levels = [[0]]
    while True:
        nx = [c for u in levels[-1] for c in ch[u]]       # consecutive child blocks
        if not nx: break
        levels.append(nx)
    h = len(levels) - 1; m = n - 1; M = 2 * m - h - len(levels[-1]) + 1
    f = {}; L = 0
    for i, lev in enumerate(levels):
        for j, v in enumerate(lev):
            f[v] = L + j - i // 2 if i % 2 == 0 else M + 1 - L - j + (i - 1) // 2
        L += len(lev)
    d = {v: abs(f[v] - f[par[v]]) for v in range(1, n)}
    ok = (len(set(f.values())) == n and min(f.values()) == 0 == f[0] and max(f.values()) <= M
          and len(set(d.values())) == m
          and all(par[v] == 0 or d[v] < d[par[v]] for v in range(1, n)))
    bad += not ok; worst = max(worst, M / m)
print(f"{T} random rooted trees with 2..{MAXN} vertices: failures {bad}; largest M/m seen {worst:.3f}")
