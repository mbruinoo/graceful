# Theorem B (mixed bunch) -- brute-force check from the definitions.
# S: growth labeling on 0..m (root 0).  T_i, i in I=[-m,m]: growth labelings on 0..n (root 0), possibly of
# DIFFERENT trees.  delta(x) = -x-m (x<=0), m+1-x (x>0) is an involution of I with one fixed point.  Hypotheses:
#  (H0) all T_i have the same set of labels next to the root;
#  (H1) for every label l, T_i and T_delta(i) agree on the parity of the depth of the vertex labelled l;
#  (H2) for every length c that is not on a root edge, T_i and T_delta(i) agree on the parity of the depth of the
#       LOWER-labelled end of the bracket of length c.
# (All three hold if T_i = T_delta(i) as labelings and (H0) holds.)
# Composite: S unchanged; vertex of T_i with label l at depth d>=1 -> (2m+1) l + (i if d odd else delta(i)).
# Claim: a growth placement of "S and all T_i glued at their roots", anchored at the glued root.
import sys, itertools
from common import *

def info(par):
    d = depth_of(par); n = len(par) - 1
    rootset = frozenset(v for v in par if par[v] == 0)
    cls = tuple(d[l] % 2 for l in range(n + 1))
    low = tuple((d[min(v, p)] % 2) if p != 0 else 2 for c in range(1, n + 1)
                for v, p in par.items() if p is not None and abs(v - p) == c)
    return d, rootset, cls, low

def composite(parS, Ts, m):
    k = 2 * m + 1; edges = [(p, v) for v, p in parS.items() if p is not None]
    for i, (par, d) in Ts.items():
        off = lambda v: 0 if v == 0 else (i if d[v] % 2 else delta(i, m))
        for v, p in par.items():
            if p is not None: edges.append((k * p + off(p), k * v + off(v)))
    return edges

def abstract(parS, Ts):
    E = []
    nm = lambda tag, a: "root" if a == 0 else (tag, a)
    for v, p in parS.items():
        if p is not None: E.append((nm("S", p), nm("S", v)))
    for i, (par, d) in Ts.items():
        for v, p in par.items():
            if p is not None: E.append((nm(i, p), nm(i, v)))
    return E

if __name__ == "__main__":
    m = int(sys.argv[1]); NT = int(sys.argv[2]); identical_only = len(sys.argv) > 3
    I = list(range(-m, m + 1))
    fixed = [i for i in I if delta(i, m) == i]; assert len(fixed) == 1
    pairs = [(i, delta(i, m)) for i in I if i < delta(i, m)]
    tot = bad = distinct_pairs = 0
    for n in range(1, NT + 1):
        L = growth_labelings(n); inf = [info(p) for p in L]
        byroot = {}
        for t, x in enumerate(inf): byroot.setdefault(x[1], []).append(t)
        for rs, idx in byroot.items():
            # admissible (T_i, T_delta(i)) pairs
            adm = [(a, b) for a in idx for b in idx
                   if (a == b) or (not identical_only and inf[a][2] == inf[b][2] and inf[a][3] == inf[b][3])]
            distinct_pairs += sum(1 for a, b in adm if a < b)
            for choice in itertools.product(adm, repeat=len(pairs)):
                for f in idx:
                    Ts = {fixed[0]: (L[f], inf[f][0])}
                    for (i, j), (a, b) in zip(pairs, choice):
                        Ts[i] = (L[a], inf[a][0]); Ts[j] = (L[b], inf[b][0])
                    for parS in growth_labelings(m):
                        tot += 1
                        edges = composite(parS, Ts, m)
                        ok = is_growth_from_definition(edges, (2 * m + 1) * n + m)
                        if ok:
                            ok = canon_rooted(adj_from_edges(edges), 0) == canon_rooted(adj_from_edges(abstract(parS, Ts)), "root")
                        if not ok:
                            bad += 1
                            if bad < 4: print("FAIL", parS, Ts)
    print(f"m={m}, T_i with at most {NT} edges, {'identical pairs only' if identical_only else 'hypotheses H0-H2'}: "
          f"{tot} composites checked, failures {bad}; unordered pairs of distinct labelings admissible as (T_i,T_delta(i)): {distinct_pairs}")
