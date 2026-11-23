#!/usr/bin/env python3
"""Large-k spot checks and design identities far beyond the claimed range. Usage: spot.py KDES"""
import sys, random
from referee import designs, design_ok, build, valid_deal
random.seed(1)
KD = int(sys.argv[1]); nd = 0; bad = []
for k in range(1, KD + 1):
    for name, c, d in designs(k):
        nd += 1; e = design_ok(k, c, d)
        if e: bad.append((k, name, e))
        if c - k > 2 * k: bad.append((k, name, "threshold > 2k"))
print("designs checked for k<=%d: %d, failures %d" % (KD, nd, len(bad)), bad[:5])
ks = sorted(set(list(range(331, 2000, 97)) + [512, 729, 1024, 1296, 1458, 1536, 2187, 3000, 2999, 2998, 4096, 3645, 5000, 6561]))
n = 0; inv = []
for k in ks:
    for name, c, d in designs(k):
        r0 = max(c - k, 1)
        while (r0 + k - c) % 3: r0 += 1
        for r in sorted({r0, r0 + 3, r0 + 6, r0 + 3 * random.randint(3, 2000), r0 + 3 * random.randint(2000, 20000)}):
            dl = build(r, k, c, d, random.choice([0, 0, 1, 7]))
            ok, why = valid_deal(*dl); n += 1
            if not ok: inv.append((k, r, name, why))
print("spot deals (k in %s): %d checked, invalid %d" % (ks, n, len(inv)), inv[:5])
