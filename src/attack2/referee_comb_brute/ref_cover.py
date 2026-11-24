#!/usr/bin/env python3
"""Referee: own enumeration of the closed-form families (sizes only; the theorems are tested elsewhere)
to see which diameter-4 trees with n<=N lie in a family.  Rules as listed in REPORT s10.
'under' = Z applied only to P,R,C,Q,O (w known from the statements); 'over' = Z also applied to T3/EQ with
ANY r>=threshold (their w is not in the statements I was given)."""
import sys, itertools
from collections import Counter
from ref_verify import multisets
N = int(sys.argv[1])
CAP = N - 2            # k + sum(S) + w <= N-2  (n = r+k+sum+2, r>=w)
fam = {}               # S (sorted tuple) -> set of w
def add(S, w, tag):
    S = tuple(sorted(S, reverse=True))
    if len(S) + sum(S) + w <= CAP: fam.setdefault(S, {}).setdefault(w, tag)

def Psizes(k):
    """all dicts label->size of Theorem P for k hubs within cap"""
    J = k // 2; out = []
    def rec(pre, rem):
        if len(pre) == J:
            if k % 2 == 0: out.append((list(pre), None))
            else:
                for c in range(0, rem + 1):
                    if c % 2 == 0 or c >= k: out.append((list(pre), c))
            return
        for v in range(0, rem // 2 + 1):
            pre.append(v); rec(pre, rem - 2 * v); pre.pop()
    rec([], CAP - k - (k - 1) if True else 0)
    res = []
    for bs, c in out:
        s = {}
        for g, b in enumerate(bs): s[2 * g + 1] = b; s[2 * k - 2 * g - 1] = b
        if c is not None: s[k] = c
        res.append((s, c))
    return res

for k in range(1, CAP + 1):
    labels = set(range(1, 2 * k, 2))
    Ps = Psizes(k) if 2 * k - 1 <= CAP else []
    for s, c in Ps: add(s.values(), k - 1, 'P')
    # R: rounds
    if 2 * k > CAP: continue
    rounds = []
    for B in range(1, 2 * k, 2):
        for pi in itertools.permutations(range(k)):
            hs = [B + 2 * (pi[i] - i) for i in range(k)]
            if all(h in labels for h in hs): rounds.append((B, tuple(sorted(Counter(hs).items()))))
    rounds = sorted(set(rounds))
    def recR(seq, tot):
        if seq:
            BT = seq[-1][0]
            w = k - 1 + sum(B - k for B, _ in seq)
            for s, c in Psizes(k):
                if BT < k - 1 or (c is not None and c % 2 == 1 and BT < k): continue
                s2 = dict(s)
                for _, cnts in seq:
                    for h, m in cnts: s2[h] = s2.get(h, 0) + m
                assert w >= 0
                add(s2.values(), w, 'R')
        if k + (len(seq) + 1) * k > CAP: return
        for rd in rounds:
            if seq and seq[-1][0] + rd[0] < 2 * k: continue
            recR(seq + [rd], tot + k)
    recR([], 0)

# C: block L = l..l+k-1
for k in range(1, CAP + 1):
    for l in range(1, CAP):
        w0 = 2 * (l - 1)
        if k + w0 > CAP: break
        L = list(range(l, l + k)); Ls = set(L)
        moves = set()
        rmax = min(k, CAP - k - w0)
        for r in range(1, rmax + 1):
            for pi in itertools.permutations(range(r)):
                hs = [k + pi[j] - j for j in range(r)]
                if all(h in Ls for h in hs): moves.add((0, tuple(sorted(Counter(hs).items()))))
        if k <= rmax:
            for d in range(1, CAP):
                if k + w0 + d + k > CAP: break
                for pi in itertools.permutations(range(k)):
                    hs = [k + d + pi[j] - j for j in range(k)]
                    if all(h in Ls for h in hs): moves.add((d, tuple(sorted(Counter(hs).items()))))
        moves = sorted(moves)
        seen = set()
        start = (tuple([0] * k), 0)
        stack = [start]; seen.add(start)
        while stack:
            sz, D = stack.pop()
            add(sz, w0 + D, 'C')
            for d, cnts in moves:
                s2 = list(sz)
                for h, m in cnts: s2[h - l] += m
                st = (tuple(s2), D + d)
                if k + sum(s2) + w0 + D + d <= CAP and st not in seen: seen.add(st); stack.append(st)
for k in range(1, CAP + 1):
    add([2] * k, [0, 0, 1, 2][k % 4], 'Q'); add([1] * k, [0, 0, 1][k % 3], 'O')

def covered(Sigma, mode):
    """returns tag or None"""
    Sigma = tuple(sorted(Sigma, reverse=True))
    if sum(1 for s in Sigma if s > 0) <= 2: return 'cat'
    def direct(Sg, exact):
        for r in set(Sg):
            S = list(Sg); S.remove(r); S = tuple(S)
            if not S: continue
            for w, tag in fam.get(S, {}).items():
                if (r == w) if exact else (r >= w): return tag
            if not exact or mode == 'over':
                if len(S) == 2 and S[1] >= 1 and r >= S[0]: return 'T3'
                if len(set(S)) == 1 and r >= len(S) - 1: return 'EQ'
        return None
    t = direct(Sigma, False)
    if t: return t
    z = Sigma.count(0)
    for j in range(1, z + 1):
        Sp = Sigma[:len(Sigma) - j]
        t = direct(Sp, True)
        if t: return 'Z+' + t
    return None

tot = 0
for n in range(5, N + 1):
    trees = []
    for m in range(5, n + 1):
        for S in multisets(m): trees.append(tuple(sorted(S + (S[0] + n - m,), reverse=True)))
    assert len(set(trees)) == len(trees)
    for mode in ('under', 'over'):
        un = [T for T in trees if covered(T, mode) is None]
        print("n=%d trees=%d  no rule (%s): %d %s" % (n, len(trees), mode, len(un), un[:12]))

if len(sys.argv) > 2:
    # diff against claimant's list of open patterns: file with lines of sizes
    import re
    theirs = set()
    for line in open(sys.argv[2]):
        line = line.strip()
        if re.fullmatch(r"[0-9 ]+", line): theirs.add(tuple(int(x) for x in line.split()))
    mine = set()
    for m in range(5, N + 1):
        for S in multisets(m):
            for n in range(m, N + 1):
                T = tuple(sorted(S + (S[0] + n - m,), reverse=True))
                if covered(T, 'under') is None: mine.add(T)
    print("their open patterns", len(theirs), "mine", len(mine))
    print("open for them, covered for me:")
    for T in sorted(theirs - mine, key=lambda t: (len(t) + sum(t) + 1, t)):
        # witness
        wit = None
        for r in set(T):
            S = list(T); S.remove(r); S = tuple(S)
            for w, tag in fam.get(S, {}).items():
                if r >= w: wit = (r, S, w, tag)
        z = T.count(0)
        if wit is None:
            for j in range(1, z + 1):
                Sp = T[:len(T) - j]
                for r in set(Sp):
                    S = list(Sp); S.remove(r); S = tuple(S)
                    for w, tag in fam.get(S, {}).items():
                        if r == w: wit = (r, S, w, 'Z+' + tag)
        print("  ", T, "n=%d" % (len(T) + sum(T) + 1), "witness (root, S, w, rule):", wit)
    print("open for me, covered for them:", sorted(mine - theirs)[:20])
