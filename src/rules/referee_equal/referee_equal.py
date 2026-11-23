#!/usr/bin/env python3
"""Independent referee check of BLOCK / STACKING / TOWER, written from the rule statement only."""
import sys, time, random

def check(legs, lo, hi):
    """legs: list of (numbers, signs) ; first move from 0 up. Numbers must be exactly lo..hi once,
    decreasing on each leg; labels visited must be exactly lo..hi once. Returns None or error string."""
    seen_n = set(); seen_l = set()
    for idx, (nums, signs) in enumerate(legs):
        tip = 0
        for j, w in enumerate(nums):
            if j and nums[j-1] <= w: return f"leg {idx}: numbers not decreasing {nums}"
            if w in seen_n or not (lo <= w <= hi): return f"leg {idx}: bad number {w}"
            seen_n.add(w)
            if j == 0: tip = w
            else: tip = tip + w if signs[j] > 0 else tip - w
            if not (lo <= tip <= hi): return f"leg {idx}: label {tip} out of range"
            if tip in seen_l: return f"leg {idx}: label {tip} repeated"
            seen_l.add(tip)
    n = hi - lo + 1
    if len(seen_n) != n: return "numbers not all used"
    if len(seen_l) != n: return "labels not all visited"
    return None

def block(t, L):
    k = 2*t + 1
    legs = []
    for s in range(1, k+1):
        u = 2*s if s <= t else 2*s - k
        nums = [t + (L-1)*k + s] + [t + (L-j)*k + u for j in range(2, L+1)]
        signs = [1 if j % 2 == 0 else -1 for j in range(L)]   # up, down, up, ...
        legs.append((nums, signs))
    return legs

def closed_form_ok(t, L):
    k = 2*t+1
    for s, (nums, signs) in enumerate(block(t, L), 1):
        u = 2*s if s <= t else 2*s - k
        tip = 0
        for j, w in enumerate(nums, 1):
            tip = w if j == 1 else tip + signs[j-1]*w
            i = j // 2
            exp = t + (L-1-i)*k + s if j % 2 else i*k + s - u
            if j % 2 == 0:
                alt = i*k - s if s <= t else (i+1)*k - s
                if alt != exp: return False
            if tip != exp: return False
    return True

def tower(L, n):
    t = 0; stages = []
    for _ in range(n+1):
        stages.append(block(t, L)); t += (2*t+1)*L
    legs = [l for st in reversed(stages) for l in st]
    return legs, t

def all_deals(pattern):
    """every valid deal of spider with given leg lengths (legs distinguishable), from the definition."""
    m = sum(pattern); k = len(pattern); out = []
    nums = [[] for _ in pattern]; sg = [[] for _ in pattern]; tip = [0]*k; used = [False]*(m+1)
    def rec(w):
        if w == 0:
            out.append([(list(a), list(b)) for a, b in zip(nums, sg)]); return
        tried_empty = set()
        for i in range(k):
            if len(nums[i]) == pattern[i]: continue
            if not nums[i]:
                if pattern[i] in tried_empty: continue   # symmetry among untouched equal legs
                tried_empty.add(pattern[i]); cands = [(w, 1)]
            else:
                cands = [(tip[i]+w, 1), (tip[i]-w, -1)]
            for lab, s in cands:
                if 1 <= lab <= m and not used[lab]:
                    old = tip[i]; used[lab] = True; tip[i] = lab; nums[i].append(w); sg[i].append(s)
                    rec(w-1)
                    nums[i].pop(); sg[i].pop(); tip[i] = old; used[lab] = False
    rec(m); return out

def partitions(m, mx=None):
    if mx is None: mx = m
    if m == 0: yield []; return
    for a in range(min(m, mx), 0, -1):
        for r in partitions(m-a, a): yield [a]+r

def main():
    T0 = time.time(); fails = []
    # example
    legs, m = tower(2, 1)
    ex = sorted(tuple(l[0]) for l in legs)
    assert ex == sorted([(8,4),(9,6),(10,3),(11,5),(12,7),(2,1)]), ex
    print("example TOWER(2,1) matches statement; valid:", check(legs, 1, m) is None)
    # (1) blocks
    TB = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    c = 0
    for t in range(0, TB+1):
        for L in range(1, TB+1):
            e = check(block(t, L), t+1, t+(2*t+1)*L); c += 1
            if e: fails.append(("BLOCK", t, L, e))
            if t <= 40 and L <= 40 and not closed_form_ok(t, L): fails.append(("CLOSED", t, L))
    print(f"blocks 0<=t<={TB},1<=L<={TB}: {c} checked, fails {len(fails)}  [{time.time()-T0:.0f}s]")
    # extreme-shape blocks
    for t, L in [(0, 100000), (1, 50000), (2, 30000), (50000, 1), (30000, 2), (20000, 3), (1000, 77), (777, 100), (3, 20001)]:
        e = check(block(t, L), t+1, t+(2*t+1)*L); c += 1
        if e: fails.append(("BLOCK", t, L, e))
    print(f"extreme blocks done, fails {len(fails)}  [{time.time()-T0:.0f}s]")
    # (2) towers
    MAXM = int(sys.argv[2]) if len(sys.argv) > 2 else 400000
    cnt = 0; big = None
    for L in range(1, MAXM):
        if (2*L+2)*L > MAXM: break
        n = 0
        while True:
            K = sum((2*L+1)**i for i in range(n+1))
            if K*L > MAXM: break
            legs, m = tower(L, n)
            assert len(legs) == K and m == K*L and all(len(l[0]) == L for l in legs)
            e = check(legs, 1, m); cnt += 1
            if e: fails.append(("TOWER", L, n, e))
            if n >= 1 and (big is None or m > big[2]): big = (L, n, m, K)
            n += 1
    print(f"towers (all n>=0) with m<={MAXM}: {cnt} checked, largest {big}, fails {len(fails)}  [{time.time()-T0:.0f}s]")
    # (3) stacking on every valid deal of every spider with <= ME edges
    ME = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    npat = nd = ns = 0
    for t in range(1, ME+1):
        for pat in partitions(t):
            deals = all_deals(pat)
            for D in deals: assert check(D, 1, t) is None
            if deals: npat += 1
            nd += len(deals)
            for D in deals:
                for L in range(1, 8):
                    comb = block(t, L) + D
                    e = check(comb, 1, t + (2*t+1)*L); ns += 1
                    if e: fails.append(("STACK", pat, L, e))
    print(f"stacking: {npat} leg patterns with a deal (<= {ME} edges), {nd} deals, {ns} stacked, fails {len(fails)}  [{time.time()-T0:.0f}s]")
    # mixed-length iterated stacking (random L per stage) from a small base
    random.seed(1)
    for trial in range(300):
        t = 0; legs = []
        while True:
            L = random.randint(1, 6)
            if t + (2*t+1)*L > 60000: break
            legs = block(t, L) + legs; t += (2*t+1)*L
        e = check(legs, 1, t)
        if e: fails.append(("MIXED", trial, e))
    print(f"mixed-L iterated stacks: 300, fails {len(fails)}  [{time.time()-T0:.0f}s]")
    print("FAILS:", fails[:5] if fails else "none")

main()
