"""Shared helpers for the independent verification suite.

Everything here is written from README sections 1, 2, 8, 11 only.
Labels are 1..n as in README section 1.
"""
import sys

def adjacency(n, edges):
    adj = {v: [] for v in range(1, n + 1)}
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return adj

def rooted_code(adj, root):
    """AHU parenthesis code of the tree rooted at `root` (iterative)."""
    parent = {root: None}
    order = [root]
    for v in order:
        for w in adj[v]:
            if w != parent[v]:
                parent[w] = v
                order.append(w)
    code = {}
    for v in reversed(order):
        code[v] = "(" + "".join(sorted(code[w] for w in adj[v] if w != parent[v])) + ")"
    return code[root]

def centres(adj):
    deg = {v: len(adj[v]) for v in adj}
    layer = [v for v in adj if deg[v] <= 1]
    left = len(adj)
    while left > 2:
        left -= len(layer)
        nxt = []
        for v in layer:
            for w in adj[v]:
                deg[w] -= 1
                if deg[w] == 1:
                    nxt.append(w)
        layer = nxt
    return layer

def canon(n, edges):
    """Isomorphism invariant of an unrooted tree (complete: equal iff isomorphic)."""
    adj = adjacency(n, edges)
    return min(rooted_code(adj, c) for c in centres(adj))

def is_tree(n, edges):
    if len(edges) != n - 1:
        return False
    par = list(range(n + 1))
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        par[ra] = rb
    return True

def connected_on_own_vertices(edges):
    """True iff the edge set is connected and acyclic (a tree on the vertices it touches)."""
    verts = set()
    for a, b in edges:
        verts.add(a); verts.add(b)
    par = {v: v for v in verts}
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        par[ra] = rb
    return len(edges) == len(verts) - 1

def is_growth_by_definition(n, edges):
    """README section 2, first form: for every k, the brackets of length >= k form a connected tree.
    Also requires that the edges are one bracket of each length 1..n-1."""
    lens = sorted(abs(a - b) for a, b in edges)
    if lens != list(range(1, n)):
        return False
    for k in range(1, n):
        if not connected_on_own_vertices([e for e in edges if abs(e[0] - e[1]) >= k]):
            return False
    return True

def run_profile(n, edges):
    """Watch the unused labels while brackets are placed longest first (README section 11).
    Returns (max number of runs, max number of runs of size >= 2, max number of size-1 runs
    seen at a moment where the big-run count is <= 1 ... ) as a list of per-moment (runs, bigruns)."""
    used = [False] * (n + 2)
    prof = []
    for a, b in sorted(edges, key=lambda e: -abs(e[0] - e[1])):
        used[a] = used[b] = True
        runs = big = 0
        i = 1
        while i <= n:
            if not used[i]:
                j = i
                while j <= n and not used[j]:
                    j += 1
                runs += 1
                if j - i >= 2:
                    big += 1
                i = j
            else:
                i += 1
        prof.append((runs, big))
    return prof

def max_runs(n, edges):
    return max(r for r, _ in run_profile(n, edges))

def skips_needed(n, edges):
    """Number of single skipped cells this build needs, or None if at some moment the unused
    labels are not 'one run together with isolated single labels'.
    Reading used (stated in REPORT.md): at every moment at most one run has size >= 2; the
    number of skips at that moment is (number of runs - 1), or 0 if there are no runs."""
    worst = 0
    for runs, big in run_profile(n, edges):
        if big > 1:
            return None
        worst = max(worst, runs - 1)
    return worst
