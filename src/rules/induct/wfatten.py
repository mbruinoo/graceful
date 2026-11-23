#!/usr/bin/env python3
"""WEIGHTED FATTENING (generalises fatten.py) and its verification from the definition.

wfatten(DS, DT, k):  DS valid deal on m edges, DT valid deal with legs 1..r, k = (k_1..k_r) positive odd integers
(k_lam may be any integer >= 0 if leg lam has length 1 ... here we only use odd ones) such that
(2m+1, k_1, .., k_r) solves the midpoint system of weights.py.  Result: legs of DS, plus k_lam copies of leg lam.
Copy i (i = -h..h, h = (k_lam-1)/2) of leg lam gets, at position j, the number
     mid(number window of the j-th edge) + e_j,   e_1 = i,  e_j = -s_j * tau_h(delta_h^(j-2)(i)),
with delta_h(x) = -x-h (x<=0), h+1-x (x>0), tau_h(x) = x - delta_h(x).
Usage: wfatten.py nmax kmax   checks every valid deal DT on <= nmax edges, every odd weight vector with entries <= kmax
       that solves the system with some m >= 0, DS = star with m leaves (and all deals DS for m <= 4).
"""
import sys, itertools
from fatten import read_deals, labels, is_valid, shape, star
from weights import system

def wfatten(DS, DT, k):
    m = sum(len(l) for l in DS); lab = labels(DT)
    legof_num = {}; legof_lab = {}
    for a, leg in enumerate(DT):
        for j, x in enumerate(leg): legof_num[abs(x)] = a; legof_lab[lab[a][j]] = a
    n = len(legof_num)
    numstart = {}; p = m
    for c in range(1, n + 1): numstart[c] = p; p += k[legof_num[c]]
    out = [list(l) for l in DS]
    for a, leg in enumerate(DT):
        h = (k[a] - 1) // 2
        delta = lambda x: (-x - h) if x <= 0 else (h + 1 - x)
        for i in range(-h, h + 1):
            new = []; E = i
            for j, x in enumerate(leg):
                s = 1 if x > 0 else -1
                midnum = numstart[abs(x)] + h + 1
                if j == 0: e = i
                else:
                    e = -s * (E - delta(E)); E = delta(E)
                new.append(s * (midnum + e))
            out.append(new)
    return out

if __name__ == '__main__':
    nmax = int(sys.argv[1]); kmax = int(sys.argv[2])
    small = {m: read_deals(m) for m in range(1, 5)}; small[0] = [[]]
    checked = 0; nonuniform = 0; shapes = set()
    for n in range(1, nmax + 1):
        for DT in read_deals(n):
            rows = system(DT); r = len(DT)
            for k in itertools.product(range(1, kmax + 1, 2), repeat=r):
                # k0 from the first non-trivial equation, then check all equations
                k0 = None
                for row in rows:
                    if row[0] != 0:
                        num = -sum(c * x for c, x in zip(row[1:], k))
                        if num % row[0]: k0 = -1
                        else: k0 = num // row[0]
                        break
                cands = [k0] if k0 is not None else list(range(1, 2 * kmax, 2))
                for k0 in cands:
                    if k0 < 1 or k0 % 2 == 0: continue
                    if any(row[0] * k0 + sum(c * x for c, x in zip(row[1:], k)) != 0 for row in rows): continue
                    m = (k0 - 1) // 2
                    for DS in (small[m] if m <= 4 else [star(m)]):
                        R = wfatten(DS, DT, k)
                        assert is_valid(R), (DS, DT, k)
                        checked += 1
                        if len(set(k) | {k0}) > 1: nonuniform += 1
                        shapes.add(shape(R))
    print(f"weighted fattenings checked: {checked} (non-uniform weights: {nonuniform}), all valid; distinct result shapes {len(shapes)}")
