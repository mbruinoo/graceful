#!/usr/bin/env python3
"""Referee's own certificate checker (written from README s1-2 and the claim text only).
usage: ref_verify.py lo hi files...   Checks: comb conditions (L),(C); and the tree D(a1;S), a1 in
{max S, w}, built on labels 0..m: labels distinct, lengths 1..m once, growth order, shape, root hub at 0.
Completeness: every multiset S (entries>=0,max>=1) with |S|+sum+max+2 in [lo,hi] has a line with w<=max S."""
import sys, gzip
from collections import Counter, defaultdict

def parse(line):
    p = [x.strip() for x in line.split('|')]
    S = tuple(int(x) for x in p[0].split()[1:])
    t = p[1].split(); w = int(t[1]); y = int(t[3])
    hubs = []
    for tok in p[2].split():
        h, us = tok.split(':')
        hubs.append((int(h), [int(u) for u in us.split(',')] if us else []))
    W = [int(x) for x in p[3].split()[1:]]
    return S, w, y, hubs, W

def comb_ok(S, w, y, hubs, W):
    if sorted((len(U) for _, U in hubs), reverse=True) != sorted(S, reverse=True): return "sizes"
    if len(W) != w or len(set(W)) != w: return "w"
    hs = [h for h, _ in hubs]
    if len(set(hs)) != len(hs): return "hubdup"
    full = list(range(1, y))
    L = [y - h for h in hs] + W; C = hs + W
    for h, U in hubs:
        if not (1 <= h <= y - 1): return "hubrange"
        for u in U:
            if not (1 <= u <= y - 1 - h): return "urange"
            L.append(u); C.append(h + u)
    if sorted(L) != full: return "L"
    if sorted(C) != full: return "C"
    return None

def tree_ok(S, w, y, hubs, W, a1):
    """build edges on labels 0..m and test growth placement + shape from scratch"""
    if a1 < w: return "a1<w"
    m = y + a1 - w
    edges = [(0, y)] + [(0, x) for x in W] + [(0, x) for x in range(y + 1, m + 1)]
    for h, U in hubs:
        edges.append((h, y))
        edges += [(h, h + u) for u in U]
    if len(edges) != m: return "edgecount"
    bylen = {}
    for a, b in edges:
        d = abs(a - b)
        if d in bylen or not (0 <= a <= m and 0 <= b <= m): return "len"
        bylen[d] = (a, b)
    if sorted(bylen) != list(range(1, m + 1)): return "lens"
    used = set()
    for d in range(m, 0, -1):
        a, b = bylen[d]
        if d == m: used |= {a, b}; continue
        if (a in used) == (b in used): return "growth at %d" % d
        used |= {a, b}
    if len(used) != m + 1: return "verts"
    adj = defaultdict(set)
    for a, b in edges: adj[a].add(b); adj[b].add(a)
    # shape: centre = y ; neighbours are hubs; their other neighbours are leaves
    sizes = []
    for h in adj[y]:
        for x in adj[h]:
            if x != y and len(adj[x]) != 1: return "notleaf"
        sizes.append(len(adj[h]) - 1)
    if 1 + len(sizes) + sum(sizes) != m + 1: return "shape"
    if Counter(sizes) != Counter(list(S) + [a1]): return "sizes2"
    if len(adj[0]) - 1 != a1 or 0 not in adj[y]: return "root"
    return None

def multisets(n):
    """all nonincreasing tuples, entries>=0, max>=1, with k+sum+max+2==n"""
    out = []
    def rec(pre, rem, mx):   # rem = remaining budget for (count+sum) of further parts
        if rem == 0: out.append(tuple(pre)); return
        for v in range(min(mx, rem - 1), -1, -1):
            pre.append(v); rec(pre, rem - 1 - v, v); pre.pop()
    for a in range(1, n):
        rem = n - 2 - a - (1 + a)
        if rem < 0: continue
        rec([a], rem, a)
    return out

if __name__ == "__main__":
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    best = {}; nlines = 0; bad = 0
    for f in sys.argv[3:]:
        op = gzip.open if f.endswith('.gz') else open
        for line in op(f, 'rt'):
            if not line.startswith('S '): continue
            nlines += 1
            S, w, y, hubs, W = parse(line)
            S = tuple(sorted(S, reverse=True))
            e = comb_ok(S, w, y, hubs, W)
            for a1 in (max(S), w, w + 3):
                if a1 >= w: e = e or tree_ok(S, w, y, hubs, W, a1)
            if y - 1 != len(S) + sum(S) + w: e = e or "count"
            if e: bad += 1; print("BAD", f, line.strip(), e); continue
            if w <= max(S) and (S not in best or w < best[S]): best[S] = w
    tot = 0; miss = 0
    for n in range(lo, hi + 1):
        ms = multisets(n); assert len(set(ms)) == len(ms)
        mi = [S for S in ms if S not in best]
        tot += len(ms); miss += len(mi)
        print("n=%d multisets %d missing %d %s" % (n, len(ms), len(mi), mi[:3]))
    print("lines", nlines, "bad", bad, "total multisets", tot, "missing", miss)
