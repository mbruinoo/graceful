#!/usr/bin/env python3
"""Referee: Theorems Q and O rebuilt from the statement; pair sequences from own CP-SAT search and from
the explicit formulas quoted in REPORT s7-8 (validated here for larger orders)."""
import sys
from ortools.sat.python import cp_model
from ref_rules import chk
from ref_verify import comb_ok

def pairs_sat(n, positions):
    """pairs (a,a+d), d=1..n, exactly covering positions"""
    pos = set(positions); m = cp_model.CpModel(); v = {}
    for d in range(1, n + 1):
        for a in positions:
            if a + d in pos: v[d, a] = m.NewBoolVar('')
        m.AddExactlyOne([v[d, a] for a in positions if (d, a) in v])
    for p in positions:
        m.AddExactlyOne([v[d, a] for (d, a) in v if a == p or a + d == p])
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = 300; s.parameters.num_workers = 4
    r = s.Solve(m)
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return None
    return {d: (a, a + d) for (d, a) in v if s.Value(v[d, a])}

def is_pairs(P, n, positions):
    return sorted(P) == list(range(1, n + 1)) and all(b - a == d for d, (a, b) in P.items()) and \
        sorted(x for ab in P.values() for x in ab) == sorted(positions)

def skolem_formula(n):
    if n % 4 == 0:
        s = n // 4
        P = [(4*s+r-1, 8*s-r+1) for r in range(1, 2*s+1)] + [(r, 4*s-r-1) for r in range(1, s-1)]
        P += [(s+r+1, 3*s-r) for r in range(1, s-1)] + [(s-1, 3*s), (s, s+1), (2*s, 4*s-1), (2*s+1, 6*s)]
    else:
        s = n // 4
        P = [(4*s+r+1, 8*s-r+3) for r in range(1, 2*s+1)] + [(r, 4*s-r+1) for r in range(1, s+1)]
        P += [(s+r+2, 3*s-r+1) for r in range(1, s-1)] + [(s+1, s+2), (2*s+1, 6*s+2), (2*s+2, 4*s+1)]
    return P
def hooked_formula(n):
    if n % 4 == 2:
        s = n // 4
        P = [(r, 4*s-r+2) for r in range(1, 2*s+1)] + [(4*s+r+3, 8*s-r+4) for r in range(1, s)]
        P += [(5*s+r+2, 7*s-r+3) for r in range(1, s)] + [(2*s+1, 6*s+2), (4*s+2, 6*s+3), (4*s+3, 8*s+5), (7*s+3, 7*s+4)]
    else:
        s = (n + 1) // 4
        P = [(4*s+r, 8*s-r-2) for r in range(1, 2*s-1)] + [(r, 4*s-r-1) for r in range(1, s-1)]
        P += [(s+r+1, 3*s-r) for r in range(1, s-1)] + [(s-1, 3*s), (s, s+1), (2*s, 4*s-1), (2*s+1, 6*s-1), (4*s, 8*s-1)]
    return P
def formula_ok(P, n, positions):
    return sorted(b - a for a, b in P) == list(range(1, n + 1)) and sorted(x for ab in P for x in ab) == sorted(positions)

def mirror(y, heads, W):
    """Lemma M: heads = [(t, teeth)] -> comb hubs y-t with the same sets"""
    for t, U in heads: assert sorted(t - u for u in U) == sorted(U) and all(1 <= u <= t - 1 for u in U)
    assert sorted(y - x for x in W) == sorted(W)
    return [(y - t, U) for t, U in heads]

def Q(k, sk):
    if k % 4 in (0, 1):
        P = sk(k, range(1, 2 * k + 1)); y = 3 * k + 1
        return y, mirror(y, [(b + k, [i, a + k]) for i, (a, b) in P.items()], []), [], 0
    if k % 4 == 2:
        P = {}
        for r in range(1, k // 2 + 1):
            P[2 * r] = (k // 2 + 1 - r, k // 2 + 1 + r); P[2 * r - 1] = (3 * k // 2 + 2 - r, 3 * k // 2 + 1 + r)
        assert is_pairs(P, k, [x for x in range(1, 2 * k + 2) if x != k // 2 + 1])
        y = 3 * k + 2; W = [y // 2]
        return y, mirror(y, [(b + k, [i, a + k]) for i, (a, b) in P.items()], W), W, 1
    K = k + 1; P = sk(K, range(1, 2 * K + 1)); y = 3 * K; W = []; heads = []
    for i, (a, b) in P.items():
        if b + K == y: W = [i, a + K]
        else: heads.append((b + K, [i, a + K]))
    return y, mirror(y, heads, W), W, 2

def O(k, find):
    """find(n, positions) -> pairs"""
    def heff(K):
        j = K // 3; c = 2 * K + 1
        if K % 3 == 0:
            P = find(j, list(range(1, 2 * j + 1))) if j % 4 in (0, 1) else find(j, [x for x in range(1, 2 * j + 2) if x != 2 * j])
        else:
            P = find(j, [x for x in range(1, 2 * j + 2) if x != j + 1]) if j % 4 in (0, 3) else \
                find(j, [x for x in range(1, 2 * j + 3) if x not in (j + 1, 2 * j + 1)])
        return c, [(i, a + j, c - (b + j)) for i, (a, b) in P.items()]
    def comb(K):
        c, tr = heff(K); hubs = []
        for p, q, r in tr: hubs += [(q, [p]), (r, [q]), (p, [r])]
        if K % 3 == 1: hubs.append((c // 3, [c // 3]))
        return c, hubs
    if k == 4: return 9, [(1, [2]), (2, [6]), (4, [3]), (5, [1])], [], 0
    if k % 3 != 2:
        y, hubs = comb(k); return y, hubs, [], 0
    y, hubs = comb(k + 1)
    one = [U for h, U in hubs if h == 1]; assert len(one) == 1      # label 1 is a hub (shift lemma S)
    return y - 1, [(h - 1, U) for h, U in hubs if h != 1], one[0], 1

if __name__ == "__main__":
    KQ, KO, F = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    bad = [n for n in range(8, F) if n % 4 in (0, 1) and not formula_ok(skolem_formula(n), n, range(1, 2 * n + 1))]
    badh = [n for n in range(6, F) if n % 4 in (2, 3) and not formula_ok(hooked_formula(n), n, [x for x in range(1, 2 * n + 2) if x != 2 * n])]
    print("explicit Skolem formulas (n>=8) fail at orders:", bad[:10], " hooked (n>=6) fail at:", badh[:10], " tested orders <", F)
    cache = {}
    def find(n, positions):
        key = (n, tuple(positions))
        if key not in cache:
            if n == 0: cache[key] = {}
            else:
                P = pairs_sat(n, list(positions)); assert P is not None, ("no pairs", n); assert is_pairs(P, n, positions); cache[key] = P
        return cache[key]
    ok = True; cq = 0
    for k in range(1, KQ + 1):
        y, hubs, W, w = Q(k, find)
        assert w == [0, 0, 1, 2][k % 4]
        ok &= chk("Q k=%d" % k, [2] * k, w, y, hubs, W, a1s=(0, 1, 2, 5)); cq += 1
    print("Theorem Q: k=1..%d (own Skolem sequences by CP-SAT) ok=%s" % (KQ, ok))
    # with formulas, large k
    def fsk(n, positions):
        if n in (1, 4, 5): return find(n, positions)
        return {b - a: (a, b) for a, b in skolem_formula(n)}
    okf = True
    for k in range(1, 600):
        if k % 4 == 3 and k + 1 in (4,): pass
        y, hubs, W, w = Q(k, fsk); okf &= chk("Qf k=%d" % k, [2] * k, w, y, hubs, W, a1s=(0,))
    print("Theorem Q with explicit formulas, k=1..599 ok=%s" % okf)
    oko = True
    for k in range(1, KO + 1):
        if k == 1:   # K=1: j=0, c=3: point 1; comb y=3 hub 1 length 1
            pass
        y, hubs, W, w = O(k, find)
        assert w == [0, 0, 1][k % 3]
        oko &= chk("O k=%d" % k, [1] * k, w, y, hubs, W, a1s=(0, 1, 2, 5))
    print("Theorem O: k=1..%d (own (hooked) Skolem/Rosa sequences by CP-SAT) ok=%s" % (KO, oko))
