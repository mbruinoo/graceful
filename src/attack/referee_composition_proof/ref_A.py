# Referee check of Theorem A, coded from the STATEMENT (T* built as an abstract tree) and from the proof's labeling.
import sys, random, itertools
from ref_common import *
def case2_ok(S, m):
    return all(not (b - a <= m and a <= m < b) for a, b in S)
def build(T, n, C, S, m):
    """returns (labelled edges, N, abstract edges, abstract root)"""
    k = 2 * m + 1; I = range(-m, m + 1)
    par, order = rooted(T, 0)
    case2 = n in C
    dist = {}
    for u in order: dist[u] = 0 if u in C else dist[par[u]] + 1
    L = []; A = []
    def off(i, v): return i if dist[v] % 2 else delta(i, m)
    for y in order:
        p = par[y]
        if p is None: continue
        if y in C:
            if case2 and y == n:
                continue
            L.append((k * p, k * y)); A.append((('c', p), ('c', y)))
            for j in I:
                if j: L.append((k * p, k * y + j)); A.append((('c', p), ('leaf', y, j)))
        else:
            for i in I:
                lp = k * p if p in C else k * p + off(i, p)
                L.append((lp, k * y + off(i, y)))
                A.append(((('c', p) if p in C else ('cp', p, i)), ('cp', y, i)))
    if not case2:
        for a, b in S:
            L.append((a, b)); A.append(((('c', 0) if a == 0 else ('s', a)), ('s', b)))
        N = k * n + m
    else:
        sh = k * n - 2 * m - 1
        f = lambda g: g if g <= m else g + sh
        nm = lambda g: ('c', 0) if g == 0 else (('c', n) if g == 2 * m + 1 else ('s', g))
        for a, b in S:
            L.append((f(a), f(b))); A.append((nm(a), nm(b)))   # includes the top bracket = edge rz
        N = k * n
    return L, N, A
def check(T, n, C, S, m):
    L, N, A = build(T, n, C, S, m)
    if not is_growth(L, N): return False
    return canon(L, 0) == canon(A, ('c', 0))
def cores(T, n):
    par, order = rooted(T, 0)
    nr = order[1:]
    for mask in range(1 << len(nr)):
        C = {0} | {nr[i] for i in range(len(nr)) if mask >> i & 1}
        if all(par[v] in C for v in C if v): yield C
if __name__ == "__main__":
    NT = int(sys.argv[1]); MM = int(sys.argv[2]); NR = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    tot = [0, 0]; bad = 0; neg = [0, 0]
    for m in range(MM + 1):
        S1 = all_growth(m); Sall = all_growth(2 * m + 1); S2 = [s for s in Sall if case2_ok(s, m)]; Sbad = [s for s in Sall if not case2_ok(s, m)]
        print("m", m, "case-2 end pieces", len(S2), "rooted shapes", len(set(canon(s, 0) for s in S2)))
        for n in range(1, NT + 1):
            for T in all_growth(n):
                for C in cores(T, n):
                    c2 = n in C
                    for S in (S2 if c2 else S1):
                        tot[c2] += 1
                        if not check(T, n, C, S, m): bad += 1; print("FAIL", T, C, S, m)
                    if c2 and n <= 4:
                        for S in Sbad:
                            neg[0] += 1; neg[1] += not check(T, n, C, S, m)
    print(f"exhaustive n<={NT}, m<={MM}: case1 {tot[0]}, case2 {tot[1]}, total {sum(tot)}, failures {bad}")
    print(f"negative control (inadmissible case-2 end piece, n<=4): {neg[1]} of {neg[0]} fail")
    rng = random.Random(1); rt = rb = 0
    while rt < NR:
        n = rng.randint(7, 12); m = rng.randint(1, 5)
        T = rand_growth(n, rng)
        if T is None: continue
        par, order = rooted(T, 0)
        C = {0}
        for u in order[1:]:
            if par[u] in C and rng.random() < 0.55: C.add(u)
        if n in C:
            S = None
            for _ in range(200):
                s = rand_growth(2 * m + 1, rng)
                if s and case2_ok(s, m): S = s; break
            if S is None: continue
        else:
            S = rand_growth(m, rng)
            if S is None: continue
        rt += 1
        if not check(T, n, C, S, m): rb += 1; print("FAIL(random)", T, C, S, m)
    print(f"random n in 7..12, m in 1..5: {rt} triples, failures {rb}")
