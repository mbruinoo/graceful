"""Common definitions, written from README sections 1-3 only (labels 0..m instead of 1..n).

A placement on n vertices (m = n-1 edges) is a dict/list P with P[k] = left foot of the bracket of
length k, 0 <= P[k] <= m-k; the bracket is the edge {P[k], P[k]+k}.
It is a GROWTH placement if, taking brackets longest first, each bracket after the first has exactly
one foot on a label already used (README section 2, Definition).
"""
import sys
from itertools import product

def is_growth(P, m):
    """P: list of length m+1 (index 0 unused). Straight from the definition."""
    if m == 0:
        return True
    if sorted(P[1:]) is None: pass
    if P[m] != 0: return False
    used = {0, m}
    for k in range(m - 1, 0, -1):
        a = P[k]; b = a + k
        if a < 0 or b > m: return False
        if (a in used) == (b in used): return False
        used.add(a); used.add(b)
    return True

def all_growth(m):
    """All growth placements with m edges, by direct search."""
    out = []
    if m == 0: return [[None]]
    P = [None] * (m + 1)
    P[m] = 0
    def rec(k, used):
        if k == 0:
            out.append(P[:]); return
        for a in range(0, m - k + 1):
            b = a + k
            if (a in used) != (b in used):
                P[k] = a
                rec(k - 1, used | {a, b})
    rec(m - 1, frozenset({0, m}))
    return out

def edges(P, m):
    return [(P[k], P[k] + k) for k in range(m, 0, -1)]

def info(P, m):
    """For a growth placement: new[k] = label added by bracket k, old[k] = its used foot,
    ell[v] = length of the bracket that added label v (ell[0] undefined)."""
    used = {0}
    new = {}; old = {}; ell = {}
    for k in range(m, 0, -1):
        a = P[k]; b = a + k
        if a in used: new[k] = b; old[k] = a
        else: new[k] = a; old[k] = b
        ell[new[k]] = k
        used.add(new[k])
    return new, old, ell

def free_at(P, m, k):
    """Labels unused at time k (when exactly the brackets longer than k are placed)."""
    used = {0}
    for i in range(m, k, -1):
        used.add(P[i]); used.add(P[i] + i)
    return frozenset(range(m + 1)) - used

def adj_of(edge_list):
    adj = {}
    for a, b in edge_list:
        adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    return adj

def rooted_canon(adj, r, parent=None):
    return '(' + ''.join(sorted(rooted_canon(adj, c, r) for c in adj.get(r, []) if c != parent)) + ')'

def is_tree(edge_list, nv):
    adj = adj_of(edge_list)
    if len(edge_list) != nv - 1: return False
    if nv == 1: return True
    if len(adj) != nv: return False
    start = next(iter(adj)); seen = {start}; st = [start]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    return len(seen) == nv

def tree_canon(edge_list):
    """Canonical form of an unrooted tree (root at the centre(s))."""
    if not edge_list: return '()'
    adj = adj_of(edge_list)
    deg = {v: len(adj[v]) for v in adj}
    leaves = [v for v in adj if deg[v] == 1]
    left = len(adj)
    while left > 2:
        nl = []
        for v in leaves:
            left -= 1
            for w in adj[v]:
                deg[w] -= 1
                if deg[w] == 1: nl.append(w)
            deg[v] = 0
        leaves = nl
    return min(rooted_canon(adj, c) for c in leaves)

def complement(P, m):
    return [None] + [m - k - P[k] for k in range(1, m + 1)]

def is_staircase(P, m):
    if m == 0: return True
    if P[m] != 0: return False
    return all(P[k] - P[k + 1] in (0, 1) for k in range(1, m))

def is_caterpillar(edge_list):
    adj = adj_of(edge_list)
    inner = [v for v in adj if len(adj[v]) > 1]
    return all(sum(1 for w in adj[v] if len(adj[w]) > 1) <= 2 for v in inner)

def fmt(P, m):
    return ' '.join('%d-%d' % (P[k], P[k] + k) for k in range(m, 0, -1))
