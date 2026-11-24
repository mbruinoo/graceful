# permsearch.py -- referee's tree-guided search for a growth placement obeying a vocabulary rule, under the
# PERMISSIVE reading of the F33-style wording: a step is allowed if ANY of its readings is allowed.
# Ambiguities that the literal wording leaves open (tidy.cpp resolves each one a single way):
#   * 2-cell gap, x at one end, partner on x's own side: "B" or "K1 across" (other cell becomes a hole);
#   * 3-cell gap, x in the middle: K1 with the hole on either side (across or back-skip);
#   * 1-cell gap: S in either direction.
# All readings are branched on.  usage: python3 permsearch.py RULE "edges"   (bits as in REPORT.txt section 1)
import sys
from functools import lru_cache
sys.setrecursionlimit(10000)

def main(rule, el):
    E = list(zip(el[0::2], el[1::2])); n = len(E) + 1
    adj = [[] for _ in range(n)]
    for u, v in E: adj[u].append(v); adj[v].append(u)
    @lru_cache(None)
    def shape(w, p):  # canonical string of subtree at w away from p
        return '(' + ''.join(sorted(shape(c, w) for c in adj[w] if c != p)) + ')'
    seen = set(); sol = []

    def readings(x, y, lo, hi, holes):
        out = []
        if lo <= hi and x in (lo, hi):
            if lo == hi: out.append(('S', lo + 1, hi, holes))
            elif x == lo: out.append(('S' if y > hi else 'B', lo + 1, hi, holes))
            else: out.append(('S' if y < lo else 'B', lo, hi - 1, holes))
        if lo + 1 <= hi and x == lo + 1:
            out.append(('Ka' if y > x else 'Kb', lo + 2, hi, holes + (lo,)))
        if lo + 1 <= hi and x == hi - 1:
            out.append(('Ka' if y < x else 'Kb', lo, hi - 2, holes + (hi,)))
        if x in holes:
            ok = True
            if rule & 8 and x != holes[0]: ok = False
            if rule & 16 and x != holes[-1]: ok = False
            if rule & 32 and x not in (min(holes), max(holes)): ok = False
            if ok: out.append(('F', lo, hi, tuple(h for h in holes if h != x)))
        return [o for o in out if not (o[0] == 'B' and rule & 4) and not (o[0] == 'Kb' and rule & 2)]

    def dfs(t, lab, pend, lo, hi, holes):
        # pend: tuple of (cell, child vertex, parent vertex)
        if t == 0: sol.append(dict(lab)); return True
        used = set(lab.values())
        key = (frozenset(used), tuple(sorted((c, shape(w, p)) for c, w, p in pend)), lo, hi, holes)
        if key in seen: return False
        seen.add(key)
        tried = set()
        for i, (y, w, p) in enumerate(pend):
            sh = (y, shape(w, p))
            if sh in tried: continue
            tried.add(sh)
            for x in (y - t, y + t):
                if x < 1 or x > n or x in used: continue
                for _, nlo, nhi, nholes in readings(x, y, lo, hi, holes):
                    lab2 = dict(lab); lab2[w] = x
                    pend2 = pend[:i] + pend[i + 1:] + tuple((x, c, w) for c in adj[w] if c != p)
                    if dfs(t - 1, lab2, pend2, nlo, nhi, nholes): return True
        return False

    # root edge {1,n}: every edge, both orientations
    for u, v in E:
        for a, b in ((u, v), (v, u)):
            lab = {a: 1, b: n}
            pend = tuple((1, c, a) for c in adj[a] if c != b) + tuple((n, c, b) for c in adj[b] if c != a)
            if dfs(n - 2, lab, pend, 2, n - 1, ()):
                return n, sol[0]
    return n, None

if __name__ == '__main__':
    rule = int(sys.argv[1]) | 1
    n, s = main(rule, list(map(int, sys.argv[2].split())))
    print(f'n={n} rule={rule} permissive:', 'FOUND labels ' + ' '.join(str(s[v]) for v in range(n)) if s else 'NONE (exhaustive)')
