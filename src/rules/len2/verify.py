#!/usr/bin/env python3
"""Independent check of rule.py: hand the numbers m, m-1, ..., 1 out one at a time, exactly as in the definition of a deal.
Usage: verify.py K        (all k = 1..K)"""
import sys
from rule import build, deal_from_graph
K=int(sys.argv[1]); zig=0; one=0
for k in range(1,K+1):
    legs,signs=deal_from_graph(build(k)); m=2*k
    owner={}                                   # number -> (leg index, position in leg)
    for i,l in enumerate(legs):
        assert len(l)==2
        for p,w in enumerate(l):
            assert w not in owner; owner[w]=(i,p)
    assert sorted(owner)==list(range(1,m+1))
    tip=[0]*k; got=[0]*k; visited={0}; twice_up=0
    for w in range(m,0,-1):                    # largest number first
        i,p=owner[w]
        assert p==got[i], "a leg must receive its numbers in decreasing order"
        up = (p==0) or signs[i][p]==1
        if p>0 and up: twice_up+=1
        tip[i] += w if up else -w
        assert 1<=tip[i]<=m and tip[i] not in visited, (k,w,tip[i])
        visited.add(tip[i]); got[i]+=1
    assert visited==set(range(0,m+1))
    assert twice_up==(1 if k%3==2 else 0)
    zig+=twice_up==0; one+=twice_up==1
print("k = 1..%d: %d zigzag deals (k = 0,1 mod 3), %d deals with exactly one leg going up twice (k = 2 mod 3); all valid"%(K,zig,one))
