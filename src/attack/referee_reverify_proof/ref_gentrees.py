# Referee: all trees on n vertices via networkx, one per line "n a b a b ..."; count asserted against OEIS A000055.
import sys, networkx as nx
A=[1,1,1,1,2,3,6,11,23,47,106,235,551,1301,3159,7741,19320,48629,123867,317955,823065,2144505,5623756]
n=int(sys.argv[1]); c=0; out=sys.stdout
for T in nx.nonisomorphic_trees(n):
    out.write(str(n)+" "+" ".join("%d %d"%e for e in T.edges())+"\n"); c+=1
assert c==A[n], (c,A[n])
