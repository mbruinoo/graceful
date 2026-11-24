#!/usr/bin/env python3
"""Exploration tool (mirror combs in 'ruler' form).
Positions 1..P, P = M+k+1.  A ruler = head at position p with teeth at p-u (u in A).  Rulers of the k hubs
plus the root ruler (head at P, v teeth) must tile [1,P] and use each distance 1..M once.
Here hubs come in nest families: family (E,q) = E rulers with heads c+1..c+E; ruler r (r=1..E) has q teeth
at c-delta_j-r, i.e. distances delta_j+2r (j=1..q).
Usage: nestsearch.py vmax E1 q1 [E2 q2 ...]"""
import sys
def run(fams, v, limit=3, mid=0):
    k=sum(E for E,q in fams); M=sum(E*q for E,q in fams)+v; P=M+k+1+mid
    if mid and k%2: return P,M,[]
    fullP=(1<<(P+1))-2; fullD=(1<<(M+1))-2
    sols=[]; cur=[]
    def fam(i,uP,uD):
        if len(sols)>=limit: return
        if i==len(fams):
            lp=[x for x in range(1,P) if not uP>>x&1]; ld=[x for x in range(1,M+1) if not uD>>x&1]
            if mid:
                p0=(k+2)//2
                if p0 not in lp: return
                lp.remove(p0)
            if sorted(P-x for x in lp)==ld: sols.append(([list(z) for z in cur],ld))
            return
        E,q=fams[i]
        for c in range(E, P-E):   # heads c+1..c+E <= P-1
            hm=((1<<E)-1)<<(c+1)
            if hm&uP: continue
            cur.append([c]); teeth(i,c,0,-2,uP|hm,uD); cur.pop()
    def teeth(i,c,j,dprev,uP,uD):
        if len(sols)>=limit: return
        E,q=fams[i]
        if j==q: fam(i+1,uP,uD); return
        for d in range(dprev+1, c-E):   # tooth block c-d-E .. c-d-1 >= 1
            if d+2*E>M: break
            tm=((1<<E)-1)<<(c-d-E)
            if tm&uP: continue
            dm=0
            for r in range(1,E+1): dm|=1<<(d+2*r)
            if dm&uD: continue
            cur[-1].append(d); teeth(i,c,j+1,d,uP|tm,uD|dm); cur[-1].pop()
    fam(0,0,0)
    return P,M,sols
if __name__=="__main__":
    vmax=int(sys.argv[1]); a=list(map(int,sys.argv[2:])); fams=[(a[i],a[i+1]) for i in range(0,len(a),2)]
    for v2 in range(2*vmax+2):
        v=v2//2; mid=v2%2
        P,M,sols=run(fams,v,3,mid)
        if sols:
            for s,ld in sols: print("v=%d mid=%d P=%d M=%d"%(v,mid,P,M), ' '.join("fam(E=%d,q=%d): c=%d deltas=%s"%(fams[i][0],fams[i][1],s[i][0],s[i][1:]) for i in range(len(fams))), "root distances",ld)
            break
        else: print("v=%d mid=%d none"%(v,mid))
