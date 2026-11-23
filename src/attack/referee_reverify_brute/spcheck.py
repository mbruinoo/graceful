# sanity: each line of a spiders file is a spider (>=3 legs) with a distinct leg multiset; count = #partitions of n-1 into >=3 parts
import sys
from collections import defaultdict
def parts(n,mx):
    if n==0: yield (); return
    for p in range(min(n,mx),0,-1):
        for r in parts(n-p,p): yield (p,)+r
for fn in sys.argv[1:]:
    seen=set(); 
    for line in open(fn):
        t=list(map(int,line.split())); n=t[0]; e=t[1:]; assert len(e)==2*(n-1)
        adj=defaultdict(list)
        for i in range(0,len(e),2): adj[e[i]].append(e[i+1]); adj[e[i+1]].append(e[i])
        big=[v for v in adj if len(adj[v])>=3]; assert len(big)==1 and len(adj)==n
        c=big[0]; legs=[]
        for w in adj[c]:
            L=1; p=c; x=w
            while len(adj[x])==2: p,x=x,[y for y in adj[x] if y!=p][0]; L+=1
            assert len(adj[x])==1 or L==1 and len(adj[x])==1; legs.append(L)
        assert sum(legs)==n-1; seen.add((n,tuple(sorted(legs))))
    ns={k[0] for k in seen}
    exp=sum(1 for n in ns for p in parts(n-1,n-1) if len(p)>=3) if len(ns)==1 else None
    print(fn,len(seen),'distinct spiders; expected for single n:',exp)
