#!/usr/bin/env python3
"""Which rule does README section 11, table row 3 ("one run, at most one skipped cell on each
side of the run": first failure S(3,3,3) at n = 10) actually correspond to?

Pure-Python enumeration of all growth placements on n vertices (definition of README section 2)
with several candidate readings of the side rule, all with at most two single skipped cells:
  each_side      while a run of size > 1 exists: at most one single on each side of it
                 (states that are all singles are unrestricted beyond "at most 3 runs")
  each_leftmost  main run := the FIRST run of maximal size (so with all singles, the leftmost
                 single); at most one single on each side of it
  each_any       main run := any run of maximal size, chosen favourably
  same_side      while a run of size > 1 exists: all singles on one side of it
Prints the number of placements for each reading; compare with `src/holes n 3 1 SIDE`
(run, not read): n=10: side-rule 1 -> 4728 placements, 105 shapes; side-rule 2 -> 5672, 106.
Usage: probe_side.py n"""
import sys
from canon import ucode

def runs_of(n, used):
    runs = []
    for x in range(1, n + 1):
        if not (used >> x & 1):
            if runs and runs[-1][1] == x - 1: runs[-1][1] = x
            else: runs.append([x, x])
    return runs

def ok(rule, n, used):
    runs = runs_of(n, used)
    if not runs: return True
    sizes = [b - a + 1 for a, b in runs]
    if sum(1 for s in sizes if s > 1) > 1 or len(runs) > 3: return False
    big = [i for i, s in enumerate(sizes) if s > 1]
    if rule == "each_side":
        return not big or (big[0] <= 1 and len(runs) - 1 - big[0] <= 1)
    if rule == "same_side":
        return not big or big[0] == 0 or big[0] == len(runs) - 1
    mx = max(sizes); cands = [i for i, s in enumerate(sizes) if s == mx]
    if rule == "each_leftmost": cands = cands[:1]
    return any(i <= 1 and len(runs) - 1 - i <= 1 for i in cands)

def enum(n, rule):
    count = 0; shapes = set(); pos = {}
    def rec(k, used):
        nonlocal count
        if k == 0:
            count += 1
            adj = [[] for _ in range(n)]
            for kk, p in pos.items():
                adj[p - 1].append(p + kk - 1); adj[p + kk - 1].append(p - 1)
            shapes.add(ucode(n, adj)); return
        for p in range(1, n - k + 1):
            a, b = used >> p & 1, used >> (p + k) & 1
            if (a + b != 0) if k == n - 1 else (a + b != 1): continue
            u2 = used | 1 << p | 1 << (p + k)
            if ok(rule, n, u2):
                pos[k] = p; rec(k - 1, u2)
    rec(n - 1, 0)
    return count, len(shapes)

n = int(sys.argv[1])
for rule in ["each_side", "each_leftmost", "each_any", "same_side"]:
    c, s = enum(n, rule)
    print(f"n={n} {rule}: placements {c}, shapes {s}")
