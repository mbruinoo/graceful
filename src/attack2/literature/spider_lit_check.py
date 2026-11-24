#!/usr/bin/env python3
"""Do the published centre-0 spider labelings happen to be 'deals' (README section 13: centre 0 and
edge lengths strictly decreasing outward along every leg)?  Two published constructions are
re-implemented from the papers' formulas and tested.

 (1) Bahls, Lake, Wertheim, Involve 3 (2010) 241-247, proof of Theorem 1, odd number l of legs,
     l1 legs of length m+1 and l-l1 legs of length m.
 (2) Shan, Zhong, arXiv:2605.14295v2 (2026), proof of Theorem 4: s legs of length 2 and one leg of
     length ell.
Usage: spider_lit_check.py
"""
def check(legs, m):
    """legs: list of label lists going outward from the centre (centre label 0 not included)."""
    labs = [0] + [x for L in legs for x in L]
    ok_v = sorted(labs) == list(range(m + 1))
    lens, dec = [], True
    for L in legs:
        prev, last = 0, None
        for x in L:
            d = abs(x - prev); lens.append(d)
            if last is not None and d >= last: dec = False
            last, prev = d, x
    graceful = ok_v and sorted(lens) == list(range(1, m + 1))
    return graceful, dec

def blw(l, m, l1):
    n = l * m + l1
    legs = []
    for i in range(1, l + 1):
        L = []
        for j in range(1, (m + 1 if i <= l1 else m) + 1):
            if i % 2 and j % 2:        v = n - (i - 1) // 2 - (j - 1) * l // 2
            elif i % 2 == 0 and j % 2 == 0: v = n - (l - 1) // 2 - i // 2 - (j - 2) * l // 2
            elif i % 2 == 0:           v = i // 2 + (j - 1) * l // 2
            else:                      v = (l - 1) // 2 + (i + 1) // 2 + (j - 2) * l // 2
            L.append(v)
        legs.append(L)
    return legs, n

def sz(s, ell):
    m = 2 * s + ell
    legs = []
    for i in range(1, s + 1):
        legs.append([m - (2 * i - 1), 2 * i - 1] if ell % 2 else [m - 2 * (i - 1), 2 * i - 1])
    N = []
    for i in range(1, ell + 1):
        r = i % 4
        if ell % 2:
            v = (i // 2 if r == 0 else m - (i - 1) // 2 if r == 1 else
                 2 * s - 1 + (i + 2) // 2 if r == 2 else m - (2 * s - 1) - (i + 1) // 2)
        else:
            v = (i // 2 if r == 0 else m - 2 * s - (i - 1) // 2 if r == 1 else
                 2 * s - 1 + (i + 2) // 2 if r == 2 else m - 1 - (i - 3) // 2)
        N.append(v)
    legs.append(N)
    return legs, m

tot = g = d = 0
for l in range(3, 16, 2):
    for m in range(1, 13):
        for l1 in range(0, l):
            legs, n = blw(l, m, l1); a, b = check(legs, n); tot += 1; g += a; d += (a and b)
print(f"Bahls-Lake-Wertheim: {tot} spiders (odd l<=15 legs, m<=12): graceful with centre 0: {g}; "
      f"of these with lengths decreasing outward on every leg (a deal): {d}")
tot = g = d = 0; ex = []
for s in range(2, 13):
    for ell in range(1, 41):
        legs, m = sz(s, ell); a, b = check(legs, m); tot += 1; g += a; d += (a and b)
        if a and b: ex.append((s, ell))
print(f"Shan-Zhong Thm 4: {tot} spiders (2<=s<=12 legs of length 2, long leg 1..40): graceful with "
      f"centre 0: {g}; of these deals: {d} {ex[:12]}")
