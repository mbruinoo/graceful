# referee check of claim 2 (BFS construction), written from the statement.
import itertools, random, sys
from collections import deque
def check(n, adj, r):
    sig = {r: 0}; dep = {r: 0}; par = {r: None}; q = deque([r])
    while q:
        v = q.popleft()
        for w in adj[v]:
            if w not in sig:
                sig[w] = len(sig); dep[w] = dep[v] + 1; par[w] = v; q.append(w)
    assert len(sig) == n
    me = max(sig[v] for v in sig if dep[v] % 2 == 0)
    mo = max(sig[v] for v in sig if dep[v] % 2 == 1)
    N = 1 + me + mo
    f = {v: (1 + sig[v] if dep[v] % 2 == 0 else N + 1 - sig[v]) for v in sig}
    ok = N <= 2 * n - 2 and f[r] == 1 and len(set(f.values())) == n and all(1 <= x <= N for x in f.values())
    ln = {v: abs(f[v] - f[par[v]]) for v in sig if v != r}
    ok = ok and len(set(ln.values())) == n - 1 and min(ln.values()) >= 1
    ok = ok and all(ln[v] < ln[par[v]] for v in ln if par[v] != r)
    return ok, N
def from_prufer(p, n):
    deg = [1] * n
    for x in p: deg[x] += 1
    adj = [[] for _ in range(n)]
    p = list(p)
    import heapq
    leaves = [i for i in range(n) if deg[i] == 1]; heapq.heapify(leaves)
    for x in p:
        l = heapq.heappop(leaves); adj[l].append(x); adj[x].append(l)
        deg[x] -= 1
        if deg[x] == 1: heapq.heappush(leaves, x)
    a = heapq.heappop(leaves); b = heapq.heappop(leaves); adj[a].append(b); adj[b].append(a)
    return adj
tot = bad = 0; worst = 0
for n in range(2, 9):
    c = 0
    for p in itertools.product(range(n), repeat=n - 2):
        adj = from_prufer(p, n)
        for r in range(n):
            ok, N = check(n, adj, r); c += 1
            if not ok: bad += 1; print("FAIL", n, p, r)
            if N == 2 * n - 2: worst += 1
    tot += c; print("n=%d all labelled trees x roots: %d checked, fails so far %d, cases with N=2n-2 so far %d" % (n, c, bad, worst), flush=True)
random.seed(7)
mx = 0; c = 0
def fam(n, kind):
    if kind == 0: return from_prufer([random.randrange(n) for _ in range(n - 2)], n)
    adj = [[] for _ in range(n)]
    for v in range(1, n):
        if kind == 1: p = v - 1                       # path
        elif kind == 2: p = 0                          # star
        elif kind == 3: p = random.randrange(v)        # recursive
        elif kind == 4: p = (v - 1) // 2               # heap binary
        elif kind == 5: p = v - 1 if v < n // 2 else n // 2 - 1   # broom
        else: p = v - 1 if v % 2 else max(v - 2, 0)    # caterpillar-like
        adj[p].append(v); adj[v].append(p)
    for a in adj: random.shuffle(a)
    return adj
for it in range(3000):
    n = random.randint(9, 400); kind = it % 7
    adj = fam(n, kind)
    for r in ([0, n - 1, n // 2] + random.sample(range(n), 5)):
        ok, N = check(n, adj, r); c += 1; mx = max(mx, N / n)
        if not ok: bad += 1; print("FAIL", n, kind, r)
print("random/family rooted trees checked: %d, total fails %d, max N/n %.4f" % (c, bad, mx))
