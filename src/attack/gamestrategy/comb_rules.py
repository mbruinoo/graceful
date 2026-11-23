"""Explicit (search-free) growth placements for two families of diameter-4 trees, via the 'all-up comb'.

Tree D(a1; s_1..s_d): a centre c adjacent to d+1 hubs; the root hub has a1 leaves, hub i has s_i leaves.
Comb data (labels 0..m, m = number of edges): root hub at 0, centre at y, hub i at h_i < y,
each leaf of hub i at h_i + u for u in U_i, root leaves at the cells in W (inside) and at y+1..m.
Everything is checked from the README section 1 definitions by check_growth_placement().
"""
import sys

def comb_to_labels(a1, y, hubs, W):
    """hubs: list of (h, sorted lengths U). Returns (edges as label pairs on 1..n, n). Raises if a1 too small."""
    m = 1 + len(hubs) + sum(len(U) for _, U in hubs) + a1
    above = m - y
    if above < 0 or len(W) + above != a1: raise ValueError('wildcard count mismatch')
    edges = [(0, y)]
    for x in list(W) + list(range(y+1, m+1)): edges.append((0, x))
    for h, U in hubs:
        edges.append((y, h))
        for u in U: edges.append((h, h+u))
    return [(p+1, q+1) for p, q in edges], m+1

def check_growth_placement(edges, n):
    """README section 1/2: labels 1..n, exactly one bracket of each length 1..n-1, and for every k the brackets
    of length >= k form a connected tree."""
    if len(edges) != n-1: return False
    byLen = {}
    for p, q in edges:
        if not (1 <= p <= n and 1 <= q <= n) or p == q: return False
        k = abs(p-q)
        if k in byLen: return False
        byLen[k] = (min(p, q), max(p, q))
    if sorted(byLen) != list(range(1, n)): return False
    # add brackets longest first; each must have exactly one foot already used (after the first)
    used = set(byLen[n-1])
    if used != {1, n}: return False
    for k in range(n-2, 0, -1):
        p, q = byLen[k]
        if (p in used) == (q in used): return False
        used.add(p); used.add(q)
    return len(used) == n

def canon(edges):
    """canonical form of a free tree given by an edge list (AHU encoding rooted at the centre(s))."""
    adj = {}
    for p, q in edges: adj.setdefault(p, set()).add(q); adj.setdefault(q, set()).add(p)
    deg = {v: len(adj[v]) for v in adj}; layer = [v for v in adj if deg[v] <= 1]; left = len(adj)
    while left > 2:
        left -= len(layer); nxt = []
        for v in layer:
            for w in adj[v]:
                deg[w] -= 1
                if deg[w] == 1: nxt.append(w)
        layer = nxt
    def enc(v, par): return '(' + ''.join(sorted(enc(w, v) for w in adj[v] if w != par)) + ')'
    return min(enc(v, None) for v in layer)
def target_tree(sizes):
    """D(sizes): centre 0, one hub per entry, that many leaves on it."""
    E = []; v = 1
    for s in sizes:
        h = v; E.append((0, h)); v += 1
        for _ in range(s): E.append((h, v)); v += 1
    return E

# ---------- family EQ: d equal hubs of size a, root hub of size a1 >= d-1 ----------
def rule_equal(a1, a, d):
    y = d*(a+2); hubs = []
    for i in range(d):
        h = 2*i+1
        if d % 2: s = 2*i+d if 2*i+d <= 2*d-1 else 2*i-d
        else:     s = d-1-i if i % 2 == 0 else 2*d-1-i
        hubs.append((h, [s+d*j for j in range(a)]))
    if d % 2: W = list(range(2, d, 2)) + [d*a+x for x in range(d+1, 2*d, 2)]
    else:     W = list(range(2, d-1, 2)) + [d*a+x for x in range(d, 2*d-1, 2)]
    return y, hubs, W

# ---------- family K3: three hubs of sizes a1 >= p >= q >= 1 ----------
def pattern_A(s, P):          # hub 1 has s leaves, hub 3 has P leaves, P = s (mod 2), P >= s
    odd = list(range(1, 2*s, 2)); ev = list(range(2, 2*s+1, 2))
    if P == s: return 2*s+4, [(1, odd), (3, ev)], [2*s+2]
    J = (P-s-2)//2; t = [2*s+2+3*j for j in range(J+1)]
    U3 = ev + [2*s+1] + [x for j in range(J) for x in (t[j]+1, t[j]+2)] + [t[J]+1]
    return t[J]+5, [(1, odd), (3, U3)], t + [t[J]+3]
def pattern_B(P, Q):          # hub 2 has P >= 1 leaves, hub 3 has Q leaves, Q even >= 2
    U3 = [x for j in range(Q//2) for x in (P+2+3*j, P+3+3*j)]
    return P+3*Q//2+5, [(2, list(range(2, P+2))), (3, U3)], [1] + [P+4+3*j for j in range(Q//2+1)]
def rule_three(a1, p, q):
    assert a1 >= p >= q >= 1
    if (p-q) % 2 == 0: return pattern_A(q, p)
    if q % 2 == 0:     return pattern_B(p, q)
    if (a1, p, q) == (2, 2, 1): return 8, [(1, [1, 2]), (4, [3])], [5, 6]   # the one sporadic tree
    return pattern_B(q, p)

def verify(a1, sizes, data):
    y, hubs, W = data
    edges, n = comb_to_labels(a1, y, hubs, W)
    assert check_growth_placement(edges, n), ('not a growth placement', a1, sizes)
    assert canon(edges) == canon(target_tree([a1]+list(sizes))), ('wrong tree', a1, sizes)
    assert len([e for e in edges if 1 in e]) == a1+1   # the vertex labelled 1 is the root hub (a1 leaves + centre)
    return n

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    cnt = 0; trees = set()
    for a1 in range(1, N):
        for p in range(1, a1+1):
            for q in range(1, p+1):
                if 4+a1+p+q > N: break
                n = verify(a1, (p, q), rule_three(a1, p, q)); assert n == 4+a1+p+q; cnt += 1; trees.add((n, a1, p, q))
    print('K3: every D(a1;p,q), a1>=p>=q>=1, n<=%d: %d trees, all verified growth placements rooted at the largest hub' % (N, cnt))
    cnt = 0
    for d in range(1, N):
        for a in range(1, N):
            for a1 in range(max(d-1, 0), N):
                n = 2+d+d*a+a1
                if n > N: break
                assert verify(a1, [a]*d, rule_equal(a1, a, d)) == n; cnt += 1
    print('EQ: every D(a1;a^d), d>=1, a>=1, a1>=d-1, n<=%d: %d parameter triples, all verified' % (N, cnt))
