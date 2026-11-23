#!/usr/bin/env python3
"""Checks spiderdeal.cpp output against the definitions (no search).
Usage: check_deal.py n mode < output
For each "OK" line: rebuild the spider (centre + legs) and its labeling from the deal, then
  * check the deal rules of README 13 directly (numbers m..1 each handed once, each leg gets
    exactly its length, first move of a leg is up, tips stay in 1..m, no label twice;
    mode zigzag/level/first: the extra restriction);
  * check with check_cert.verify that it is a growth placement of the spider (labels shifted
    to 1..n), that the centre carries label 1, and that lengths decrease outward on every leg.
Also checks that the spiders listed are exactly the partitions of n-1 into >= 3 parts."""
import sys
from check_cert import verify

def partitions(r, mx):
    if r == 0:
        yield []
        return
    for p in range(min(r, mx), 0, -1):
        for rest in partitions(r - p, p):
            yield [p] + rest

def main():
    n = int(sys.argv[1]); mode = sys.argv[2]; m = n - 1
    minlegs = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    want = [p for p in partitions(m, m) if len(p) >= minlegs]
    seen = []; ok = 0; none = []
    for line in sys.stdin:
        head, tail = line.split(":")
        legs = list(map(int, head.split()[1:]))
        seen.append(legs)
        if tail.split()[0] == "NONE":
            none.append(tuple(legs)); continue
        moves = tail.split()[1:]
        assert len(moves) == m
        K = len(legs)
        tips = [0] * K; got = [0] * K; last = [0] * K; path = [[0] for _ in range(K)]
        used = {0}
        for w, mv in zip(range(m, 0, -1), moves):
            i = int(mv[:-1]); d = 1 if mv[-1] == '+' else -1
            assert got[i] < legs[i]
            if got[i] == 0: assert d == 1
            if mode == "zigzag" and got[i] > 0: assert d == -last[i]
            if mode == "level": assert all(got[j] >= min(got[i], legs[j]) for j in range(K))
            if mode == "first" and got[i] >= 1: assert all(g >= 1 for g in got)
            x = tips[i] + d * w
            assert 1 <= x <= m and x not in used
            used.add(x); tips[i] = x; got[i] += 1; last[i] = d; path[i].append(x)
        assert got == legs and used == set(range(m + 1))
        # as a tree: vertex 0 = centre
        edges = []; lab = [1]; nxt = 1
        for i in range(K):
            prev = 0
            for x in path[i][1:]:
                edges.append((prev, nxt)); lab.append(x + 1); prev = nxt; nxt += 1
            ds = [abs(a - b) for a, b in zip(path[i], path[i][1:])]
            assert all(a > b for a, b in zip(ds, ds[1:]))
        assert verify(n, edges, lab) is None and lab[0] == 1
        ok += 1
    assert seen == want, "spider list is not the list of partitions"
    print(f"n={n} mode={mode}: spiders {len(want)}, deals verified {ok}, NONE {len(none)}"
          + ("" if not none or len(none) > 12 else "  " + " ".join(str(t) for t in none)))

if __name__ == "__main__":
    main()
