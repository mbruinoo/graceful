# Referee: corollaries of Theorems A and B, built via the stated end pieces / pendant labelings and
# compared with the tree described in words.  Also teeth for the case-2 hypothesis.
import sys, itertools
from base import *
def delta(x, m): return -x - m if x <= 0 else m + 1 - x
for m in range(0, 60):
    I = range(-m, m + 1)
    assert sorted(delta(x, m) for x in I) == list(I) and all(delta(delta(x, m), m) == x for x in I)
    assert sum(1 for x in I if delta(x, m) == x) == 1
    assert sorted(x - delta(x, m) for x in I) == list(I)
print('delta involution, one fixed point, tau bijection: m<60 ok')

# ---- Theorem A, book corollary: C={r,z}
def book_label(T, n, m, S):
    k = 2 * m + 1; par, dep = rooted(T, 0); E = [(0, k * n)]
    # distance to C = {0, n}
    par2 = dict(par); 
    def d(v):
        return 0 if v in (0, n) else d(par[v]) + 1
    for x in range(1, n):
        p = par[x]; dx = d(x)
        for i in range(-m, m + 1):
            ex = i if dx % 2 else delta(i, m)
            lp = k * p if p in (0, n) else k * p + (i if (dx - 1) % 2 else delta(i, m))
            E.append((lp, k * x + ex))
    sh = k * n - 2 * m - 1
    for a, b in S:
        if (a, b) != (0, 2 * m + 1):
            E.append((a if a <= m else a + sh, b if b <= m else b + sh))
    return E
def book_shape(T, n, m, G):
    E = [('r', 'z')]
    nm = lambda v, i: 'r' if v == 0 else ('z' if v == n else (v, i))
    for i in range(2 * m + 1):
        for a, b in T:
            if (a, b) != (0, n): E.append((nm(a, i), nm(b, i)))
    for a, b in G: E.append((('G', a) if a else 'r', ('G', b)))
    for j in range(m): E.append(('r', ('leaf', j)))
    return E
tot = fails = teeth_tot = teeth_fail = 0
for m in range(0, 4):
    for n in range(1, 6 if m < 3 else 5):
        for T in growth_labelings(n):
            for G in growth_labelings(m):
                S = list(G) + [(0, x) for x in range(m + 1, 2 * m + 2)]
                assert is_growth(S, 2 * m + 1)
                E = book_label(T, n, m, S); tot += 1
                if not (is_growth(E, (2 * m + 1) * n) and canon(E, 0) == canon(book_shape(T, n, m, G), 'r')
                        and canon(E, (2 * m + 1) * n) == canon(book_shape(T, n, m, G), 'z')):
                    fails += 1; print('BOOK FAIL', m, T, G)
            if m in (1, 2) and n <= 4:
                for S in growth_labelings(2 * m + 1):
                    if any(b - a <= m and a <= m < b for a, b in S):
                        teeth_tot += 1
                        if not is_growth(book_label(T, n, m, S), (2 * m + 1) * n): teeth_fail += 1
print('book corollary: composites', tot, 'fails', fails, '| teeth (end piece with a short bracket across the middle, C={r,z}):', teeth_fail, 'of', teeth_tot, 'fail')

# ---- Theorem B, tree-language corollary
def pendant(U, q):  # reflect, shift by 1, add root 0 joined to old root (now q+1)
    return [(0, q + 1)] + [(q + 1 - b, q + 1 - a) for a, b in U]
tot = fails = 0
for m, QMAX in ((1, 5), (2, 4), (3, 2)):
    k = 2 * m + 1; I = list(range(-m, m + 1))
    fx = [x for x in I if delta(x, m) == x][0]; prs = [(x, delta(x, m)) for x in I if x < delta(x, m)]
    for q in range(0, QMAX + 1):
        reps = {}
        for U in growth_labelings(q): reps.setdefault(canon(U, 0), U)   # one labeling per anchored rooted tree
        Us = list(reps.values()); n = q + 1
        for S in growth_labelings(m):
            for combo in itertools.product(Us, repeat=m + 1):
                fam = {fx: combo[0]}
                for (x, y), U in zip(prs, combo[1:]): fam[x] = U; fam[y] = U
                E = list(S)
                shape = [(('S', a) if a else 'R', ('S', b)) for a, b in S]
                for i in I:
                    P = pendant(fam[i], q); assert is_growth(P, n)
                    par, dep = rooted(P, 0)
                    lab = {0: 0}
                    for v in range(1, n + 1): lab[v] = k * v + (i if dep[v] % 2 else delta(i, m))
                    E += [(lab[a], lab[b]) for a, b in P]
                    shape.append(('R', (i, 0)))
                    shape += [((i, a), (i, b)) for a, b in fam[i]]
                tot += 1
                if not (is_growth(E, k * n + m) and canon(E, 0) == canon(shape, 'R')):
                    fails += 1; print('PENDANT FAIL', m, q)
print('mixed-bunch corollary: composites', tot, 'fails', fails)
