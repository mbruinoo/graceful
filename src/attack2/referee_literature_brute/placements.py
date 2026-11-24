# Enumerate all placements (one position per length) for n<=N; count tree placements and
# growth placements; compare growth (G) with Horton's property (H) on every tree placement.
import itertools, sys
def find(p,x):
    while p[x]!=x: p[x]=p[p[x]]; x=p[x]
    return x
N=int(sys.argv[1])
for n in range(3,N+1):
    trees=growth=disagree=0
    for pos in itertools.product(*[range(1,n-k+1) for k in range(1,n)]):
        E={k:(pos[k-1],pos[k-1]+k) for k in range(1,n)}
        par=list(range(n+1)); ok=True
        for k in range(1,n):
            a,b=map(lambda x:find(par,x),E[k])
            if a==b: ok=False;break
            par[a]=b
        if not ok: continue
        trees+=1
        # G: edges of length>=k connected (k from n-1 down), i.e. each new edge touches exactly one used vertex
        used=set(E[n-1]); g=True
        for k in range(n-2,0,-1):
            a,b=E[k]
            if (a in used)==(b in used): g=False;break
            used|={a,b}
        # H: every edge other than n-1 shares a vertex with a longer edge
        h=all(any(set(E[k])&set(E[j]) for j in range(k+1,n)) for k in range(1,n-1))
        growth+=g; disagree+=(g!=h)
    print(f"n={n}: tree placements {trees}, growth placements {growth}, G!=H on {disagree}")
