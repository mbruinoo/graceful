#!/usr/bin/env python3
"""Verify ref_comb output lines from the README section 1 definitions and the all-up property."""
import sys
ok = bad = 0
for line in sys.stdin:
    if line.startswith("NONE"): bad += 1; print(line.strip()); continue
    parts = [p.split() for p in line.strip().split("|")]
    s = list(map(int, parts[0][1:])); y = int(parts[1][1]); hubs = list(map(int, parts[2][1:]))
    leaves = [tuple(map(int, t.split(":"))) for t in parts[3][1:]]; W = list(map(int, parts[4][1:]))
    n = 1 + len(s) + sum(s); m = n-1
    E = [(0, y)] + [(0, w) for w in W] + [(0, x) for x in range(y+1, m+1)]
    assert len(E) == s[0]+1, line
    cnt = [0]*len(s)
    for i, h in enumerate(hubs, 1):
        assert 0 < h < y; E.append((y, h))
    for i, c in leaves:
        assert hubs[i-1] < c < y, line   # all-up: above hub, below centre
        E.append((hubs[i-1], c)); cnt[i] += 1
    assert cnt[1:] == s[1:], line
    lab = sorted(v for e in E[:1] for v in e) and sorted([0] + [b for a, b in E])
    assert lab == list(range(n)), line          # each vertex is the child end of one edge, plus root
    assert sorted(abs(a-b) for a, b in E) == list(range(1, n)), line
    used = set()
    for a, b in sorted(E, key=lambda e: -abs(e[0]-e[1])):
        if used: assert (a in used) + (b in used) == 1, line
        else: assert {a, b} == {0, m}, line
        used |= {a, b}
    ok += 1
print("verified %d labelings, %d trees without comb" % (ok, bad))
