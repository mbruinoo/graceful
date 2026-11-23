#!/usr/bin/env python3
# all diameter-4 trees on n vertices: centre 0, parts of a partition of n-1 (part p = child with p-1 leaves), >=2 parts >=2
import sys
def parts(n,mx):
    if n==0: yield ();return
    for p in range(min(n,mx),0,-1):
        for r in parts(n-p,p): yield (p,)+r
for n in range(int(sys.argv[1]),int(sys.argv[2])+1):
    for P in parts(n-1,n-1):
        if sum(1 for p in P if p>=2)<2: continue
        E=[];v=1
        for p in P:
            c=v;E.append((0,c));v+=1
            for _ in range(p-1): E.append((c,v));v+=1
        print(n,' '.join('%d %d'%e for e in E))
