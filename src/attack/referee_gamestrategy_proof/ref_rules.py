#!/usr/bin/env python3
"""Referee check, written independently of comb_rules.py.
Builds the labelings of claims 0 and 1 from the stated rules and checks them from README section 1.
usage: python3 ref_rules.py N"""
import sys
from collections import Counter

def check(edges, n, root_deg, hubsizes_expected):
    """edges on labels 1..n. Returns None if ok else reason."""
    if len(edges) != n-1: return "edge count"
    verts = set()
    for a, b in edges: verts |= {a, b}
    if verts != set(range(1, n+1)): return "labels not 1..n"
    L = sorted(abs(a-b) for a, b in edges)
    if L != list(range(1, n)): return "lengths not 1..n-1"
    used = set()
    for a, b in sorted(edges, key=lambda e: -abs(e[0]-e[1])):
        if not used:
            if {a, b} != {1, n}: return "top bracket"
            used |= {a, b}; continue
        if (a in used) + (b in used) != 1: return "growth fails at length %d" % abs(a-b)
        used |= {a, b}
    adj = {v: set() for v in verts}
    for a, b in edges: adj[a].add(b); adj[b].add(a)
    if len(adj[1]) != root_deg: return "root degree"
    # structure: find centre = the unique non-leaf neighbour of 1 (root hub), then hubs
    nl = [v for v in adj[1] if len(adj[v]) > 1]
    if len(nl) != 1:
        return "root hub does not have exactly one non-leaf neighbour"
    c = nl[0]
    sizes = []
    for h in adj[c]:
        lv = adj[h] - {c}
        if any(len(adj[x]) != 1 for x in lv): return "hub has non-leaf child"
        sizes.append(len(lv))
    rootsize = len(adj[1]) - 1
    sizes_other = Counter(sizes); sizes_other[rootsize] -= 1
    exp = Counter(hubsizes_expected)
    if +sizes_other != +exp: return "wrong tree %s vs %s" % (sizes, hubsizes_expected)
    return None

def comb(y, hubs, W, a1):
    """hubs: list of (h, U). labels 0..m. returns edges with +1 shift, n; plus lemma-hypothesis check."""
    m = len(hubs) + 1 + a1 + sum(len(U) for h, U in hubs)
    if len(W) > a1: return None, "W too big"
    E = [(0, y)] + [(0, w) for w in W] + [(0, x) for x in range(y+1, m+1)]
    if len(E) != a1 + 1: return None, "root leaves count %d vs %d" % (len(E)-1, a1)
    for h, U in hubs:
        E.append((y, h))
        for u in U:
            if not (1 <= u <= y-1-h): return None, "U bound"
            E.append((h, h+u))
    return ([(a+1, b+1) for a, b in E], m+1), None

def three(a1, p, q):
    if (a1, p, q) == (2, 2, 1):
        return comb(8, [(1, [1, 2]), (4, [3])], [5, 6], a1), [2, 1]
    if (p - q) % 2 == 0:
        U1 = list(range(1, 2*q, 2))
        if p == q:
            U3 = list(range(2, 2*q+1, 2)); W = [2*q+2]; y = 2*q+4
        else:
            J = (p-q-2)//2; t = lambda j: 2*q+2+3*j
            U3 = list(range(2, 2*q+1, 2)) + [2*q+1]
            for j in range(J): U3 += [t(j)+1, t(j)+2]
            U3 += [t(J)+1]
            W = [t(j) for j in range(J+1)] + [t(J)+3]; y = t(J)+5
        return comb(y, [(1, U1), (3, U3)], W, a1), [q, p]
    Q, P = (p, q) if p % 2 == 0 else (q, p)
    r = Q//2
    U2 = list(range(2, P+2))
    U3 = []
    for j in range(r): U3 += [P+2+3*j, P+3+3*j]
    W = [1] + [P+4+3*j for j in range(r+1)]; y = P+3*r+5
    return comb(y, [(2, U2), (3, U3)], W, a1), [P, Q]

def equal(d, a, a1):
    y = d*(a+2); hubs = []
    for i in range(d):
        h = 2*i+1
        if d % 2: s = 2*i+d if 2*i+d <= 2*d-1 else 2*i-d
        else: s = d-1-i if i % 2 == 0 else 2*d-1-i
        hubs.append((h, [s + d*j for j in range(a)]))
    if d % 2:
        W = [x for x in range(2, d) if x % 2 == 0] + [d*a+x for x in range(d+1, 2*d) if x % 2 == 0]
    else:
        W = [x for x in range(2, d-1) if x % 2 == 0] + [d*a+x for x in range(d, 2*d-1) if x % 2 == 0]
    return comb(y, hubs, W, a1), [a]*d

N = int(sys.argv[1])
cnt = bad = 0
for q in range(1, N):
    for p in range(q, N):
        for a1 in range(p, N):
            if a1+p+q+4 > N: break
            (res, err), sizes = three(a1, p, q)
            cnt += 1
            if err is None:
                E, n = res
                err = "n" if n != a1+p+q+4 else check(E, n, a1+1, sizes)
            if err: bad += 1; print("claim0 FAIL", (a1, p, q), err)
print("claim0: %d triples with n<=%d, %d failures" % (cnt, N, bad))
cnt = bad = 0; byd = Counter()
for d in range(1, N):
    for a in range(1, N):
        for a1 in range(max(d-1, 0), N):
            n = d*(a+1)+a1+2
            if n > N: break
            (res, err), sizes = equal(d, a, a1)
            cnt += 1; byd[d] += 1
            if err is None:
                E, n2 = res
                err = "n" if n2 != n else check(E, n, a1+1, sizes)
            if err: bad += 1; print("claim1 FAIL", (d, a, a1), err)
print("claim1: %d triples with n<=%d, %d failures; max d=%d" % (cnt, N, bad, max(byd)))
