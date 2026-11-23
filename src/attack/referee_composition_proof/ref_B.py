# Referee check of Theorem B and its tree-language corollary, coded from the statement.
import sys, random, itertools
from ref_common import *
def info(T, n):
    par, order = rooted(T, 0)
    dep = {0: 0}
    for u in order[1:]: dep[u] = dep[par[u]] + 1
    rootset = frozenset(u for u in order if par[u] == 0)
    h1 = tuple(dep[l] % 2 for l in range(1, n + 1))
    h2 = {}
    for a, b in T:
        if a != 0: h2[b - a] = dep[a] % 2          # a < b: a is the lower-labelled end; not a root edge
    return dep, rootset, h1, tuple(sorted(h2.items()))
def compose(S, Ts, deps, m):
    k = 2 * m + 1; L = list(S); A = [((('r',) if a == 0 else ('s', a)), ('s', b)) for a, b in S]
    for i in range(-m, m + 1):
        d = deps[i]
        o = lambda v: 0 if v == 0 else (i if d[v] % 2 else delta(i, m))
        for a, b in Ts[i]:
            L.append((k * a + o(a), k * b + o(b)))
            A.append(((('r',) if a == 0 else (i, a)), (i, b)))
    return L, A
def check(S, Ts, deps, m, n):
    L, A = compose(S, Ts, deps, m)
    return is_growth(L, (2 * m + 1) * n + m) and canon(L, 0) == canon(A, ('r',))
if __name__ == "__main__":
    m = int(sys.argv[1]); NT = int(sys.argv[2])
    I = list(range(-m, m + 1)); fx = [i for i in I if delta(i, m) == i]; assert len(fx) == 1
    assert all(delta(delta(i, m), m) == i for i in I)
    prs = [(i, delta(i, m)) for i in I if i < delta(i, m)]
    tot = bad = dist = 0; negH0 = [0, 0]; negH = [0, 0]
    for n in range(1, NT + 1):
        G = all_growth(n); inf = [info(T, n) for T in G]
        groups = {}
        for t, x in enumerate(inf): groups.setdefault(x[1], []).append(t)
        for rs, idx in groups.items():
            adm = [(a, b) for a in idx for b in idx if inf[a][2] == inf[b][2] and inf[a][3] == inf[b][3]]
            dist += sum(1 for a, b in adm if a < b)
            for ch in itertools.product(adm, repeat=len(prs)):
                for f in idx:
                    Ts = {fx[0]: G[f]}; deps = {fx[0]: inf[f][0]}
                    for (i, j), (a, b) in zip(prs, ch):
                        Ts[i] = G[a]; Ts[j] = G[b]; deps[i] = inf[a][0]; deps[j] = inf[b][0]
                    for S in all_growth(m):
                        tot += 1
                        if not check(S, Ts, deps, m, n): bad += 1; print("FAIL", S, Ts)
        if m == 1 and n <= 5:   # negative controls
            for a, b, f in itertools.product(range(len(G)), repeat=3):
                Ts = {-1: G[a], 0: G[b], 1: G[f]}; deps = {-1: inf[a][0], 0: inf[b][0], 1: inf[f][0]}  # delta pairs -1<->0, fixes 1
                if a == b and inf[a][1] != inf[f][1]:
                    negH0[0] += 1; negH0[1] += not check([(0, 1)], Ts, deps, 1, n)
                if a != b and inf[a][1] == inf[b][1] == inf[f][1] and (inf[a][2], inf[a][3]) != (inf[b][2], inf[b][3]):
                    negH[0] += 1; negH[1] += not check([(0, 1)], Ts, deps, 1, n)
    print(f"m={m}, n<={NT}: {tot} composites, failures {bad}; distinct admissible unordered pairs {dist}")
    if m == 1: print(f"neg controls n<=5: H0 dropped {negH0[1]}/{negH0[0]} fail; H1/H2 violated {negH[1]}/{negH[0]} fail")
