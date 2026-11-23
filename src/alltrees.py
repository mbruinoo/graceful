#!/usr/bin/env python3
"""Every tree on n vertices, one per line, in growfam's format (no networkx needed).  Usage: alltrees.py n"""
import sys
from hubscan_lib import rooted, parents, adjOf, canon
n = int(sys.argv[1]); seen = set(); i = 0
for L in rooted(n):
    par = parents(L); E = [(par[j], j) for j in range(1, n)]; c = canon(adjOf(n, E))
    if c in seen: continue
    seen.add(c); i += 1; print(f"t{n}#{i}: " + " ".join(f"{a} {b}" for a, b in E))
