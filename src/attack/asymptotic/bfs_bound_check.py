#!/usr/bin/env python3
"""Check of the BFS bound: every rooted tree (T, r) on n >= 2 vertices has a
relaxed growth labeling with labels in [1, 2n-2] and f(r) = 1.

Construction. sigma = breadth-first index from r (sigma(r) = 0, queue order).
  even depth:  f(v) = 1 + sigma(v)
  odd depth:   f(v) = N + 1 - sigma(v),   N = 1 + max(sigma on even) + max(sigma on odd)
Checked from the definition (injective into [1,N], distinct edge lengths,
lengths strictly decreasing away from the root, N <= 2n-2):
  * every labelled tree on n <= 7 vertices (Pruefer sequences), every root;
  * 2000 random trees with 8 <= n <= 300, every root for n <= 40, else 5 roots.
"""
import itertools, random, sys
from collections import deque

def prufer_tree(seq, n):
    deg = [1]*n
    for x in seq: deg[x] += 1
    edges = []
    for x in seq:
        l = min(i for i in range(n) if deg[i] == 1)
        edges.append((l, x)); deg[l] -= 1; deg[x] -= 1
    a, b = [i for i in range(n) if deg[i] == 1]
    edges.append((a, b)); return edges

def bfs_label(n, edges, r):
    adj = [[] for _ in range(n)]
    for a, b in edges: adj[a].append(b); adj[b].append(a)
    par = [-1]*n; depth = [0]*n; sigma = [None]*n; q = deque([r]); sigma[r] = 0; k = 1
    while q:
        v = q.popleft()
        for u in adj[v]:
            if sigma[u] is None:
                sigma[u] = k; k += 1; par[u] = v; depth[u] = depth[v]+1; q.append(u)
    me = max(sigma[v] for v in range(n) if depth[v] % 2 == 0)
    mo = max(sigma[v] for v in range(n) if depth[v] % 2 == 1)
    N = 1 + me + mo
    f = [1+sigma[v] if depth[v] % 2 == 0 else N+1-sigma[v] for v in range(n)]
    return f, par, N

def is_relaxed_growth(n, f, par, r, N):
    if f[r] != 1 or len(set(f)) != n or min(f) < 1 or max(f) > N: return False
    lens = {}
    for v in range(n):
        if v != r: lens[v] = abs(f[v]-f[par[v]])
    if len(set(lens.values())) != n-1 or min(lens.values()) < 1: return False
    return all(par[v] == r or lens[v] < lens[par[v]] for v in lens)

cnt = 0
for n in range(2, 8):
    seqs = [()] if n == 2 else itertools.product(range(n), repeat=n-2)
    for seq in seqs:
        e = prufer_tree(seq, n)
        for r in range(n):
            f, par, N = bfs_label(n, e, r)
            assert N <= 2*n-2 and is_relaxed_growth(n, f, par, r, N), (n, e, r)
            cnt += 1
print("exhaustive: all labelled trees, n = 2..7, all roots:", cnt, "rooted trees, all pass")
random.seed(1); cnt = 0; worst = 0
for _ in range(2000):
    n = random.randint(8, 300); e = prufer_tree([random.randrange(n) for _ in range(n-2)], n)
    roots = range(n) if n <= 40 else random.sample(range(n), 5)
    for r in roots:
        f, par, N = bfs_label(n, e, r)
        assert N <= 2*n-2 and is_relaxed_growth(n, f, par, r, N)
        cnt += 1; worst = max(worst, N/n)
print("random: 2000 trees, 8 <= n <= 300:", cnt, "rooted trees, all pass; largest N/n seen: %.3f" % worst)
