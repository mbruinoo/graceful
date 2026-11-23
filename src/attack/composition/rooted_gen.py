# All rooted trees on s vertices (one per isomorphism class), as parent arrays; optional transformation.
#   python3 rooted_gen.py s plain    -> the rooted tree itself
#   python3 rooted_gen.py s corona   -> the corona (one new leaf on every vertex), rooted at the same vertex
import sys
def rooted_trees(s):
    # canonical children-code enumeration: a rooted tree is a sorted multiset of rooted trees
    memo = {1: [()]}
    def trees(k):
        if k in memo: return memo[k]
        res = set()
        def parts(rem, maxpart, acc):
            if rem == 0:
                import itertools
                def rec(i, cur, lastkey):
                    if i == len(acc): res.add(tuple(sorted(cur))); return
                    for t in trees(acc[i]): rec(i + 1, cur + [t], None)
                rec(0, [], None); return
            for p in range(min(rem, maxpart), 0, -1): parts(rem - p, p, acc + [p])
        parts(k - 1, k - 1, [])
        memo[k] = sorted(res); return memo[k]
    return trees(s)
def to_parents(t):
    par = []
    def rec(node, me):
        for c in node:
            par.append(me); idx = len(par); rec(c, idx)
    rec(t, 0); return par
if __name__ == "__main__":
    s = int(sys.argv[1]); mode = sys.argv[2] if len(sys.argv) > 2 else "plain"
    for t in rooted_trees(s):
        par = to_parents(t)
        if mode == "corona": par = par + list(range(s))
        print(len(par) + 1, *par)
