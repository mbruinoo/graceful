#!/usr/bin/env python3
"""WEIGHTED FATTENING: which leg multiplicities does a deal admit?

Give the centre a width k0 = 2m+1 and every leg lam of a deal DT a width k_lam (the number of parallel copies).
Stack windows: label 0 has the window [-m, m]; the labels 1..n of DT get consecutive windows above it, the window
of a label on leg lam having k_lam cells; likewise the numbers 1..n get consecutive windows starting at m+1.
The copies of a leg can be routed window to window (as in fatten.py) iff for every vertex v of DT
      mid(label window of v) = sum over the edges e_1..e_j from the centre to v of  s_t * mid(number window of e_t).
This is a homogeneous linear system in (k0, k_1, .., k_r); the all-equal vector is always a solution (fatten.py).
This script computes the solution space for every valid deal and prints those with more solutions.
Usage: weights.py mmax
"""
import sys
from fractions import Fraction
from fatten import read_deals, labels, shape

def system(D):
    r = len(D); n = sum(len(l) for l in D)
    legof_num = {}; legof_lab = {}
    lab = labels(D)
    for a, leg in enumerate(D):
        for j, x in enumerate(leg):
            legof_num[abs(x)] = a; legof_lab[lab[a][j]] = a
    def mid2(legof, val, a):          # 2*midpoint as coefficient vector over (k0,k1..kr)
        v = [0] * (r + 1); v[0] = 1
        for u in range(1, val): v[1 + legof[u]] += 2
        v[1 + a] += 1
        return v
    rows = []
    for a, leg in enumerate(D):
        acc = [0] * (r + 1)
        for j, x in enumerate(leg):
            s = 1 if x > 0 else -1
            mv = mid2(legof_num, abs(x), a)
            acc = [p + s * q for p, q in zip(acc, mv)]
            lv = mid2(legof_lab, lab[a][j], a)
            rows.append([p - q for p, q in zip(lv, acc)])
    return rows

def nullspace(rows, ncol):
    A = [[Fraction(x) for x in row] for row in rows]
    piv = []; rr = 0
    for c in range(ncol):
        p = next((i for i in range(rr, len(A)) if A[i][c] != 0), None)
        if p is None: continue
        A[rr], A[p] = A[p], A[rr]
        A[rr] = [x / A[rr][c] for x in A[rr]]
        for i in range(len(A)):
            if i != rr and A[i][c] != 0:
                f = A[i][c]; A[i] = [x - f * y for x, y in zip(A[i], A[rr])]
        piv.append(c); rr += 1
    free = [c for c in range(ncol) if c not in piv]
    basis = []
    for f in free:
        v = [Fraction(0)] * ncol; v[f] = Fraction(1)
        for i, c in enumerate(piv): v[c] = -A[i][f]
        basis.append(v)
    return basis

if __name__ == '__main__':
    mmax = int(sys.argv[1])
    for m in range(1, mmax + 1):
        hist = {}
        ex = []
        for D in read_deals(m):
            B = nullspace(system(D), len(D) + 1)
            d = len(B); hist[d] = hist.get(d, 0) + 1
            if d >= 2 and any(len(l) >= 2 for l in D): ex.append((D, B))
        print(f"m={m}: dimension histogram {sorted(hist.items())}; deals with a leg >=2 and dim>=2: {len(ex)}")
        if len(sys.argv) > 2:
            for D, B in ex:
                print("   ", shape(D), D, " basis:", [[str(x) for x in v] for v in B])
