# Claim 2: Theorem M construction, checked from README section 1 on every rooted tree
# with <= N vertices and no leaf at the root.
import sys
from lib import check_growth
from functools import lru_cache
from itertools import combinations_with_replacement
@lru_cache(None)
def rooted(n):
    """all rooted trees on n vertices as nested sorted tuples"""
    if n==1: return [()]
    out=[]
    def parts(rem,mx):
        if rem==0: yield []; return
        for s in range(min(rem,mx),0,-1):
            for p in parts(rem-s,s): yield [s]+p
    for p in parts(n-1,n-1):
        # choose multiset of subtrees for each size group
        from collections import Counter
        groups=sorted(Counter(p).items())
        def rec(i):
            if i==len(groups): yield (); return
            s,c=groups[i]
            for combo in combinations_with_replacement(range(len(rooted(s))),c):
                for rest in rec(i+1): yield tuple(rooted(s)[j] for j in combo)+rest
        for t in rec(0): out.append(tuple(sorted(t)))
    return sorted(set(out))
def build(t):
    """-> children lists, depth"""
    ch=[[]];dep=[0]
    def rec(node,sub):
        for s in sub:
            i=len(ch); ch.append([]); dep.append(dep[node]+1); ch[node].append(i); rec(i,s)
    rec(0,t); return ch,dep
def test(t):
    ch,dep=build(t); nv=len(ch); mp=nv-1; r=len(ch[0]); D=max(dep)
    assert D>=2 and r>=1
    q=[None]*(D+2)
    for j in range(2,D+1):
        k=max(len(ch[u]) for u in range(nv) if dep[u]==j-1)
        q[j]=k if k%2 else k+1
    Q=1
    for j in range(2,D+1): Q*=q[j]
    g=[None]*(D+2)
    for j in range(1,D+1):
        g[j]=1
        for i in range(j+1,D+1): g[j]*=q[i]
    M=2**(D-1)*((2*r+1)*Q-2)
    S=[None]*nv
    for i,c in enumerate(ch[0],1): S[c]=(2*i+1)*Q-2
    order=sorted(range(1,nv),key=lambda u:dep[u])
    for u in order:
        k=len(ch[u])
        if not k: continue
        j=dep[u]+1; h=k//2
        taus=[tt for tt in range(-h,h+1) if tt!=0 or k%2]
        assert len(taus)==k
        for c,tt in zip(ch[u],taus): S[c]=S[u]+2*g[j]*tt
    f=[0]+[2**(D-dep[u])*S[u] for u in range(1,nv)]
    if M<mp: return False,M,"M<m'"
    # gapped-labelling conditions (Lemma 0 form)
    labs=f[1:]
    if len(set(f))!=nv or min(labs)<1 or max(labs)>M: return False,M,"labels"
    edges=[(u,c) for u in range(nv) for c in ch[u]]
    if sorted(abs(f[a]-f[b]) for a,b in edges)!=sorted(labs): return False,M,"lengths!=labels"
    # add leaves and check the definition directly
    unused=[x for x in range(1,M+1) if x not in set(f)]
    lab=f+unused; E=edges+[(0,nv+i) for i in range(len(unused))]
    ok=check_growth(M+1,0,E,lab)
    return ok,M,len(unused)
N=int(sys.argv[1]); tot=0; fails=0; maxleaves=0
for n in range(3,N+1):
    c=0
    for t in rooted(n):
        if any(s==() for s in t): continue   # leaf at root
        c+=1; ok,M,info=test(t)
        if not ok: fails+=1; print("FAIL",t,M,info)
        else: maxleaves=max(maxleaves,info)
    tot+=c; print("n=%d rooted trees (all %d) with no root leaf: %d, cumulative %d, fails %d, max leaves added %d"%(n,len(rooted(n)),c,tot,fails,maxleaves)); sys.stdout.flush()
