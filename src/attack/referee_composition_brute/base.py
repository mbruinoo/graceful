# Referee's own primitives, written from README sections 1-2, 8 (labels from 0).
import sys
sys.setrecursionlimit(10000)

def growth_labelings(n):
    """All growth placements on labels 0..n (n edges): longest bracket first,
    each later bracket has exactly one foot on a used label.  Returns list of
    edge lists [(a,b)], a<b, in order of decreasing length."""
    if n == 0:
        return [[]]
    out = []
    def rec(c, used, edges):
        if c == 0:
            out.append(list(edges)); return
        for p in range(0, n - c + 1):
            a, b = p, p + c
            if (a in used) != (b in used):
                new = b if a in used else a
                used.add(new); edges.append((a, b))
                rec(c - 1, used, edges)
                edges.pop(); used.discard(new)
    rec(n - 1, {0, n}, [(0, n)])
    return out

def is_growth(edges, N):
    """Definition check: labels 0..N once, lengths 1..N once, brackets taken
    longest first each have exactly one foot on a used label (equivalent to
    'brackets of length >= j connected for every j')."""
    if len(edges) != N: return False
    labs = set()
    for a, b in edges: labs.add(a); labs.add(b)
    if labs != set(range(N + 1)): return False
    es = sorted(edges, key=lambda e: -abs(e[0] - e[1]))
    if [abs(a - b) for a, b in es] != list(range(N, 0, -1)): return False
    if N == 0: return True
    used = set(es[0])
    for a, b in es[1:]:
        if (a in used) == (b in used): return False
        used.add(a); used.add(b)
    # independent literal check of connectivity for every threshold j
    for j in range(1, N + 1):
        sub = [e for e in es if abs(e[0] - e[1]) >= j]
        vs = set(); adj = {}
        for a, b in sub:
            adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
        st = [sub[0][0]]; seen = {sub[0][0]}
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen: seen.add(y); st.append(y)
        if len(seen) != len(adj): return False
    return True

def adjacency(edges):
    adj = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    return adj

def rooted(edges, root):
    """parent, depth dicts."""
    adj = adjacency(edges)
    par = {root: None}; dep = {root: 0}; st = [root]
    while st:
        x = st.pop()
        for y in adj.get(x, []):
            if y not in par:
                par[y] = x; dep[y] = dep[x] + 1; st.append(y)
    return par, dep

def canon(edges, root):
    adj = adjacency(edges)
    def rec(x, p):
        return '(' + ''.join(sorted(rec(y, x) for y in adj.get(x, []) if y != p)) + ')'
    return rec(root, None)
