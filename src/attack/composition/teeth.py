# Sanity: the checkers can fail.  (1) Theorem B with hypothesis H0 dropped (identical pairs, different root sets);
# (2) Theorem B with T_i != T_delta(i) chosen freely; (3) Theorem A case 2 with an end piece that has a short
# bracket crossing the middle; (4) an even number of copies: two copies of an anchored tree glued at the anchor
# (plus nothing) need not be anchored there -- path on 4 vertices from its end, twice = path on 7 from its middle.
import itertools
from common import *
import mixed_bunch as MB, core_fatten as CF
m = 1; fails = {1: 0, 2: 0}; tot = {1: 0, 2: 0}
for n in range(1, 6):
    L = growth_labelings(n); inf = [MB.info(p) for p in L]
    for a, b, f in itertools.product(range(len(L)), repeat=3):
        for parS in growth_labelings(m):
            if inf[a][1] != inf[f][1]:                         # (1): T_-1 = T_0 = L[a], T_1 = L[f], root sets differ
                Ts = {-1: (L[a], inf[a][0]), 0: (L[a], inf[a][0]), 1: (L[f], inf[f][0])}
                tot[1] += 1; fails[1] += not is_growth_from_definition(MB.composite(parS, Ts, m), 3 * n + 1)
            if a != b and inf[a][1] == inf[b][1] == inf[f][1] and not (inf[a][2] == inf[b][2] and inf[a][3] == inf[b][3]):
                Ts = {-1: (L[a], inf[a][0]), 0: (L[b], inf[b][0]), 1: (L[f], inf[f][0])}
                tot[2] += 1; fails[2] += not is_growth_from_definition(MB.composite(parS, Ts, m), 3 * n + 1)
print(f"(1) H0 dropped: {fails[1]} of {tot[1]} composites are not growth placements")
print(f"(2) H1/H2 violated: {fails[2]} of {tot[2]} composites are not growth placements")
t3 = f3 = 0
for m in (1, 2):
    good = CF.S_case2(m)
    for parS in growth_labelings(2 * m + 1):
        if parS in good: continue
        for n in range(1, 5):
            for parT in growth_labelings(n):
                for C in CF.connected_subsets_with_root(parT):
                    if n in C:
                        e, N = CF.composite(parT, C, parS, m); t3 += 1; f3 += not is_growth_from_definition(e, N)
print(f"(3) end piece with a short bracket across the middle: {f3} of {t3} composites are not growth placements")
P7 = [p for p in growth_labelings(6) if canon_rooted(adj_from_edges([(v, q) for v, q in p.items() if q is not None]), 0) == "((()))((()))".join(["(", ")"])]
print(f"(4) growth placements of the path on 7 vertices anchored at its middle vertex: {len(P7)}")
