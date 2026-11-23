# Referee: Lemma F exhaustively, and island statistics, n<=10. Own enumeration (itertools.product, own tree test).
import sys, itertools
from collections import Counter
from ref01 import is_tree, adj
def legal(p,k,s):
    n=len(p)+1; q=list(p); q[k-1]+=s
    return 1<=q[k-1]<=n-k and is_tree(q)
for n in range(3,int(sys.argv[1])+1):
    trees=[p for p in itertools.product(*[range(1,n-k+1) for k in range(1,n)]) if is_tree(p)]
    S=set(trees)
    # Lemma F
    viol=0; k1cases=0
    for p in trees:
        A=adj(p)
        for k in range(1,n):
            x,y=p[k-1],p[k-1]+k
            leaf=[v for v in (x,y) if len(A[v])==1]
            if not leaf: continue
            L=[s for s in (-1,1) if legal(p,k,s)]
            if k>=2:
                if L: viol+=1
            else:
                assert len(leaf)==1
                l=leaf[0]; s=1 if l==y else -1    # moving over l: {l-1,l}->{l,l+1} is +1 ; {l,l+1}->{l-1,l} is -1
                onrail = 1<=x+s<=n-1
                if L!=([s] if onrail else []): viol+=1
                k1cases+=1
    # components
    comp={}; comps=[]
    for p in trees:
        if p in comp: continue
        c=[p]; comp[p]=len(comps); st=[p]
        while st:
            q=st.pop()
            for k in range(1,n):
                for s in (-1,1):
                    r=q[:k-1]+(q[k-1]+s,)+q[k:]
                    if r in S and r not in comp: comp[r]=len(comps); c.append(r); st.append(r)
        comps.append(c)
    star=tuple([1]*(n-1)); isl=[c for c in comps if star not in c]
    size2=[c for c in isl if len(c)==2]
    only1=sum(1 for c in size2 if all(c[0][k]==c[1][k] for k in range(1,n-1)))
    maxmov=max([len([k for k in range(n-1) if len({p[k] for p in c})>1]) for c in isl],default=0)
    R=Counter()
    for c in isl:
        mv={k for k in range(1,n) if len({p[k-1] for p in c})>1}
        for p in c:
            A=adj(p)
            for k in range(1,n):
                if k in mv: continue
                x,y=p[k-1],p[k-1]+k; pend=len(A[x])==1 or len(A[y])==1
                R["F(a)" if (pend and k>=2) else "br1 pendant, flip off rail" if pend else "non-pendant"]+=1
    tot=sum(R.values()) or 1
    print("n=%d trees=%d comps=%d LemmaF violations=%d (k=1 leaf cases %d) | islands=%d placements=%d size2=%d (only br1 moves: %d) max movers=%d | frozen: %s"%(
        n,len(trees),len(comps),viol,k1cases,len(isl),sum(map(len,isl)),len(size2),only1,maxmov,
        ", ".join("%s %d (%.1f%%)"%(a,b,100*b/tot) for a,b in R.items())))
    sys.stdout.flush()
