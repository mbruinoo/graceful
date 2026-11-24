#!/usr/bin/env python3
"""Compare the exact least number of inside fillers (combx mode 1) with the divisibility bound of Lemma G.
Usage: wstats.py logs/exact_5_30.txt"""
import sys, math, collections
from functools import reduce
ex=collections.defaultdict(list); tot=0; dist=collections.Counter(); byn={}
import gzip
for line in (gzip.open(sys.argv[1],"rt") if sys.argv[1].endswith(".gz") else open(sys.argv[1])):
    if not line.startswith('S'): continue
    p=line.split('|'); S=list(map(int,p[0].split()[1:])); w=int(p[1].split()[1])
    k=len(S); g=reduce(math.gcd,[s+2 for s in S]); w0=0
    while (k*(k+sum(S)+1+w0))%g: w0+=1
    tot+=1; dist[w]+=1
    n=k+sum(S)+max(S)+2; byn[n]=byn.get(n,0)+1
    assert w>=w0 and w<=max(S)
    if w>w0: ex[k].append((S,w,w0))
print("multisets S:",tot," n range",min(byn),max(byn))
print("distribution of the least w:",sorted(dist.items()))
for k in sorted(ex):
    print("number of non-root hubs k=%d: %d multisets with least w above the divisibility bound"%(k,len(ex[k])))
    if k>=3: print("   "+'; '.join("%s w=%d (bound %d)"%(' '.join(map(str,S)),w,w0) for S,w,w0 in ex[k]))
