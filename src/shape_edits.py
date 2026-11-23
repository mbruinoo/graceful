# shape_edits.py -- pairs of tree shapes one edge exchange apart, and how many are one slide apart in some placement (n = 5..10)
import sys, itertools
sys.setrecursionlimit(10000)
def canon(n, edges):
    adj=[[] for _ in range(n)]
    for a,b in edges: adj[a].append(b); adj[b].append(a)
    deg=[len(x) for x in adj]; layer=[v for v in range(n) if deg[v]<=1]; rem=n; gone=set()
    while rem>2:
        nx=[]
        for v in layer:
            gone.add(v); rem-=1
            for u in adj[v]:
                if u not in gone:
                    deg[u]-=1
                    if deg[u]==1: nx.append(u)
        layer=nx
    def enc(v,p): return '('+''.join(sorted(enc(u,v) for u in adj[v] if u!=p))+')'
    cs=[v for v in range(n) if v not in gone]
    return min(enc(c,-1) for c in cs)
def istree(n,p):
    par=list(range(n+1))
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for k in range(1,n):
        a,b=f(p[k]),f(p[k]+k)
        if a==b: return False
        par[a]=b
    return True
for n in range(5,11):
    slide=set(); rep={}
    p=[0]*n
    def rec(k):
        if k==n:
            if not istree(n,p): return
            E=[(p[j]-1,p[j]+j-1) for j in range(1,n)]; c=canon(n,E); rep.setdefault(c,E)
            for j in range(1,n):
                if p[j]<n-j:
                    p[j]+=1
                    if istree(n,p):
                        c2=canon(n,[(p[i]-1,p[i]+i-1) for i in range(1,n)])
                        if c2!=c: slide.add(frozenset((c,c2)))
                    p[j]-=1
            return
        for q in range(1,n-k+1): p[k]=q; rec(k+1)
    rec(1)
    exch=set()
    for c,E in rep.items():
        for i,(a,b) in enumerate(E):
            rest=E[:i]+E[i+1:]
            adj=[[] for _ in range(n)]
            for x,y in rest: adj[x].append(y); adj[y].append(x)
            A={a}; st=[a]
            while st:
                v=st.pop()
                for u in adj[v]:
                    if u not in A: A.add(u); st.append(u)
            for u in A:
                for v in range(n):
                    if v not in A:
                        c2=canon(n,rest+[(u,v)])
                        if c2!=c: exch.add(frozenset((c,c2)))
    # leaf moves only
    print(n,'shapes',len(rep),'edge-exchange pairs',len(exch),'realised by one slide',len(exch&slide), 'slide pairs', len(slide), flush=True)
