#!/usr/bin/env python3
"""Exploration: all-up combs with prescribed hub labels and sizes.  sizes: dict label->size; w fillers."""
import sys
sys.setrecursionlimit(100000)
def solve(sz, w, limit=1):
    k=len(sz); y=k+sum(sz.values())+w+1
    if max(sz)>=y: return y,[]
    T={y-h for h in sz}
    cap=dict(sz); cap[0]=w
    cells=[c for c in range(1,y) if c not in sz]
    usedL=[False]*y
    for t in T: usedL[t]=True
    out=[]; asg={}
    order=sorted(cap)   # try W first, then small hubs
    def rec(i):
        if len(out)>=limit: return
        if i==len(cells): out.append(dict(asg)); return
        c=cells[i]
        for h in order:
            u=c-h
            if u<1 or usedL[u] or cap[h]==0: continue
            if h and u>=y-h: continue
            usedL[u]=True; cap[h]-=1; asg[u]=h
            rec(i+1)
            usedL[u]=False; cap[h]+=1; del asg[u]
    rec(0)
    return y,out
def show(sz,w):
    y,r=solve(sz,w)
    if not r: return None
    d={}
    for u,h in r[0].items(): d.setdefault(h,[]).append(u)
    return "y=%d "%y+' '.join("%d:%s"%(h,sorted(d.get(h,[]))) for h in sorted(d))
if __name__=="__main__":
    a=list(map(int,sys.argv[1:]))   # sizes for labels 1,3,5,...; tries w=0..
    sz={2*i+1:s for i,s in enumerate(a)}
    for w in range(0,2*len(a)+2):
        s=show(sz,w)
        print("w=%d"%w, s)
        if s: break
