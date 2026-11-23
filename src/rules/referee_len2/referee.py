#!/usr/bin/env python3
"""Independent referee re-implementation of the len-2 spider rule, written from the STATEMENT only.
Edges are (u, w, kind): kind '+' label u+w ; kind '-' difference edge o*=u -> x*=w, label u-w."""
import sys
sys.setrecursionlimit(10000)

CAP = {  # beta, g, J0, J1, small, cross, bottom, top, diff(o*,x*) as (coef n, const)
 3: dict(beta=0, g=1, J0=0, J1=0, small=[], cross=[(1,2)], bottom=[], top=[], diff=None),
 6: dict(beta=0, g=3, J0=1, J1=2, small=[(1,3)], cross=[(1,5)], bottom=[(1,2),(1,4)],
         top=[(1,1),(2,2),(2,3),(1,5)], diff=None),
 9: dict(beta=-1, g=7, J0=5, J1=5, small=[(1,4),(1,6)], cross=[(3,6)],
         bottom=[(1,3),(1,4),(4,2),(5,2),(3,5),(2,7),(2,8),(3,9),(4,10),(5,11)],
         top=[(1,-2),(1,0),(4,-1),(2,3),(5,1),(5,2),(4,4),(3,6),(2,8),(3,8)], diff=None),
 2: dict(beta=0, g=1, J0=0, J1=1, small=[], cross=[], bottom=[], top=[(1,1)], diff=((4,3),(1,1))),
 5: dict(beta=0, g=3, J0=1, J1=2, small=[(1,3)], cross=[], bottom=[(1,2),(1,4)],
         top=[(1,1),(2,2),(2,3)], diff=((4,6),(1,1))),
 8: dict(beta=-2, g=7, J0=5, J1=5, small=[(1,3)], cross=[(3,5)],
         bottom=[(2,2),(3,2),(5,1),(1,6),(1,7),(4,5),(3,8),(4,9),(5,10)],
         top=[(1,-3),(1,-1),(4,-2),(2,2),(5,0),(5,1),(4,3),(3,5),(2,7),(3,7)], diff=((3,10),(1,4))),
}
SMALL_TXT = {
 (6,0): "5+7 3+8 2+8 2+7 1+5 1+3",
 (9,0): "8+10 6+11 6+10 4+11 2+12 1+12 1+8 3+4 2+3",
 (9,3): "11+25 13+22 10+24 11+22 7+25 10+21 6+24 9+20 7+21 8+19 6+20 4+19 5+13 5+9 4+8",
 (9,6): "18+36 17+35 17+36 18+33 15+35 14+34 13+33 12+32 11+31 10+30 15+34 19+28 14+31 11+32 12+29 9+30 8+29 10+28 7+9 7+13 8+19",
 (5,0): "5+5 3+6 4+4 1+6 3-1",
 (8,0): "8+8 5+10 5+9 4+9 6+6 1+10 3+4 3-1",
 (8,3): "17+17 13+20 11+21 7+24 8+22 7+22 4+24 6+21 6+20 12+13 11+12 9+10 8+10 9-4",
 (8,6): "26+26 19+32 19+31 18+31 12+36 11+36 9+37 11+34 7+37 9+34 10+32 13+28 13+27 12+27 10+28 17+18 16+17 14+16 14+15 15-7",
}
def parse(txt):
    out = []
    for t in txt.split():
        if '+' in t:
            a, b = t.split('+'); out.append((int(a), int(b), '+'))
        else:
            a, b = t.split('-'); out.append((int(a), int(b), '-'))
    return out
SMALL = {key: parse(v) for key, v in SMALL_TXT.items()}

def cap_formula(c, n):
    d = CAP[c]; h3 = (c + 1) // 3; h = n + h3
    beta, g, J0, J1 = d['beta'], d['g'], d['J0'], d['J1']
    H = lambda j: 3 * n + c + j
    L = lambda v: n + v
    E = []
    for j in range(J0 + 1, h - J1 + 1):
        E.append((H(j), L(j + beta), '+')); E.append((H(j), L(j + beta + g), '+'))
    for j, v in d['bottom']: E.append((H(j), L(v), '+'))
    for jp, vp in d['top']: E.append((H(h - J1 + jp), L(n + vp), '+'))
    for a, b in d['small']: E.append((n + a, n + b, '+'))
    for p, q in d['cross']: E.append((n + p, 2 * n + q, '+'))
    if d['diff']:
        (oa, ob), (xa, xb) = d['diff']
        E.append((oa * n + ob, xa * n + xb, '-'))
    return E

def cap(c, n, use_small=True):
    if use_small and (c, n) in SMALL: return list(SMALL[(c, n)])
    return cap_formula(c, n)

def build(k):
    if k == 0: return []
    if k % 3 == 1:
        T = k - 1
        sh = lambda x: x + 1 if x > T else x
        return [(sh(u), sh(w), s) for u, w, s in build(k - 1)] + [(k, k, '+')]
    c = {3: 3, 6: 6, 0: 9, 2: 2, 5: 5, 8: 8}[k % 9]
    n = (k - c) // 3
    assert n % 3 == 0 and n >= 0
    delta = n + c - 1
    sh = lambda x: x + delta if x > n else x
    return [(sh(u), sh(w), s) for u, w, s in build(n)] + cap(c, n)

def lab(e): return e[0] + e[1] if e[2] == '+' else e[0] - e[1]

def check_graph(E, vertset_labels):
    """structure: degree 2, labels partition. returns error or None; vertset_labels = set of all labels expected"""
    deg = {}
    for u, w, s in E:
        deg[u] = deg.get(u, 0) + 1; deg[w] = deg.get(w, 0) + 1
    bad = [v for v, x in deg.items() if x != 2]
    if bad: return "degree != 2 at %s" % sorted(bad)[:6]
    labs = [lab(e) for e in E]
    allv = sorted(list(deg) + labs)
    if allv != sorted(vertset_labels): 
        return "labels not a partition (dups %s, missing %s)" % (
            sorted(set(x for x in allv if allv.count(x) > 1))[:6] if len(allv) < 4000 else '?',
            sorted(set(vertset_labels) - set(allv))[:6])
    return None

def deal_from_graph(E):
    """orient cycles; return list of legs, each a tuple of numbers (first, second). None on failure."""
    adj = {}
    for i, (u, w, s) in enumerate(E):
        adj.setdefault(u, []).append(i); adj.setdefault(w, []).append(i)
    for v in adj:
        if len(adj[v]) != 2: return None, "degree"
    out = {}  # vertex -> edge id used as its out-edge
    def walk(start, eid):
        v, e = start, eid
        while True:
            if v in out: return "orientation conflict at %d" % v
            out[v] = e
            u, w, s = E[e]
            nxt = w if u == v else u      # loop: nxt = v
            if u == w: nxt = v
            a, b = adj[nxt]
            ne = b if a == e else a       # the other edge at nxt (for loop a==b==e)
            v, e = nxt, ne
            if v == start: return None
    # difference edges force orientation o* -> x*
    for i, (u, w, s) in enumerate(E):
        if s == '-':
            if u in out: return None, "two forced orientations"
            r = walk(u, i)
            if r: return None, r
    for v in list(adj):
        if v not in out:
            r = walk(v, adj[v][0])
            if r: return None, r
    legs = []
    for v, e in out.items():
        u, w, s = E[e]
        x = w if u == v else u
        if s == '+': legs.append((v + x, x))
        else:
            if u != v: return None, "difference edge oriented backwards"
            legs.append((u - w, w))
    return legs, None

def check_deal(k, legs, want_upup):
    """From the definition: hand m..1; each leg gets 2 numbers in decreasing order; tip moves.
    Tries both signs for the second number per leg (independent of intended sign) but requires distinctness overall
    using the unique feasible sign if only one is in range; reports number of up-up legs."""
    m = 2 * k
    if len(legs) != k: return "wrong number of legs %d" % len(legs)
    owner = {}
    for li, (a, b) in enumerate(legs):
        if not a > b: return "leg not decreasing %s" % ((a, b),)
        for x in (a, b):
            if x in owner: return "number %d dealt twice" % x
            owner[x] = li
    if sorted(owner) != list(range(1, m + 1)): return "numbers dealt are not m..1"
    tip = [0] * k; seen = [False] * (m + 1); upup = 0
    # first pass: tips after first number
    second = []
    for w in range(m, 0, -1):
        li = owner[w]
        if tip[li] == 0:
            tip[li] = w
            if seen[w]: return "label %d visited twice" % w
            seen[w] = True
        else:
            second.append((li, w))
    # second numbers: the down move tip-w and up move tip+w; choose so that all distinct.
    # Since all 2k visited labels must be exactly 1..2k, the second labels must be exactly the unseen ones.
    # choose greedily when forced, otherwise try down first then verify (backtracking unnecessary if check passes)
    pend = []
    for li, w in second:
        opts = [t for t in (tip[li] - w, tip[li] + w) if 1 <= t <= m and not seen[t]]
        if not opts: return "leg with numbers %s has no free label" % (legs[li],)
        pend.append((li, w, opts))
    # resolve: forced ones first, iterate
    used = set()
    changed = True; final = {}
    while pend and changed:
        changed = False; rest = []
        for li, w, opts in pend:
            opts = [t for t in opts if t not in used]
            if not opts: return "leg %s collides" % (legs[li],)
            if len(opts) == 1:
                used.add(opts[0]); final[li] = (opts[0], w); changed = True
            else: rest.append((li, w, opts))
        pend = rest
    if pend:
        # ambiguous: take the down move for each and verify
        for li, w, opts in pend:
            t = tip[li] - w
            if t in used: t = tip[li] + w
            if t in used: return "collision in ambiguous resolution"
            used.add(t); final[li] = (t, w)
    for li, (t, w) in final.items():
        if seen[t]: return "label %d visited twice" % t
        seen[t] = True
        if t > tip[li]: upup += 1
    if not all(seen[1:]): return "not all labels visited"
    if upup != want_upup: return "up-up legs = %d, wanted %d" % (upup, want_upup)
    return None

def is_split(E, T):
    for u, w, s in E:
        if s != '+': return False
        if (u > T) + (w > T) != (u + w > T): return False
    return True

def check_k(k, G=None):
    if G is None: G = build(k)
    r = check_graph(G, range(1, 2 * k + 1))
    if r: return "graph: " + r
    legs, err = deal_from_graph(G)
    if err: return "orient: " + err
    r = check_deal(k, legs, 1 if k % 3 == 2 else 0)
    if r: return "deal: " + r
    if k % 3 == 0 and not is_split(G, k): return "G(k) not in C0(k): T=k is not a split"
    if k % 3 == 2 and sum(1 for e in G if e[2] == '-') != 1: return "not exactly one difference edge"
    return None

def check_cap(c, n, use_small=False):
    E = cap(c, n, use_small)
    labels = list(range(n + 1, 2 * n + c)) + list(range(3 * n + c, 6 * n + 2 * c + 1))
    r = check_graph(E, labels)
    if r: return r
    if c in (3, 6, 9) and not is_split(E, 3 * n + c): return "3n+c not a split"
    if c in (2, 5, 8):
        d = [e for e in E if e[2] == '-']
        if len(d) != 1 or not d[0][0] - d[0][1] > d[0][1]: return "difference edge bad"
    return None

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'all':
        K = int(sys.argv[2]); fails = []
        for k in range(1, K + 1):
            r = check_k(k)
            if r: fails.append((k, r)); print("FAIL k=%d: %s" % (k, r)); 
            if len(fails) > 20: break
        print("checked k=1..%d, failures: %d" % (K, len(fails)))
    elif mode == 'list':
        fails = 0
        for k in map(int, sys.argv[2:]):
            r = check_k(k); print(k, k % 9, r or "ok"); fails += bool(r)
        print("failures:", fails)
    elif mode == 'caps':
        N = int(sys.argv[2])
        for c in (3, 6, 9, 2, 5, 8):
            bad = [(n, check_cap(c, n)) for n in range(0, N + 1)]
            bad = [(n, r) for n, r in bad if r]
            print("cap_%d formula, n=0..%d: failing n = %s" % (c, N, [n for n, _ in bad]))
        for (c, n) in sorted(SMALL):
            print("stored cap_%d(%d):" % (c, n), check_cap(c, n, True) or "ok")
    elif mode == 'show':
        k = int(sys.argv[2]); G = build(k); print(G); print(deal_from_graph(G)); print(check_k(k, G))
