#!/usr/bin/env python3
"""Tree families for the counterexample hunt (results/counterexample-hunt/REPORT.md).

Usage: huntfam.py FAMILY ARG [ARG ...] [maxn=N] [minn=N]
Each ARG is an integer or a range a..b; all combinations are generated.
Output: one tree per line, "name: u v u v ..." (0-based edge list), for growfam.

Families (c = centre):
  spider k L          k legs of length L
  hubspider k a m     k arms of a edges from c, each ending in a hub carrying m leaves
  hublegs m k L       c carries one adjacent hub with m leaves and k legs of length L
  hubleaflegs m k L   c itself carries m leaves and k legs of length L
  sph d1 d2 ...       spherically symmetric: every vertex at depth i has d_{i+1} children
  dbl m P t r         two hubs with m leaves each joined by a path of P edges; a pendant path of r edges
                      on the path vertex at distance t from the second hub  (README s.11: dbl 6 7 1 2)
  bin k d             c carries k complete binary trees of depth d
  comb p L            path on p vertices, a pendant path of L edges on each
  forkhub a m b       path of a edges; one end carries two legs of length b, the other a hub of m leaves
  brooms k a m L      c carries k arms of a edges ending in hubs of m leaves, plus one leg of length L
  twolevel k j m      c has k children, each has j children, each of those carries m leaves
"""
import sys, itertools

class T:
    def __init__(s): s.n = 1; s.E = []
    def add(s, p): v = s.n; s.n += 1; s.E.append((p, v)); return v
    def path(s, p, L):
        for _ in range(L): p = s.add(p)
        return p
    def leaves(s, p, m):
        for _ in range(m): s.add(p)

def spider(k, L):
    t = T()
    for _ in range(k): t.path(0, L)
    return t
def hubspider(k, a, m):
    t = T()
    for _ in range(k): t.leaves(t.path(0, a), m)
    return t
def hublegs(m, k, L):
    t = T(); t.leaves(t.add(0), m)
    for _ in range(k): t.path(0, L)
    return t
def hubleaflegs(m, k, L):
    t = T(); t.leaves(0, m)
    for _ in range(k): t.path(0, L)
    return t
def sph(*d):
    t = T(); level = [0]
    for di in d: level = [t.add(v) for v in level for _ in range(di)]
    return t
def dbl(m, P, tt, r):
    t = T(); t.leaves(0, m); p = [0]
    for _ in range(P): p.append(t.add(p[-1]))
    t.leaves(p[-1], m); t.path(p[P - tt], r)
    return t
def bin_(k, d):
    t = T()
    for _ in range(k):
        level = [t.add(0)]
        for _ in range(d): level = [t.add(v) for v in level for _ in range(2)]
    return t
def comb(p, L):
    t = T(); sp = [0]
    for _ in range(p - 1): sp.append(t.add(sp[-1]))
    for v in sp: t.path(v, L)
    return t
def forkhub(a, m, b):
    t = T(); t.path(0, b); t.path(0, b); t.leaves(t.path(0, a), m)
    return t
def brooms(k, a, m, L):
    t = T()
    for _ in range(k): t.leaves(t.path(0, a), m)
    t.path(0, L)
    return t
def twolevel(k, j, m):
    t = T()
    for _ in range(k):
        x = t.add(0)
        for _ in range(j): t.leaves(t.add(x), m)
    return t

FAM = dict(spider=spider, hubspider=hubspider, hublegs=hublegs, hubleaflegs=hubleaflegs, sph=sph, dbl=dbl, bin=bin_,
           comb=comb, forkhub=forkhub, brooms=brooms, twolevel=twolevel)

def rng(a):
    if '..' in a: lo, hi = a.split('..'); return range(int(lo), int(hi) + 1)
    return [int(a)]

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in FAM: sys.exit(__doc__)
    fam = sys.argv[1]; args = [a for a in sys.argv[2:] if '=' not in a]
    opt = dict(a.split('=') for a in sys.argv[2:] if '=' in a); maxn = int(opt.get('maxn', 126)); minn = int(opt.get('minn', 3))
    for combo in itertools.product(*[rng(a) for a in args]):
        t = FAM[fam](*combo)
        if not (minn <= t.n <= maxn): continue
        print(f"{fam}({','.join(map(str, combo))}): " + " ".join(f"{a} {b}" for a, b in t.E))
