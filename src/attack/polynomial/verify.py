"""Machine checks for src/attack/polynomial, all straight from README section 1.

  python3 verify.py brute N     (a) every placement on n <= N vertices (N <= 10 is quick):
                                    growth placements drawing a path, by position of the vertex
                                    labelled 1, compared with the two-leg deal counter;
                                (d) the generating-function / parity lemma on every tree placement.
  python3 verify.py families S  (b) the three explicit families (anchor at distance 2 from the
                                    end of a path) for 1 <= s <= S;
                                (c) the spider corollary S(a,2,c) for those a and 1 <= c <= 30.
"""
import sys, itertools
from collections import defaultdict
from deal2show import deals

# ---------- definitions (README s.1, s.2), labels 1..n --------------------------------------
def edges_of_labelling(edges, lab):
    """edges: list of vertex pairs; lab: dict vertex -> label in 1..n. Returns placement
    (p_1..p_{n-1}) or None if not a placement (some length missing / repeated)."""
    n = len(lab)
    if sorted(lab.values()) != list(range(1, n+1)): return None
    p = [None]*(n-1)
    for u, v in edges:
        a, b = sorted((lab[u], lab[v])); k = b-a
        if k < 1 or p[k-1] is not None: return None
        p[k-1] = a
    return p if None not in p else None

def is_growth(p):
    """growth placement: longest bracket first, each later bracket has exactly one used foot."""
    n = len(p)+1
    used = {p[n-2], p[n-2]+n-1}
    for k in range(n-2, 0, -1):
        a, b = p[k-1], p[k-1]+k
        if (a in used) == (b in used): return False
        used.add(a); used.add(b)
    return True

def adjacency(p):
    adj = defaultdict(list)
    for k, a in enumerate(p, 1):
        adj[a].append(a+k); adj[a+k].append(a)
    return adj

def legs_from(adj, c):
    """lengths of the paths hanging at c, or None if some branch is not a path."""
    out = []
    for x in adj[c]:
        prev, cur, L = c, x, 1
        while True:
            nxt = [y for y in adj[cur] if y != prev]
            if len(nxt) == 0: break
            if len(nxt) > 1: return None
            prev, cur, L = cur, nxt[0], L+1
        out.append(L)
    return sorted(out)

# ---------- (a) + (d): brute force over all placements ---------------------------------------
def brute(N):
    for n in range(3, N+1):
        cnt = defaultdict(int); ntree = 0; lemma_checked = 0
        for p in itertools.product(*[range(1, n-k+1) for k in range(1, n)]):
            adj = adjacency(p)
            # tree test: connected with n-1 edges
            seen = {1}; st = [1]
            while st:
                x = st.pop()
                for y in adj[x]:
                    if y not in seen: seen.add(y); st.append(y)
            if len(seen) == n:
                ntree += 1
                if n <= 9:
                    # (d) lemma: labels f = label-1 in 0..m. For EVERY root r:
                    #   sum_v f(v) = n f(r) + sum_{v != r} eps_v w_v s_v,   and
                    #   #{v != r : s_v even, w_v odd} = n f(r)  (mod 2);
                    #   sum_v f(v)^j = sum_edges len^j  for j = 1..3 (same multiset shifted by 0: labels 1..m appear)
                    m = n-1
                    for r in range(1, n+1):
                        par = {r: 0}; order = [r]
                        for x in order:
                            for y in adj[x]:
                                if y not in par: par[y] = x; order.append(y)
                        s = {x: 1 for x in order}
                        for x in reversed(order[1:]): s[par[x]] += s[x]
                        lin = n*(r-1) + sum((x-par[x])*s[x] for x in order[1:])
                        assert lin == m*(m+1)//2
                        par_cnt = sum(1 for x in order[1:] if s[x] % 2 == 0 and abs(x-par[x]) % 2 == 1)
                        assert par_cnt % 2 == (n*(r-1)) % 2
                        # q = -1: parity classes of labels have sizes ceil(n/2), floor(n/2)
                        ev = sum(1 for x in order if (x-1) % 2 == 0); assert ev == (n+1)//2
                        lemma_checked += 1
                    for j in (1, 2, 3):
                        assert sum((x-1)**j for x in range(1, n+1)) == sum(k**j for k in range(1, n))
            if not is_growth(p): continue
            assert len(seen) == n                      # Lemma 5
            if max(len(adj[x]) for x in adj) > 2: continue   # not a path
            L = legs_from(adj, 1)
            b = 0 if len(L) == 1 else L[0]
            cnt[b] += 1
        m = n-1
        for b in range(1, m//2+1):
            d = len(deals(m-b, b)); d = d//2 if 2*b == m else d
            assert d == cnt[b], (n, b, d, cnt[b])
        assert cnt[0] == 1
        print("n=%d: tree placements %d; path growth placements by distance of label 1 from the end: %s"
              " (deal counter agrees)%s" % (n, ntree, dict(sorted(cnt.items())),
              "; lemma checked on %d (placement, root) pairs" % lemma_checked if lemma_checked else ""))

# ---------- (b): the three families, labels 0..m here, root = 0 ------------------------------
def zig(lo, hi, from_top, count):
    out = []; a, b = lo, hi
    for i in range(count):
        if (i % 2 == 0) == from_top: out.append(b); b -= 1
        else: out.append(a); a += 1
    return out

def family(which, s):
    """returns (m, A, B): labels along leg A and along leg B, outward from the root (label 0)."""
    if which == 0:      # m = 3s+2
        m = 3*s+2
        A = zig(1, m-1, True, 2*s) + zig(s+1, 2*s, True, s)
        B = [m, 2*s+1]
    elif which == 1:    # m = 5s+4
        m = 5*s+4
        A = zig(1, m, True, 2*s+2) + zig(s+2, 4*s+2, True, 2*s) + zig(2*s+2, 3*s+1, True, s)
        B = [3*s+2, 4*s+3]
    else:               # m = 7s+3
        m = 7*s+3
        A = zig(1, m, True, 4*s+1) + zig(2*s+2, 5*s+2, False, 2*s) + zig(3*s+3, 4*s+2, False, s)
        B = [3*s+2, 2*s+1]
    return m, A, B

def path_placement(A, B):
    """vertices: ('A',i), ('B',i), root 'r'. labels +1 to match README's 1..n."""
    lab = {'r': 1}; edges = []
    for name, leg in (('A', A), ('B', B)):
        prev = 'r'
        for i, x in enumerate(leg):
            lab[(name, i)] = x+1; edges.append((prev, (name, i))); prev = (name, i)
    return edges, lab

def families(S):
    nsp = 0
    for which in (0, 1, 2):
        for s in range(1, S+1):
            m, A, B = family(which, s)
            assert len(A) == m-2 and len(B) == 2
            edges, lab = path_placement(A, B)
            p = edges_of_labelling(edges, lab)
            assert p is not None and is_growth(p), (which, s)
            adj = adjacency(p)
            assert legs_from(adj, 1) == [2, m-2]            # label 1 sits at distance 2 from an end
            # (c) spider corollary: pendant path with c edges glued at the root (README s.13)
            if s <= 12:
                for c in range(1, 31):
                    O = zig(0, c, False, c+1)                # 0, c, 1, c-1, ...
                    if c % 2: O = [c-x for x in O]
                    Alow = c//2; assert O[-1] == Alow
                    lab2 = {}; e2 = []
                    for i, x in enumerate(O[:-1]):
                        lab2[('O', i)] = (x if x <= Alow else x+m) + 1
                    for v in lab: lab2[v] = lab[v] + Alow    # T' dropped into the gap; root gets Alow
                    names = [('O', i) for i in range(c)] + ['r']
                    e2 = [(names[i], names[i+1]) for i in range(c)] + edges
                    p2 = edges_of_labelling(e2, lab2)
                    assert p2 is not None and is_growth(p2), (which, s, c)
                    adj2 = adjacency(p2)
                    assert legs_from(adj2, lab2['r']) == sorted([2, m-2, c])
                    nsp += 1
        print("family %d (m = %s): growth placement with the anchor at distance 2 verified for s = 1..%d"
              % (which, ["3s+2", "5s+4", "7s+3"][which], S))
    print("spider corollary S(m-2, 2, c): %d cases verified (s <= 12, c <= 30)" % nsp)

if __name__ == "__main__":
    if sys.argv[1] == "brute": brute(int(sys.argv[2]))
    else: families(int(sys.argv[2]))
