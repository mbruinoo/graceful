"""Brute-force check of Rules B and D, failing rule F3 and Propositions 1, 2 (as restated in REPORT.txt).
usage: python3 check_BD.py [PMAX=7] [TMAX=5]"""
import sys
from itertools import product
from gp import *
PMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
TMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 5
G = {m: all_growth(m) for m in range(0, PMAX)}

def band(j, v): return j - v if v <= j else v - j - 1

def build(f, mf, design, t):
    """The placement of Rule B: label i -> t*i, leaves of the owner of block j on jt+1..jt+t-1.
    Returns dict length -> (a,b), or None if two brackets get the same length."""
    brs = {}
    for i in range(1, mf + 1): brs[t * i] = (t * f[i], t * (f[i] + i))
    for j, v in enumerate(design):
        for d in range(1, t):
            a, b = sorted((t * v, j * t + d))
            if b - a in brs: return None
            brs[b - a] = (a, b)
    return brs

def growth_general(brs, m):
    if brs is None or sorted(brs) != list(range(1, m + 1)): return False
    used = set(brs[m])
    for k in range(m - 1, 0, -1):
        a, b = brs[k]
        if (a in used) == (b in used): return False
        used.add(a); used.add(b)
    return True

def expected_tree(f, mf, design, t):
    E = edges(f, mf); c = 0
    for j, v in enumerate(design):
        for d in range(1, t):
            E.append((v, ('leaf', c))); c += 1
    return tree_canon(E)

apps = bad = treebad = 0
inv = inv_growth = 0; cond1 = 0
fam = {}
for mf in range(1, PMAX):
    p = mf + 1
    for f in G[mf]:
        new, old, ell = info(f, mf)
        for design in product(range(p), repeat=mf):       # owner of block j, j = 0..p-2
            bands = [band(j, v) for j, v in enumerate(design)]
            if sorted(bands) != list(range(mf)): continue  # condition 1
            c2 = all(v == 0 or bands[j] < ell[v] for j, v in enumerate(design))
            if c2:
                for t in range(2, TMAX + 1):
                    brs = build(f, mf, design, t); apps += 1
                    M = mf * t
                    if not growth_general(brs, M): bad += 1; print('B FAILS', fmt(f, mf), design, t)
                    elif tree_canon(list(brs.values())) != expected_tree(f, mf, design, t): treebad += 1
            if p <= 6:
                cond1 += 1
                g2 = growth_general(build(f, mf, design, 2), 2 * mf)
                if g2 != c2: print('B t=2: growth <=> condition 2 FAILS', fmt(f, mf), design)
                if not c2:
                    inv += 1; inv_growth += g2
print('Rule B: applications (valid design, t=2..%d, p<=%d):' % (TMAX, PMAX), apps, ' not growth:', bad, ' tree statement wrong:', treebad)
print('Rule B, t=2, p<=6: assignments with condition 1:', cond1, ' without condition 2:', inv, ' of which growth:', inv_growth)

# ---------------- Rule D
appsD = badD = 0
for mf in range(1, PMAX):
    p = mf + 1
    for f in G[mf]:
        new, old, ell = info(f, mf)
        for w in range(1, p + 1):
            hyp = all((ell[i] >= w - 2 * i) if 2 * i <= w - 1 else (ell[i] >= 2 * i - w + 1) for i in range(1, w))
            design = [w - 1 - j if j < w - 1 else 0 for j in range(mf)]
            bands = [band(j, v) for j, v in enumerate(design)]
            c1 = sorted(bands) == list(range(mf))
            c2 = all(v == 0 or bands[j] < ell[v] for j, v in enumerate(design))
            if not c1: print('D: window design not a bijection', fmt(f, mf), w)
            if hyp != c2: print('D: hypothesis differs from condition 2', fmt(f, mf), w)
            if hyp:
                for t in range(2, TMAX + 1):
                    appsD += 1
                    brs = build(f, mf, design, t)
                    if not growth_general(brs, mf * t): badD += 1; print('D FAILS')
                    else:
                        E = edges(f, mf); c = 0
                        for i in range(1, w):
                            for d in range(t - 1): E.append((i, ('l', c))); c += 1
                        for d in range((p - w) * (t - 1)): E.append((0, ('l', c))); c += 1
                        if tree_canon(E) != tree_canon(list(brs.values())): badD += 1; print('D tree wrong')
print('Rule D: applications:', appsD, ' failures:', badD)

# ---------------- F3 and Proposition 2
QMAX = 5
tot = graceful = growth = starcases = 0; nonstar_growth = 0; smallest = None; d_agree = 0
for mf in range(1, QMAX):
    p = mf + 1
    for f in G[mf]:
        newf, oldf, ellf = info(f, mf)
        for mg in range(1, QMAX):
            q = mg + 1
            for g in G[mg]:
                adj = adj_of(edges(g, mg))
                dist = {0: 0}; st = [0]
                while st:
                    x = st.pop()
                    for y in adj[x]:
                        if y not in dist: dist[y] = dist[x] + 1; st.append(y)
                lab = lambda i, x: (i if dist[x] % 2 == 0 else p - 1 - i) * q + x
                E = [(lab(i, a), lab(i, b)) for i in range(p) for a, b in edges(g, mg)]
                E += [(a * q, b * q) for a, b in edges(f, mf)]
                M = p * q - 1
                tot += 1
                labs = {x for e in E for x in e}; lens = sorted(abs(a - b) for a, b in E)
                gr = labs == set(range(M + 1)) and lens == list(range(1, M + 1)) and is_tree(E, M + 1)
                graceful += gr
                brs = {abs(a - b): tuple(sorted((a, b))) for a, b in E}
                isg = gr and growth_general(brs, M)
                star = max(dist.values()) <= 1
                growth += isg
                if isg and not star: nonstar_growth += 1
                if not isg and smallest is None: smallest = (fmt(f, mf), fmt(g, mg), ' '.join('%d-%d' % brs[k] for k in range(M, 0, -1)))
                if star:
                    starcases += 1
                    w = p
                    hyp = all((ellf[i] >= w - 2 * i) if 2 * i <= w - 1 else (ellf[i] >= 2 * i - w + 1) for i in range(1, w))
                    d_agree += (hyp == isg)
print('F3: pairs of placements p,q<=%d:' % QMAX, tot, ' graceful trees:', graceful, ' growth:', growth,
      ' growth with T\' not a star centred at v\':', nonstar_growth)
print('F3: first failure (f | g | labelling):', smallest)
print('F3: pairs with T\' a star centred at 0:', starcases, ' of which "growth <=> mirror condition of Rule D with w=p":', d_agree)

# ---------------- Proposition 1 (staircases closed under C, P, T), n <= PMAX
S = {m: [P for P in G[m] if is_staircase(P, m)] for m in range(1, PMAX)}
for m in S: assert len(S[m]) == 2 ** (m - 1)
cC = cP = cT = 0; badS = 0
for mf in range(1, PMAX):
    for f in S[mf]:
        cC += 1; badS += not is_staircase(complement(f, mf), mf)
        for k in range(1, mf):
            F = sorted(free_at(f, mf, k)); x = F[0]
            assert F == list(range(x, x + k))          # a staircase has one run at every time
            for g in S[k]:
                for pos in (0, 1):
                    P = f[:]
                    for i in range(1, k + 1): P[i] = g[i] + x - 1 + pos
                    cP += 1; badS += not is_staircase(P, mf)
            for mh in range(2, PMAX):
                if k >= mh: continue
                for h in S[mh]:
                    Fh = sorted(free_at(h, mh, k)); s = x - Fh[0]
                    newh, oldh, _ = info(h, mh)
                    if not all(0 <= oldh[i] + s <= mf for i in range(1, k + 1)): continue
                    P = f[:]
                    for i in range(1, k + 1): P[i] = h[i] + s
                    cT += 1; badS += not is_staircase(P, mf)
print('Proposition 1: C on %d staircases, P %d applications, T %d applications; results that are not staircases: %d' % (cC, cP, cT, badS))
