# Theorem A (core fattening) -- brute-force check from the definitions.
# Input: growth labeling f of T on 0..n (root r=label 0, top z=label n), a subtree C containing r, m >= 0, k=2m+1.
#  case 1 (z not in C): S = growth labeling on 0..m.
#  case 2 (z in C)    : S = growth labeling on 0..2m+1 in which no bracket of length <= m joins a label <= m to a
#                       label >= m+1.
# Composite labeling (labels 0..kn+m in case 1, 0..kn in case 2):
#   x in C                       -> k f(x)
#   edge p->x of C (not r-z in case 2): 2m leaves at p, labels k f(x)+j, j in [-m,m]\{0}
#   v outside C, depth d>=1 below C, copy i in [-m,m] -> k f(v) + delta^(d-1)(i), joined to the copy i of its parent
#   S: case 1 unchanged; case 2 labels <= m unchanged, labels >= m+1 raised by kn-2m-1.
# The abstract tree T* is built separately (no labels) and compared with the labelled composite as a rooted tree.
import sys, itertools
from common import *

def connected_subsets_with_root(par):
    """all vertex sets C containing root 0 and closed under taking parents"""
    verts = sorted(par); out = []
    nonroot = [v for v in verts if v != 0]
    for mask in range(1 << len(nonroot)):
        C = {0} | {nonroot[i] for i in range(len(nonroot)) if mask >> i & 1}
        if all(par[v] in C for v in C if v != 0): out.append(C)
    return out

def composite(parT, C, parS, m):
    n = len(parT) - 1; k = 2 * m + 1; case2 = n in C
    edges = []
    dC = {}  # depth below C
    def dc(v):
        if v in C: return 0
        if v not in dC: dC[v] = dc(parT[v]) + 1
        return dC[v]
    def dp(i, j):
        return i if j % 2 == 0 else delta(i, m)
    for v, p in parT.items():
        if p is None: continue
        if v in C:
            if case2 and v == n: continue          # the top edge is supplied by S
            edges.append((k * p, k * v))
            for j in range(-m, m + 1):
                if j: edges.append((k * p, k * v + j))
        else:
            d = dc(v)
            for i in range(-m, m + 1):
                lv = k * v + dp(i, d - 1)
                lp = k * p if p in C else k * p + dp(i, d - 2)
                edges.append((lp, lv))
    sh = (k * n - 2 * m - 1) if case2 else 0
    mv = lambda a: a if a <= m else a + sh
    for v, p in parS.items():
        if p is not None: edges.append((mv(p), mv(v)))
    N = k * n if case2 else k * n + m
    return edges, N

def abstract(parT, C, parS, m):
    """T* as an unlabelled tree: vertices are tuples, built from the verbal description."""
    n = len(parT) - 1; k = 2 * m + 1; case2 = n in C
    E = []
    for v, p in parT.items():
        if p is None: continue
        if v in C:
            E.append((("C", p), ("C", v)))
            if not (case2 and v == n):
                for j in range(2 * m): E.append((("C", p), ("leaf", v, j)))
        else:
            for i in range(k):
                E.append(((("C", p) if p in C else ("copy", p, i)), ("copy", v, i)))
    top = len(parS) - 1
    nm = lambda a: ("C", 0) if a == 0 else (("C", n) if (case2 and a == top) else ("S", a))
    for v, p in parS.items():
        if p is None: continue
        if case2 and v == top: continue            # S's top bracket is the edge r-z of C, already present
        E.append((nm(p), nm(v)))
    return E

def S_case2(m):
    out = []
    for par in growth_labelings(2 * m + 1):
        if all(not (abs(v - p) <= m and (min(v, p) <= m < max(v, p))) for v, p in par.items() if p is not None):
            out.append(par)
    return out

if __name__ == "__main__":
    NT = int(sys.argv[1]) if len(sys.argv) > 1 else 6     # T has at most NT edges
    MM = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    tot = bad = 0; c1 = c2 = 0
    for m in range(0, MM + 1):
        S1 = growth_labelings(m); S2 = S_case2(m)
        print(f"m={m}: {len(S1)} end pieces for case 1, {len(S2)} for case 2 "
              f"({len(set(canon_rooted(adj_from_edges([(v,p) for v,p in s.items() if p is not None]),0) for s in S2)) if m else 1} rooted shapes)")
        for n in range(1, NT + 1):
            for parT in growth_labelings(n):
                for C in connected_subsets_with_root(parT):
                    for parS in (S2 if n in C else S1):
                        edges, N = composite(parT, C, parS, m)
                        tot += 1
                        if n in C: c2 += 1
                        else: c1 += 1
                        ok = is_growth_from_definition(edges, N)
                        if ok:
                            A = abstract(parT, C, parS, m)
                            ok = canon_rooted(adj_from_edges(edges), 0) == canon_rooted(adj_from_edges(A), ("C", 0))
                        if not ok:
                            bad += 1
                            if bad < 5: print("FAIL", parT, C, parS, m)
    print(f"T with at most {NT} edges, m <= {MM}: {tot} (labeling, core, end piece) triples "
          f"({c1} case 1, {c2} case 2); failures: {bad}")
