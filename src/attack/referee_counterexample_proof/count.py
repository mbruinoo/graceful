# Enumerate ALL growth placements on n vertices from the definition (longest bracket first, exactly one foot
# on a used label), group by tree shape (AHU canonical form at the centre).  Reports:
#  total count; min count over non-caterpillars; count for family A (centre c; hub h with m leaves; two legs of length 2);
#  and checks the Lemma-6 step: adding bracket {1,n+1} gives a growth placement with the same label-1 vertex + a leaf.
import sys
from collections import defaultdict
def canon(n,E):
    adj=defaultdict(list)
    for a,b in E: adj[a].append(b); adj[b].append(a)
    deg={v:len(adj[v]) for v in adj}; layer=[v for v in adj if deg[v]==1]; rem=n; gone=set()
    while rem>2:
        nx=[]
        for x in layer:
            gone.add(x); rem-=1
            for y in adj[x]:
                if y not in gone:
                    deg[y]-=1
                    if deg[y]==1: nx.append(y)
        layer=nx
    def enc(v,p): return "("+"".join(sorted(enc(u,v) for u in adj[v] if u!=p))+")"
    if len(layer)==1: return enc(layer[0],None)
    a,b=layer; return min(enc(a,b)+enc(b,a), enc(b,a)+enc(a,b))
def is_cat(n,E):
    adj=defaultdict(list)
    for a,b in E: adj[a].append(b); adj[b].append(a)
    inner=[v for v in adj if len(adj[v])>1]
    return all(sum(1 for u in adj[v] if len(adj[u])>1)<=2 for v in inner)
def famA(n):
    m=n-6; E=[(0,1),(0,2),(2,3),(0,4),(4,5)]+[(1,6+i) for i in range(m)]; return canon(n,E)
def growth_ok(E,n):
    by={abs(a-b):(a,b) for a,b in E}
    if sorted(by)!=list(range(1,n)): return False
    used=set(by[n-1])
    for k in range(n-2,0,-1):
        a,b=by[k]
        if (a in used)==(b in used): return False
        used|={a,b}
    return len(used)==n
for n in map(int,sys.argv[1:]):
    cnt=defaultdict(int); cat={}; tot=0; l6bad=0
    E=[(1,n)]; used=[False]*(n+2); used[1]=used[n]=True
    def rec(k):
        global tot,l6bad
        if k==0:
            tot+=1; c=canon(n,E); cnt[c]+=1
            if c not in cat: cat[c]=is_cat(n,E)
            if n<=10:
                E2=E+[(1,n+1)]
                if not growth_ok(E2,n+1): l6bad+=1
            return
        for p in range(1,n-k+1):
            if used[p]!=used[p+k]:
                new=p if not used[p] else p+k
                used[new]=True; E.append((p,p+k)); rec(k-1); E.pop(); used[new]=False
    rec(n-2)
    nc=[v for c,v in cnt.items() if not cat[c]]
    print("n=%d growth placements=%d shapes with one=%d  non-caterpillar shapes=%d min count over them=%s  family A count=%s  Lemma6-step failures=%s"%(n,tot,len(cnt),len(nc),min(nc) if nc else None,cnt.get(famA(n)) if n>=7 else None,l6bad if n<=10 else "n/a"),flush=True)
