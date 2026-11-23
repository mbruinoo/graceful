# Referee check of Theorem B (mixed bunch). Usage: claim1.py m NMAX [mode]
# mode: ok (default) | noH0 | noH12   (teeth: violate one hypothesis)
import sys, itertools, random
from base import *
m = int(sys.argv[1]); NMAX = int(sys.argv[2]); mode = sys.argv[3] if len(sys.argv) > 3 else 'ok'
k = 2 * m + 1; I = list(range(-m, m + 1))
def delta(x): return -x - m if x <= 0 else m + 1 - x
assert all(delta(delta(x)) == x for x in I)
fixed = [x for x in I if delta(x) == x]; assert len(fixed) == 1
pairs = [(x, delta(x)) for x in I if x < delta(x)]

def info(T, n):
    par, dep = rooted(T, 0)
    rootnb = frozenset(x for x in range(1, n + 1) if par[x] == 0)
    h1 = tuple(dep[l] % 2 for l in range(n + 1))
    h2 = []
    for a, b in T:
        if a == 0 or b == 0: # root edge (a<b so a==0)
            h2.append((b - a, None))
        else:
            h2.append((b - a, dep[a] % 2))   # a is the lower-labelled end
    return par, dep, rootnb, h1, tuple(sorted(h2))

def compose(fam, n, S):
    E = list(S)
    for i in I:
        T, par, dep = fam[i]
        lab = {0: 0}
        for v in range(1, n + 1):
            lab[v] = k * v + (i if dep[v] % 2 == 1 else delta(i))
        for a, b in T: E.append((lab[a], lab[b]))
    return E

def shape(fam, n, S):
    E = [(('S', a) if a else 'R', ('S', b)) for a, b in S]
    for i in I:
        T = fam[i][0]
        for a, b in T:
            E.append(((i, a) if a else 'R', (i, b)))
    return E

Ss = growth_labelings(m)
tot = 0; fails = 0; distinct_pairs = 0
for n in range(0, NMAX + 1):
    Ls = [(T,) + info(T, n) for T in growth_labelings(n)]
    N = k * n + m
    if mode == 'ok':
        groups = {}
        for L in Ls: groups.setdefault(L[3], []).append(L)
        for g in groups.values():
            # ordered pairs satisfying H1,H2
            good = [(A, B) for A in g for B in g if A[4] == B[4] and A[5] == B[5]]
            distinct_pairs += sum(1 for A, B in good if A[0] != B[0]) // 2
            for F in g:
                for choice in itertools.product(good, repeat=m):
                    fam = {fixed[0]: (F[0], F[1], F[2])}
                    for (x, y), (A, B) in zip(pairs, choice):
                        fam[x] = (A[0], A[1], A[2]); fam[y] = (B[0], B[1], B[2])
                    for S in Ss:
                        tot += 1
                        E = compose(fam, n, S)
                        ok = is_growth(E, N) and canon(E, 0) == canon(shape(fam, n, S), 'R')
                        if not ok:
                            fails += 1
                            if fails <= 3: print('FAIL', n, [fam[i][0] for i in I], S)
    else:
        if m != 1: raise SystemExit('teeth only for m=1')
        for A in Ls:
            for B in Ls:
                for F in Ls:
                    h0 = (A[3] == B[3] == F[3])
                    h12 = (A[4] == B[4] and A[5] == B[5])
                    if mode == 'noH0' and h0: continue
                    if mode == 'noH0' and not h12: continue   # keep H1,H2 (as far as they make sense)
                    if mode == 'noH12' and (not h0 or h12): continue
                    fam = {fixed[0]: F[:3], pairs[0][0]: A[:3], pairs[0][1]: B[:3]}
                    for S in Ss:
                        tot += 1
                        E = compose(fam, n, S)
                        if not is_growth(E, N): fails += 1
    print('m', m, 'n<=', n, 'composites', tot, 'fails', fails, 'distinct H1H2 unordered pairs', distinct_pairs, flush=True)
