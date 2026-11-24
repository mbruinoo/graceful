# rulebrute.py -- referee's own brute force (shares no code with folds/).
# Enumerates ALL growth placements of n cells, keeps those whose tree is isomorphic to the target,
# and tests a vocabulary rule read from REPORT.txt section 1 / Conjecture F33 wording:
#   unused cells = one gap (interval) + isolated single holes; steps S, K1 (across / back-skip), B, F.
#   bits: 2 across-only skips, 4 no B, 8 FIFO, 16 LIFO, 32 ENDS (leftmost/rightmost hole).
# Ambiguous steps (3-cell gap, x in the middle) are tried under BOTH readings. Counts are of (placement,
# reading) paths, so 'obeying' counts may exceed distinct placements; only zero vs non-zero matters.
# The single last gap cell is treated as gap (never as a hole), which is the PERMISSIVE reading,
# so a failure found here is a failure under any stricter reading.
# usage: python3 rulebrute.py RULE "edge list (0-based pairs)"
import sys
import networkx as nx

def canon(n, edges):
    return nx.weisfeiler_lehman_graph_hash(nx.Graph(edges))

def run(rule, elist):
    E = list(zip(elist[0::2], elist[1::2]))
    n = len(E) + 1
    T = nx.Graph(E)
    found = [0, 0]  # growth placements of T total, obeying rule

    def dfs(t, used, lo, hi, holes, edges, ok):
        if t == 0:
            G = nx.Graph([(a, b) for a, b in edges])
            if nx.is_isomorphic(G, T):
                found[0] += 1
                if ok:
                    found[1] += 1
            return False
        for x in range(1, n + 1):
            if x in used:
                continue
            for y in (x - t, x + t):
                if y < 1 or y > n or y not in used:
                    continue
                opts = []  # possible (ok, lo, hi, holes) readings of this step
                if not ok:
                    opts = [(False, lo, hi, holes)]
                else:
                    if lo <= hi and x == lo:
                        opts.append(('S' if y > hi else 'B', lo + 1, hi, list(holes)))
                    if lo <= hi and x == hi and lo != hi:
                        opts.append(('S' if y < lo else 'B', lo, hi - 1, list(holes)))
                    if lo + 1 <= hi and x == lo + 1:
                        opts.append(('Ka' if y > x else 'Kb', lo + 2, hi, holes + [lo]))
                    if lo + 1 <= hi and x == hi - 1:
                        opts.append(('Ka' if y < x else 'Kb', lo, hi - 2, holes + [hi]))
                    if x in holes:
                        typ = 'F'
                        if rule & 8 and x != holes[0]: typ = None
                        if rule & 16 and x != holes[-1]: typ = None
                        if rule & 32 and x not in (min(holes), max(holes)): typ = None
                        opts.append((typ, lo, hi, [h for h in holes if h != x]))
                    good = [o for o in opts if o[0] is not None and not (o[0] == 'B' and rule & 4)
                            and not (o[0] == 'Kb' and rule & 2)]
                    opts = [(True,) + o[1:] for o in good] if good else [(False, lo, hi, holes)]
                for nok, nlo, nhi, nholes in opts:
                    dfs(t - 1, used | {x}, nlo, nhi, nholes, edges + [(x, y)], nok)
        return False

    dfs(n - 2, frozenset({1, n}), 2, n - 1, [], [(1, n)], True)
    return n, found

if __name__ == '__main__':
    rule = int(sys.argv[1]) | 1
    el = list(map(int, sys.argv[2].split()))
    n, f = run(rule, el)
    print(f'n={n} rule={rule}: growth placements of T (incl. both orientations) = {f[0]}, obeying rule = {f[1]}')
