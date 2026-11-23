# Shared helpers for the composition checks.  Everything is tested from the definitions of README section 1:
# labels 0..N (README uses 1..N+1), one bracket of each length 1..N, the brackets form a tree, and (growth
# placement) for every k the brackets of length >= k form a connected tree.  "Anchored at r" = r carries label 0.
import itertools

def growth_labelings(N):
    """All growth placements on labels 0..N, as dict child_label -> parent_label (root 0 -> None).
    Generated straight from the definition: brackets N, N-1, ..., 1, each with exactly one foot already used."""
    out = []
    def rec(k, used, par):
        if k == 0:
            out.append(dict(par)); return
        for a in range(0, N - k + 1):
            b = a + k
            if (a in used) != (b in used):
                new, old = (b, a) if a in used else (a, b)
                par[new] = old; used.add(new)
                rec(k - 1, used, par)
                used.discard(new); del par[new]
    if N == 0:
        return [{0: None}]
    # the longest bracket is {0, N}; root is the vertex labelled 0
    rec(N - 1, {0, N}, {0: None, N: 0})
    return out

def is_growth_from_definition(edges, N):
    """edges: list of (a,b) labels.  True iff labels are 0..N, lengths are 1..N once each, and for every k the
    brackets of length >= k form a connected tree (README section 2 definition).  Independent of how it was built."""
    if len(edges) != N: return False
    lab = set()
    for a, b in edges: lab.add(a); lab.add(b)
    if lab != set(range(N + 1)): return False
    if sorted(abs(a - b) for a, b in edges) != list(range(1, N + 1)): return False
    es = sorted(edges, key=lambda e: -abs(e[0] - e[1]))
    if set(es[0]) != {0, N}: return False
    used = set(es[0])
    for a, b in es[1:]:
        if (a in used) == (b in used): return False   # must have exactly one foot on a used vertex
        used.add(a); used.add(b)
    return True

def canon_rooted(adj, root):
    """AHU canonical string of the tree given by adjacency dict, rooted at root (iterative)."""
    par = {root: None}; order = [root]
    for u in order:
        for v in adj[u]:
            if v != par[u]:
                par[v] = u; order.append(v)
    code = {}
    for u in reversed(order):
        code[u] = "(" + "".join(sorted(code[v] for v in adj[u] if v != par[u])) + ")"
    return code[root]

def adj_from_edges(edges):
    adj = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    return adj

def canon_free(adj):
    """canonical form of an unrooted tree: minimum rooted code over centres"""
    n = len(adj)
    if n == 1: return "()"
    deg = {u: len(adj[u]) for u in adj}; leaves = [u for u in adj if deg[u] <= 1]; rem = n
    while rem > 2:
        rem -= len(leaves); nl = []
        for u in leaves:
            for v in adj[u]:
                deg[v] -= 1
                if deg[v] == 1: nl.append(v)
            deg[u] = 0
        leaves = nl
    return min(canon_rooted(adj, c) for c in leaves)

def depth_of(par):
    d = {}
    def f(v):
        if v not in d: d[v] = 0 if par[v] is None else f(par[v]) + 1
        return d[v]
    for v in par: f(v)
    return d

def delta(x, m):
    return -x - m if x <= 0 else m + 1 - x
