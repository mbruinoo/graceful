#!/usr/bin/env python3
"""Sanity checks of covergen.py (which only does bookkeeping of sizes):
 (a) for every generated (S, w) whose S is in the exact log, w >= the exact least w found by combx mode 1;
 (b) for a random sample of generated (S, w), CP-SAT finds an all-up comb with exactly w fillers, and
     verify.check accepts it.
Usage: covercheck.py N logs/exact_5_30.txt [samples]"""
import sys, random
from covergen import families
from cpsat import solve
from verify import check
N=int(sys.argv[1]); least={}
import gzip
for line in (gzip.open(sys.argv[2],"rt") if sys.argv[2].endswith(".gz") else open(sys.argv[2])):
    if line.startswith('S'):
        p=line.split('|'); least[tuple(map(int,p[0].split()[1:]))]=int(p[1].split()[1])
f=families(N); bad=0; cmp_=0
for S,d in f.items():
    if S in least and S[0]>=1:
        for w in d:
            cmp_+=1
            if w<least[S]: bad+=1; print("CONTRADICTION",S,w,least[S])
print("(a) %d generated pairs (S,w) compared with the exact least w: %d contradictions"%(cmp_,bad))
rng=random.Random(5); items=[(S,w) for S,d in f.items() for w in d if S[0]>=1]
ns=int(sys.argv[3]) if len(sys.argv)>3 else 60; ok=0
for S,w in rng.sample(items,ns):
    r=solve(list(S),w,120,2)
    if r and r!="NONE":
        p=[x.strip() for x in r.split('|')]; hubs=[]
        for tok in p[2].split():
            h,_,us=tok.partition(':'); hubs.append((int(h),[int(u) for u in us.split(',')] if us else []))
        W=list(map(int,p[3].split()[1:])); check(list(S),w,int(p[1].split()[3]),hubs,W,w); ok+=1
    else: print("NOT CONFIRMED",S,w,r)
print("(b) %d of %d sampled pairs confirmed by CP-SAT with exactly w fillers"%(ok,ns))
