# Theorem I check: for n >= 7 the two placements
#   P  = (2, n-3, 1, ..., 1, 2, 1)   and   P' = (3, n-3, 1, ..., 1, 2, 1)
# form a component of the unit-slide graph (every other neighbour on the rails is not a tree).
from lib import *
import sys
for n in range(7,int(sys.argv[1])+1):
    P=(2,n-3)+(1,)*(n-5)+(2,1); Q=(3,)+P[1:]
    assert len(P)==n-1 and is_tree(P) and is_tree(Q)
    for p,other in ((P,Q),(Q,P)):
        nb=[]
        for k in range(1,n):
            for s in (-1,1):
                q=p[:k-1]+(p[k-1]+s,)+p[k:]
                if 1<=q[k-1]<=n-k and is_tree(q): nb.append(q)
        assert nb==[other],(n,p,nb)
print("2-island {P,P'} verified for 7 <= n <=",sys.argv[1])
for n in (5,6):
    P=(2,n-3)+(1,)*(n-5)+(2,1); print("n=%d: P is a tree?"%n, is_tree(P))
