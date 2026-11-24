#!/usr/bin/env python3
# verify_lemmas.py NMAX  -- machine check of every numbered step of PROOFS.txt on ALL solutions of the reduced
# problem R(h1,h2,d) with N = h1+h2+2+d <= NMAX (all parities, 1 <= h1,h2).  Any failure prints FAIL.
# Reduced problem: a = N+1; hubs at g1 != g2 in [1,N] with edges a-g1, a-g2; hub i has h_i leaves, a leaf of
# length w (< a-g_i) has label g_i+w or g_i-w; d gaps; every number of [1,N] is used once as a label, once as a length.
import sys
from collections import Counter
NMAX=int(sys.argv[1]); stats=Counter(); fails=0
def fail(msg,ctx):
    global fails; fails+=1
    if fails<20: print("FAIL",msg,ctx)
def solutions(h1,h2,d):
    N=h1+h2+2+d; a=N+1
    for g1 in range(1,N+1):
        for g2 in range(1,N+1):
            if g1==g2: continue
            g=(g1,g2); x=(a-g1,a-g2); H=(h1,h2)
            lens=[w for w in range(N,0,-1) if w not in x]
            used=set(g); cap=[h1,h2,d]; asg=[]
            def rec(i):
                if i==len(lens):
                    yield list(asg); return
                w=lens[i]
                if cap[2] and w not in used:
                    cap[2]-=1; used.add(w); asg.append((w,2,0)); yield from rec(i+1); asg.pop(); used.discard(w); cap[2]+=1
                for k in (0,1):
                    if cap[k] and w<x[k]:
                        for s in (1,-1):
                            L=g[k]+s*w
                            if 1<=L<=N and L not in used:
                                cap[k]-=1; used.add(L); asg.append((w,k,s)); yield from rec(i+1); asg.pop(); used.discard(L); cap[k]+=1
            for sol in rec(0): yield N,a,g,sol
def check(h1,h2,d,N,a,gs,sol):
    H=(h1,h2); lo=0 if gs[0]<gs[1] else 1; hi=1-lo
    e,g=gs[lo],gs[hi]; hE,hG=H[lo],H[hi]; X,Y=a-e,a-g
    A={w for w,k,s in sol if k==lo and s==1}; D={w for w,k,s in sol if k==lo and s==-1}
    U={w for w,k,s in sol if k==hi and s==1}; V={w for w,k,s in sol if k==hi and s==-1}
    G={w for w,k,s in sol if k==2}
    ctx=(h1,h2,d,gs,sorted(A),sorted(D),sorted(U),sorted(V),sorted(G))
    cnt=lambda S,lo_,hi_: sum(1 for z in S if lo_<=z<=hi_)
    INF=10**6
    # (B1)
    if not (e-1<=d and all(z in G for z in range(X+1,N+1)) and g<=X and Y>=e): fail("B1",ctx)
    # (STAR) for every t
    for t in range(0,N+2):
        lhs=cnt(A,t-e+1,t)+cnt(U,t-g+1,t)
        rhs=(e<=t)+(g<=t)-(X<=t)-(Y<=t)+cnt(V,g-t,INF)-cnt(V,1,t)+cnt(D,e-t,INF)-cnt(D,1,t)
        if lhs!=rhs: fail("STAR",ctx)
    # (T1) sum identity and parity lemma
    if 2*d!=(e-2)*(hE+2)+(g-2)*(hG+2)+2-2*sum(V)-2*sum(D): fail("T1",ctx)
    p,q=min(h1,h2),max(h1,h2)
    if h1!=h2:
        gQ=gs[0] if h1>h2 else gs[1]; gP=gs[1] if h1>h2 else gs[0]
        if p%2==0 and q%2==1 and gQ%2: fail("parity",ctx)
    # (I)
    L=sum(min(e,g-z) for z in A if z<g)+sum(g-z for z in U if z<g)
    if e*len(A)+g*len(U)-L!=X-g+max(Y-g,0): fail("I",ctx)
    iota=1 if any(z<g for z in U) else 0
    # (B4)
    if cnt(A,g-e,g-1)+cnt(U,1,g-1)!=1-(Y<=g-1): fail("B4",ctx)
    if sum(1 for z in U if z<g)>1: fail("B4b",ctx)
    if g<=Y:
        stats['part2']+=1
        Alow=sum(1 for z in A if z<g)
        if Alow+iota+len(V)+len(D)>g-1: fail("lowcount",ctx)
        al=(e-2)*(hE+len(V))+(g-2)*len(U)-(e-3)*g+2*e-6-(g-1-e)*iota
        be=-2*hE-2*len(V)+(g-2)*len(U)+e+3*g-6-(g-1)*iota
        if 2*d<al: fail("alpha",ctx)
        if 2*d<be: fail("beta",ctx)
        if e==2:
            stats['e2']+=1
            if len(V)>g-2: fail("e2 V",ctx)
            if 2*d<hG: fail("e2 concl",ctx)
        if e>=3:
            stats['e>=3']+=1
            if 2*d<hE+hG+e-3: fail("e>=3 concl",ctx)
        if e==1:
            stats['e1']+=1
            if len(U)<1: fail("e1 k>=1",ctx)
            if g==2 and hE>=1: fail("e1 g=2",ctx)
            if len(V)>g-2: fail("e1 j",ctx)
            if len(U)==1 and iota==1:
                u=min(U)
                if not (Y<=u+g and all(t in A for t in range(g,Y)) and all(t in A for t in range(u+g,X))): fail("e1 k=1 structure",ctx)
            # conclusion of section 6: low hub at 1 with fewer leaves, g>=4  =>  2d >= hE
            if hE<hG and g>=4 and 2*d<hE: fail("e1 concl",ctx)
    else:
        stats['part1']+=1
        if U: fail("p1 U",ctx)
        if any(not(g-Y<=v<=Y-1) for v in V): fail("p1 V",ctx)
        if any(Y-e<z<=g-1 for z in A): fail("p1 A",ctx)
        if Y%e: fail("p1 e|Y",ctx)
        else:
            y=Y//e; c=g-Y-1
            if {z for z in A if z>=g}!={g+i*e for i in range(y-1)}: fail("p1 A2",ctx)
            gam=sum(1 for z in G if z<Y)
            if d!=y*(e-1)+c+gam: fail("p1 d",ctx)
            if hE+hG!=Y+y-2-gam: fail("p1 count",ctx)
            if e>=2 and h1!=h2 and 2*d<p: fail("p1 e>=2 concl",ctx)
            if e==1 and hE<hG: fail("p1 e=1: low hub with fewer leaves should be impossible",ctx)
    # MAIN THEOREM: p<q and 2d<p  =>  gQ=1 or (gP,gQ)=(1,3)
    if h1!=h2 and 2*d<p:
        stats['2d<p solutions']+=1
        if not (gQ==1 or (gP,gQ)==(1,3)): fail("MAIN",ctx)
        stats[('exception',gP if gQ==3 else '*',gQ)]+=1
    if h1!=h2 and e>=2 and 2*d<p: fail("e>=2 main",ctx)
tot=0
for N in range(4,NMAX+1):
    for d in range(0,N-3):
        for h1 in range(1,N-2-d):
            h2=N-2-d-h1
            if h2<1: continue
            for (N_,a,g,sol) in solutions(h1,h2,d):
                tot+=1; check(h1,h2,d,N_,a,g,sol)
    print("N<=%d: solutions checked so far %d, failures %d"%(N,tot,fails),flush=True)
print(dict(stats)); print("TOTAL solutions",tot,"FAILURES",fails)
