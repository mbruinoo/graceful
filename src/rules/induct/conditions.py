#!/usr/bin/env python3
"""Exact conditions for the explicit single-deal transformations, checked on ALL valid deals with m <= MMAX edges.
Every transformation is built explicitly and validated from the definition; the stated condition is compared.
Usage: conditions.py MMAX
"""
import sys, itertools
from fatten import read_deals, labels, is_valid, shape

def sigma(D):   # per vertex: (#up moves) - (#down moves) from the centre
    return [[sum(1 if x > 0 else -1 for x in leg[:j + 1]) for j in range(len(leg))] for leg in D]
def shift(D, c): return [[x + c if x > 0 else x - c for x in leg] for leg in D]
def in_A(D):    # zigzag and every odd-depth label above every even-depth label (an alpha-labeling, centre 0)
    lab = labels(D)
    if any((leg[j] > 0) != (j % 2 == 0) for leg in D for j in range(len(leg))): return False
    hi = [lab[a][j] for a in range(len(D)) for j in range(len(D[a])) if j % 2 == 0]
    lo = [0] + [lab[a][j] for a in range(len(D)) for j in range(len(D[a])) if j % 2 == 1]
    return min(hi) > max(lo)

MMAX = int(sys.argv[1])
for m in range(1, MMAX + 1):
    deals = read_deals(m)
    st = dict(tip_pairs=0, tip_deals=0, A=0, A_shapes=set(), bm_pairs=0, bm_deals=0, bk_pairs=0, bk_deals=0, abm=0, abm_tested=0, dbl=0, dbl_legs=0)
    for D in deals:
        lab = labels(D); sg = sigma(D); r = len(D)
        # ---- TIP(i,s): all numbers +1, leg i gets the number 1 with sign s
        phi = sorted(lab[a][j] + sg[a][j] for a in range(r) for j in range(len(D[a])))
        inj = len(set(phi)) == m and phi[0] >= 1 and phi[-1] <= m + 1
        missing = (set(range(1, m + 2)) - set(phi)).pop() if inj else None
        any_tip = False
        for a in range(r):
            for s in (1, -1):
                Dn = shift(D, 1); Dn[a] = Dn[a] + [s]
                cond = inj and lab[a][-1] + sg[a][-1] + s == missing
                assert is_valid(Dn) == cond
                if cond: st['tip_pairs'] += 1; any_tip = True
        st['tip_deals'] += any_tip
        # ---- class A: the leg holding number 1 (or, if that leg has length 1 ... any leg whose tip is T or T+1) extends, staying in A
        if in_A(D):
            st['A'] += 1; st['A_shapes'].add(shape(D))
            a = next(a for a in range(r) if abs(D[a][-1]) == 1)
            s = -1 if D[a][-1] > 0 else 1
            Dn = shift(D, 1); Dn[a] = Dn[a] + [s]
            assert is_valid(Dn) and in_A(Dn)
            assert in_A(D + [[m + 1]])
        # ---- BASE-MIRROR(i): leg i gets m+1 at its base, all its old signs flipped
        # ---- BASE-KEEP(i):   leg i gets m+1 at its base, its old first number goes down, the rest keeps its signs
        bm = bk = False
        for a in range(r):
            Dn = [list(l) for l in D]; Dn[a] = [m + 1] + [-x for x in D[a]]
            cond = set(lab[a]) == set(m + 1 - x for x in lab[a])
            assert is_valid(Dn) == cond
            if cond: st['bm_pairs'] += 1; bm = True
            Dn = [list(l) for l in D]; Dn[a] = [m + 1, -D[a][0]] + D[a][1:]
            cond = 2 * D[a][0] == m + 1
            assert is_valid(Dn) == cond
            if cond: st['bk_pairs'] += 1; bk = True
        st['bm_deals'] += bm; st['bk_deals'] += bk
        # ---- ALLBASE-MIRROR(pi): leg i gets m+pi(i) at its base and is mirrored; condition: the sets m+pi(i)-A_i partition 1..m
        if r <= 6:
            st['abm_tested'] += 1; ok = False
            for pi in itertools.permutations(range(1, r + 1)):
                Dn = [[m + pi[a]] + [-x for x in D[a]] for a in range(r)]
                cond = sorted(m + pi[a] - x for a in range(r) for x in lab[a]) == list(range(1, m + 1))
                assert is_valid(Dn) == cond
                ok |= cond
            st['abm'] += ok
        # ---- DOUBLE-TIP: all numbers doubled; every leg whose tip label x is odd and x < 2*(its last number) gets the
        #      number x (down move, new label x); every other odd number below 2m becomes a new leg of length 1.  Always valid.
        Dn = [[2 * x for x in leg] for leg in D]; usedodd = set()
        for a in range(r):
            x = lab[a][-1]
            if x % 2 == 1 and x < 2 * abs(D[a][-1]): Dn[a].append(-x); usedodd.add(x); st['dbl_legs'] += 1
        Dn += [[j] for j in range(1, 2 * m, 2) if j not in usedodd]
        assert is_valid(Dn); st['dbl'] += 1
    n = len(deals)
    print(f"m={m} deals={n}: TIP some leg {st['tip_deals']} (pairs deal,leg,sign {st['tip_pairs']}); class A deals {st['A']} on {len(st['A_shapes'])} shapes {sorted(st['A_shapes'])[:6]}; "
          f"BASE-MIRROR some leg {st['bm_deals']}; BASE-KEEP some leg {st['bk_deals']}; ALLBASE-MIRROR some pi {st['abm']}/{st['abm_tested']}; DOUBLE-TIP valid {st['dbl']}/{n}, legs lengthened {st['dbl_legs']}")
