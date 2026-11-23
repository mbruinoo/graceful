# Referee check of Theorem A (core fattening). Usage: claim0.py NMAX MMAX [nmin]
import sys, itertools
from base import *
NMAX = int(sys.argv[1]); MMAX = int(sys.argv[2]); NMIN = int(sys.argv[3]) if len(sys.argv) > 3 else 1

def delta(x, m): return -x - m if x <= 0 else m + 1 - x

def crosses_short(S, m):
    for a, b in S:
        if b - a <= m and a <= m and b >= m + 1: return True
    return False

def build_labelled(T, n, C, m, S, case):
    k = 2 * m + 1; I = range(-m, m + 1)
    par, dep = rooted(T, 0)
    E = []
    dC = {}
    def dist(v):
        if v in C: return 0
        if v not in dC: dC[v] = dist(par[v]) + 1
        return dC[v]
    for x in range(1, n + 1):
        p = par[x]
        if x in C:
            E.append((k * p, k * x))
            if case == 2 and x == n and p == 0: continue   # edge rz: no leaves
            for j in I:
                if j != 0: E.append((k * p, k * x + j))
        else:
            d = dist(x)
            for i in I:
                ex = i if d % 2 == 1 else delta(i, m)
                if p in C: lp = k * p
                else:
                    ep = i if (d - 1) % 2 == 1 else delta(i, m)
                    lp = k * p + ep
                E.append((lp, k * x + ex))
    if case == 1:
        E += list(S)
    else:
        sh = k * n - 2 * m - 1
        f = lambda g: g if g <= m else g + sh
        for a, b in S:
            if (a, b) == (0, 2 * m + 1): continue    # top bracket of S is the edge rz itself
            E.append((f(a), f(b)))
    return E

def build_shape(T, n, C, m, S, case):
    """T* from the verbal description, no labels. Returns edges and root."""
    par, dep = rooted(T, 0)
    E = []
    node = lambda x: ('C', x)
    cnt = 0
    for x in range(1, n + 1):
        p = par[x]
        if x in C:
            E.append((node(p), node(x)))
            if case == 2 and {p, x} == {0, n}: continue
            for j in range(2 * m):
                E.append((node(p), ('L', x, j)))
        else:
            for i in range(2 * m + 1):
                pp = node(p) if p in C else ('B', p, i)
                E.append((pp, ('B', x, i)))
    if case == 1:
        sn = lambda g: node(0) if g == 0 else ('S', g)
    else:
        sn = lambda g: node(0) if g == 0 else (node(n) if g == 2 * m + 1 else ('S', g))
    for a, b in S:
        if case == 2 and (a, b) == (0, 2 * m + 1): continue
        E.append((sn(a), sn(b)))
    return E, node(0)

tot = {1: 0, 2: 0}; fails = []
ends1 = {m: growth_labelings(m) for m in range(MMAX + 1)}
ends2 = {m: [S for S in growth_labelings(2 * m + 1) if not crosses_short(S, m)] for m in range(MMAX + 1)}
print('case-2 end pieces per m:', [len(ends2[m]) for m in range(MMAX + 1)],
      'rooted shapes:', [len({canon(S, 0) for S in ends2[m]}) for m in range(MMAX + 1)])
for n in range(NMIN, NMAX + 1):
    for T in growth_labelings(n):
        par, dep = rooted(T, 0)
        others = list(range(1, n + 1))
        for r in range(len(others) + 1):
            for sub in itertools.combinations(others, r):
                C = set(sub) | {0}
                if any(par[x] not in C for x in sub): continue
                case = 2 if n in C else 1
                for m in range(MMAX + 1):
                    k = 2 * m + 1
                    N = k * n + m if case == 1 else k * n
                    for S in (ends1[m] if case == 1 else ends2[m]):
                        tot[case] += 1
                        E = build_labelled(T, n, C, m, S, case)
                        ok = is_growth(E, N)
                        if ok:
                            SE, root = build_shape(T, n, C, m, S, case)
                            ok = (len(SE) == N and canon(E, 0) == canon(SE, root))
                            if ok and case == 2:
                                # z must carry top label kn
                                ok = any(set(e) == {0, k * n} for e in E)
                        if not ok:
                            fails.append((n, T, sorted(C), m, S, case))
                            if len(fails) <= 5: print('FAIL', fails[-1])
    print('n<=', n, 'triples', tot[1] + tot[2], 'case1', tot[1], 'case2', tot[2], 'fails', len(fails), flush=True)
