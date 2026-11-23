#!/usr/bin/env python3
# Referee check of claim 2 (own implementation): BFS construction on ALL free trees n=2..12 x all roots,
# x several child orders (the proof must hold for any queue order), plus the line-by-line proof facts.
import sys, random, networkx as nx
from collections import deque
def run(T, r, rnd):
    n = T.number_of_nodes(); sig = {r: 0}; par = {}; dep = {r: 0}; q = deque([r]); k = 1
    while q:
        v = q.popleft(); nb = [u for u in T[v] if u not in sig]
        if rnd: random.shuffle(nb)
        for u in nb: sig[u] = k; k += 1; par[u] = v; dep[u] = dep[v] + 1; q.append(u)
    me = max(sig[v] for v in T if dep[v] % 2 == 0); mo = max(sig[v] for v in T if dep[v] % 2 == 1)
    N = 1 + me + mo; f = {v: 1 + sig[v] if dep[v] % 2 == 0 else N + 1 - sig[v] for v in T}
    assert N <= 2 * n - 2 and f[r] == 1 and len(set(f.values())) == n and all(1 <= x <= N for x in f.values())
    L = {c: abs(f[c] - f[p]) for c, p in par.items()}
    assert all(L[c] == N - sig[c] - sig[par[c]] >= 1 for c in L)          # proof step "length = N - sigma(p) - sigma(c)"
    assert len(set(L.values())) == n - 1
    assert all(par[c] == r or L[c] < L[par[c]] for c in L)
    # proof step: s(c) strictly increasing in sigma(c)
    cs = sorted(L, key=lambda c: sig[c]); s = [sig[c] + sig[par[c]] for c in cs]; assert all(a < b for a, b in zip(s, s[1:]))
    return N
cnt = 0; worst = 0
for n in range(2, 13):
    for T in nx.nonisomorphic_trees(n):
        for r in T:
            for rnd in (0, 1, 1):
                N = run(T, r, rnd); cnt += 1; worst = max(worst, N / n)
                if n >= 2 and nx.is_isomorphic(T, nx.path_graph(n)) and T.degree(r) == 1: assert N == 2 * n - 2   # bound attained
print("all free trees n=2..12, all roots, 3 queue orders:", cnt, "runs pass; max N/n = %.3f" % worst)
random.seed(7); c2 = 0
for _ in range(300):
    n = random.randint(13, 400); T = nx.random_labeled_tree(n, seed=random.randrange(10**9)) if hasattr(nx, "random_labeled_tree") else nx.random_tree(n, seed=random.randrange(10**9))
    for r in random.sample(list(T), 4): run(T, r, 1); c2 += 1
print("random trees 13..400:", c2, "runs pass")
