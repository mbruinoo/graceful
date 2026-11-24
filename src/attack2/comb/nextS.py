#!/usr/bin/env python3
"""List the multisets S that a combx run (lo, part, nparts) has not yet certified in a log file.
Usage: nextS.py lo N part nparts logfile"""
import sys
def gen(total,k,maxv):
    if k==0:
        if total==0: yield []
        return
    for f in range(min(total,maxv),-1,-1):
        for rest in gen(total-f,k-1,f): yield [f]+rest
lo,N,part,nparts=map(int,sys.argv[1:5])
done=set()
for line in open(sys.argv[5]):
    if line.startswith('S'): done.add(tuple(map(int,line.split('|')[0].split()[1:])))
idx=0
for n in range(lo,N+1):
    for k in range(1,n):
        mx=1
        while k+mx+mx+2<=n:
            rest=n-2-k-mx-mx
            for p in gen(rest,k-1,mx):
                S=tuple([mx]+p)
                if idx%nparts==part and S not in done: print(n,*S)
                idx+=1
            mx+=1
