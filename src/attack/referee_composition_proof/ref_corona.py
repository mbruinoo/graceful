# Referee: independent anchored-growth search (README Theorem 7 form) for rooted trees and their coronas.
import sys
from ref_common import is_growth
sys.setrecursionlimit(10000)
def rooted_trees(s):
    """all rooted trees on s vertices as canonical nested tuples, by adding a leaf anywhere and deduplicating"""
    cur = {()}
    for _ in range(s - 1):
        nxt = set()
        def add(t):
            yield tuple(sorted(t + ((),)))
            for i, c in enumerate(t):
                for c2 in add(c): yield tuple(sorted(t[:i] + (c2,) + t[i + 1:]))
        for t in cur: nxt.update(add(t))
        cur = nxt
    return sorted(cur)
def parents(t, corona):
    par = [None]
    def rec(node, me):
        for c in node:
            par.append(me); rec(c, len(par) - 1)
    rec(t, 0)
    if corona: par += list(range(len(par)))
    return par
def solve(par):
    """growth placement with vertex 0 at label 0: give lengths n-1..1 to an unlabelled child of a labelled vertex"""
    n = len(par); kids = [[] for _ in range(n)]
    for v in range(1, n): kids[par[v]].append(v)
    lab = [None] * n; lab[0] = 0; used = [False] * n; used[0] = True
    def rec(k, fr):
        if k == 0: return True
        seen = set()
        for u in fr:
            p = par[u]
            if not kids[u]:
                if p in seen: continue      # leaf children of the same parent are interchangeable
                seen.add(p)
            for sg in (1, -1):
                L = lab[p] + sg * k
                if 0 <= L < n and not used[L]:
                    lab[u] = L; used[L] = True
                    if rec(k - 1, [x for x in fr if x != u] + kids[u]): return True
                    used[L] = False; lab[u] = None
        return False
    if not rec(n - 1, list(kids[0])): return None
    return [(lab[v], lab[par[v]]) for v in range(1, n)]
if __name__ == "__main__":
    S0, S1, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    for s in range(S0, S1 + 1):
        R = rooted_trees(s); fail = []
        for t in R:
            par = parents(t, mode == "corona")
            E = solve(par)
            if E is None: fail.append(t)
            else: assert len(par) == 1 or (is_growth(E, len(par) - 1) and any(0 in e for e in E))
        print(f"s={s} {mode}: {len(R)} rooted trees, {len(fail)} with no growth placement anchored at the root", fail[:6], flush=True)
