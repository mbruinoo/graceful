# Corollary of Theorem B in tree language: S (m edges, anchored at s0), U_0..U_m (q edges each, U_j anchored at u_j);
# join s0 by new edges to u_0 and to two copies of each u_j, j>=1.  Built here from random growth labelings of S, U_j
# following the proof (reflect, shift by 1, add root), then tested from the definition and against the verbal tree.
import random
from ref_common import *
rng = random.Random(7); tot = bad = 0
while tot < 3000:
    m = rng.randint(1, 4); q = rng.randint(0, 8); k = 2 * m + 1; n = q + 1
    S = rand_growth(m, rng); U = [rand_growth(q, rng) for _ in range(m + 1)]
    if S is None or any(u is None for u in U): continue
    I = list(range(-m, m + 1)); fx = [i for i in I if delta(i, m) == i][0]
    prs = [(i, delta(i, m)) for i in I if i < delta(i, m)]; assert len(prs) == m
    which = {fx: 0}
    for j, (a, b) in enumerate(prs, 1): which[a] = j; which[b] = j
    L = list(S); A = [((('r',) if a == 0 else ('s', a)), ('s', b)) for a, b in S]
    for i in I:
        Uj = U[which[i]]
        # pendant U_j: reflect x -> q - x, shift by 1, root 0 joined to u_j (now label q+1)
        P = [(0, q + 1)] + [tuple(sorted((q - a + 1, q - b + 1))) for a, b in Uj]
        par, order = rooted(P, 0); dep = {0: 0}
        for u in order[1:]: dep[u] = dep[par[u]] + 1
        o = lambda v: 0 if v == 0 else (i if dep[v] % 2 else delta(i, m))
        for a, b in P: L.append((k * a + o(a), k * b + o(b)))
        # verbal tree: copy of U_j with original labels, new edge s0 -- u_j (label 0 in U_j)
        A.append((('r',), (i, 0)))
        for a, b in Uj: A.append(((i, a), (i, b)))
    tot += 1
    if not (is_growth(L, k * n + m) and canon(L, 0) == canon(A, ('r',))): bad += 1; print("FAIL", m, q, S, U)
print(f"corollary of Theorem B, random m in 1..4, q in 0..8: {tot} composites, failures {bad}")
