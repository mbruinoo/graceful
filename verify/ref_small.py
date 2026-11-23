"""Reference brute force for small n, straight from the definitions.

usage: python3 ref_small.py selftest          # definitions cross-checked on all placements, n <= 8
       python3 ref_small.py slide N           # README section 4 table row
       python3 ref_small.py growth N          # growth placements: count, anchors, runs, skips, Thm 9, Lemma 10
"""
import sys, itertools, json
from collections import defaultdict
from common import *

def all_placements(n):
    return itertools.product(*[range(1, n - k + 1) for k in range(1, n)])

def edges_of(p):
    return [(pk, pk + k) for k, pk in enumerate(p, start=1)]

def growth_placements(n):
    """Longest first; each bracket after the first has exactly one foot on a used vertex."""
    out = []
    used = [False] * (n + 2)
    edges = [(1, n)]
    used[1] = used[n] = True
    def rec(k):
        if k == 0:
            out.append(tuple(edges))
            return
        for p in range(1, n - k + 1):
            a, b = p, p + k
            if used[a] != used[b]:
                new = b if used[a] else a
                used[new] = True
                edges.append((a, b))
                rec(k - 1)
                edges.pop()
                used[new] = False
    rec(n - 2)
    return out

def tree_placements(n):
    """All tree placements, by depth-first choice of positions with early cycle rejection."""
    out = []
    p = [0] * n  # p[k] for k = 1..n-1
    def rec(k, par):
        if k == 0:
            out.append(tuple(p[1:]))
            return
        for pos in range(1, n - k + 1):
            a, b = pos, pos + k
            ra, rb = a, b
            while par[ra] != ra: ra = par[ra]
            while par[rb] != rb: rb = par[rb]
            if ra == rb:
                continue
            par2 = par[:]
            par2[ra] = rb
            p[k] = pos
            rec(k - 1, par2)
    rec(n - 1, list(range(n + 1)))
    return out

def selftest():
    # 1. tree_placements against the plain definition (all (n-1)! placements)
    for n in range(2, 9):
        plain = sorted(p for p in all_placements(n) if is_tree(n, edges_of(p)))
        fast = sorted(tree_placements(n))
        assert plain == fast, n
        # 2. growth placements: definition by connectivity vs. one-foot rule
        g_def = sorted(tuple(sorted(edges_of(p))) for p in all_placements(n)
                       if is_growth_by_definition(n, edges_of(p)))
        g_rec = sorted(tuple(sorted(e)) for e in growth_placements(n))
        assert g_def == g_rec, n
        # Lemma 5: every growth placement is a tree placement
        assert all(is_tree(n, list(e)) for e in g_rec)
        print(f"n={n}: {len(plain)} tree placements of {len(list(all_placements(n)))}, "
              f"{len(g_rec)} growth placements; definitions agree")
    # hand cases
    assert not is_tree(4, [(1, 4), (1, 3), (3, 4)])          # README section 1 triangle
    assert canon(4, [(1, 2), (2, 3), (3, 4)]) == canon(4, [(1, 4), (4, 2), (2, 3)])
    assert canon(4, [(1, 2), (1, 3), (1, 4)]) != canon(4, [(1, 2), (2, 3), (3, 4)])
    # run profile by hand: n=6, edges 1-6, 1-5, 3-6(len3), then 3-5? (len 2), 3-4
    assert run_profile(6, [(1, 6), (1, 5), (3, 6), (2, 4), (3, 4)])[:3] == [(1, 1), (1, 1), (2, 0)]
    print("selftest ok")

def slide(n):
    tp = tree_placements(n)
    idx = {p: i for i, p in enumerate(tp)}
    par = list(range(len(tp)))
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    right = [[] for _ in tp]
    nolegal = 0
    for i, p in enumerate(tp):
        deg = 0
        for k in range(n - 1):
            q = p[:k] + (p[k] + 1,) + p[k + 1:]
            j = idx.get(q)
            if j is not None:
                right[i].append(j)
                deg += 1
                ri, rj = find(i), find(j)
                if ri != rj:
                    par[ri] = rj
            if p[k] > 1 and (p[:k] + (p[k] - 1,) + p[k + 1:]) in idx:
                deg += 1
        if deg == 0:
            nolegal += 1
    comps = len({find(i) for i in range(len(tp))})
    star = idx[tuple([1] * (n - 1))]
    rs = find(star)
    in_star = sum(1 for i in range(len(tp)) if find(i) == rs)
    shapes = {canon(n, edges_of(p)) for p in tp}
    seen = {star}
    stack = [star]
    while stack:
        i = stack.pop()
        for j in right[i]:
            if j not in seen:
                seen.add(j)
                stack.append(j)
    rshapes = {canon(n, edges_of(tp[i])) for i in seen}
    print(json.dumps(dict(n=n, tree_shapes=len(shapes), tree_placements=len(tp), components=comps,
                          in_star_component=in_star, shapes_by_right_slides=len(rshapes),
                          placements_by_right_slides=len(seen), placements_with_no_legal_slide=nolegal)))

def is_staircase(n, edges):
    pos = {abs(a - b): min(a, b) for a, b in edges}
    return pos[n - 1] == 1 and all(pos[k] - pos[k + 1] in (0, 1) for k in range(1, n - 1))

def is_alpha(n, edges):
    # all brackets jump over one common point: some x with min(e) <= x < max(e) for every edge
    return max(min(e) for e in edges) < min(max(e) for e in edges)

def balance_game(n):
    """README Lemma 10: play on n cells, ends used and joined; returns the set of edge sets."""
    out = set()
    used = [False] * (n + 2)
    used[1] = used[n] = True
    edges = [(1, n)]
    def rec(left):
        if left == 0:
            out.add(tuple(sorted(edges)))
            return
        for x in range(1, n + 1):
            if used[x]:
                continue
            for y in range(1, n + 1):
                if not used[y]:
                    continue
                lo, hi = min(x, y), max(x, y)
                used_between = sum(1 for c in range(lo + 1, hi) if used[c])
                unused_outside = sum(1 for c in range(1, n + 1) if not used[c] and (c < lo or c > hi))
                if used_between == unused_outside:
                    used[x] = True
                    edges.append((lo, hi))
                    rec(left - 1)
                    edges.pop()
                    used[x] = False
    rec(n - 2)
    return out

def growth(n):
    gp = growth_placements(n)
    res = dict(n=n, growth_placements=len(gp))
    # Theorem 9
    alpha = [e for e in gp if is_alpha(n, e)]
    res["alpha_and_growth"] = len(alpha)
    res["two_pow_n_minus_2"] = 2 ** (n - 2)
    res["alpha_growth_all_staircases"] = all(is_staircase(n, e) for e in alpha)
    res["staircases_among_growth"] = sum(1 for e in gp if is_staircase(n, e))
    # Lemma 10
    if n <= 10:
        game = balance_game(n)
        res["balance_game_trees"] = len(game)
        res["balance_game_equals_growth"] = (game == {tuple(sorted(e)) for e in gp})
    # per-shape statistics
    minruns = {}
    minskip = {}
    anchor_codes = set()
    for e in gp:
        c = canon(n, e)
        r = max_runs(n, e)
        if r < minruns.get(c, 99):
            minruns[c] = r
        s = skips_needed(n, e)
        if s is not None and s < minskip.get(c, 99):
            minskip[c] = s
        adj = adjacency(n, e)
        anchor_codes.add(rooted_code(adj, 1))
    res["shapes_with_growth_placement"] = len(minruns)
    hist = defaultdict(int)
    for c, r in minruns.items():
        hist[r] += 1
    res["shapes_by_min_runs"] = dict(sorted(hist.items()))
    hist = defaultdict(int)
    for c in minruns:
        hist[minskip.get(c, "none")] += 1
    res["shapes_by_min_skips"] = {str(k): v for k, v in sorted(hist.items(), key=lambda kv: str(kv[0]))}
    res["anchor_rooted_codes"] = len(anchor_codes)
    print(json.dumps(res))
    with open(f"out/ref_growth_{n}.json", "w") as f:
        json.dump(dict(minruns=minruns, minskip=minskip, anchors=sorted(anchor_codes)), f)

if __name__ == "__main__":
    import os
    os.makedirs("out", exist_ok=True)
    cmd = sys.argv[1]
    if cmd == "selftest":
        selftest()
    elif cmd == "slide":
        slide(int(sys.argv[2]))
    elif cmd == "growth":
        growth(int(sys.argv[2]))
