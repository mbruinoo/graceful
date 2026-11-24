# referee: all nonisomorphic trees on n vertices (networkx order), 0-based edge list per line
import sys, networkx as nx
n=int(sys.argv[1])
for T in nx.nonisomorphic_trees(n):
    print(' '.join(f"{u} {v}" for u,v in T.edges()))
