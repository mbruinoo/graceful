"""Same statistic as signsum.py but generating growth placements by depth-first search
(bracket k = n-1, ..., 1; position p_k in 1..n-k with exactly one foot already used; root = label 1),
so that n = 13 is reachable.  Prints the smallest classes with two valid sign vectors."""
import sys
from collections import defaultdict
def run(n, show=0):
    cls = defaultdict(list)
    par = {}                                   # label -> (parent label, k)
    used = [False]*(n+2)
    def canon():
        ch = defaultdict(list)
        for v, (u, k) in par.items(): ch[u].append((k, v))
        def c(v): return "(" + "".join(sorted("%d%s" % (k, c(x)) for k, x in ch[v])) + ")"
        return c(1)
    def go(k):
        if k == 0:
            cls[canon()].append(dict(par)); return
        for a in range(1, n-k+1):
            b = a+k
            if used[a] == used[b]: continue
            if used[a]: par[b] = (a, k); used[b] = True; go(k-1); used[b] = False; del par[b]
            else:       par[a] = (b, k); used[a] = True; go(k-1); used[a] = False; del par[a]
    used[1] = used[n] = True; par[n] = (1, n-1); go(n-2)
    hist = defaultdict(int); zero = 0; multi = 0
    for key, v in cls.items():
        hist[len(v)] += 1
        sg = [(-1)**sum(1 for x, (u, k) in d.items() if x < u) for d in v]
        if sum(sg) == 0: zero += 1
        if len(v) > 1 and show:
            show -= 1
            print("  example class", key)
            for d in v:
                print("    edges (parent->child:length):", " ".join("%d->%d:%d" % (u-1, x-1, k) for x, (u, k) in sorted(d.items(), key=lambda t: -t[1][1])))
    print("n=%d: (rooted tree, heap order) classes with a growth placement: %d; total placements %d; "
          "valid sign vectors -> number of classes: %s; classes with signed count 0: %d"
          % (n, len(cls), sum(len(v) for v in cls.values()), dict(sorted(hist.items())), zero))
N = int(sys.argv[1])
for n in range(4, N+1): run(n, show=2 if n == 10 else 0)
