"""SAT formulation (PySAT) of 'tree T has a growth placement with at most R runs of unused labels, at most B
of them of size >= 2', straight from README sections 1, 2, 11.  A third, independent method for the
negative claims.  Every SAT answer is decoded and re-checked by check_cert.check_labels.

usage: python3 sat_check.py R B  < trees      (R, B integers or 'inf')   -> 'SAT'/'UNSAT' per tree
"""
import sys, itertools
from pysat.solvers import Cadical153
from pysat.card import CardEnc, EncType
from check_cert import check_labels

def solve(n, edges, R, B):
    cnt = itertools.count(1)
    L = [[next(cnt) for l in range(n + 1)] for v in range(n)]              # L[v][l], l = 1..n
    D = [[next(cnt) for k in range(n)] for e in edges]                     # D[e][k], k = 1..n-1
    U = [[next(cnt) for s in range(n)] for v in range(n)]                  # U[v][s]: v used after step s
    X = [[next(cnt) for s in range(n)] for l in range(n + 2)]              # X[l][s]: label l used after step s
    cl = []
    def exactly_one(lits):
        cl.append(list(lits))
        for a, b in itertools.combinations(lits, 2): cl.append([-a, -b])
    for v in range(n): exactly_one(L[v][1:])
    for l in range(1, n + 1): exactly_one([L[v][l] for v in range(n)])
    for e in range(n - 1): exactly_one(D[e][1:])
    for k in range(1, n): exactly_one([D[e][k] for e in range(n - 1)])
    for e, (u, w) in enumerate(edges):
        for k in range(1, n):
            for a in range(1, n + 1):
                for p, q in ((u, w), (w, u)):
                    c = [-D[e][k], -L[p][a]]
                    if a + k <= n: c.append(L[q][a + k])
                    if a - k >= 1: c.append(L[q][a - k])
                    cl.append(c)
    inc = [[] for _ in range(n)]
    for e, (u, w) in enumerate(edges): inc[u].append(e); inc[w].append(e)
    for v in range(n):
        cl.append([-U[v][0]])
        for s in range(1, n):                      # step s places the bracket of length n - s
            k = n - s
            now = [D[e][k] for e in inc[v]]
            cl.append([-U[v][s], U[v][s - 1]] + now)
            cl.append([U[v][s], -U[v][s - 1]])
            for d in now: cl.append([U[v][s], -d])
    for e, (u, w) in enumerate(edges):
        for s in range(2, n):                      # exactly one foot already used
            k = n - s
            cl.append([-D[e][k], U[u][s - 1], U[w][s - 1]])
            cl.append([-D[e][k], -U[u][s - 1], -U[w][s - 1]])
    top = next(cnt) - 1
    for s in range(1, n - 1):
        for l in range(1, n + 1):
            for v in range(n):
                cl.append([-L[v][l], -U[v][s], X[l][s]])
                cl.append([-L[v][l], U[v][s], -X[l][s]])
        starts = []; bigs = []
        for l in range(2, n + 1):
            top += 1; st = top; starts.append(st)
            cl.append([X[l][s], -X[l - 1][s], st])             # unused l after used l-1 starts a run
            if l + 1 <= n:
                top += 1; bg = top; bigs.append(bg)
                cl.append([X[l][s], -X[l - 1][s], X[l + 1][s], bg])   # ... of size >= 2
        for lits, bound in ((starts, R), (bigs, B)):
            if bound is not None and bound < len(lits):
                enc = CardEnc.atmost(lits=lits, bound=bound, top_id=top, encoding=EncType.seqcounter)
                top = max(top, enc.nv); cl.extend(enc.clauses)
    with Cadical153(bootstrap_with=cl) as sol:
        if not sol.solve(): return None
        model = set(x for x in sol.get_model() if x > 0)
    labels = [next(l for l in range(1, n + 1) if L[v][l] in model) for v in range(n)]
    r, b = check_labels(n, edges, labels)
    assert (R is None or r <= R) and (B is None or b <= B)
    return labels

if __name__ == "__main__":
    R = None if sys.argv[1] == "inf" else int(sys.argv[1])
    B = None if sys.argv[2] == "inf" else int(sys.argv[2])
    for line in sys.stdin:
        t = line.split()
        if not t: continue
        n = int(t[0]); edges = [tuple(map(int, x.split("-"))) for x in t[1:]]
        print("SAT" if solve(n, edges, R, B) else "UNSAT", flush=True)
