#!/usr/bin/env python3
"""Explicit deals for equal-leg spiders: the STACKING RULE.

Definitions (README section 13).  Spider, centre labelled 0, m edges.  A deal hands m, m-1, ..., 1 to the legs;
a leg's numbers are strictly decreasing; its first number moves the tip up from 0, each later number moves the
tip up or down by that amount.  Valid = every label visited lies in 1..m and none is visited twice.

BLOCK(t, L)  (t >= 0, L >= 1):  k = 2t+1 legs of length L, using exactly the numbers t+1 .. t+kL and visiting
exactly the labels t+1 .. t+kL.  Leg s (s = 1..k) receives
        first   t + (L-1)k + s,
        then    t + (L-j)k + u(s)   for j = 2..L,     u(s) = 2s if s <= t,  u(s) = 2s - k if s > t,
and moves up, down, up, down, ...           (BLOCK(0, L) is the single zigzag path L, 1, L-1, 2, ...)

STACKING.  If a spider S with t edges has a valid deal D, then S plus 2t+1 new legs of length L has the valid
deal "BLOCK(t, L) for the new legs, then D for the old ones".

TOWER(L, n): start with BLOCK(0, L) (one leg), and n times add BLOCK(t, L) with t = current number of edges.
It has K = 1 + (2L+1) + ... + (2L+1)^n legs of length L.   n = 1 gives 2L+2 legs of length L.

Everything below is checked straight from the definition by check_deal(); nothing is searched.
Usage:  rule_equal.py show L n      print the deal
        rule_equal.py verify [M]    check every tower with at most M edges (default 20000), every block with
                                    t <= 60, L <= 60, and stacking on top of every deal of every small spider
"""
import sys, itertools

def u(s, t):
    k = 2 * t + 1
    return 2 * s if s <= t else 2 * s - k

def block(t, L):
    """list of legs; a leg is a list of (number, direction) with direction +1 / -1"""
    k = 2 * t + 1
    legs = []
    for s in range(1, k + 1):
        leg = [(t + (L - 1) * k + s, +1)]
        for j in range(2, L + 1):
            leg.append((t + (L - j) * k + u(s, t), -1 if j % 2 == 0 else +1))
        legs.append(leg)
    return legs

def tower(L, n):
    legs = block(0, L); t = L
    for _ in range(n):
        legs = block(t, L) + legs
        t += (2 * t + 1) * L
    return legs

def stack(base_legs, L):
    t = sum(len(l) for l in base_legs)
    return block(t, L) + base_legs

def check_deal(legs, lo=1):
    """Check, from the definition only, that `legs` is a valid deal on the numbers lo..lo+m-1 with labels lo..lo+m-1
    (lo = 1 is an ordinary deal).  Returns None if valid, else a reason."""
    m = sum(len(l) for l in legs)
    nums = sorted(w for l in legs for w, _ in l)
    if nums != list(range(lo, lo + m)): return "numbers are not exactly lo..lo+m-1"
    seen = set()
    for l in legs:
        tip = 0; prev = None
        for idx, (w, d) in enumerate(l):
            if prev is not None and w >= prev: return "numbers of a leg not strictly decreasing"
            if idx == 0 and d != +1: return "first move must go up from 0"
            if d not in (+1, -1): return "bad direction"
            tip += d * w; prev = w
            if tip < lo or tip > lo + m - 1: return f"label {tip} out of range"
            if tip in seen: return f"label {tip} visited twice"
            seen.add(tip)
    return None

def labels(leg):
    out = []; tip = 0
    for w, d in leg: tip += d * w; out.append(tip)
    return out

def all_deals(lengths, limit=None):
    """every valid deal of the spider with the given leg lengths, by exhaustive search (used only to supply bases)"""
    k = len(lengths); m = sum(lengths); cur = [0] * k; legs = [[] for _ in range(k)]; used = [False] * (m + 1); out = []
    def rec(w):
        if w == 0:
            out.append([l[:] for l in legs]); return limit is not None and len(out) >= limit
        for i in range(k):
            if len(legs[i]) == lengths[i]: continue
            if not legs[i] and any(not legs[j] and lengths[j] == lengths[i] for j in range(i)): continue
            for d in ((+1,) if not legs[i] else (-1, +1)):
                x = cur[i] + d * w
                if x < 1 or x > m or used[x]: continue
                used[x] = True; cur[i] = x; legs[i].append((w, d))
                if rec(w - 1): return True
                legs[i].pop(); cur[i] = x - d * w; used[x] = False
        return False
    rec(m); return out

def verify(M):
    bad = 0
    # 1. every block, as a generalised deal on t+1..t+kL
    nb = 0
    for t in range(0, 61):
        for L in range(1, 61):
            r = check_deal(block(t, L), lo=t + 1); nb += 1
            if r: bad += 1; print("BLOCK FAILS", t, L, r)
    print(f"blocks: BLOCK(t,L) checked for all 0<=t<=60, 1<=L<=60 ({nb} blocks): {'all valid' if not bad else 'FAILURES'}")
    # 2. every tower with at most M edges
    nt = 0; rows = []
    L = 1
    while True:
        if (2 * L + 2) * L > M: break
        n = 1
        while True:
            K = sum((2 * L + 1) ** i for i in range(n + 1))
            if K * L > M: break
            legs = tower(L, n); r = check_deal(legs); nt += 1
            assert len(legs) == K and all(len(l) == L for l in legs)
            if r: bad += 1; print("TOWER FAILS", L, n, r)
            rows.append((L, n, K, K * L)); n += 1
        L += 1
    print(f"towers: all (L,n) with n>=1 and at most {M} edges: {nt} spiders, L up to {L-1}: {'all valid' if not bad else 'FAILURES'}")
    print("   largest few:", sorted(rows, key=lambda r: -r[3])[:4], "(L, n, legs, edges)")
    # 3. stacking on every deal of every spider with at most 9 edges (all leg-length patterns), new legs of length 1..6
    ns = 0; nsp = 0
    def parts(n, mx):
        if n == 0: yield []; return
        for x in range(min(n, mx), 0, -1):
            for p in parts(n - x, x): yield [x] + p
    for tt in range(1, 10):
        for p in parts(tt, tt):
            ds = all_deals(p)
            if not ds: continue
            nsp += 1
            for D in ds:
                for L in range(1, 7):
                    r = check_deal(stack(D, L)); ns += 1
                    if r: bad += 1; print("STACK FAILS", p, L, r)
    print(f"stacking: on every deal of every spider with <= 9 edges that has one ({nsp} spiders), new legs of length 1..6: {ns} stacked deals: {'all valid' if not bad else 'FAILURES'}")
    # 4. equal legs from searched bases: j legs of length L (deal found by search) -> j(2L+1)+1 legs of length L
    ne = 0; got = []
    for j in range(2, 7):
        for L in range(2, 9):
            if j * L > 30: continue
            ds = all_deals([L] * j, limit=1)
            if not ds: continue
            r = check_deal(stack(ds[0], L)); ne += 1; got.append((j * (2 * L + 1) + 1, L))
            if r: bad += 1; print("EQUAL STACK FAILS", j, L, r)
    print(f"searched bases: {ne} pairs (j,L) with a searched deal for j legs of length L stacked to (legs,L) = {got}: {'all valid' if not bad else 'FAILURES'}")
    print("RESULT:", "everything valid" if not bad else f"{bad} FAILURES")
    return bad

if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "show":
        L, n = int(sys.argv[2]), int(sys.argv[3]); legs = tower(L, n)
        print(f"{len(legs)} legs of length {L}, m = {len(legs)*L}:  {check_deal(legs) or 'valid deal'}")
        for l in legs:
            print("   numbers", " ".join(f"{w:3d}" for w, _ in l), "   labels", " ".join(f"{x:3d}" for x in labels(l)))
    else:
        sys.exit(1 if verify(int(sys.argv[2]) if len(sys.argv) > 2 else 20000) else 0)
