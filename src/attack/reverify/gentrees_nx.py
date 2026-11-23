#!/usr/bin/env python3
"""Write every tree on n vertices (networkx.nonisomorphic_trees), one per line:
   n u1 v1 u2 v2 ...   Usage: gentrees_nx.py n > file
The count is checked against OEIS A000055."""
import sys
import networkx as nx
A000055 = {1: 1, 2: 1, 3: 1, 4: 2, 5: 3, 6: 6, 7: 11, 8: 23, 9: 47, 10: 106, 11: 235, 12: 551,
           13: 1301, 14: 3159, 15: 7741, 16: 19320, 17: 48629, 18: 123867, 19: 317955, 20: 823065, 21: 2144505, 22: 5623756, 23: 14828074}
n = int(sys.argv[1])
c = 0
out = sys.stdout
for T in nx.nonisomorphic_trees(n):
    out.write(str(n) + " " + " ".join(f"{u} {v}" for u, v in T.edges()) + "\n")
    c += 1
assert c == A000055[n], (c, A000055[n])
sys.stderr.write(f"n={n}: {c} trees\n")
