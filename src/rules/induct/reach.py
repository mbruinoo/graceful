#!/usr/bin/env python3
"""Which spiders are reached by the steps that always work?
Seeds: the empty spider, single legs (path from one end, zigzag deal L, L-1, .., 1).  Stars arise by LEAF.
Steps:  LEAF      D -> D + new leg [m+1]
        FATTEN    (S, T) -> S + (2|S|+1) copies of every leg of T                (fatten.py)
        WFATTEN   (S, T, k) -> S + k_lam copies of leg lam of T, k odd solving the weight system   (wfatten.py)
        DOUBLETIP D -> all numbers doubled; any chosen legs whose tip label x is odd with x < 2*(last number) get the
                  number x as a down move; the remaining odd numbers below 2m become legs of length 1   (conditions.py)
All generated deals are re-verified from the definition.  Deals (not only shapes) are tracked, up to BOUND edges.
Usage: reach.py BOUND [w]     (w: also use WFATTEN)
"""
import sys, itertools
from fatten import is_valid, fatten, add_leaf, path, shape, labels
from wfatten import wfatten
from weights import system

BOUND = int(sys.argv[1]); USEW = len(sys.argv) > 2
def canon(D): return tuple(sorted((tuple(l) for l in D), key=lambda l: (-len(l), -l[0])))
def size(D): return sum(len(l) for l in D)
deals = {canon([])}
for L in range(1, BOUND + 1): deals.add(canon(path(L)))
def odd_solutions(T, room):
    rows = system([list(l) for l in T]); r = len(T); Ls = [len(l) for l in T]
    def rec(i, k, used):
        if i == r:
            for k0 in range(1, 2 * room + 2, 2):
                if all(row[0] * k0 + sum(c * x for c, x in zip(row[1:], k)) == 0 for row in rows): yield k0, tuple(k)
            return
        kk = 1
        while used + kk * Ls[i] + sum(Ls[i + 1:]) <= room:
            yield from rec(i + 1, k + [kk], used + kk * Ls[i]); kk += 2
    yield from rec(0, [], 0)
changed = True
while changed:
    changed = False
    cur = list(deals)
    for D in cur:
        m = size(D)
        if m + 1 <= BOUND:
            R = canon(add_leaf([list(l) for l in D]))
            if R not in deals: assert is_valid(R); deals.add(R); changed = True
    for D in cur:
        m = size(D)
        if 0 < 2 * m <= BOUND:
            lab = labels([list(l) for l in D])
            elig = [a for a in range(len(D)) if lab[a][-1] % 2 == 1 and lab[a][-1] < 2 * abs(D[a][-1])]
            for sub in itertools.chain.from_iterable(itertools.combinations(elig, t) for t in range(1, len(elig) + 1)):
                Dn = [[2 * x for x in leg] for leg in D]; usedodd = set()
                for a in sub: Dn[a].append(-lab[a][-1]); usedodd.add(lab[a][-1])
                Dn += [[j] for j in range(1, 2 * m, 2) if j not in usedodd]
                R = canon(Dn)
                if R not in deals: assert is_valid(R); deals.add(R); changed = True
    for S in cur:
        m = size(S)
        for T in cur:
            n = size(T)
            if n == 0: continue
            if m + (2 * m + 1) * n <= BOUND:
                R = canon(fatten([list(l) for l in S], [list(l) for l in T]))
                if R not in deals: assert is_valid(R); deals.add(R); changed = True
    if USEW:
        for T in cur:
            n = size(T)
            if n == 0: continue
            for k0, k in odd_solutions(T, BOUND):
                m = (k0 - 1) // 2
                if m + sum(a * len(l) for a, l in zip(k, T)) > BOUND: continue
                for S in cur:
                    if size(S) != m: continue
                    R = canon(wfatten([list(l) for l in S], [list(l) for l in T], k))
                    if R not in deals: assert is_valid(R); deals.add(R); changed = True
def partitions(n, mx=None):
    if mx is None: mx = n
    if n == 0: yield (); return
    for x in range(min(n, mx), 0, -1):
        for p in partitions(n - x, x): yield (x,) + p
reached = {}
for D in deals: reached.setdefault(size(D), set()).add(shape(D))
print("m : spiders with >=3 legs and a leg >=2 not of the form S(L,1,..,1) | reached | list of reached")
for m in range(1, BOUND + 1):
    allp = [p for p in partitions(m) if len(p) >= 3 and p[1] >= 2]
    got = sorted(p for p in reached.get(m, ()) if len(p) >= 3 and p[1] >= 2)
    print(f"m={m}: {len(allp)} | {len(got)} | " + " ".join("S(" + ",".join(map(str, p)) + ")" for p in got))
print("total deals generated:", len(deals))
