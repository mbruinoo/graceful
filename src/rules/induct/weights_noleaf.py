#!/usr/bin/env python3
"""Deals with no leg of length 1 whose weight system (weights.py) has solutions beyond the all-equal one.
Usage: weights_noleaf.py mmin mmax"""
import sys
from fatten import read_deals, shape
from weights import system, nullspace
for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    tot = 0; found = 0
    for D in read_deals(m):
        if min(len(l) for l in D) < 2: continue
        tot += 1
        B = nullspace(system(D), len(D) + 1)
        if len(B) >= 2:
            found += 1
            print("  ", shape(D), D, "basis (k0,k1..):", [[str(x) for x in v] for v in B])
    print(f"m={m}: leafless deals {tot}, with extra weight solutions {found}")
