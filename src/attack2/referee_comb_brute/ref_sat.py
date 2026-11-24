#!/usr/bin/env python3
"""Referee's own CP-SAT model of an all-up comb (size classes, no hub symmetry).
solve(S,w) -> comb or None(infeasible) or 'T'(timeout).  Main: exact least w for all S with n in [lo,hi],
compare with claimant's exact log."""
import sys, gzip
from collections import Counter
from math import gcd
from functools import reduce
from ortools.sat.python import cp_model
from ref_verify import multisets, comb_ok, parse

def solve(S, w, tl=120.0, workers=1):
    k = len(S); y = 1 + k + sum(S) + w
    cls = sorted(Counter(S).items())
    m = cp_model.CpModel()
    P = range(1, y)
    x = {(c, h): m.NewBoolVar('') for c, _ in cls for h in P}
    f = {p: m.NewBoolVar('') for p in P}
    z = {}
    for c, _ in cls:
        if c == 0: continue
        for h in P:
            for u in range(1, y - h):
                z[c, h, u] = m.NewBoolVar('')
                m.AddImplication(z[c, h, u], x[c, h])
            m.Add(sum(z[c, h, u] for u in range(1, y - h)) == c * x[c, h])
    for c, mult in cls: m.Add(sum(x[c, h] for h in P) == mult)
    m.Add(sum(f.values()) == w)
    for p in P:
        m.Add(sum(x[c, p] for c, _ in cls) + f[p] + sum(z[c, h, p - h] for c, _ in cls if c for h in range(1, p)) == 1)
        m.Add(sum(x[c, y - p] for c, _ in cls) + f[p] + sum(z[c, h, p] for c, _ in cls if c for h in range(1, y - p)) == 1)
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = tl; s.parameters.num_workers = workers
    r = s.Solve(m)
    if r == cp_model.INFEASIBLE: return None
    if r not in (cp_model.OPTIMAL, cp_model.FEASIBLE): return 'T'
    hubs = [(h, [u for u in range(1, y - h) if c and s.Value(z[c, h, u])]) for c, _ in cls for h in P if s.Value(x[c, h])]
    W = [p for p in P if s.Value(f[p])]
    assert comb_ok(S, w, y, hubs, W) is None
    return (y, hubs, W)

def gbound(S):
    k = len(S); g = reduce(gcd, [s + 2 for s in S])
    w = 0
    while (k * (w + 1 - k)) % g: w += 1
    return w

def least(S):
    w = 0; note = ''
    while True:
        r = solve(S, w)
        if r == 'T': note += 'T%d ' % w
        elif r is not None: return S, w, note
        w += 1

if __name__ == "__main__":
    from multiprocessing import Pool
    lo, hi, logf = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    theirs = {}
    for line in gzip.open(logf, 'rt'):
        if line.startswith('S '):
            S, w, y, hubs, W = parse(line); theirs[tuple(sorted(S, reverse=True))] = w
    todo = [S for n in range(lo, hi + 1) for S in multisets(n)]
    dist = Counter(); mism = 0; exc = Counter(); tnotes = 0
    with Pool(4) as p:
        for S, w, note in p.imap_unordered(least, todo, chunksize=4):
            dist[w] += 1
            if note: tnotes += 1; print("TIMEOUT", S, note)
            if theirs.get(S) != w: mism += 1; print("MISMATCH", S, "mine", w, "theirs", theirs.get(S))
            gb = gbound(S)
            if w < gb: print("LEMMA G VIOLATED", S, w, gb)
            if w > gb: exc[len(S)] += 1; print("above G bound: k=%d S=%s w=%d bound=%d" % (len(S), S, w, gb))
            if w > max(S): print("ALL-UP FAILS", S, w)
    print("multisets", len(todo), "dist", sorted(dist.items()), "mismatch", mism, "timeouts", tnotes, "exceptions by k", sorted(exc.items()))
