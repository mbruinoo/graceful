# referee: emit all free trees on n vertices (networkx, independent of src/treegen.h)
# one line per tree: n  u1 v1 u2 v2 ...
import sys, networkx as nx
n = int(sys.argv[1])
if n == 1:
    print(1)
else:
    for T in nx.nonisomorphic_trees(n):
        print(n, " ".join(f"{u} {v}" for u, v in T.edges()))
