from lib import *
import sys
def spider_canon(legs):
    # build a placement-free canon via adjacency
    n=1+sum(legs); adj=[[] for _ in range(n+1)]; v=2
    for L in legs:
        prev=1
        for _ in range(L):
            adj[prev].append(v); adj[v].append(prev); prev=v; v+=1
    def enc(u,pa): return "("+"".join(sorted(enc(w,u) for w in adj[u] if w!=pa))+")"
    return min(enc(u,0) for u in range(1,n+1))
def reach_with_parent(n,S):
    star=tuple([1]*(n-1)); par={star:None}; q=[star]
    for p in q:
        for k in range(1,n):
            if p[k-1]<n-k:
                r=p[:k-1]+(p[k-1]+1,)+p[k:]
                if r in S and r not in par: par[r]=(p,k); q.append(r)
    return par
legs=[int(x) for x in sys.argv[1:]]; n=1+sum(legs)
S=set(all_tree_placements(n)); par=reach_with_parent(n,S); c=spider_canon(legs)
hits=[p for p in par if canon(p)==c]
print(len(hits),"reachable placements;", sum(1 for p in S if canon(p)==c),"total")
for p in sorted(hits):
    route=[]; x=p
    while par[x]: x,k=par[x]; route.append(k)
    print(p,"growth" if is_growth(p) else "", "edges",edges(p),"route",route[::-1])
