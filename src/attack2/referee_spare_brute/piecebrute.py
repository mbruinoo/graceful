# brute-force cross-check of the 'piece' mode of rs.cpp: all one-spare labelings of path arms (b,j), filter crossing + innermost tip
from thm import *
import sys
for b,j in [(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(3,2),(4,2),(3,3),(7,3),(5,2),(6,2),(7,2),(5,3),(6,3),(4,3),(8,2)]:
    n=b+j+1; par={0:None}
    for i in range(1,b+1): par[i]=i-1
    for i in range(1,j+1): par[b+i]=0 if i==1 else b+i-1
    y=b+j; cnt=0
    for g in labelings(par,n+1):
        for a in thresholds(par,g):
            used=sorted(g.values()); lows=[x for x in used if x<=a]; highs=[x for x in used if x>a]
            if (highs and g[y]==min(highs)) or (lows and g[y]==max(lows)): cnt+=1; break
    print("arms (%d,%d): crossing one-spare labelings with innermost tip: %d"%(b,j,cnt))
