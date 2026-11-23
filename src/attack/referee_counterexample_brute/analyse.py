#!/usr/bin/env python3
"""Referee analysis of enumall output (an_n.txt = every rooted shape that occurs as
'tree rooted at the vertex labelled 1' over ALL growth placements on n vertices, with counts).
Own rooted-tree generator (leaf-addition closure), own canonical form.
usage: analyse.py N      (uses an_2..an_N)"""
import sys
from collections import defaultdict
N=int(sys.argv[1])
def canon(t):
    """t = tuple of child trees (each a tuple).  returns (bits,len) ; children sorted desc by (len,bits)"""
    ks=sorted((canon(c) for c in t),key=lambda x:(x[1],x[0]),reverse=True)
    b=1;l=1
    for cb,cl in ks:
        b=(b<<cl)|cb;l+=cl
    return (b<<1,l+1)
def parse(code):
    s=bin(code)[2:]
    st=[]
    for ch in s:
        if ch=='1': st.append([])
        else:
            t=tuple(st.pop())
            if st: st[-1].append(t)
            else: return t
def norm(t):  # canonical nested tuple
    return parse(canon(t)[0])
def add_leaf_everywhere(t):
    # yield all trees obtained by adding one leaf at some vertex
    yield t+((),)
    for i,c in enumerate(t):
        for c2 in add_leaf_everywhere(c):
            yield t[:i]+(c2,)+t[i+1:]
def adj_of(t):
    adj=[[]]
    def rec(t,v):
        for c in t:
            u=len(adj);adj.append([v]);adj[v].append(u);rec(c,u)
    rec(t,0)
    return adj
def rooted_at(adj,r):
    def rec(v,p): return tuple(rec(u,v) for u in adj[v] if u!=p)
    return rec(r,-1)
def unrooted(t):
    adj=adj_of(t);n=len(adj)
    deg=[len(a) for a in adj];rem=n;leaves=[v for v in range(n) if deg[v]<=1];alive=[True]*n
    while rem>2:
        nl=[]
        for v in leaves:
            alive[v]=False;rem-=1
            for u in adj[v]:
                if alive[u]:
                    deg[u]-=1
                    if deg[u]==1:nl.append(u)
        leaves=nl
    cs=[v for v in range(n) if alive[v]]
    return max(canon(rooted_at(adj,c))[0] for c in cs), adj
def is_caterpillar(adj):
    n=len(adj)
    inner=[v for v in range(n) if len(adj[v])>1]
    return all(sum(1 for u in adj[v] if len(adj[u])>1)<=2 for v in inner)
def famA(n):
    # centre c; hub h with m leaves; c-x1-y1; c-x2-y2 ; n = 6+m
    m=n-6
    t=( ((),)*m , ((),), ((),) )
    return unrooted(t)[0]
import sys
sys.setrecursionlimit(10000)
rooted={1:{canon(())[0]}}
allr=rooted[1]
for n in range(2,N+1):
    new=set()
    for code in rooted[n-1]:
        for t2 in add_leaf_everywhere(parse(code)):
            new.add(canon(t2)[0])
    rooted[n]=new
anch={}
for n in range(2,N+1):
    d={}
    for line in open('an_%d.txt'%n):
        a,b=line.split();d[int(a,16)]=int(b)
    anch[n]=d
anch[1]={canon(())[0]:1}
print("n rootedtrees anchors(rooted shapes) nonanchors nonanchor_rootdeg_hist  unrooted trees  trees_without_growth  min_noncat_count  famA_count")
for n in range(2,N+1):
    R=rooted[n];A=anch[n]
    assert set(A)<=R, "enumerated shape not in generator output"
    non=[c for c in R if c not in A]
    hist=defaultdict(int)
    for c in non: hist[len(parse(c))]+=1
    cnt=defaultdict(int);iscat={}
    for c in R:
        u,adj=unrooted(parse(c))
        cnt[u]+=A.get(c,0)
        if u not in iscat: iscat[u]=is_caterpillar(adj)
    nogrow=[u for u in cnt if cnt[u]==0]
    nc=[cnt[u] for u in cnt if not iscat[u]]
    fa=cnt.get(famA(n)) if n>=8 else None
    deg4=sum(1 for c in R if len(parse(c))>=4)
    print(n,len(R),len(A),len(non),dict(sorted(hist.items())),len(cnt),len(nogrow),min(nc) if nc else None,fa,"deg>=4 rooted:",deg4,flush=True)
# hub theorem: for each rooted D on d vertices, least m with T(D,m) root-anchored
print("\nhub: d  #D  hist of least m0 (None = none with d+m<=N)   then list of D with m0>=2")
def show(t): return '('+''.join(show(c) for c in t)+')'
for d in range(1,N+1):
    hist=defaultdict(int);bad=[]
    for c in rooted[d]:
        t=parse(c);m0=None
        fails=[]
        for m in range(0,N-d+1):
            code=canon(t+((),)*m)[0]
            if code in anch[d+m]:
                if m0 is None: m0=m
            else:
                fails.append(m)
        # monotonicity (Lemma 6 step): once anchored, stays anchored
        if m0 is not None: assert all(f<m0 for f in fails), ("non-monotone",show(t),fails)
        hist[m0]+=1
        if m0 is None or m0>=2: bad.append((show(t),m0))
        # members below first success must have some growth placement (any root)
    print(d,len(rooted[d]),dict(hist),bad[:12],flush=True)
