# Referee: for each n, which unrooted tree shapes have some (root=label 0, heap order) class with exactly one valid sign vector?
import sys
from collections import defaultdict
sys.setrecursionlimit(10000)
def canon(adj,n):
    # centre-based AHU
    deg=[len(a) for a in adj]; leaves=[v for v in range(n) if deg[v]<=1]; rem=n
    while rem>2:
        new=[]
        for v in leaves:
            rem-=1
            for u in adj[v]:
                deg[u]-=1
                if deg[u]==1:new.append(u)
            deg[v]=0
        leaves=new
    def enc(v,p): return "("+"".join(sorted(enc(u,v) for u in adj[v] if u!=p))+")"
    return min(enc(c,-1) for c in leaves) if len(leaves)==1 else min(enc(leaves[0],leaves[1])+enc(leaves[1],leaves[0]),enc(leaves[1],leaves[0])+enc(leaves[0],leaves[1]))
def run(n):
    m=n-1; used=[False]*n; used[0]=True; inlen=[0]*n; par=[0]*(m+1); edges=[]
    classes=defaultdict(list)
    def rec(k):
        if k==0:
            classes[tuple(par)].append(list(edges)); return
        for p in range(0,m-k+1):
            a,b=p,p+k
            if used[a]==used[b]: continue
            u,v=(a,b) if used[a] else (b,a)
            used[v]=True; inlen[v]=k; par[k]=inlen[u]; edges.append((u,v))
            rec(k-1)
            edges.pop(); used[v]=False
    rec(m)
    uniq=set(); allshapes=set()
    for key,lst in classes.items():
        for E in lst[:1]:
            adj=[[] for _ in range(n)]
            for u,v in E: adj[u].append(v); adj[v].append(u)
            c=canon(adj,n); allshapes.add(c)
            if len(lst)==1: uniq.add(c)
    print(n,"placements",sum(len(l) for l in classes.values()),"shapes with growth placement",len(allshapes),"shapes with a unique-sign class",len(uniq))
for n in range(4,int(sys.argv[1])+1): run(n)
