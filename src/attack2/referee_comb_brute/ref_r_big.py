"""Theorem R, k=7..9: all single rounds (k=7) x small P-parts, plus random 2-4 round sequences (rejection-sampled)."""
import random, itertools, sys
from ref_rules import *
rng = random.Random(11); cnt = 0; ok = True
def randround(k):
    labels = set(range(1, 2 * k, 2))
    while True:
        B = rng.randrange(1, 2 * k, 2)
        # random permutation with displacement constraint by sequential choice
        pi = [None] * k; used = set(); good = True
        for i in rng.sample(range(k), k):
            c = [p for p in range(k) if p not in used and B + 2 * (p - i) in labels]
            if not c: good = False; break
            p = rng.choice(c); pi[i] = p; used.add(p)
        if good: return (B, tuple(pi))
def randP(k):
    J = k // 2; bs = [rng.choice([0, 0, 1, 2, 5]) for _ in range(J)]
    if k % 2 == 0: return bs, None
    return bs, rng.choice([0, 2, 4, k, k + 1, k + 2, k + 6])
vr7 = valid_rounds(7)
print("k=7 valid rounds", len(vr7), flush=True)
for rd in vr7:
    for bs, c in (([0, 0, 0], 0), ([1, 0, 2], 7), ([2, 1, 0], 4), ([0, 3, 1], 9)):
        if rd[0] < 6 or (c % 2 == 1 and rd[0] < 7): continue
        y, hubs, W, wc = R(7, [rd], bs, c)
        ok &= chk("R k=7 %s %s %s" % (rd, bs, c), [len(u) for _, u in hubs], wc, y, hubs, W); cnt += 1
print("k=7 single rounds:", cnt, ok, flush=True)
for k in range(2, 13):
    done = 0
    while done < 15000:
        T = rng.randint(1, 5)
        s = [randround(k) for _ in range(T)]
        if any(s[t][0] + s[t + 1][0] < 2 * k for t in range(T - 1)): continue
        bs, c = randP(k)
        if s[-1][0] < k - 1 or (c is not None and c % 2 == 1 and s[-1][0] < k): continue
        y, hubs, W, wc = R(k, s, bs, c)
        ok &= chk("R k=%d %s %s %s" % (k, s, bs, c), [len(u) for _, u in hubs], wc, y, hubs, W); cnt += 1; done += 1
    print("k=%d random multi-round ok=%s total %d" % (k, ok, cnt), flush=True)
