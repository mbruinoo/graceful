# Is every growth placement reachable from the star by legal right slides (through arbitrary tree placements)?
# Also: from a growth placement, can one always make a legal LEFT slide (unless it is the star)?
import sys
from collections import deque
from growslide import growth_cfgs
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
for n in range(4,int(sys.argv[1])+1):
    star=tuple([0]+[1]*(n-1)); seen={star}; dq=deque([star])
    while dq:
        c=dq.popleft()
        for k in range(1,n-1):
            if c[k]<n-k:
                d=c[:k]+(c[k]+1,)+c[k+1:]
                if d not in seen and tree_ok(n,d): seen.add(d); dq.append(d)
    G=growth_cfgs(n); out=[g for g in G if g not in seen]
    noleft=0
    for g in G:
        if g==star: continue
        if not any(g[k]>1 and tree_ok(n,g[:k]+(g[k]-1,)+g[k+1:]) for k in range(1,n-1)): noleft+=1
    print(f"n={n}: growth placements={len(G)}  not right-reachable from star={len(out)}  with no legal left slide={noleft}", out[:2])
