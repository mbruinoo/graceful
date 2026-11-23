# Double broom B(d1,d2): hubs u,w joined by a path u-x-w; u has d1 leaves, w has d2 leaves. n=d1+d2+3.
# Enumerate ALL graceful labelings (= all tree placements of this shape) and count those with no legal left slide.
from lib import *
import sys
def labelings(d1,d2):
    n=d1+d2+3; out=[]
    for u in range(1,n+1):
        for x in range(1,n+1):
            if x==u: continue
            for w in range(1,n+1):
                if w in (u,x): continue
                if d1==d2 and u>w: continue          # symmetry of the tree
                used={abs(u-x),abs(x-w)}
                if len(used)<2: continue
                rest=[l for l in range(1,n+1) if l not in (u,x,w)]
                def rec(i,cu,cw,used,E):
                    if i==len(rest):
                        out.append(E[:]); return
                    l=rest[i]
                    for hub,c in ((u,cu),(w,cw)):
                        d=abs(hub-l)
                        if d in used: continue
                        if hub==u and cu==d1: continue
                        if hub==w and cw==d2: continue
                        used.add(d); E.append((min(hub,l),max(hub,l)))
                        rec(i+1,cu+(hub==u),cw+(hub==w),used,E)
                        E.pop(); used.discard(d)
                rec(0,0,0,used,[(min(u,x),max(u,x)),(min(x,w),max(x,w))])
    res=[]
    for E in out:
        p=[0]*(n-1)
        for a,b in E: p[b-a-1]=a
        res.append(tuple(p))
    return res
def has_left(p):
    return any(p[k-1]>1 and is_tree(p[:k-1]+(p[k-1]-1,)+p[k:]) for k in range(1,len(p)+1))
N=int(sys.argv[1])
for n in range(4,N+1):
    row=[]
    for d2 in range(0,(n-3)//2+1):
        d1=n-3-d2; L=sorted(set(labelings(d1,d2))); assert all(is_tree(p) for p in L)
        m=sum(1 for p in L if not has_left(p))
        row.append("B(%d,%d): %d placements, %d local minima%s"%(d1,d2,len(L),m," <== NONE" if m==0 else ""))
    print("n=%d"%n); print("   "+"\n   ".join(row))
