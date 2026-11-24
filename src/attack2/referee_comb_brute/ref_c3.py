import random, itertools
from ref_rules import *
rng = random.Random(7); cnt = 0; ok = True
for k in range(3, 9):
    for l in range(2, k):
        L = list(range(l, l + k))
        for _ in range(150000):
            sz = tuple(rng.choice([0, 0, 1, 2, 3, rng.randint(0, 9)]) for _ in range(k))
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
            if d != s or wc != 2 * (l - 1) + B: print("COUNTEREXAMPLE C3", k, l, s, d); ok = False
            ok &= chk("C3", list(sz), wc, y, hubs, W); cnt += 1
print("C3 random-filtered instances", cnt, "ok", ok)
