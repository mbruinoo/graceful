# Referee: all tree placements drawing the double broom B(d+1,d), by backtracking over bracket LENGTHS
# (longest first), a different search from the claimant's.  Then test each for a legal left slide.
import sys
from ref01 import is_tree, adj
def brooms(d1,d2):
    n=d1+d2+3; out=set()
    for u in range(1,n+1):
        for w in range(1,n+1):
            if w==u: continue
            for x in range(1,n+1):
                if x in (u,w): continue
                ku,kw=abs(u-x),abs(w-x)
                if ku==kw: continue
                p=[0]*(n-1); used={u,w,x}
                def rec(k,cu,cw):
                    if k==0:
                        if cu==d1 and cw==d2: out.add(tuple(p))
                        return
                    if k==ku: p[k-1]=min(u,x); rec(k-1,cu,cw); return
                    if k==kw: p[k-1]=min(w,x); rec(k-1,cu,cw); return
                    for hub,isu in ((u,True),(w,False)):
                        if isu and cu==d1: continue
                        if (not isu) and cw==d2: continue
                        for l in (hub-k,hub+k):
                            if 1<=l<=n and l not in used:
                                used.add(l); p[k-1]=min(hub,l)
                                rec(k-1,cu+isu,cw+(not isu))
                                used.discard(l)
                rec(n-1,0,0)
    return out
def is_broom(p,d1,d2):
    A=adj(p); n=len(p)+1
    hubs=[v for v in A if sum(1 for t in A[v] if len(A[t])==1)>0 or False]
    # check structure directly: exists path u-x-w with deg x=2, u has d1 leaf nbrs + x, w has d2 leaf nbrs + x
    for x in A:
        if len(A[x])!=2: continue
        u,w=sorted(A[x])
        for u,w in ((u,w),(w,u)):
            if len(A[u])==d1+1 and len(A[w])==d2+1 and all(len(A[t])==1 for t in A[u]-{x}) and all(len(A[t])==1 for t in A[w]-{x}): return True
    return False
def has_left(p):
    for k in range(1,len(p)+1):
        if p[k-1]>1:
            q=list(p); q[k-1]-=1
            if is_tree(q): return True
    return False
for d in range(0,int(sys.argv[1])+1):
    L=brooms(d+1,d)
    assert all(is_tree(p) and is_broom(p,d+1,d) for p in L)
    mins=[p for p in L if not has_left(p)]
    print("d=%d n=%d: B(d+1,d) placements=%d local minima=%d %s"%(d,2*d+4,len(L),len(mins),mins if mins else "")); sys.stdout.flush()
