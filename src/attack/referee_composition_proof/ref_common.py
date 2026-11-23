# Referee helpers, written independently of ../composition/common.py.
import random
def all_growth(n):
    """all growth labelings on 0..n as sets of edges (a,b), a<b; longest bracket first, exactly one used foot"""
    res = []
    def go(c, used, E):
        if c == 0: res.append(list(E)); return
        for a in range(n - c + 1):
            b = a + c
            if (a in used) ^ (b in used):
                go(c - 1, used | {a, b}, E + [(a, b)])
    if n == 0: return [[]]
    go(n - 1, frozenset({0, n}), [(0, n)])
    return res
def rand_growth(n, rng):
    used = {0, n}; E = [(0, n)] if n else []
    for c in range(n - 1, 0, -1):
        opts = [a for a in range(n - c + 1) if (a in used) ^ (a + c in used)]
        if not opts: return None
        a = rng.choice(opts); used |= {a, a + c}; E.append((a, a + c))
    return E
def connected(vs, E):
    vs = set(vs)
    if not vs: return True
    adj = {v: [] for v in vs}
    for a, b in E: adj[a].append(b); adj[b].append(a)
    s = [next(iter(vs))]; seen = set(s)
    while s:
        u = s.pop()
        for w in adj[u]:
            if w not in seen: seen.add(w); s.append(w)
    return seen == vs
def is_growth(E, N):
    """literal definition: labels 0..N once, lengths 1..N once, for every j brackets of length >= j connected tree"""
    if len(E) != N: return False
    V = set(x for e in E for x in e)
    if V != set(range(N + 1)): return False
    if sorted(abs(a - b) for a, b in E) != list(range(1, N + 1)): return False
    for j in range(1, N + 1):
        F = [e for e in E if abs(e[0] - e[1]) >= j]
        VF = set(x for e in F for x in e)
        if len(VF) != len(F) + 1 or not connected(VF, F): return False
    return True
def rooted(E, root):
    adj = {}
    for a, b in E: adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
    par = {root: None}; order = [root]
    for u in order:
        for w in adj.get(u, []):
            if w not in par: par[w] = u; order.append(w)
    return par, order
def canon(E, root):
    par, order = rooted(E, root)
    code = {}
    kids = {u: [] for u in order}
    for u in order:
        if par[u] is not None: kids[par[u]].append(u)
    for u in reversed(order): code[u] = tuple(sorted(code[w] for w in kids[u]))
    return code[root], len(order)
def delta(x, m): return -x - m if x <= 0 else m + 1 - x
