#!/usr/bin/env python3
"""Compare three things for the double-hub tree DH(p,q) (path c1 - v - c2, p leaves on c1, q on c2,
m = p+q+2 edges):
  (1) README section 16 / src/attack/anchors rule H2 (v is an anchor);
  (2) Van Bussel 2004 criterion as restated by Superdock (arXiv:1403.1564, Theorem 2.54) for
      "0-centred graceful" (v can carry label 0 in SOME graceful labeling, no growth condition);
  (3) brute force of both properties from the definitions.
Usage: vb_check.py MFORM MBRUTE   (formula comparison for m <= MFORM, brute force for m <= MBRUTE)
"""
import sys
sys.setrecursionlimit(10000)

def h2_rule(p, q):
    m = p + q + 2
    for x in (p, q):
        for s in range(2, m + 1):
            if m % s: continue
            t = m // s
            j = x - (s - 2)
            if 0 <= j <= t - 1 and (t % 2 == 0 or j % 2 == 0):
                return True
    return False

def vb_rule(p, q):
    n = p + q + 2
    m1, m2 = max(p, q), min(p, q)
    for r in range(2, n // 2 + 1):
        for x in range(0, min(r - 1, m2) + 1):
            if x % 2 == 1 and r % 2 == 1: continue
            if m1 == (m2 + 2 - x) * (r - 1) - x:
                return True
    return False

def brute(p, q, growth):
    """Is there a graceful labeling of DH(p,q) with v = 0 (growth: lengths decreasing away from v)?"""
    m = p + q + 2
    for a, b in [(m, None), (None, m)]:
        for other in range(1, m):
            A, B = (m, other) if a == m else (other, m)   # labels of c1, c2
            labels = [l for l in range(1, m + 1) if l not in (A, B)]
            used = {A, B}                                   # edge lengths used (v-c1 = A, v-c2 = B)
            def rec(i, ca, cb):
                if i == len(labels):
                    return ca == p and cb == q
                l = labels[i]
                if ca < p:
                    d = abs(A - l)
                    if d not in used and (not growth or d < A):
                        used.add(d)
                        if rec(i + 1, ca + 1, cb): used.discard(d); return True
                        used.discard(d)
                if cb < q:
                    d = abs(B - l)
                    if d not in used and (not growth or d < B):
                        used.add(d)
                        if rec(i + 1, ca, cb + 1): used.discard(d); return True
                        used.discard(d)
                return False
            if rec(0, 0, 0): return True
    return False

MF, MB = int(sys.argv[1]), int(sys.argv[2])
dis = tot = non = 0
for m in range(4, MF + 1):
    for p in range(1, m - 2):
        q = m - 2 - p
        if q < p: continue
        tot += 1
        a, b = h2_rule(p, q), vb_rule(p, q)
        non += (not a)
        if a != b: dis += 1; print("FORMULA MISMATCH", p, q, a, b)
print(f"formulas: {tot} trees DH(p,q), 1<=p<=q, m<={MF}: {non} with v not an anchor by H2; "
      f"H2 rule vs Van Bussel rule disagreements: {dis}")
bad = cnt = 0
for m in range(4, MB + 1):
    for p in range(1, m - 2):
        q = m - 2 - p
        if q < p: continue
        cnt += 1
        g, z, f = brute(p, q, True), brute(p, q, False), h2_rule(p, q)
        if not (g == z == f): bad += 1; print("BRUTE MISMATCH", p, q, "growth", g, "0-centred", z, "rule", f)
print(f"brute force: {cnt} trees, m<={MB}: anchor == 0-centred graceful == rule in all but {bad} cases")
