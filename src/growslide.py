# How do growth configurations sit inside the slide graph?
import sys, itertools
from collections import deque
def canon(n,p):
    adj=[[] for _ in range(n+1)]
    for k in range(1,n):
        adj[p[k]].append(p[k]+k); adj[p[k]+k].append(p[k])
    deg=[len(a) for a in adj]; layer=[v for v in range(1,n+1) if deg[v]<=1]; rem=n; gone=[0]*(n+1)
    while rem>2:
        nx=[]
        for v in layer:
            gone[v]=1; rem-=1
            for u in adj[v]:
                if not gone[u]:
                    deg[u]-=1
                    if deg[u]==1: nx.append(u)
        layer=nx
    def enc(v,pa): return "("+"".join(sorted(enc(u,v) for u in adj[v] if u!=pa))+")"
    if len(layer)==1: return enc(layer[0],0)
    return "".join(sorted([enc(layer[0],layer[1]),enc(layer[1],layer[0])]))
def is_growth(n,p):
    S={1,n}
    for k in range(n-2,0,-1):
        a,b=p[k],p[k]+k
        if (a in S)==(b in S): return False
        S|={a,b}
    return True
def growth_cfgs(n):
    res=[]
    p=[0]*n; p[n-1]=1
    def rec(k,S):
        if k==0: res.append(tuple(p)); return
        for q in range(1,n-k+1):
            if (q in S)!=(q+k in S):
                p[k]=q; rec(k-1,S|{q,q+k})
    rec(n-2,frozenset({1,n})); return res
for n in range(4,12):
    G=set(growth_cfgs(n)); star=tuple([0]+[1]*(n-1))
    shapes={canon(n,p) for p in G}
    def reach(dirs):
        seen={star}; dq=deque([star])
        while dq:
            c=dq.popleft()
            for k in range(1,n-1):
                for s in dirs:
                    q=c[k]+s
                    if 1<=q<=n-k:
                        d=c[:k]+(q,)+c[k+1:]
                        if d in G and d not in seen: seen.add(d); dq.append(d)
        return seen
    R=reach((1,)); B=reach((1,-1))
    print(f"n={n} growth={len(G)} shapes={len(shapes)} | growth-preserving RIGHT slides from star: {len(R)} cfgs, {len({canon(n,p) for p in R})} shapes | both directions: {len(B)} cfgs, {len({canon(n,p) for p in B})} shapes")
