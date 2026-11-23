# Referee: all graceful labelings (as placements = edge sets) of the double broom
# B(d1,d2): hubs u,w joined by path u-x-w, u has d1 leaves, w has d2 leaves.
# For each, test for a legal left slide straight from the definition.
import sys
def is_tree(p,n):
    par=list(range(n+1))
    def f(x):
        while par[x]!=x:
            par[x]=par[par[x]];x=par[x]
        return x
    for k in range(1,n):
        a,b=f(p[k]),f(p[k]+k)
        if a==b:return False
        par[a]=b
    return True
def labelings(d1,d2):
    n=d1+d2+3; out=set()
    for u in range(1,n+1):
        for w in range(1,n+1):
            if w==u:continue
            for x in range(1,n+1):
                if x in(u,w):continue
                l1,l2=abs(u-x),abs(x-w)
                if l1==l2:continue
                used={u,w,x}; p=[0]*n; p[l1]=min(u,x); p[l2]=min(x,w)
                def rec(k,c1,c2):
                    while k>=1 and p[k]:k-=1
                    if k==0:
                        if c1==d1 and c2==d2: out.add(tuple(p))
                        return
                    for h,isu in ((u,True),(w,False)):
                        if isu and c1==d1:continue
                        if (not isu) and c2==d2:continue
                        for l in (h-k,h+k):
                            if 1<=l<=n and l not in used:
                                used.add(l);p[k]=min(h,l)
                                rec(k-1,c1+isu,c2+(not isu))
                                used.discard(l);p[k]=0
                rec(n-1,0,0)
    return n,out
for d in range(0,int(sys.argv[1])+1):
    n,L=labelings(d+1,d)
    mins=0
    for p in L:
        p=list(p); assert is_tree(p,n)
        left=False
        for k in range(1,n):
            if p[k]>1:
                p[k]-=1
                if is_tree(p,n):left=True
                p[k]+=1
        if not left:mins+=1
    print("d=%d n=%d B(d+1,d): labelings=%d local minima=%d"%(d,n,len(L),mins),flush=True)
