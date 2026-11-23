# Probe of a Delta-type rule (Stanton-Zarnke / Koh-Rogers-Tan style) for the corona  S (.) K_1  (a leaf on every vertex).
# S: growth labeling on 0..s-1, root 0; e_i = length of the bracket from i towards the root.
# A permutation pi of 0..s-1 is ADMISSIBLE if, with d_i = pi(i)-i and phi(d) = d (d>=0), -d-1 (d<0):
#     the values phi(d_i) are all different (hence are 0..s-1), and phi(d_i) <= e_i - 1 for every non-root i.
# Lemma C: then labelling vertex i with 2i and its new leaf with 2 pi(i)+1 is a growth placement of the corona,
# anchored at the same root.  (S-brackets get the even lengths 2e, leaf brackets the odd lengths 2 phi(d_i)+1.)
# This program (a) checks Lemma C from the definitions on every admissible (labeling, pi) and
# (b) counts for which rooted trees (S, anchor) some labeling has an admissible pi.
import sys
from common import *

def phi(d): return d if d >= 0 else -d - 1

def admissible(par):
    s = len(par); e = {i: abs(i - par[i]) for i in par if par[i] is not None}
    out = []; pi = [None] * s; usedv = set(); usedphi = set()
    order = sorted(range(s), key=lambda i: e.get(i, s))   # most constrained first
    def rec(t):
        if t == s: out.append(list(pi)); return True
        i = order[t]
        for v in range(s):
            if v in usedv: continue
            f = phi(v - i)
            if f in usedphi or (i != 0 and f > e[i] - 1): continue
            pi[i] = v; usedv.add(v); usedphi.add(f)
            if rec(t + 1): 
                usedv.discard(v); usedphi.discard(f); return True
            usedv.discard(v); usedphi.discard(f)
        return False
    rec(0)
    return out

if __name__ == "__main__":
    SMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    for s in range(1, SMAX + 1):
        shapes = {}; nlab = nadm = bad = 0
        for par in growth_labelings(s - 1):
            E = [(v, p) for v, p in par.items() if p is not None]
            key = canon_rooted(adj_from_edges(E), 0) if E else "()"
            nlab += 1
            A = admissible(par)
            shapes[key] = shapes.get(key, False) or bool(A)
            for pi in A:
                nadm += 1
                edges = [(2 * p, 2 * v) for v, p in E] + [(2 * i, 2 * pi[i] + 1) for i in range(s)]
                ok = is_growth_from_definition(edges, 2 * s - 1)
                if ok:
                    ab = [(("v", p), ("v", v)) for v, p in E] + [(("v", i), ("leaf", i)) for i in range(s)]
                    ok = canon_rooted(adj_from_edges(edges), 0) == canon_rooted(adj_from_edges(ab), ("v", 0))
                if not ok: bad += 1
        miss = [k for k, v in shapes.items() if not v]
        print(f"s={s}: {nlab} growth labelings, {nadm} with an admissible pi (Lemma C failures: {bad}); "
              f"anchored rooted trees (S,anchor): {len(shapes)}, covered by the rule: {len(shapes)-len(miss)}"
              + (f"; first uncovered: {min(miss, key=len)}" if miss else ""), flush=True)
