#!/usr/bin/env python3
"""Referee check of claim 0: build the three path labellings exactly as the
proof text describes (landing labels written out phase by phase), then check
from README section 1/2 only.  Also the corollary by the section 7/13 gluing.
Labels 0..m here; README labels are these +1."""
import sys

def zig_hi(p, q, cnt):   # q, p, q-1, p+1, ...
    out = []; lo, hi = p, q
    for i in range(cnt):
        if i % 2 == 0: out.append(hi); hi -= 1
        else: out.append(lo); lo += 1
    return out
def zig_lo(p, q, cnt):   # p, q, p+1, q-1, ...
    out = []; lo, hi = p, q
    for i in range(cnt):
        if i % 2 == 0: out.append(lo); lo += 1
        else: out.append(hi); hi -= 1
    return out

def fam1(s):
    m = 3*s+2
    A = [0]; B = [0, m]
    for i in range(1, s+1): A += [m-i, i]
    B.append(2*s+1)
    A += zig_hi(s+1, 2*s, s)
    return m, A, B
def fam2(s):
    m = 5*s+4
    A = [0]; B = [0]
    for i in range(0, s+1): A += [m-i, i+1]          # m,1,m-1,2,...,m-s,s+1
    B.append(3*s+2)
    for i in range(1, s+1): A += [4*s+3-i, s+1+i]
    B.append(4*s+3)
    A += zig_hi(2*s+2, 3*s+1, s)
    return m, A, B
def fam3(s):
    m = 7*s+3
    A = [0]; B = [0]
    for i in range(0, 2*s): A += [m-i, i+1]          # 4s numbers
    A.append(m-2*s)                                  # the (4s+1)-th, lands 5s+3
    B.append(3*s+2)
    for i in range(1, s+1): A += [2*s+1+i, 5*s+3-i]
    B.append(2*s+1)
    A += zig_lo(3*s+3, 4*s+2, s)
    return m, A, B

def check_growth(edges, nv):
    """edges: list of (u,v) labels in 0..nv-1. README sec 1+2 test."""
    assert len(edges) == nv-1
    lens = sorted(abs(u-v) for u, v in edges)
    if lens != list(range(1, nv)): return "lengths not 1..m once each"
    bylen = {abs(u-v): (u, v) for u, v in edges}
    used = set(bylen[nv-1])
    if used != {0, nv-1}: return "top bracket"
    for k in range(nv-2, 0, -1):
        u, v = bylen[k]
        if (u in used) == (v in used): return "bracket %d has %d used feet" % (k, 2*(u in used))
        used |= {u, v}
    if used != set(range(nv)): return "labels"
    return None

def path_edges(seq): return list(zip(seq, seq[1:]))

def check_family(name, fam, smax):
    bad = 0
    for s in range(1, smax+1):
        m, A, B = fam(s)
        seq = B[::-1] + A[1:]          # the whole path, end of B first
        ok = (len(A) == m-1 and len(B) == 3 and sorted(seq) == list(range(m+1)) and seq[2] == 0)
        err = None if ok else "shape"
        if ok: err = check_growth(path_edges(seq), m+1)
        # also: deal order -- lengths decrease outward along each leg
        if not err:
            for L in (A, B):
                d = [abs(a-b) for a, b in zip(L, L[1:])]
                if any(x <= y for x, y in zip(d, d[1:])): err = "not decreasing outward"
        if err:
            bad += 1
            if bad < 5: print("  FAIL", name, "s=%d m=%d: %s" % (s, m, err))
    print("%s: s=1..%d, failures: %d" % (name, smax, bad))
    return bad

def glue_spider(m, A, B, c):
    """Section 7 gluing. O = zigzag path on c edges, labels 1..c+1 (README labels),
    x = end with the largest low label a+1.  T' = path labelling (README labels 1..m+1,
    y labelled 1).  Result on labels 1..m+c+1; returned 0-based."""
    O = []
    lo, hi = 1, c+1
    for i in range(c+1):
        if i % 2 == 0: O.append(lo); lo += 1
        else: O.append(hi); hi -= 1
    if c % 2 == 1: O = [c+2-x for x in O]
    x = O[-1]            # far end
    a = x - 1            # x labelled a+1
    assert all((min(u, v) <= a+1) and (max(u, v) > a+1) for u, v in zip(O, O[1:])), "O not bipartite about a+1"
    assert x == max(v for v in O if v <= a+1)
    nT = m+1
    newO = [v if v <= a+1 else v + nT - 1 for v in O]
    shift = a            # T' label t (1..nT) -> a + t ; y (label 1) -> a+1 = x
    edges = path_edges(newO)
    edges += [(u+1+shift, v+1+shift) for u, v in path_edges(A)]
    edges += [(u+1+shift, v+1+shift) for u, v in path_edges(B)]
    return [(u-1, v-1) for u, v in edges]

def spider_legs(edges, nv):
    adj = {i: [] for i in range(nv)}
    for u, v in edges: adj[u].append(v); adj[v].append(u)
    deg3 = [v for v in adj if len(adj[v]) >= 3]
    if len(deg3) != 1 or len(adj[deg3[0]]) != 3: return None
    c = deg3[0]; legs = []
    for w in adj[c]:
        prev, cur, d = c, w, 1
        while len(adj[cur]) == 2:
            nx = [z for z in adj[cur] if z != prev][0]; prev, cur = cur, nx; d += 1
        if len(adj[cur]) != 1: return None
        legs.append(d)
    return sorted(legs)

if __name__ == "__main__":
    smax = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    tot = 0
    for name, fam in (("m=3s+2", fam1), ("m=5s+4", fam2), ("m=7s+3", fam3)):
        tot += check_family(name, fam, smax)
    # corollary
    cases = bad = 0
    for name, fam in (("a=3s", fam1), ("a=5s+2", fam2), ("a=7s+1", fam3)):
        for s in range(1, 41):
            m, A, B = fam(s)
            for c in range(1, 61):
                cases += 1
                E = glue_spider(m, A, B, c)
                nv = m+c+1
                err = check_growth(E, nv)
                legs = spider_legs(E, nv)
                if err or legs != sorted([m-2, 2, c]):
                    bad += 1
                    if bad < 5: print("  FAIL spider", name, s, c, err, legs)
    print("spider corollary by gluing: %d cases (s<=40, c<=60), failures: %d" % (cases, bad))
    sys.exit(1 if tot or bad else 0)
