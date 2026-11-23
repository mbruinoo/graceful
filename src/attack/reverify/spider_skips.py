#!/usr/bin/env python3
"""Least number of skips for spiders (README section 12), using gp (H=0,1,2,3) tree by tree.
Every "can be built with h skips" is certificate-checked with check_cert.verify; every
"cannot with fewer" is an exhaustive NONE from gp.

Usage: spider_skips.py /path/to/gp table          equal-leg table, L=1..6, k=3,4,5,6,8
       spider_skips.py /path/to/gp all n [n ...]  all spiders (>= 3 legs) on n vertices
"""
import sys, subprocess, collections
from check_cert import verify

def spider(legs):
    e = []; nx = 1
    for L in legs:
        p = 0
        for _ in range(L):
            e.append((p, nx)); p = nx; nx += 1
    return nx, e

def partitions(r, mx):
    if r == 0:
        yield []; return
    for p in range(min(r, mx), 0, -1):
        for rest in partitions(r - p, p):
            yield [p] + rest

def least(gp, legs, hmax=4):
    n, e = spider(legs)
    line = f"{n} " + " ".join(f"{a} {b}" for a, b in e) + "\n"
    for H in range(hmax + 1):
        out = subprocess.run([gp, f"H={H}"], input=line, capture_output=True, text=True).stdout
        if out.startswith("OK"):
            lab = list(map(int, out.split()[1:]))
            assert verify(n, e, lab, H=H) is None
            return H
        assert out.startswith("NONE")
    return None

gp = sys.argv[1]
if sys.argv[2] == "table":
    print("L\\k   3 4 5 6 8")
    for L in range(1, 7):
        print(f"L={L}: ", " ".join(str(least(gp, [L] * k)) for k in (3, 4, 5, 6, 8)), flush=True)
else:
    for n in map(int, sys.argv[3:]):
        c = collections.Counter(); tot = 0
        for p in partitions(n - 1, n - 1):
            if len(p) >= 3:
                c[least(gp, p)] += 1; tot += 1
        print(f"n={n}: spiders {tot}, need 0: {c[0]}, need 1: {c[1]}, need 2: {c[2]}, need more: {tot - c[0] - c[1] - c[2]}", flush=True)
