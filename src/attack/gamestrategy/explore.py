# Exploration: growth placements of diameter-4 trees D(a_1..a_k) (centre, hubs with a_i leaves; a_i=0 = leaf of centre)
import sys, itertools
def partitions(total, k, maxv=None):
    if maxv is None: maxv = total
    if k == 0:
        if total == 0: yield ()
        return
    for first in range(min(total, maxv), -1, -1):
        for rest in partitions(total-first, k-1, first):
            yield (first,)+rest
def d4trees(n):
    for k in range(2, n):
        for a in partitions(n-1-k, k):
            if sum(1 for x in a if x > 0) >= 2: yield a
def build(a):
    par = [-1]; kind=['c']
    for i, ai in enumerate(a):
        h = len(par); par.append(0); kind.append(('h', i))
        for _ in range(ai): par.append(h); kind.append(('l', i))
    return par, kind
def solve(par, root, limit=1, sym=None):
    """growth labelings with root at label 0 (labels 0..m). returns list of label arrays"""
    n = len(par); m = n-1
    adj = [[] for _ in range(n)]
    for v, p in enumerate(par):
        if p >= 0: adj[v].append(p); adj[p].append(v)
    lab = [-1]*n; used = [False]*n; res = []
    lab[root] = 0; used[0] = True
    frontier = [(v, root) for v in adj[root]]
    def rec(k, frontier):
        if k == 0:
            res.append(lab[:]); return len(res) >= limit
        seen = set()
        for idx, (v, p) in enumerate(frontier):
            key = (lab[p], len(adj[v]))   # children of same parent with same degree are interchangeable in diam<=4 w/ this root? only safe for leaves
            if len(adj[v]) == 1:
                if key in seen: continue
                seen.add(key)
            for x in (lab[p]+k, lab[p]-k):
                if 0 <= x <= m and not used[x]:
                    lab[v] = x; used[x] = True
                    nf = frontier[:idx]+frontier[idx+1:]+[(c, v) for c in adj[v] if c != p]
                    if rec(k-1, nf): return True
                    lab[v] = -1; used[x] = False
        return False
    rec(m, frontier)
    return res
if __name__ == '__main__':
    N = int(sys.argv[1])
    for n in range(5, N+1):
        for a in d4trees(n):
            par, kind = build(a)
            roots = {}
            for v in range(n):
                kd = kind[v] if kind[v]=='c' else (kind[v][0], a[kind[v][1]])
                if kd in roots: continue
                roots[kd] = len(solve(par, v, limit=1))
            print(n, a, ' '.join(f"{k if k=='c' else k[0]+str(k[1])}:{v}" for k, v in roots.items()))
