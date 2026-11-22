# Dump all non-isomorphic trees on n vertices, one per line: "u v u v ..." (0-based edges)
import sys, networkx as nx
n=int(sys.argv[1])
out=sys.stdout
for T in nx.nonisomorphic_trees(n):
    out.write(' '.join(f"{u} {v}" for u,v in T.edges())+'\n')
