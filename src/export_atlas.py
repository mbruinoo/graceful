# Export, for every tree shape on n<=10 vertices: a minimum-length right-slide path from the star,
# and one growth configuration.  Output: ../web/atlas.json
import json
from collections import deque
from growslide import canon, growth_cfgs  # noqa (growslide prints its table on import; harmless)
def tree_ok(n,p):
    par=list(range(n+1))
    def f(x):
        while par[x]!=x: x=par[x]
        return x
    for k in range(1,n):
        a,b=f(p[k]),f(p[k]+k)
        if a==b: return False
        par[a]=b
    return True
out={}
for n in range(4,11):
    star=tuple([0]+[1]*(n-1)); prev={star:None}; dq=deque([star]); best={}
    while dq:
        c=dq.popleft()
        s=canon(n,c)
        if s not in best: best[s]=c          # BFS order => minimum potential
        for k in range(1,n-1):
            if c[k]<n-k:
                d=c[:k]+(c[k]+1,)+c[k+1:]
                if d not in prev and tree_ok(n,d): prev[d]=(c,k); dq.append(d)
    grow={}
    for g in growth_cfgs(n):
        s=canon(n,g)
        if s not in grow or sum(g)<sum(grow[s]): grow[s]=g
    assert set(grow)==set(best)
    L=[]
    for s,c in best.items():
        path=[]; x=c
        while prev[x]: x,k=prev[x]; path.append(k)
        L.append({"p":list(c[1:]),"path":path[::-1],"g":list(grow[s][1:])})
    L.sort(key=lambda e:(len(e["path"]),e["p"]))
    out[n]=L; print(n,len(L),max(len(e["path"]) for e in L))
import os; os.makedirs("../web",exist_ok=True)
json.dump(out,open("../web/atlas.json","w"),separators=(",",":"))
