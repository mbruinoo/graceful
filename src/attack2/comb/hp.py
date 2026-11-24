#!/usr/bin/env python3
"""Exploration: the half problem (headless comb).  Hubs at labels H (list), q[h] = number of mirror pairs of
hub h (hub size 2q[h]), v = number of root pairs.  M = sum q + v.  Find a bijection psi from lengths [1,M]
onto cells [1,M+k] minus H with psi(u)-u in H (used q[h] times) or 0 (used v times).
By Lemma M/H of REPORT.txt this gives a mirror comb with y = 2M+k+1, heads y-h, pairs {u, y-h-u}, W = {u, y-u}."""
import sys
def solve(H, q, v, limit=1):
    k=len(H); M=sum(q)+v; cap=dict(zip(H,q)); cap[0]=v
    cells=[c for c in range(1,M+k+1) if c not in cap or c==0]
    used=[False]*(M+1); out=[]; asg={}
    order=sorted(cap.keys(), reverse=True)
    def rec(i):
        if len(out)>=limit: return
        if i==len(cells): out.append(dict(asg)); return
        c=cells[i]
        for h in order:
            u=c-h
            if u<1: continue
            if u>M or used[u] or cap[h]==0: continue
            used[u]=True; cap[h]-=1; asg[u]=h
            rec(i+1)
            used[u]=False; cap[h]+=1; del asg[u]
    rec(0)
    return out
def show(H,q,v):
    r=solve(H,q,v)
    if not r: return None
    a=r[0]; d={}
    for u,h in a.items(): d.setdefault(h,[]).append(u)
    return ' '.join("%d:%s"%(h,sorted(d.get(h,[]))) for h in sorted(d))
if __name__=="__main__":
    import itertools
    k=int(sys.argv[1]); qmax=int(sys.argv[2]); H=[2*i+1 for i in range(k)]
    bad=0; tot=0
    for q in itertools.product(range(0,qmax+1),repeat=k):
        num=sum(q[i]*(2*(i+1)-1-k) for i in range(k))+k*(k-1)//2
        if num%k or num<0: continue
        v=num//k; tot+=1
        s=show(H,list(q),v)
        if s is None: bad+=1; print("NO ",q,"v=",v)
        elif len(sys.argv)>3: print("ok ",q,"v=",v,s)
    print("k=%d qmax=%d: assignments with integer v>=0: %d, unsolvable: %d"%(k,qmax,tot,bad))
