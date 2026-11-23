#!/usr/bin/env python3
"""Brute-force check of the composition rules of REPORT.md, from the definitions.

Independent of closure.cpp.  A placement on n vertices is a dict {k: a}: the bracket of length k is the edge {a, a+k},
labels 0..n-1.  is_gp() is the definition of a growth placement (README section 2).  Every rule is applied to ALL
growth placements of ALL trees with at most S vertices (default 7) that satisfy its hypothesis, and every output is
tested with is_gp().  Where a hypothesis is claimed to be necessary, outputs violating it are tested to fail.

  python3 verify_rules.py [S=7] [CLOSE=9]
The last part recomputes the closure D_n for n <= CLOSE with this code, for comparison with closure.cpp.
"""
import sys, itertools
from collections import defaultdict
S = int(sys.argv[1]) if len(sys.argv) > 1 else 7
CLOSE = int(sys.argv[2]) if len(sys.argv) > 2 else 9

def is_gp(n, p):
    """definition: lengths 1..n-1 once each, labels in 0..n-1, longest first each bracket has exactly one used foot"""
    m = n - 1
    if sorted(p) != list(range(1, m + 1)): return False
    if m == 0: return True
    if p[m] != 0: return False
    used = {0, m}
    for k in range(m - 1, 0, -1):
        a, b = p[k], p[k] + k
        if a < 0 or b > m: return False
        if (a in used) == (b in used): return False
        used |= {a, b}
    return len(used) == n

def all_gp(n):
    m = n - 1; out = []
    if m == 0: return [dict()]
    def rec(k, used, p):
        if k == 0: out.append(dict(p)); return
        for a in range(0, m - k + 1):
            if (a in used) != (a + k in used):
                p[k] = a; rec(k - 1, used | {a, a + k}, p)
        p.pop(k, None)
    rec(m - 1, {0, m}, {m: 0}); return out

def info(n, p):
    """parent label and parent bracket length of every label, tree rooted at label 0"""
    m = n - 1; par = {0: None}; plen = {0: 10**9}; used = {0}
    if m: par[m] = 0; plen[m] = m; used.add(m)
    for k in range(m - 1, 0, -1):
        a, b = p[k], p[k] + k
        if a in used: par[b] = a; plen[b] = k
        else: par[a] = b; plen[a] = k
        used |= {a, b}
    return par, plen

def unused_after(n, p, k):
    """labels not yet used when exactly the brackets longer than k have been placed"""
    used = set()
    for i in range(n - 1, k, -1): used |= {p[i], p[i] + i}
    return set(range(n)) - used

def comp(n, p): m = n - 1; return {k: m - k - a for k, a in p.items()}
def key(p): return tuple(sorted(p.items()))

def canon(n, p):
    adj = defaultdict(list)
    for k, a in p.items(): adj[a].append(a + k); adj[a + k].append(a)
    def enc(v, pa): return "(" + "".join(sorted(enc(u, v) for u in adj[v] if u != pa)) + ")"
    return min(enc(v, None) for v in range(n))

GP = {n: all_gp(n) for n in range(1, S + 1)}
print("growth placements, n = 1..%d:" % S, [len(GP[n]) for n in range(1, S + 1)])
assert all(is_gp(n, p) for n in GP for p in GP[n])

# ---------------------------------------------------------------- Rule C
for n in GP:
    for p in GP[n]: assert is_gp(n, comp(n, p))
print("Rule C  (complement): ok on all", sum(len(v) for v in GP.values()), "placements")

# ---------------------------------------------------------------- Rule T (completion transplant) and Rule P (run filling)
def completions(n, p):
    """(k, shift-free pattern of unused labels, touched used labels, brackets) for every k = 1..m-1, coordinates relative to the lowest unused label"""
    out = []
    for k in range(1, n - 1):
        U = unused_after(n, p, k); lo = min(U)
        br = {i: p[i] - lo for i in range(1, k + 1)}
        touched = {x - lo for i in range(1, k + 1) for x in (p[i], p[i] + i) if x not in U}
        out.append((k, frozenset(u - lo for u in U), frozenset(touched), br))
    return out
def transplant(nf, f, k, lo, br):
    q = {i: f[i] for i in range(k + 1, nf)}
    for i, a in br.items(): q[i] = a + lo
    return q
cnt = bad = neg = 0
COMP = {n: [completions(n, p) for p in GP[n]] for n in GP}
for nf in range(3, S + 1):
    for f in GP[nf]:
        for k in range(1, nf - 1):
            U = unused_after(nf, f, k); lo = min(U); pat = frozenset(u - lo for u in U); usedrel = {x - lo for x in range(nf) if x not in U}
            for nh in range(3, S + 1):
                if k > nh - 2: continue
                for cl in COMP[nh]:
                    kk, pat2, touched, br = cl[k - 1]; assert kk == k
                    if pat2 != pat: continue
                    q = transplant(nf, f, k, lo, br); ok = is_gp(nf, q)
                    if touched <= usedrel:
                        cnt += 1
                        if not ok: bad += 1
                    else:
                        neg += 1; assert not ok          # hypothesis violated => not a growth placement
print("Rule T  (completion transplant): %d applications (f, h, k) with f, h on <= %d vertices, %d failures; %d applications with a touched label unused, all of them fail" % (cnt, S, bad, neg))
assert bad == 0
cnt = 0
for nf in range(3, S + 1):
    for f in GP[nf]:
        for k in range(1, nf - 1):
            U = unused_after(nf, f, k); lo = min(U)
            if U != set(range(lo, lo + k)): continue
            for g in GP[k + 1]:
                for off in (lo - 1, lo):
                    q = {i: f[i] for i in range(k + 1, nf)}
                    for i, a in g.items(): q[i] = a + off
                    assert is_gp(nf, q); cnt += 1
print("Rule P  (run filling): %d applications, all growth placements" % cnt)

# ---------------------------------------------------------------- Rule N (nesting at a clean cut); Lemma 8 is the case g = 1
def lifted(nh, h, j):
    """if labels 1..j-1 are the last j-1 added, return the brackets of length >= j (the truncation U')"""
    if unused_after(nh, h, j - 1) != set(range(1, j)): return None
    return {i: h[i] for i in range(j, nh)}
cnt = neg = negok = 0
for nf in range(2, S + 1):
    for f in GP[nf]:
        par, plen = info(nf, f); m = nf - 1
        for L in range(1, m + 1):
            J = [k for k in f if f[k] < L <= f[k] + k]; c = len(J)
            if min(J) != m - c + 1: continue                  # not a clean cut
            j = nf - c; u = L - j
            if u < 0: continue
            cond = (u == 0) or plen[u] >= j
            for nh in range(j + 1, S + 1):
                g = nh - j
                for h in GP[nh]:
                    U1 = lifted(nh, h, j)
                    if U1 is None: continue
                    q = {}
                    for k, a in f.items():
                        jump = a < L <= a + k
                        q[k + g if jump else k] = a + g if a >= L else a
                    for k, a in U1.items(): q[k] = u + a
                    ok = is_gp(nf + g, q)
                    if cond: assert ok; cnt += 1
                    else:
                        neg += 1; negok += ok
print("Rule N  (nesting at a clean cut, low side; the high side is its complement): %d applications with T, T' on <= %d vertices, all growth placements;" % (cnt, S))
print("         with the condition on u violated: %d applications, %d growth placements (so the condition is necessary here)" % (neg, negok))

# ---------------------------------------------------------------- Rule B (block designs) and Rule D (mirror windows)
def designs(p, plen, explicit):
    """all valid designs: vert[j] for blocks j = 0..p-2"""
    out = []
    if explicit:
        for w in range(1, p + 1):
            vert = [0 if j >= w - 1 else w - 1 - j for j in range(p - 1)]
            ok = all(v == 0 or (j - v if v <= j else v - j - 1) < plen[v] for j, v in enumerate(vert))
            if ok and vert not in out: out.append(vert)
        return out
    def rec(beta, vert):
        if beta < 0: out.append([vert[j] for j in range(p - 1)]); return
        for j in range(p - 1):
            if j in vert: continue
            for v in (j - beta, j + beta + 1):
                if 0 <= v <= p - 1 and (v == 0 or beta < plen[v]):
                    vert[j] = v; rec(beta - 1, vert); del vert[j]
    rec(p - 2, {}); return out
def blow(p, f, vert, t):
    q = {k * t: a * t for k, a in f.items()}
    for j, v in enumerate(vert):
        for d in range(1, t):
            a, b = j * t + d, v * t
            q[abs(a - b)] = min(a, b)
    return q
cntB = cntD = 0; famB = set(); famD = set()
for p in range(2, S + 1):
    for f in GP[p]:
        par, plen = info(p, f)
        dB = designs(p, plen, False); dD = designs(p, plen, True)
        for vert in dD: assert vert in dB
        for t in (2, 3, 4, 5):
            n = (p - 1) * t + 1
            for vert in dB:
                q = blow(p, f, vert, t); assert len(q) == n - 1 and is_gp(n, q); cntB += 1
                # the tree is T with (t-1) * (number of blocks owned) leaves on each vertex
                deg = defaultdict(int)
                for k, a in q.items(): deg[a] += 1; deg[a + k] += 1
                assert all(deg[x] == 1 for x in range(n) if x % t)
                if vert in dD: cntD += 1
        # negative control: an invalid design (band not smaller than the parent bracket) must fail
print("Rule B  (block designs): %d applications (T on <= %d vertices, t = 2..5), all growth placements; %d of them are mirror-window designs (Rule D)" % (cntB, S, cntD))
# necessity of the design conditions: every assignment block -> (vertex, side) with distinct bands that violates beta < plen fails
neg = 0
for p in range(2, min(S, 6) + 1):
    for f in GP[p]:
        par, plen = info(p, f)
        for perm in itertools.permutations(range(p - 1)):          # perm[j] = band of block j
            for sides in itertools.product((0, 1), repeat=p - 1):
                vert = []
                for j in range(p - 1):
                    v = j - perm[j] if sides[j] == 0 else j + perm[j] + 1
                    vert.append(v)
                if any(v < 0 or v > p - 1 for v in vert): continue
                valid = all(v == 0 or perm[j] < plen[v] for j, v in enumerate(vert))
                ok = is_gp(2 * p - 1, blow(p, f, vert, 2))
                assert ok == valid
                neg += (not valid)
print("         (t = 2, T on <= %d vertices: a block assignment with distinct bands gives a growth placement exactly when the design is valid; %d invalid ones tested)" % (min(S, 6), neg))

# ---------------------------------------------------------------- A rule that fails: the classical Delta-labelling does not preserve growth
def delta(p, f, q, g):
    """Stanton-Zarnke / Koh-Rogers-Tan: copy i of T' has its vertices at even distance from v' (label 0 of g) in block i,
    the others in block p-1-i; copies are joined at v' along the edges of T."""
    adj = defaultdict(list)
    for k, a in g.items(): adj[a].append(a + k); adj[a + k].append(a)
    dist = {0: 0}; st = [0]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in dist: dist[y] = dist[x] + 1; st.append(y)
    lab = lambda i, x: (i if dist[x] % 2 == 0 else p - 1 - i) * q + x
    edges = [(lab(i, a), lab(i, a + k)) for i in range(p) for k, a in g.items()]
    edges += [(lab(a, 0), lab(a + k, 0)) for k, a in f.items()]
    return {abs(x - y): min(x, y) for x, y in edges}, len(edges)
res = defaultdict(lambda: [0, 0]); graceful_all = True
for p in range(2, 6):
    for f in GP[p]:
        for q in range(2, 6):
            for g in GP[q]:
                d, ne = delta(p, f, q, g)
                graceful_all &= (len(d) == ne == p * q - 1 and sorted(d) == list(range(1, p * q)))
                r = res[(canon(p, f), canon(q, g) + "@" + str(sorted(k for k, a in g.items() if a == 0)))]
                r[0] += 1; r[1] += is_gp(p * q, d)
print("Classical Delta-labelling of T by T' (p, q <= 5): always graceful: %s." % graceful_all)
star = lambda q, g: all(a == 0 for a in g.values())
tot = grow = growstar = 0
for p in range(2, 6):
    for f in GP[p]:
        for q in range(2, 6):
            for g in GP[q]:
                d, ne = delta(p, f, q, g); ok = is_gp(p * q, d); tot += 1; grow += ok
                if ok: assert star(q, g)
print("         It is a growth placement in %d of %d cases, and in every one of them T' is a star centred at v'." % (grow, tot))
d, ne = delta(2, {1: 0}, 3, {2: 0, 1: 1})
print("         Smallest failure: T = K2, T' = path on 3 vertices rooted at an end:", sorted((a, a + k) for k, a in d.items()), "growth:", is_gp(6, d))

# ---------------------------------------------------------------- closure in Python, to compare with closure.cpp
def closure(NMAX, useP, useN, useB, useT):
    D = {1: {(): {}}}
    for n in range(2, NMAX + 1):
        m = n - 1; cur = {}; queue = []
        def add(q):
            assert is_gp(n, q)
            for r in (q, comp(n, q)):
                kk = key(r)
                if kk not in cur: cur[kk] = r; queue.append(r)
        for s in itertools.product((0, 1), repeat=m - 1):          # staircases
            q = {m: 0}
            for k in range(m - 1, 0, -1): q[k] = q[k + 1] + s[k - 1]
            add(q)
        if useN:
            for n1 in range(2, n):
                g = n - n1
                if useN == 1 and g != 1: continue
                for f in D[n1].values():
                    par, plen = info(n1, f); m1 = n1 - 1
                    for L in range(1, m1 + 1):
                        J = [k for k in f if f[k] < L <= f[k] + k]; c = len(J)
                        if min(J) != m1 - c + 1: continue
                        j = n1 - c; u = L - j
                        if u < 0 or not (u == 0 or plen[u] >= j): continue
                        base = {}
                        for k, a in f.items():
                            jump = a < L <= a + k
                            base[k + g if jump else k] = a + g if a >= L else a
                        for h in D[g + j].values():
                            U1 = lifted(g + j, h, j)
                            if U1 is None: continue
                            q = dict(base)
                            for k, a in U1.items(): q[k] = u + a
                            add(q)
        if useB:
            for t in range(2, n):
                if (n - 1) % t: continue
                p = (n - 1) // t + 1
                if p < 2: continue
                for f in D[p].values():
                    par, plen = info(p, f)
                    for vert in designs(p, plen, useB == 1): add(blow(p, f, vert, t))
        qi = 0; seenc = set(); comps = defaultdict(list)
        while True:
            while qi < len(queue):
                f = queue[qi]; qi += 1
                if useP:
                    for k in range(1, m):
                        U = unused_after(n, f, k); lo = min(U)
                        if U != set(range(lo, lo + k)): continue
                        for g in D[k + 1].values():
                            for off in (lo - 1, lo):
                                if off < 0 or off + k > m: continue
                                q = {i: f[i] for i in range(k + 1, n)}
                                for i, a in g.items(): q[i] = a + off
                                add(q)
            if not useT: break
            # completions of everything derived so far (all sizes <= n), then one round of transplants
            comps = defaultdict(list); seenc = set()
            for nh in range(3, n + 1):
                src = D[nh].values() if nh < n else list(cur.values())
                for h in src:
                    for (k, pat, touched, br) in completions(nh, h):
                        kk = (k, pat, key(br))
                        if kk not in seenc: seenc.add(kk); comps[(k, pat)].append((touched, br))
            before = len(cur)
            for f in list(cur.values()):
                for k in range(1, m):
                    U = unused_after(n, f, k); lo = min(U); pat = frozenset(u - lo for u in U); usedrel = {x - lo for x in range(n) if x not in U}
                    for touched, br in comps.get((k, pat), ()):
                        if touched <= usedrel: add(transplant(n, f, k, lo, br))
            if len(cur) == before: break
        D[n] = cur
    return D
for name, cfg in (("C P", (1, 0, 0, 0)), ("C P D", (1, 0, 1, 0)), ("C P B", (1, 0, 2, 0)), ("C L8", (0, 1, 0, 0)), ("C N", (0, 2, 0, 0)),
                  ("C P T L8", (1, 1, 0, 1)), ("C P T B", (1, 0, 2, 1)), ("C P T N B", (1, 2, 2, 1))):
    D = closure(CLOSE, *cfg)
    print("closure %-10s n=2..%d  placements %s  trees %s" % (name, CLOSE, [len(D[n]) for n in range(2, CLOSE + 1)],
          [len({canon(n, p) for p in D[n].values()}) for n in range(2, CLOSE + 1)]))
