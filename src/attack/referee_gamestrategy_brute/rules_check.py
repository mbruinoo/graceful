#!/usr/bin/env python3
"""Referee check of claims 0 and 1 (three-hub rule, equal-hub rule).
Written from the claim text and README section 1 only.  Usage: rules_check.py NMAX"""
import sys

def verify(n, root_leaves, y, hubs, a1, others):
    """hubs: list of (h, [leaf labels]) for non-root hubs; labels 0..m.
    others: expected multiset of non-root hub sizes.  Returns error string or None."""
    m = n - 1
    edges = [(0, y)] + [(0, x) for x in root_leaves]
    for h, lv in hubs:
        edges.append((y, h))
        edges += [(h, x) for x in lv]
    # shift to README labels 1..n
    edges = [(a + 1, b + 1) for a, b in edges]
    if len(edges) != n - 1: return "edge count %d" % len(edges)
    labs = set()
    for a, b in edges: labs |= {a, b}
    if labs != set(range(1, n + 1)): return "labels not 1..n"
    # every label used by exactly one tree vertex: vertices are identified with labels here, so
    # check instead that the *intended* vertices got distinct labels
    intended = [0, y] + list(root_leaves) + [h for h, _ in hubs] + [x for _, lv in hubs for x in lv]
    if len(intended) != n or len(set(intended)) != n: return "vertex labels collide"
    lens = sorted(abs(a - b) for a, b in edges)
    if lens != list(range(1, n)): return "lengths not 1..n-1"
    # growth: longest first, exactly one used foot
    bylen = {abs(a - b): (a, b) for a, b in edges}
    if set(bylen[n - 1]) != {1, n}: return "top bracket"
    used = {1, n}
    for k in range(n - 2, 0, -1):
        a, b = bylen[k]
        if (a in used) + (b in used) != 1: return "growth fails at length %d" % k
        used |= {a, b}
    # tree shape, from the edge set alone
    adj = {v: set() for v in range(1, n + 1)}
    for a, b in edges: adj[a].add(b); adj[b].add(a)
    if len(adj[1]) != a1 + 1: return "deg(label 1) = %d" % len(adj[1])
    nonleaf = [v for v in adj[1] if len(adj[v]) > 1]
    if a1 + len(others) + 2 + sum(others) != n: return "n mismatch"
    if len(nonleaf) != 1: return "root has %d non-leaf nbrs" % len(nonleaf)
    c = nonleaf[0]
    sizes = []
    for hv in adj[c]:
        if hv == 1: continue
        for x in adj[hv]:
            if x != c and len(adj[x]) != 1: return "not depth 2"
        sizes.append(len(adj[hv]) - 1)
    if sorted(sizes) != sorted(others): return "hub sizes %s != %s" % (sorted(sizes), sorted(others))
    return None

def three_hub(a1, p, q):
    n = a1 + p + q + 4; m = n - 1
    if (a1, p, q) == (2, 2, 1):
        hs = [(1, [1, 2]), (4, [3])]; W = [5, 6]; y = 8
    elif (p - q) % 2 == 0:
        U1 = list(range(1, 2 * q, 2))
        if p == q:
            U3 = list(range(2, 2 * q + 1, 2)); W = [2 * q + 2]; y = 2 * q + 4
        else:
            J = (p - q - 2) // 2
            t = lambda j: 2 * q + 2 + 3 * j
            U3 = list(range(2, 2 * q + 1, 2)) + [2 * q + 1]
            for j in range(J): U3 += [t(j) + 1, t(j) + 2]
            U3 += [t(J) + 1]
            W = [t(j) for j in range(J + 1)] + [t(J) + 3]; y = t(J) + 5
        hs = [(1, U1), (3, U3)]
    else:
        Q, P = (p, q) if p % 2 == 0 else (q, p)
        r = Q // 2
        U2 = list(range(2, P + 2))
        U3 = []
        for j in range(r): U3 += [P + 2 + 3 * j, P + 3 + 3 * j]
        W = [1] + [P + 4 + 3 * j for j in range(r + 1)]; y = P + 3 * r + 5
        hs = [(2, U2), (3, U3)]
    return n, y, hs, W

def comb_conditions(y, hs, W, a1):
    full = list(range(1, y))
    L = sorted([y - h for h, _ in hs] + [u for _, U in hs for u in U] + list(W))
    C = sorted([h for h, _ in hs] + [h + u for h, U in hs for u in U] + list(W))
    if L != full: return "(L) fails"
    if C != full: return "(C) fails"
    for h, U in hs:
        if U and (min(U) < 1 or max(U) > y - 1 - h): return "U bound"
    if len(W) > a1: return "|W|>a1"
    return None

def equal_hub(d, a, a1):
    n = d * (a + 1) + a1 + 2
    y = d * (a + 2)
    hs = []
    for i in range(d):
        h = 2 * i + 1
        if d % 2 == 1:
            s = 2 * i + d if 2 * i + d <= 2 * d - 1 else 2 * i - d
        else:
            s = d - 1 - i if i % 2 == 0 else 2 * d - 1 - i
        hs.append((h, [s + d * j for j in range(a)]))
    if d % 2 == 1:
        W = [x for x in range(2, d) if x % 2 == 0] + [d * a + x for x in range(d + 1, 2 * d) if x % 2 == 0]
    else:
        W = [x for x in range(2, d - 1) if x % 2 == 0] + [d * a + x for x in range(d, 2 * d - 1) if x % 2 == 0]
    return n, y, hs, W

def main():
    N = int(sys.argv[1])
    bad = 0; cnt = 0
    for a1 in range(1, N):
        for p in range(1, a1 + 1):
            for q in range(1, p + 1):
                if a1 + p + q + 4 > N: break
                n, y, hs, W = three_hub(a1, p, q); m = n - 1
                cnt += 1
                e = comb_conditions(y, hs, W, a1)
                if e is None:
                    if m - y != a1 - len(W) or m < y: e = "m-y mismatch"
                if e is None:
                    rl = list(W) + list(range(y + 1, m + 1))
                    e = verify(n, rl, y, [(h, [h + u for u in U]) for h, U in hs], a1, [p, q])
                if e:
                    bad += 1
                    if bad < 20: print("CLAIM0 FAIL", (a1, p, q), e)
    print("claim 0: %d triples with n <= %d, %d failures" % (cnt, N, bad))
    bad = 0; cnt = 0; perd = {}
    for d in range(1, N):
        for a in range(1, N):
            if d * (a + 1) + (d - 1) + 2 > N: break
            for a1 in range(max(d - 1, 0), N):
                n, y, hs, W = equal_hub(d, a, a1); m = n - 1
                if n > N: break
                cnt += 1; perd[d] = perd.get(d, 0) + 1
                e = comb_conditions(y, hs, W, a1)
                if e is None and (m - y != a1 - len(W) or m < y): e = "m-y mismatch"
                if e is None:
                    rl = list(W) + list(range(y + 1, m + 1))
                    e = verify(n, rl, y, [(h, [h + u for u in U]) for h, U in hs], a1, [a] * d)
                if e:
                    bad += 1
                    if bad < 20: print("CLAIM1 FAIL", (d, a, a1), e)
    print("claim 1: %d triples (d,a,a1) with n <= %d, %d failures; max d = %d" % (cnt, N, bad, max(perd)))
    print("  per d:", sorted(perd.items())[:12])
main()
