# The fattening step for TREES (not only spiders), checked by brute force.
# Let S and T be trees with growth placements anchored at their roots (root label 0, labels 0..m and 0..n; edge lengths
# strictly decrease away from the root).  Put k = 2m+1 and, for x in [-m, m], delta(x) = -x-m if x <= 0 else m+1-x.
# Build a new labelled tree: the root 0; S unchanged; and for every non-root vertex v of T (label l, depth j >= 1) and
# every i in [-m, m] a copy with label k*l + delta^(j-1)(i), joined to the copy of its parent with the same i
# (copies of the root's children are joined to the root).  The result is S with 2m+1 copies of T glued at the root.
# Claim: it is again a growth placement anchored at the root.
import sys, itertools
from growslide import growth_cfgs
def rooted(n,p):
    # placement -> dict label0 -> parent label0 (root = label 1 -> 0), using 0-based labels
    adj={i:[] for i in range(n)}
    for k in range(1,n): a,b=p[k]-1,p[k]+k-1; adj[a].append(b); adj[b].append(a)
    par={0:None}; depth={0:0}; st=[0]
    while st:
        u=st.pop()
        for v in adj[u]:
            if v not in par: par[v]=u; depth[v]=depth[u]+1; st.append(v)
    return par,depth
def is_growth(par):
    # labels are keys; check differences are 1..M once each and decrease away from root
    M=len(par)-1
    if sorted(par)!=list(range(M+1)): return False
    w={v:abs(v-par[v]) for v in par if par[v] is not None}
    if sorted(w.values())!=list(range(1,M+1)): return False
    return all(par[par[v]] is None or w[v]<w[par[v]] for v in w)
def fatten(S,T):
    parS,_=S; parT,depT=T; m=len(parS)-1; k=2*m+1
    delta=lambda x: -x-m if x<=0 else m+1-x
    def dpow(x,j):
        for _ in range(j): x=delta(x)
        return x
    par=dict(parS)
    for v in parT:
        if parT[v] is None: continue
        for i in range(-m,m+1):
            lab=k*v+dpow(i,depT[v]-1); pv=parT[v]
            par[lab]= 0 if parT[pv] is None else k*pv+dpow(i,depT[pv]-1)
    return par
tot=bad=0
N=int(sys.argv[1]) if len(sys.argv)>1 else 6
P={n:[rooted(n,p) for p in growth_cfgs(n)] for n in range(2,N+1)}
P[1]=[({0:None},{0:0})]
for a in range(1,N+1):
    for b in range(2,N+1):
        for S in P[a]:
            for T in P[b]:
                tot+=1
                if not is_growth(fatten(S,T)): bad+=1
print(f"pairs of anchored growth placements with at most {N} vertices each: {tot}; composites that are not growth placements: {bad}")
