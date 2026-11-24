#!/usr/bin/env python3
# lsol.py l h1 h2 [max]  -- enumerate ALL growth placements of L(l;h1,h2) anchored at v (labels 0..m, v=0),
# straight from the root form: c at a; g_i at a-x_i or a+x_i; root leaf: label=length; leaf of g_i: g_i +- w, w<x_i.
# Prints each solution as: a | g1(x1) g2(x2) | root leaves | hub1 leaves (signed lengths) | hub2 leaves
import sys
l,h1,h2=map(int,sys.argv[1:4]); mx=int(sys.argv[4]) if len(sys.argv)>4 else 10**9
m=l+h1+h2+3; sols=[]
def run():
    cnt=0
    for a in range(1,m+1):
        for s1 in (-1,1):
            for x1 in range(1,a):
                g1=a+s1*x1
                if not (1<=g1<=m): continue
                for s2 in (-1,1):
                    for x2 in range(1,a):
                        g2=a+s2*x2
                        if not(1<=g2<=m) or g2==g1 or x2==x1: continue
                        usedL={a,g1,g2}; g=(g1,g2); x=(x1,x2); H=(h1,h2)
                        lens=[w for w in range(m,0,-1) if w not in (a,x1,x2)]
                        assign={}
                        cap=[h1,h2,l]
                        def rec(i):
                            nonlocal cnt
                            if i==len(lens):
                                cnt+=1
                                if cnt<=mx:
                                    R=sorted(w for w,(c,L) in assign.items() if c==2)
                                    A=[sorted(((L-g[k]) for w,(c,L) in assign.items() if c==k),key=abs) for k in (0,1)]
                                    print(f"a={a} | g1={g1}(x={x1}) g2={g2}(x={x2}) | root {R} | hub1 {A[0]} | hub2 {A[1]}")
                                return
                            w=lens[i]
                            if cap[2] and w not in usedL:
                                cap[2]-=1; usedL.add(w); assign[w]=(2,w); rec(i+1); del assign[w]; usedL.discard(w); cap[2]+=1
                            for k in (0,1):
                                if cap[k] and w<x[k]:
                                    for s in (-1,1):
                                        L=g[k]+s*w
                                        if 1<=L<=m and L not in usedL:
                                            cap[k]-=1; usedL.add(L); assign[w]=(k,L); rec(i+1); del assign[w]; usedL.discard(L); cap[k]+=1
                        rec(0)
    return cnt
c=run(); print("L(%d;%d,%d) m=%d solutions=%d"%(l,h1,h2,m,c))
