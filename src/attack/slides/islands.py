# Islands (components of the unit-slide graph other than the star's) for small n: what moves, what is frozen.
# Reads islands_<n>.txt written by `./sl n dump`.  Everything is re-derived from the definitions.
from lib import *
from collections import Counter
import sys
def pieces(p,k):
    n=len(p)+1; adj={v:[] for v in range(1,n+1)}
    for j,(a,b) in enumerate(edges(p),1):
        if j!=k: adj[a].append(b); adj[b].append(a)
    a=p[k-1]; seen={a}; st=[a]
    while st:
        v=st.pop()
        for u in adj[v]:
            if u not in seen: seen.add(u); st.append(u)
    return seen
def degs(p):
    n=len(p)+1; d=[0]*(n+2)
    for a,b in edges(p): d[a]+=1; d[b]+=1
    return d
for n in range(7,int(sys.argv[1])+1):
    isl=[]; 
    for line in open("islands_%d.txt"%n):
        if line[0]=='I': isl.append([])
        else: isl[-1].append(tuple(int(x) for x in line.split()))
    # sanity: every island is closed under legal unit slides
    for I in isl:
        S=set(I)
        for p in I:
            for k in range(1,n):
                for s in (-1,1):
                    q=p[:k-1]+(p[k-1]+s,)+p[k:]
                    if 1<=q[k-1]<=n-k and is_tree(q): assert q in S
    movers=Counter(); reasons=Counter(); sizes=Counter(); nshapes=Counter(); product=Counter(); maxmover=Counter()
    for I in isl:
        mv=sorted({k for k in range(1,n) if len({p[k-1] for p in I})>1})
        movers[len(mv)]+=1; sizes[len(I)]+=1; nshapes[len({canon(p) for p in I})]+=1; maxmover[max(mv)]+=1
        box=1
        for k in mv: box*=len({p[k-1] for p in I})
        product["box" if box==len(I) else "not a box"]+=1
        for p in I:
            d=degs(p)
            for k in range(1,n):
                if k in mv: continue
                a,b=p[k-1],p[k-1]+k
                if k>=2 and (d[a]==1 or d[b]==1): reasons["leaf foot, length>=2 (Lemma F)"]+=1
                elif k==1 and (d[a]==1 or d[b]==1): reasons["bracket 1 pendant but its one flip is off the rail"]+=1
                else: reasons["not pendant: both new positions keep both feet in one piece or are off the rail"]+=1
    print("n=%d islands=%d placements in islands=%d"%(n,len(isl),sum(len(I) for I in isl)))
    print("   island sizes:",dict(sorted(sizes.items())))
    print("   number of brackets that ever move in an island:",dict(sorted(movers.items())))
    print("   longest bracket that moves:",dict(sorted(maxmover.items())))
    print("   tree shapes per island:",dict(sorted(nshapes.items())))
    print("   island = full box of its movers' ranges?",dict(product))
    tot=sum(reasons.values())
    for r,c in reasons.most_common(): print("   frozen bracket instances: %-90s %d (%.1f%%)"%(r,c,100*c/tot))
