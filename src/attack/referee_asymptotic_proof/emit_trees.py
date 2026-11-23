#!/usr/bin/env python3
# emit all free trees on n vertices (networkx), one per line: n then n-1 edges "a b"
import sys, networkx as nx
n = int(sys.argv[1])
for T in nx.nonisomorphic_trees(n):
    print(n, " ".join("%d %d" % e for e in T.edges()))
