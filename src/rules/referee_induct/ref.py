#!/usr/bin/env python3
"""Referee re-implementation of the FATTENING STEP, from its statement only.
A deal = list of legs; a leg = list of signed ints, |.| strictly decreasing, first positive."""
import sys, itertools, random
from collections import Counter

def valid(deal, m=None):
    """From the definition. Returns (ok, reason)."""
    nums = sorted(abs(w) for leg in deal for w in leg)
    M = len(nums)
    if m is not None and M != m: return False, "edge count %d != %d" % (M, m)
    if nums != list(range(1, M+1)): return False, "numbers not 1..m once each"
    seen = set()
    for leg in deal:
        if not leg: return False, "empty leg"
        if leg[0] <= 0: return False, "first move not up"
        tip = 0
        prev = None
        for w in leg:
            if prev is not None and not abs(w) < prev: return False, "not decreasing"
            prev = abs(w)
            tip += w
            if not (1 <= tip <= M): return False, "label %d out of range" % tip
            if tip in seen: return False, "label %d twice" % tip
            seen.add(tip)
    return True, ""

def shape(deal): return tuple(sorted((len(l) for l in deal), reverse=True))

def fatten(DS, DT):
    m = sum(len(l) for l in DS)
    k = 2*m+1
    def delta(x): return -x-m if x <= 0 else m+1-x
    def tau(x): return x - delta(x)
    out = [list(l) for l in DS]
    for leg in DT:
        for i in range(-m, m+1):
            new = []; E = i
            for j, w in enumerate(leg):
                c = abs(w); s = 1 if w > 0 else -1
                if j == 0:
                    new.append(k*c + i)
                else:
                    # E = delta^(j-1 -1)(i) in 1-based terms: delta^(j-2)(i)
                    new.append(s*(k*c - s*tau(E)))
                    E = delta(E)
            out.append(new)
    return out

def star(j): return [[w] for w in range(j, 0, -1)]
def single(L): return [[(L-p) * (1 if p % 2 == 0 else -1) for p in range(L)]] if L > 0 else []

def family_i_formula(L, j):
    """The explicit closed form given in the statement for family (i)."""
    m = j
    def delta(x): return -x-m if x <= 0 else m+1-x
    def tau(x): return x - delta(x)
    out = star(j)
    for i in range(-j, j+1):
        leg = []; 
        for p in range(1, L+1):
            if p == 1: e = i
            else:
                x = i
                for _ in range(p-2): x = delta(x)
                e = (-1)**p * tau(x)
            num = (2*j+1)*(L-p+1) + e
            leg.append(num if p % 2 == 1 else -num)
        out.append(leg)
    return out

def enum_deals(m):
    """All valid deals on m edges (signed), by brute force from the definition."""
    res = []
    legs = []; used = [False]*(m+2)
    def rec(w):
        if w == 0:
            res.append([list(l) for l in legs]); return
        # new leg
        if not used[w]:
            used[w] = True; legs.append([w]); tips.append(w)
            rec(w-1)
            legs.pop(); tips.pop(); used[w] = False
        for idx in range(len(legs)):
            t = tips[idx]
            for s in (1, -1):
                nt = t + s*w
                if 1 <= nt <= m and not used[nt]:
                    used[nt] = True; legs[idx].append(s*w); tips[idx] = nt
                    rec(w-1)
                    legs[idx].pop(); tips[idx] = t; used[nt] = False
    tips = []
    rec(m)
    return res

def double_tip(D, choose):
    """choose(leg_index, x) -> bool: whether an eligible leg takes the number x."""
    m = sum(len(l) for l in D)
    out = []; usedodd = set()
    for idx, leg in enumerate(D):
        new = [2*w for w in leg]
        x = sum(leg)
        if x % 2 == 1 and x < 2*abs(leg[-1]) and choose(idx, x):
            new.append(-x); usedodd.add(x)
        out.append(new)
    for o in range(1, 2*m, 2):
        if o not in usedodd: out.append([o])
    return out

def leaf(D):
    m = sum(len(l) for l in D)
    return [list(l) for l in D] + [[m+1]]

def check(deal, m, what):
    ok, why = valid(deal, m)
    if not ok:
        print("FAIL", what, why, deal if m < 80 else ""); sys.exit(1)

def main():
    random.seed(1)
    # sanity: validator rejects bad things
    assert not valid([[2, 1]])[0] and not valid([[1, -2]])[0] and valid([[2, -1]])[0]
    assert not valid([[3], [2, 1]])[0]
    # 0. base deals
    for j in range(0, 200): check(star(j), j, "star")
    for L in range(0, 500): check(single(L), L, "single")
    print("base deals ok")
    # 1. all pairs of valid deals
    MAXM = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    deals = {m: enum_deals(m) for m in range(0, MAXM+1)}
    for m in deals:
        for d in deals[m]: check(d, m, "enum")
    print("deal counts", {m: len(deals[m]) for m in deals})
    for cap in (60, 10**9):
        cnt = Counter()
        for m in range(0, MAXM+1):
            for n in range(0, MAXM+1):
                M = m + (2*m+1)*n
                if M > cap: continue
                for DS in deals[m]:
                    sS = shape(DS)
                    for DT in deals[n]:
                        out = fatten(DS, DT)
                        check(out, M, ("fatten", DS, DT))
                        exp = tuple(sorted(sS + shape(DT)*(2*m+1), reverse=True))
                        if shape(out) != exp: print("FAIL shape", DS, DT); sys.exit(1)
                        cnt["all"] += 1
                        if m >= 1 and n >= 1: cnt["m,n>=1"] += 1
                        if n >= 1: cnt["n>=1"] += 1
                        if m >= 1: cnt["m>=1"] += 1
        print("pairs cap", cap, dict(cnt))
        if MAXM > 8: break
    # 2. family (i)
    c = 0
    CAP = 4000
    for L in range(1, CAP+1):
        for j in range(0, CAP):
            M = j + (2*j+1)*L
            if M > CAP: break
            d = fatten(star(j), single(L))
            check(d, M, ("fam i", L, j))
            if shape(d) != tuple(sorted([L]*(2*j+1) + [1]*j, reverse=True)): print("FAIL shape i", L, j); sys.exit(1)
            f = family_i_formula(L, j) if M <= 1500 else None
            if f is not None and sorted(map(tuple, f)) != sorted(map(tuple, d)):
                print("FAIL closed form differs from fatten", L, j); sys.exit(1)
            c += 1
    print("family (i): %d members up to %d edges ok; <=400: %d" % (c, CAP,
          sum(1 for L in range(1, 401) for j in range(0, 401) if j + (2*j+1)*L <= 400)))
    # 3. family (ii)
    c = 0; CAP2 = 20000
    for L in range(1, 200):
        d = []; K = 0
        while True:
            K2 = K*(2*L+1)+1
            if K2*L > CAP2: break
            d = fatten(d, single(L)); K = K2
            check(d, K*L, ("fam ii", L, K))
            if shape(d) != (L,)*K: print("FAIL shape ii"); sys.exit(1)
            c += 1
            if L in (2, 3, 4, 5) : print("  S(%d^%d)" % (L, K), end="")
    print("\nfamily (ii): %d iterates up to %d edges ok" % (c, CAP2))
    # 4. iterated / random compositions with larger deals
    pool = [d for m in range(0, min(MAXM, 7)+1) for d in deals[m]]
    c = 0
    for _ in range(3000):
        a = random.choice(pool); b = random.choice(pool)
        x = fatten(a, b)
        y = random.choice(pool)
        for z in (fatten(x, y), fatten(y, x)):
            if sum(map(len, z)) <= 6000:
                check(z, None, "random composite"); c += 1
    print("random composites ok", c)
    # 5. LEAF and DOUBLE-TIP on all deals
    c = 0; elig = 0
    for m in deals:
        for d in deals[m]:
            check(leaf(d), m+1, ("leaf", d))
            ne = sum(1 for l in d if sum(l) % 2 == 1 and sum(l) < 2*abs(l[-1]))
            elig += ne
            if ne <= 6:
                masks = range(1 << len(d)) if len(d) <= 6 else [0, (1 << len(d)) - 1]
            else: masks = [0, (1 << len(d)) - 1]
            for mask in masks:
                check(double_tip(d, lambda idx, x: (mask >> idx) & 1), 2*m, ("double-tip", d, mask)); c += 1
    print("LEAF ok; DOUBLE-TIP ok on %d (deal, subset) instances; eligible legs seen %d" % (c, elig))
    print("ALL OK")
main()
