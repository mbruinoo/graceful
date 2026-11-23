"""Rooted-tree generator (level sequences), canonical form and caterpillar test, shared by hubscan.py and huntsets.py."""
import sys
def rooted(a):
    L = list(range(a))
    while True:
        yield L[:]
        p = len(L) - 1
        while p > 0 and L[p] == 1: p -= 1
        if p <= 0: return
        q = p - 1
        while L[q] != L[p] - 1: q -= 1
        for i in range(p, len(L)): L[i] = L[i - (p - q)]
def parents(L):
    par = [-1] * len(L); st = []
    for i, l in enumerate(L):
        while st and L[st[-1]] >= l: st.pop()
        if st: par[i] = st[-1]
        st.append(i)
    return par
def adjOf(n, E):
    adj = [[] for _ in range(n)]
    for a, b in E: adj[a].append(b); adj[b].append(a)
    return adj
def caterpillar(adj): return all(sum(1 for u in adj[v] if len(adj[u]) > 1) <= 2 for v in range(len(adj)))
def canon(adj):
    n = len(adj); deg = [len(a) for a in adj]; layer = [v for v in range(n) if deg[v] <= 1]; gone = [False] * n; rem = n
    while rem > 2:
        nx = []
        for v in layer:
            gone[v] = True; rem -= 1
            for u in adj[v]:
                if not gone[u]:
                    deg[u] -= 1
                    if deg[u] == 1: nx.append(u)
        layer = nx
    def enc(v, p): return "(" + "".join(sorted(enc(u, v) for u in adj[v] if u != p)) + ")"
    if len(layer) == 1: return enc(layer[0], -1)
    return "|".join(sorted([enc(layer[0], layer[1]), enc(layer[1], layer[0])]))
