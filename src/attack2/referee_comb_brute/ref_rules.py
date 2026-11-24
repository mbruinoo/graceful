#!/usr/bin/env python3
"""Referee's own implementation of Theorems P, R, C (from the claim statements) and attempts to break them.
Every comb is checked by ref_verify.comb_ok and (sampled a1) tree_ok."""
import sys, itertools, random
from ref_verify import comb_ok, tree_ok

def chk(tag, S, w_claim, y, hubs, W, a1s=(0, 1)):
    S = sorted(S, reverse=True)
    e = None
    if len(W) != w_claim: e = "w is %d, claimed %d" % (len(W), w_claim)
    e = e or comb_ok(S, len(W), y, hubs, W)
    if not e:
        for d in a1s: e = e or tree_ok(S, len(W), y, hubs, W, len(W) + d)
    if e: print("COUNTEREXAMPLE", tag, S, e); return False
    return True

# ---------- Theorem P
def P(bs, c=None):
    J = len(bs); k = 2 * J + (c is not None)
    assert k >= 1 and (c is None or c % 2 == 0 or c >= k)
    odd = c is not None and c % 2 == 1
    e = 0 if c is None else ((c - k) // 2 if odd else c // 2)
    N = sum(bs) + e
    U = {h: [] for h in range(1, 2 * k, 2)}
    Z = set(); i = 0
    for g, cnt in list(enumerate(bs)) + [(J, e)]:
        for _ in range(cnt):
            i += 1; x = 2 * i - 1; h = 2 * g + 1; z = x + h
            U[h].append(x); U[2 * k - h].append(z); Z.add(z)
    if not odd:
        y = 2 * k + 2 * N
        W = [v for v in range(2, y - 1, 2) if v not in Z]
    else:
        y = 3 * k + 2 * N
        U[k] += list(range(2 * N + 1, 2 * N + 2 * k, 2))
        W = [v for v in range(2, y - 2 * k) if v % 2 == 0 and v not in Z] + [v for v in range(y - k + 1, y - 1) if v % 2 == 1]
    size = {h: len(U[h]) for h in U}
    # stated sizes
    for g, b in enumerate(bs): assert size[2 * g + 1] == b and size[2 * k - 2 * g - 1] == b
    if c is not None: assert size[k] == c
    return y, sorted(U.items()), sorted(W), k

def test_P(N):
    cnt = 0; ok = True
    def comps(total, maxparts):
        # all tuples (ordered) of nonneg ints
        def rec(pre, rem):
            yield tuple(pre)
            if len(pre) < maxparts:
                for v in range(0, rem + 1):
                    pre.append(v); yield from rec(pre, rem - v); pre.pop()
        yield from rec([], total)
    # n = a1 + k + sum + 2 with a1 = k-1 : 2k+1+sum <= N
    for J in range(0, N):
        for bs in comps_bounded(J, N):
            for c in [None] + list(range(0, N)):
                k = 2 * J + (c is not None)
                if k < 1: continue
                if c is not None and c % 2 == 1 and c < k: continue
                tot = 2 * sum(bs) + (c or 0)
                if 2 * k + 1 + tot > N: continue
                y, hubs, W, k = P(list(bs), c)
                S = [b for b in bs for _ in (0, 1)] + ([c] if c is not None else [])
                ok &= chk("P bs=%s c=%s" % (bs, c), S, k - 1, y, hubs, W); cnt += 1
    print("Theorem P: all ordered (bs,c) with n<=%d at a1=k-1,k: %d combs, ok=%s" % (N, cnt, ok))

def comps_bounded(J, N):
    # ordered tuples of length J, entries>=0, with 2*sum + 4J+1 <= N+? (cheap bound)
    def rec(pre, rem):
        if len(pre) == J: yield tuple(pre); return
        for v in range(0, rem + 1):
            pre.append(v); yield from rec(pre, rem - v); pre.pop()
    budget = (N - 4 * J - 1) // 2
    if budget < 0: return
    yield from rec([], budget)

def test_P_two(N):
    cnt = 0; ok = True
    for a in range(0, N):
        for b in range(0, a):
            for d in range(1, N):
                for e in range(1, N):
                    k = d + e
                    if 2 * k + 1 + a * d + b * e > N: break
                    if d % 2 and e % 2: continue
                    if d % 2 == 0 and e % 2 == 0: bs = [a] * (d // 2) + [b] * (e // 2); c = None
                    elif d % 2: 
                        if not (a % 2 == 0 or a >= k): continue
                        bs = [a] * (d // 2) + [b] * (e // 2); c = a
                    else:
                        if not (b % 2 == 0 or b >= k): continue
                        bs = [a] * (d // 2) + [b] * (e // 2); c = b
                    for B in (bs, bs[::-1]):
                        y, hubs, W, k2 = P(B, c)
                        ok &= chk("Ptwo", [a] * d + [b] * e, k - 1, y, hubs, W); cnt += 1
    print("Theorem P two sizes a^d b^e (a>b) n<=%d: %d combs ok=%s" % (N, cnt, ok))

# ---------- Theorem R
def reflect(y, hubs, W):
    return y, [(h, sorted(y - h - u for u in U)) for h, U in hubs], sorted(y - x for x in W)

def R(k, rounds, bs, c=None):
    """rounds: list of (B, pi). Preconditions asserted exactly as in the statement."""
    labels = set(range(1, 2 * k, 2))
    for B, pi in rounds:
        assert B % 2 == 1 and B > 0 and sorted(pi) == list(range(k))
        assert all(B + 2 * (pi[i] - i) in labels for i in range(k))
    for t in range(len(rounds) - 1): assert rounds[t][0] + rounds[t + 1][0] >= 2 * k
    assert 2 * len(bs) + (c is not None) == k
    if rounds:
        assert rounds[-1][0] >= k - 1
        if c is not None and c % 2 == 1: assert rounds[-1][0] >= k
    yP, hubsP, WP, _ = P(bs, c)
    yP, hubsP, WP = reflect(yP, hubsP, WP)
    Q = set(range(1, yP)) - set(WP)
    U = {h: [] for h in labels}
    sig = 0; A = []
    for B, pi in rounds:
        A.append({sig + 2 * i + 1 for i in range(k)})
        for i in range(k):
            U[B + 2 * (pi[i] - i)].append(sig + 2 * i + 1)
        sig += B
    for h, Us in hubsP: U[h] += [u + sig for u in Us]
    y = yP + sig
    used = set().union(*A) if A else set()
    used |= {sig + q for q in Q}
    W = sorted(set(range(1, y)) - used)
    w_claim = k - 1 + sum(B - k for B, _ in rounds)
    return y, sorted(U.items()), W, w_claim

def valid_rounds(k):
    out = []
    labels = set(range(1, 2 * k, 2))
    for B in range(1, 4 * k, 2):
        for pi in itertools.permutations(range(k)):
            if all(B + 2 * (pi[i] - i) in labels for i in range(k)): out.append((B, pi))
    return out

def test_R(kmax, Tmax, full_k):
    rng = random.Random(1); cnt = 0; ok = True
    for k in range(1, kmax + 1):
        vr = valid_rounds(k) if k <= 7 else None
        J = k // 2
        Pparams = []
        for bs in itertools.product(range(0, 3), repeat=J):
            if k % 2 == 0: Pparams.append((list(bs), None))
            else:
                for c in list(range(0, 5)) + [k, k + 1, k + 2, k + 4]:
                    if c % 2 == 0 or c >= k: Pparams.append((list(bs), c))
        for T in range(1, Tmax + 1):
            seqs = itertools.product(vr, repeat=T)
            allseq = [s for s in seqs if all(s[t][0] + s[t + 1][0] >= 2 * k for t in range(T - 1))]
            if k > full_k or len(allseq) * len(Pparams) > 150000:
                pairs = [(rng.choice(allseq), rng.choice(Pparams)) for _ in range(40000)]
            else:
                pairs = [(s, p) for s in allseq for p in Pparams]
            for s, (bs, c) in pairs:
                BT = s[-1][0]
                if BT < k - 1 or (c is not None and c % 2 == 1 and BT < k): continue
                y, hubs, W, wc = R(k, list(s), bs, c)
                if wc < 0: print("NEGATIVE w claimed", k, s, bs, c); ok = False
                S = [len(u) for _, u in hubs]
                ok &= chk("R k=%d rounds=%s bs=%s c=%s" % (k, s, bs, c), S, wc, y, hubs, W); cnt += 1
        print("  R k=%d done, running total %d ok=%s (#valid rounds %d)" % (k, cnt, ok, len(vr)), flush=True)
    print("Theorem R: %d combs, ok=%s" % (cnt, ok))

def test_R1(N):
    cnt = 0; ok = True
    for d in range(1, N, 2):
        for e in range(1, N, 2):
            k = d + e
            for j in range(1, N):
                for b in range(0, N):
                    w = k - 1 + j
                    n = w + k + (b + k * j) * d + b * e + 2
                    if n > N: break
                    bs = [b + k * j] * ((d - 1) // 2) + [b] * ((e - 1) // 2)
                    # pair with labels k-1,k+1 : g with 2g+1 = k-1 -> g = k/2-1 = last group
                    bs = bs + [b]
                    y, hubs, W, wc = R(k, [(k + 1, tuple(range(k)))] * j, bs, None)
                    assert wc == w
                    ok &= chk("R1 d=%d e=%d j=%d b=%d" % (d, e, j, b), [b + k * j] * d + [b] * e, w, y, hubs, W); cnt += 1
                if b == 0 and n > N: break
    print("Corollary R1 n<=%d: %d patterns ok=%s" % (N, cnt, ok))

# ---------- Theorem C
def C(k, l, moves):
    L = set(range(l, l + k))
    U = {h: [] for h in L}
    c = l; W = list(range(1, l))
    for delta, pi in moves:
        r = len(pi)
        assert delta >= 0 and 1 <= r <= k and sorted(pi) == list(range(r)) and (delta == 0 or r == k)
        assert all(k + delta + pi[j] - j in L for j in range(r))
        for j in range(r): U[k + delta + pi[j] - j].append(c + j)
        W += list(range(c + k, c + k + delta))
        c += r + delta
    y = c + l + k - 1
    W += list(range(y - l + 1, y))
    return y, sorted(U.items()), sorted(W), 2 * (l - 1) + sum(d for d, _ in moves)

def valid_moves(k, l, dmax):
    L = set(range(l, l + k)); out = []
    for r in range(1, k + 1):
        for pi in itertools.permutations(range(r)):
            if all(k + pi[j] - j in L for j in range(r)): out.append((0, pi))
    for d in range(1, dmax + 1):
        for pi in itertools.permutations(range(k)):
            if all(k + d + pi[j] - j in L for j in range(k)): out.append((d, pi))
    return out

def test_C(kmax, Tmax):
    rng = random.Random(2); cnt = 0; ok = True
    for k in range(1, kmax + 1):
        for l in range(1, k + 4):
            vm = valid_moves(k, l, k + 3)
            for T in range(0, Tmax + 1):
                if len(vm) ** T <= 30000: seqs = itertools.product(vm, repeat=T)
                else: seqs = (tuple(rng.choice(vm) for _ in range(T)) for _ in range(20000))
                for s in seqs:
                    y, hubs, W, wc = C(k, l, list(s))
                    ok &= chk("C k=%d l=%d moves=%s" % (k, l, s), [len(u) for _, u in hubs], wc, y, hubs, W); cnt += 1
        print("  C k=%d done total %d ok=%s" % (k, cnt, ok), flush=True)
    # long random sequences
    for _ in range(20000):
        k = rng.randint(1, 6); l = rng.randint(1, k + 2); vm = valid_moves(k, l, 4)
        if not vm: continue
        s = [rng.choice(vm) for _ in range(rng.randint(4, 12))]
        y, hubs, W, wc = C(k, l, s)
        ok &= chk("C long", [len(u) for _, u in hubs], wc, y, hubs, W); cnt += 1
    print("Lemma C: %d combs ok=%s" % (cnt, ok))

def Rm(a, b): return (0, tuple([j + a for j in range(b)] + [j - b for j in range(b, a + b)]))
def Bm(a, k): return (a, tuple(range(k)))
Zm = (0, (0,))

def test_C1(N):
    cnt = 0; ok = True; rng = random.Random(3)
    for s in range(0, N):
        for t in range(0, N):
            for z in range(0, N):
                n = (z + 2) + 3 + (s + 3 * z) + t + s + 2
                if n > N: break
                mv = [Rm(1, 1)] * s + [Zm] * t + [Bm(1, 3)] * z
                for order in (mv, mv[::-1], rng.sample(mv, len(mv))):
                    y, hubs, W, wc = C(3, 2, order)
                    d = dict((h, len(u)) for h, u in hubs)
                    assert (d[4], d[3], d[2]) == (s + 3 * z, t, s) and wc == z + 2
                    ok &= chk("C1 %d %d %d" % (s, t, z), [s + 3 * z, t, s], z + 2, y, hubs, W, a1s=(0, 1, 7)); cnt += 1
    print("Corollary C1 n<=%d: %d combs ok=%s" % (N, cnt, ok))

def test_C3(kmax, smax):
    cnt = 0; ok = True; rng = random.Random(4)
    for k in range(3, kmax + 1):
        for l in range(2, k):
            L = list(range(l, l + k))
            it = itertools.product(range(0, smax + 1), repeat=k) if (smax + 1) ** k <= 300000 else \
                 (tuple(rng.choice([0, 0, 0, 1, 2, rng.randint(0, 12)]) for _ in range(k)) for _ in range(300000))
            for sz in it:
                s = dict(zip(L, sz))
                mom = sum(s[h] * (h - k) for h in L)
                if mom < 0 or mom % k: continue
                B = mom // k
                need = sum((h - k) * s[h] for h in L if h - k >= 2)
                if s[k - 1] < need: continue
                mv = []
                for h in L:
                    if h - k >= 2: mv += [Rm(h - k, 1)] * s[h]
                    if k - h >= 2: mv += [Rm(1, k - h)] * s[h]
                mv += [Rm(1, 1)] * (s[k - 1] - need) + [Bm(1, k)] * B + [Zm] * s.get(k, 0)
                rng.shuffle(mv)
                y, hubs, W, wc = C(k, l, mv)
                d = dict((h, len(u)) for h, u in hubs)
                if d != s: print("COUNTEREXAMPLE C3 sizes", k, l, s, d); ok = False
                if wc != 2 * (l - 1) + B: print("COUNTEREXAMPLE C3 w", k, l, s); ok = False
                ok &= chk("C3", list(sz), wc, y, hubs, W); cnt += 1
    print("Corollary C3 k<=%d: %d instances ok=%s" % (kmax, cnt, ok))

if __name__ == "__main__":
    what = sys.argv[1]
    if what == "P": test_P(int(sys.argv[2])); test_P_two(int(sys.argv[3]))
    if what == "R": test_R(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    if what == "R1": test_R1(int(sys.argv[2]))
    if what == "C": test_C(int(sys.argv[2]), int(sys.argv[3])); test_C1(int(sys.argv[4])); test_C3(6, 3)
    if what == "ex":
        y, hubs, W, k = P([2, 1], 2); print("P example", y, hubs, W)
        y, hubs, W, wc = R(5, [(5, (1, 2, 0, 4, 3))], [0, 1], 2); print("R example", sorted((len(u) for _, u in hubs), reverse=True), wc, y, comb_ok(sorted((len(u) for _, u in hubs), reverse=True), len(W), y, hubs, W))
        y, hubs, W, wc = C(3, 2, [Rm(1, 1), Zm, Bm(1, 3)]); print("C example", y, hubs, W, wc)
