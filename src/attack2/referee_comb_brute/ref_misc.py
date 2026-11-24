#!/usr/bin/env python3
"""Referee: Lemmas D, G, S on all stored certificates; mirror-comb search (Lemma M form); counts."""
import sys, gzip, glob
from collections import Counter
from ref_verify import parse, comb_ok, multisets

def lemmas(files):
    n = 0; nS = 0
    for f in files:
        for line in gzip.open(f, 'rt'):
            if not line.startswith('S '): continue
            S, w, y, hubs, W = parse(line); S = sorted(S, reverse=True); n += 1
            k = len(S)
            assert sum((len(U) + 2) * h for h, U in hubs) == k * y, ("G fails", line)
            hubs2 = [(h, sorted(y - h - u for u in U)) for h, U in hubs]; W2 = sorted(y - x for x in W)
            assert comb_ok(S, w, y, hubs2, W2) is None, ("D fails", line)
            if w == 0:
                one = [U for h, U in hubs if h == 1]
                if one:
                    S2 = list(S); S2.remove(len(one[0]))
                    if S2 and max(S2) >= 1 or S2:
                        e = comb_ok(sorted(S2, reverse=True), len(one[0]), y - 1, [(h - 1, U) for h, U in hubs if h != 1], one[0])
                        assert e is None, ("S fails", line, e); nS += 1
    print("Lemma G identity and Lemma D reflection hold on %d certificates; Lemma S on %d (w=0, hub at 1)" % (n, nS))

def mirror_exists(S, w):
    """heads t_i (distinct), teeth symmetric in [1,t-1], W symmetric about y/2; all partition [1,y-1]"""
    y = 1 + len(S) + sum(S) + w
    if w % 2 == 1 and y % 2 == 1: return False
    free = [False] + [True] * (y - 1)
    sizes = Counter(S)
    wleft = [w]
    def top():
        for x in range(y - 1, 0, -1):
            if free[x]: return x
        return 0
    def teeth(t, need, lo, cont):
        # choose 'need' more teeth for head t as symmetric pairs {u,t-u} with u>=lo, u<t-u ; middle handled by caller
        if need == 0: return cont()
        for u in range(lo, (t + 1) // 2):
            v = t - u
            if u != v and free[u] and free[v]:
                free[u] = free[v] = False
                if teeth(t, need - 2, u + 1, cont): return True
                free[u] = free[v] = True
        return False
    def rec():
        x = top()
        if x == 0: return wleft[0] == 0 and sum(sizes.values()) == 0
        # x is the largest free point: a head, or the larger member of a W pair (or the W midpoint)
        free[x] = False
        if wleft[0] > 0:
            p = y - x
            if p == x:
                wleft[0] -= 1
                if rec(): return True
                wleft[0] += 1
            elif wleft[0] >= 2 and 1 <= p and free[p]:
                free[p] = False; wleft[0] -= 2
                if rec(): return True
                free[p] = True; wleft[0] += 2
        for s in [s for s in sizes if sizes[s] > 0]:
            sizes[s] -= 1
            if s % 2 == 1:
                if x % 2 == 0 and free[x // 2]:
                    free[x // 2] = False
                    if teeth(x, s - 1, 1, rec): return True
                    free[x // 2] = True
            else:
                if teeth(x, s, 1, rec): return True
            sizes[s] += 1
        free[x] = True
        return False
    return rec()

if __name__ == "__main__":
    if sys.argv[1] == "lemmas": lemmas(sys.argv[2:])
    if sys.argv[1] == "mirror":
        S = [2] + [1] * 14
        for w in range(0, 3): print("S=2,1^14 mirror comb with w=%d:" % w, mirror_exists(S, w))
        # sanity: 2^k has mirror combs per Theorem Q
        print("sanity 2^4 w0", mirror_exists([2] * 4, 0), " 2^6 w1", mirror_exists([2] * 6, 1), " 2^6 w0", mirror_exists([2] * 6, 0), " 2^7 w2", mirror_exists([2] * 7, 2))
        N = int(sys.argv[2]); first = None
        for n in range(5, N + 1):
            no = [S for S in multisets(n) if not any(mirror_exists(list(S), w) for w in range(0, max(S) + 1))]
            print("n=%d: multisets with NO mirror comb with w<=max(S): %d of %d %s" % (n, len(no), len(multisets(n)), no[:6]), flush=True)
    if sys.argv[1] == "count":
        c = 0
        for n in range(5, 46):
            m = len(multisets(n)); c += m
            if n in (30, 44, 45): print("n=%d multisets %d cumulative (= trees of diameter 4 on n vertices) %d" % (n, m, c))
