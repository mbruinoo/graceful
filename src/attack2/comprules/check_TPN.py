"""Brute-force check of Rules T, P, N (as restated in REPORT.txt) from the definitions in gp.py.
usage: python3 check_TPN.py [NMAX=7]"""
import sys
from gp import *
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
G = {m: all_growth(m) for m in range(0, NMAX)}

def growth_general(brs, m):
    """brs: dict length -> (a,b) for lengths 1..m. Growth test from the definition (any feet)."""
    if sorted(brs) != list(range(1, m + 1)): return False
    for k, (a, b) in brs.items():
        if b - a != k or a < 0 or b > m: return False
    used = set(brs[m])
    for k in range(m - 1, 0, -1):
        a, b = brs[k]
        if (a in used) == (b in used): return False
        used.add(a); used.add(b)
    return True

# ---------------- Rule T
okT = badT = 0; viol_growth = 0; viol = 0
for mf in range(2, NMAX):
    for f in G[mf]:
        for mh in range(2, NMAX):
            for h in G[mh]:
                newh, oldh, _ = info(h, mh)
                for k in range(1, min(mf, mh)):
                    Ff = free_at(f, mf, k); Fh = free_at(h, mh, k)
                    s = min(Ff) - min(Fh)
                    if frozenset(x + s for x in Fh) != Ff: continue      # hypothesis 1
                    touched = {oldh[i] for i in range(1, k + 1) if oldh[i] not in Fh}
                    hyp2 = all(0 <= a + s <= mf and (a + s) not in Ff for a in touched)
                    brs = {i: (f[i], f[i] + i) for i in range(k + 1, mf + 1)}
                    for i in range(1, k + 1): brs[i] = (h[i] + s, h[i] + s + i)
                    g = growth_general(brs, mf)
                    if hyp2:
                        okT += 1
                        if not g: badT += 1; print('T FAILS', fmt(f, mf), '|', fmt(h, mh), k)
                    else:
                        viol += 1
                        if g: viol_growth += 1; print('T: growth without hyp 2', fmt(f, mf), '|', fmt(h, mh), k)
print('Rule T: applications with hyp 1 and 2:', okT, ' not growth:', badT)
print('Rule T: hyp 1 without hyp 2:', viol, ' of which growth:', viol_growth)

# ---------------- Rule P
okP = badP = 0; treebad = 0
for mf in range(2, NMAX):
    for f in G[mf]:
        for k in range(1, mf):
            F = sorted(free_at(f, mf, k)); x = F[0]
            if F != list(range(x, x + k)): continue
            for g in G[k]:
                for pos in (0, 1):
                    base = x - 1 + pos                 # g sits on [base, base+k]
                    brs = {i: (f[i], f[i] + i) for i in range(k + 1, mf + 1)}
                    for i in range(1, k + 1): brs[i] = (g[i] + base, g[i] + base + i)
                    okP += 1
                    if not growth_general(brs, mf):
                        badP += 1; print('P FAILS', fmt(f, mf), k, fmt(g, k), pos)
                    # tree statement: prefix tree R of f with tree(g) attached, R's vertex (x-1 resp. x+k)
                    # identified with g's vertex 0 resp. k
                    R = [(f[i], f[i] + i) for i in range(k + 1, mf + 1)]
                    glue_f = x - 1 if pos == 0 else x + k
                    glue_g = 0 if pos == 0 else k
                    ge = [(('g', a) if a != glue_g else glue_f, ('g', b) if b != glue_g else glue_f) for a, b in edges(g, k)]
                    if tree_canon(R + ge) != tree_canon(list(brs.values())): treebad += 1
print('Rule P: applications:', okP, ' not growth:', badP, ' tree statement wrong:', treebad)

# ---------------- Rule N
okN = badN = 0; violN = violN_growth = 0; treebadN = 0; uneg = 0
for mf in range(1, NMAX):
    n = mf + 1
    for f in G[mf]:
        newf, oldf, ellf = info(f, mf) if mf else ({}, {}, {})
        for L in range(1, mf + 1):
            jump = [i for i in range(1, mf + 1) if f[i] <= L - 1 and f[i] + i >= L]
            c = len(jump)
            if sorted(jump) != list(range(mf - c + 1, mf + 1)): continue      # clean cut
            j = n - c
            u = L - j
            if u < 0: uneg += 1; continue
            admissible = (u == 0) or (ellf.get(u, 0) > j - 1)        # u added by a jumping bracket
            for g in range(1, NMAX + 1 - j):
                mh = g + j - 1
                if mh > NMAX - 1: continue
                for h in G[mh]:
                    newh, oldh, _ = info(h, mh)
                    if sorted(newh[i] for i in range(1, j)) != list(range(1, j)): continue
                    M = mf + g
                    brs = {}
                    up = lambda x: x + g if x >= L else x
                    for i in range(1, mf + 1):
                        a, b = up(f[i]), up(f[i] + i)
                        brs[b - a] = (a, b)
                    emb = lambda y: u if y == 0 else u + y
                    Uedges = []
                    for i in range(j, mh + 1):
                        a, b = sorted((emb(h[i]), emb(h[i] + i)))
                        if (b - a) in brs: brs = None; break
                        brs[b - a] = (a, b); Uedges.append((h[i], h[i] + i))
                    gr = brs is not None and growth_general(brs, M)
                    if admissible:
                        okN += 1
                        if not gr: badN += 1; print('N FAILS', fmt(f, mf), L, fmt(h, mh))
                        else:
                            ge = [(('h', a) if a != 0 else u, ('h', b) if b != 0 else u) for a, b in Uedges]
                            if tree_canon(edges(f, mf) + ge) != tree_canon(list(brs.values())): treebadN += 1
                    else:
                        violN += 1
                        if gr: violN_growth += 1; print('N: growth with bad u', fmt(f, mf), L, fmt(h, mh))
print('Rule N: applications:', okN, ' not growth:', badN, ' tree statement wrong:', treebadN)
print('Rule N: u >= 0 not admissible:', violN, ' of which growth:', violN_growth, ' (clean cuts with u < 0:', uneg, ')')
