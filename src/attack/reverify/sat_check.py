#!/usr/bin/env python3
"""SAT formulation (python-sat) of "tree T has a growth placement obeying a run/skip rule".
Third method, independent of gp.cpp (tree search) and enumgp.cpp (placement enumeration).

Variables
  x[v][l]   vertex v carries label l                       (bijection vertices <-> labels 1..n)
  b[k][p]   the bracket of length k sits at position p     (exactly one p in 1..n-k for each k)
  u[k][l]   label l is a foot of a bracket of length >= k
Clauses
  x[u][a] & x[v][c] -> b[|a-c|][min(a,c)]   for every tree edge uv   (so the n-1 edges use
                                            n-1 distinct lengths: T is drawn by the placement)
  u[k][l] <-> u[k+1][l] | b[k][l] | b[k][l-k]
  growth (README section 2): for k < n-1,  b[k][p] -> exactly one of u[k+1][p], u[k+1][p+k]
  shape after bracket k (README section 11), on unused = not u[k]:
     s[k][l] <-> unused(l) & (l == 1 or used(l-1))      (run starts)
     R:  at most R of the s[k][.]
     H:  at most H+1 of the s[k][.], and at most one l with s[k][l] & unused(l+1)
  symmetry breaking: leaves with a common neighbour get increasing labels.

Usage: sat_check.py treefile (R=r | H=h) [expect=file]   -> prints SAT/UNSAT per tree;
SAT models are verified with check_cert.verify; with expect=<gp output> the SAT/UNSAT answers
are compared line by line with gp's OK/NONE.
"""
import sys, time, itertools
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from check_cert import verify

def solve(n, edges, R=None, H=None):
    cnt = itertools.count(1)
    x = [[next(cnt) for l in range(n + 2)] for v in range(n)]          # x[v][l], l = 1..n
    b = {(k, p): next(cnt) for k in range(1, n) for p in range(1, n - k + 1)}
    u = {(k, l): next(cnt) for k in range(1, n) for l in range(1, n + 1)}
    cl = []
    for v in range(n):
        cl.append([x[v][l] for l in range(1, n + 1)])
        for l1 in range(1, n + 1):
            for l2 in range(l1 + 1, n + 1):
                cl.append([-x[v][l1], -x[v][l2]])
    for l in range(1, n + 1):
        cl.append([x[v][l] for v in range(n)])
        for v1 in range(n):
            for v2 in range(v1 + 1, n):
                cl.append([-x[v1][l], -x[v2][l]])
    for k in range(1, n):
        ps = [b[k, p] for p in range(1, n - k + 1)]
        cl.append(ps)
        for i in range(len(ps)):
            for j in range(i + 1, len(ps)):
                cl.append([-ps[i], -ps[j]])
    for (a, c) in edges:
        for la in range(1, n + 1):
            for lc in range(1, n + 1):
                if la != lc:
                    cl.append([-x[a][la], -x[c][lc], b[abs(la - lc), min(la, lc)]])
    for k in range(n - 1, 0, -1):
        for l in range(1, n + 1):
            srcs = []
            if k < n - 1: srcs.append(u[k + 1, l])
            if (k, l) in b: srcs.append(b[k, l])
            if (k, l - k) in b: srcs.append(b[k, l - k])
            cl.append([-u[k, l]] + srcs)
            for s in srcs: cl.append([u[k, l], -s])
        if k < n - 1:
            for p in range(1, n - k + 1):
                A, B = u[k + 1, p], u[k + 1, p + k]
                cl.append([-b[k, p], A, B]); cl.append([-b[k, p], -A, -B])
    top = next(cnt) - 1
    for k in range(n - 1, 0, -1):
        starts = []; bigs = []
        for l in range(1, n + 1):
            s = top + 1; top += 1
            lits = [-u[k, l]] + ([u[k, l - 1]] if l > 1 else [])   # s <-> all of lits
            for t in lits: cl.append([-s, t])
            cl.append([s] + [-t for t in lits])
            starts.append(s)
            if H is not None and l < n:
                g = top + 1; top += 1                               # g <-> s & unused(l+1)
                cl.append([-g, s]); cl.append([-g, -u[k, l + 1]]); cl.append([g, -s, u[k, l + 1]])
                bigs.append(g)
        bound = R if R is not None else H + 1
        if bound < len(starts):
            enc = CardEnc.atmost(lits=starts, bound=bound, top_id=top, encoding=EncType.seqcounter)
            cl.extend(enc.clauses); top = max(top, enc.nv)
        for i in range(len(bigs)):
            for j in range(i + 1, len(bigs)):
                cl.append([-bigs[i], -bigs[j]])
    # symmetry breaking on twin leaves
    adj = [[] for _ in range(n)]
    for a, c in edges: adj[a].append(c); adj[c].append(a)
    if n > 2:
        for v in range(n):
            lv = [w for w in adj[v] if len(adj[w]) == 1]
            for w1, w2 in zip(lv, lv[1:]):
                for l1 in range(1, n + 1):
                    for l2 in range(1, l1):
                        cl.append([-x[w1][l1], -x[w2][l2]])
    with Cadical153(bootstrap_with=cl) as S:
        if not S.solve():
            return None
        m = set(l for l in S.get_model() if l > 0)
    lab = [next(l for l in range(1, n + 1) if x[v][l] in m) for v in range(n)]
    return lab

def main():
    tf = sys.argv[1]; R = H = None; expect = None
    for a in sys.argv[2:]:
        if a.startswith("R="): R = int(a[2:])
        if a.startswith("H="): H = int(a[2:])
        if a.startswith("expect="): expect = [l.split()[0] for l in open(a[7:]) if l.strip()]
    sat = unsat = 0
    for i, line in enumerate(l for l in open(tf) if l.strip()):
        xs = list(map(int, line.split())); n = xs[0]
        edges = [(xs[1 + 2 * j], xs[2 + 2 * j]) for j in range(n - 1)]
        t0 = time.time()
        lab = solve(n, edges, R, H)
        if lab is None:
            unsat += 1; res = "NONE"
        else:
            err = verify(n, edges, lab, R, H)
            assert err is None, err
            sat += 1; res = "OK"
        if expect is not None:
            assert expect[i] == res, ("SAT and gp disagree", line, res, expect[i])
        else:
            print(f"{'UNSAT' if lab is None else 'SAT ' + ' '.join(map(str, lab))}   [{time.time() - t0:.1f}s]  {line.strip()}", flush=True)
    print(f"{tf} R={R} H={H}: SAT {sat}, UNSAT {unsat}" + (", agrees with gp on every tree" if expect is not None else ""))

if __name__ == "__main__":
    main()
