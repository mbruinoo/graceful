from lib import *
import itertools
def K(m,n):
    p=[1]*(n-1)
    for i in range(1,m): p[2*i-1]=2
    for j in range(1,m): p[2*j-2]=m+2-j
    return tuple(p)
def run(p,seq):
    for k in seq:
        p=p[:k-1]+(p[k-1]+1,)+p[k:]
        if not is_tree(p): return None
    return p
# find all valid orders for the transition K(m)->K(m+1), small m
for m in range(2,6):
    n=2*m+3
    moves=[2*j-1 for j in range(1,m)]+[2*m-1,2*m-1,2*m]
    good=set()
    for perm in set(itertools.permutations(moves)):
        q=run(K(m,n),perm)
        if q is not None: assert q==K(m+1,n); good.add(perm)
    print(m,len(good)); 
    for g in sorted(good)[:12]: print("   ",g)
