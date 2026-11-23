#!/usr/bin/env python3
# For every k <= KMAX: which residues of c mod 3 have a design, and from which construction.  usage: check_designs.py KMAX
import sys
from rule import designs
KMAX=int(sys.argv[1]); fail=[]; names={}
for k in range(1,KMAX+1):
    ds=designs(k)
    want=[0,1,2] if k%3==0 else [1]
    if sorted(ds)!=want: fail.append((k,sorted(ds)))
    for x in ds: names[ds[x][2]]=names.get(ds[x][2],0)+1
print("k <= %d: designs (all re-checked by is_design) give residue 1 for every k and residues 0,1,2 for every k divisible by 3; exceptions: %s"%(KMAX,fail))
print("constructions used:",names)
