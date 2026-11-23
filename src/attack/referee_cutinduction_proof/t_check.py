#!/usr/bin/env python3
"""Referee check of claim 0 (T1-T4), written from README sections 1-2 and the claim's
definition only.  Usage: t_check.py NMAX [NMAX_T3]"""
import sys
from itertools import combinations
NMAX=int(sys.argv[1]); NT3=int(sys.argv[2]) if len(sys.argv)>2 else NMAX

def growth_placements(n):
    out=[]
    p=[0]*(n)          # p[k] for k=1..n-1
    def rec(k,used):
        if k==0: out.append(tuple(p[1:])); return
        for a in range(1,n-k+1):
            ua=(used>>a)&1; ub=(used>>(a+k))&1
            if k==n-1 or ua+ub==1:
                p[k]=a; rec(k-1,used|(1<<a)|(1<<(a+k)))
    rec(n-1,0); return out

def is_growth(q):
    n=len(q)+1
    if sorted(1<=q[k-1]<=n-k for k in range(1,n))[0] is False: return False
    used=0
    for k in range(n-1,0,-1):
        a=q[k-1]; b=a+k
        ua=(used>>a)&1; ub=(used>>b)&1
        if k!=n-1 and ua+ub!=1: return False
        used|=(1<<a)|(1<<b)
    return True

def is_clean(p,R):
    """R = set of labels. literal conditions (1),(2)."""
    n=len(p)+1
    rb=[k for k in range(1,n) if p[k-1] in R or p[k-1]+k in R]
    if len(rb)!=len(R): return False
    for k in range(1,n):
        if k in rb: continue
        a=p[k-1]
        inside=sum(1 for x in R if a<x<a+k)
        if inside!=sum(1 for j in rb if j<k): return False
    return True

def delete(p,R):
    """returns (list of (oldlen,newleft,newlen)) for kept brackets"""
    n=len(p)+1
    new={}; c=0
    for x in range(1,n+1):
        if x not in R: c+=1; new[x]=c
    res=[]
    for k in range(1,n):
        a=p[k-1]; b=a+k
        if a in R or b in R: continue
        res.append((k,new[a],new[b]-new[a]))
    return res

def as_placement(res,m):
    """res from delete; m = number of labels left. returns placement tuple or None"""
    lens=sorted(r[2] for r in res)
    if lens!=list(range(1,m)): return None
    q=[0]*(m-1)
    for _,a,l in res: q[l-1]=a
    return tuple(q)

def order_kept(res):
    r=sorted(res); return all(r[i][2]<r[i+1][2] for i in range(len(r)-1))

def leaves(p):
    n=len(p)+1; deg=[0]*(n+1)
    for k in range(1,n): deg[p[k-1]]+=1; deg[p[k-1]+k]+=1
    return [x for x in range(1,n+1) if deg[x]==1]

def is_staircase(p):
    n=len(p)+1
    return p[n-2]==1 and all(p[k-1]-p[k] in (0,1) for k in range(1,n-1))

core_memo={}
def cores(p):
    """set of terminal placements over ALL orders of clean-leaf deletion"""
    if p in core_memo: return core_memo[p]
    n=len(p)+1
    res=set()
    if n>2:
        for L in leaves(p):
            if is_clean(p,{L}):
                q=as_placement(delete(p,{L}),n-1)
                res|=cores(q)
    if not res: res={p}
    core_memo[p]=res; return res

for n in range(3,NMAX+1):
    G=growth_placements(n)
    v1=v1c=v2=v4=0; nclean=npairs=nonorder=0; nstair=0
    for p in G:
        cleans=[]
        for r in range(1,n-1):
            for Rt in combinations(range(1,n+1),r):
                R=set(Rt)
                c=is_clean(p,R)
                res=delete(p,R)
                cond1=(len(res)==n-1-r)
                q=as_placement(res,n-r) if cond1 else None
                if c:
                    nclean+=1; cleans.append(frozenset(R))
                    if q is None or not is_growth(q) or not order_kept(res): v1+=1
                else:
                    # converse: (1) + placement + order kept => (2)
                    if cond1 and q is not None and order_kept(res): v1c+=1
                    if cond1 and q is not None and is_growth(q) and not order_kept(res): nonorder+=1
        # T2
        for R1 in cleans:
            for R2 in cleans:
                if R1&R2 or n-len(R1)-len(R2)<2: continue
                npairs+=1
                q=as_placement(delete(p,R1),n-len(R1))
                new={}; c=0
                for x in range(1,n+1):
                    if x not in R1: c+=1; new[x]=c
                img={new[x] for x in R2}
                if not is_clean(q,img): v2+=1
                if R1|R2 not in cleans_set if False else False: pass
        cs=set(cleans)
        for R1 in cleans:
            for R2 in cleans:
                if R1&R2 or n-len(R1)-len(R2)<2: continue
                if (R1|R2) not in cs: v2+=1
        # T4
        lv=leaves(p)
        allclean=all(frozenset({L}) in cs for L in lv)
        a=p[0]; b=a+1
        le=[x for x in (a,b) if x in lv]
        assert len(le)==1
        endclean=frozenset({le[0]}) in cs
        st=is_staircase(p); nstair+=st
        if not (allclean==endclean==st): v4+=1
    v3=0
    if n<=NT3:
        for p in G:
            if len(cores(p))!=1: v3+=1
    print(f"n={n} growth={len(G)} clean_sets={nclean} disjoint_pairs(ordered)={npairs} "
          f"T1viol={v1} T1conv_viol={v1c} T2viol={v2} T3viol={v3 if n<=NT3 else 'n/a'} T4viol={v4} "
          f"staircases={nstair} (2^(n-2)={2**(n-2)}) nonorder_growth_restrictions={nonorder}",flush=True)
