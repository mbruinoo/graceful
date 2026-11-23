#!/usr/bin/env python3
"""Referee check of WEIGHTED FATTENING, implemented from the weights.py docstring (the task statement alone
does not define the linear system). Brute force over odd weight vectors; no linear algebra."""
import sys, itertools
sys.setrecursionlimit(10000)
exec(open(__file__.replace('wref.py', 'ref.py')).read().split("def check(")[0])

def wfatten(m, DT, ks):
    """returns None if midpoint system fails, else the new legs (DS = star(m) supplies 1..m)."""
    n = sum(map(len, DT))
    legnum = {}; leglab = {}
    for a, leg in enumerate(DT):
        t = 0
        for w in leg:
            t += w; legnum[abs(w)] = a; leglab[t] = a
    def mids(legof):
        pos = m + 1; out = {}
        for v in range(1, n+1):
            k = ks[legof[v]]; out[v] = pos + (k-1)//2; pos += k
        return out
    nm = mids(legnum); lm = mids(leglab)
    out = star(m)
    for a, leg in enumerate(DT):
        h = (ks[a]-1)//2
        delta = lambda x: -x-h if x <= 0 else h+1-x
        tau = lambda x: x - delta(x)
        acc = 0; t = 0
        for w in leg:
            s = 1 if w > 0 else -1
            acc += s*nm[abs(w)]; t += w
            if acc != lm[t]: return None
        for i in range(-h, h+1):
            new = []; E = i
            for j, w in enumerate(leg):
                s = 1 if w > 0 else -1
                if j == 0: new.append(nm[abs(w)] + i)
                else:
                    new.append(s*(nm[abs(w)] - s*tau(E))); E = delta(E)
            out.append(new)
    return out

NMAX = int(sys.argv[1]); MMAX = int(sys.argv[2]); KMAX = int(sys.argv[3])
tot = 0; noneq = 0; noneq_noleaf = 0; bad = 0
for n in range(1, NMAX+1):
    for DT in enum_deals(n):
        r = len(DT)
        if r > 5: continue
        for m in range(0, MMAX+1):
            for ks in itertools.product(range(1, KMAX+1, 2), repeat=r):
                o = wfatten(m, DT, ks)
                if o is None: continue
                tot += 1
                eq = all(k == 2*m+1 for k in ks)
                if not eq:
                    noneq += 1
                    if all(len(l) >= 2 for l in DT): noneq_noleaf += 1; print("non-equal, no leaf:", m, DT, ks)
                ok, why = valid(o)
                if not ok:
                    bad += 1
                    if bad <= 10: print("FAIL", m, DT, ks, why)
print("weighted instances satisfying system:", tot, "non-equal:", noneq, "non-equal without leaves:", noneq_noleaf, "invalid:", bad)
