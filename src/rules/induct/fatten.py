#!/usr/bin/env python3
"""FATTENING STEP (explicit, no search) and its direct verification from the definition.

A deal is a list of legs; a leg is a list of signed numbers (first positive; +w = tip moves up by w,
-w = tip moves down by w), absolute values strictly decreasing along the leg.

fatten(DS, DT):  DS a valid deal on m edges (numbers 1..m), DT a valid deal on n edges.
  Put k = 2m+1.  Result: the legs of DS unchanged, plus k copies (i = -m..m) of every leg of DT.
  For x in [-m, m] let   delta(x) = -x-m  (x <= 0),   m+1-x  (x > 0)        [a permutation of -m..m]
                         tau(x)   = x - delta(x)                              [also a permutation of -m..m]
  Copy i of a leg of DT with signed numbers s_1 c_1, s_2 c_2, ... gets the numbers
        k*c_1 + i,      and for j >= 2:   k*c_j - s_j * tau(delta^(j-2)(i)),
  with the same signs s_j.  (Its j-th label is then k*(j-th label in DT) + delta^(j-1)(i).)
  The result is a valid deal on m + k*n edges.
"""
import sys, itertools

def labels(deal):
    out = []
    for leg in deal:
        c = 0; l = []
        for x in leg:
            c += x; l.append(c)
        out.append(l)
    return out

def is_valid(deal):
    """Directly from the definition."""
    m = sum(len(l) for l in deal)
    nums = sorted(abs(x) for l in deal for x in l)
    if nums != list(range(1, m + 1)): return False
    seen = set()
    for leg in deal:
        if not leg: return False
        if leg[0] <= 0: return False
        if any(abs(leg[j]) <= abs(leg[j + 1]) for j in range(len(leg) - 1)): return False
        c = 0
        for x in leg:
            c += x
            if c < 1 or c > m or c in seen: return False
            seen.add(c)
    return True

def fatten(DS, DT):
    m = sum(len(l) for l in DS); k = 2 * m + 1
    delta = lambda x: (-x - m) if x <= 0 else (m + 1 - x)
    tau = lambda x: x - delta(x)
    out = [list(l) for l in DS]
    for leg in DT:
        for i in range(-m, m + 1):
            new = [k * leg[0] + i]
            E = i
            for x in leg[1:]:
                s = 1 if x > 0 else -1
                new.append(s * (k * abs(x) - s * tau(E)))
                E = delta(E)
            out.append(new)
    return out

def add_leaf(D):
    m = sum(len(l) for l in D)
    return [list(l) for l in D] + [[m + 1]]

def path(L):
    """single leg of length L, zigzag: numbers L, L-1, .., 1 alternately up and down."""
    return [[(L - j) * (1 if j % 2 == 0 else -1) for j in range(L)]]

def star(j):
    return [[x] for x in range(j, 0, -1)]

def shape(D):
    return tuple(sorted((len(l) for l in D), reverse=True))

def read_deals(m):
    """all valid deals on m edges from ./enum_deals"""
    import subprocess, os
    here = os.path.dirname(os.path.abspath(__file__))
    out = subprocess.run([os.path.join(here, 'enum_deals'), str(m)], capture_output=True, text=True).stdout
    res = []
    for line in out.splitlines():
        legs = line.split('|')[1].split(';')
        res.append([[int(x) for x in l.split()] for l in legs])
    return res

if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('pairs', 'all'):
        # every pair (valid deal on m edges, valid deal on n edges) with m + (2m+1) n <= BOUND
        BOUND = int(sys.argv[2]) if len(sys.argv) > 2 else 60
        allD = {0: [[]]}
        for m in range(1, 9): allD[m] = read_deals(m)
        tot = 0
        for m in range(0, 9):
            for n in range(1, 9):
                if m + (2 * m + 1) * n > BOUND: continue
                cnt = 0
                for DS in allD[m]:
                    assert m == 0 or is_valid(DS)
                    for DT in allD[n]:
                        R = fatten(DS, DT)
                        assert is_valid(R), (DS, DT)
                        cnt += 1
                tot += cnt
                print(f"m={m} n={n}: {cnt} pairs of deals, result on {m+(2*m+1)*n} edges: all valid")
        print("pairs checked:", tot)
    if what in ('family', 'all'):
        # the closed-form family  S(L^(2j+1), 1^j):  star with j leaves fattened by a path of length L
        MAX = 400; c = 0
        for j in range(0, 200):
            for L in range(1, 200):
                M = j + (2 * j + 1) * L
                if M > MAX: continue
                R = fatten(star(j), path(L))
                assert is_valid(R) and shape(R) == tuple([L] * (2 * j + 1) + [1] * j) or L == 1
                assert is_valid(R)
                c += 1
        print(f"S(L^(2j+1),1^j): all {c} members with at most {MAX} edges valid")
        # equal legs: S(L^(2L+2)) = path(L) fattened by path(L), and the iterates K -> K + (2KL+1)
        for L in range(1, 40):
            D = path(L); K = 1; ks = [1]
            while True:
                m = K * L
                if m + (2 * m + 1) * L > 3000: break
                D = fatten(D, path(L)); K = K + 2 * m + 1; ks.append(K)
                assert is_valid(D) and shape(D) == tuple([L] * K)
            if L <= 8 or L % 10 == 0: print(f"L={L}: S(L^K) valid for K in {ks}")
