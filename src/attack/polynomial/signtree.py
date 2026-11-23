"""For every tree on n <= N vertices: does it have a root and heap order (README Thm 7) that admits
EXACTLY ONE valid sign vector (so that the signed count Z of signsum2.py is +-1, not 0)?
Growth placements are generated from the definition; trees are identified by an AHU canonical form."""
import sys
from collections import defaultdict
KNOWN = {4:2,5:3,6:6,7:11,8:23,9:47,10:106,11:235,12:551,13:1301}
def tree_canon(adj, n):
    deg = {v: len(adj[v]) for v in adj}; leaves = [v for v in adj if deg[v] <= 1]; left = n
    while left > 2:
        left -= len(leaves); new = []
        for v in leaves:
            for u in adj[v]:
                deg[u] -= 1
                if deg[u] == 1: new.append(u)
            deg[v] = 0
        leaves = new
    def c(v, p): return "(" + "".join(sorted(c(x, v) for x in adj[v] if x != p)) + ")"
    return min(c(v, None) for v in leaves)
def run(n):
    cls = defaultdict(int); shape = {}
    par = {}; used = [False]*(n+2)
    def go(k):
        if k == 0:
            key = tuple(sorted((kk, par[u][1] if u in par else 0) for v, (u, kk) in par.items()))
            cls[key] += 1
            if key not in shape:
                adj = defaultdict(list)
                for v, (u, kk) in par.items(): adj[v].append(u); adj[u].append(v)
                shape[key] = tree_canon(adj, n)
            return
        for a in range(1, n-k+1):
            b = a+k
            if used[a] == used[b]: continue
            if used[a]: par[b] = (a, k); used[b] = True; go(k-1); used[b] = False; del par[b]
            else:       par[a] = (b, k); used[a] = True; go(k-1); used[a] = False; del par[a]
    used[1] = used[n] = True; par[n] = (1, n-1); go(n-2)
    allt = set(shape.values()); uniq = set(shape[k] for k, c in cls.items() if c == 1)
    print("n=%d: trees with a growth placement %d (all trees: %d); trees having a heap-ordered rooting with "
          "exactly one sign vector: %d" % (n, len(allt), KNOWN[n], len(uniq)))
for n in range(4, int(sys.argv[1])+1): run(n)
