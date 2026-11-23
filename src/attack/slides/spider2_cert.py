# Machine check of the WRITTEN PROOF (PROOFS.txt, Theorem S2): for every slide of the schedule,
# the proof names a path in the current tree from the new left foot to the new right foot that
# passes through the sliding bracket.  By Lemma 1 (README) such a path certifies legality.
# Here each named path is checked edge by edge, and independently the placement is re-checked
# to be a tree after every slide.
from lib import *
import sys
def check(a,b):
    n=2*a+1+b; p=[1]*(n-1); nsl=0
    def E(): return {frozenset(e) for e in edges(p)}
    def slide(k,path):
        nonlocal nsl
        x,y=p[k-1],p[k-1]+k; es=E()
        assert path[0]==x+1 and path[-1]==y+1 and len(set(path))==len(path),(a,b,k,path)
        pe=[frozenset(path[i:i+2]) for i in range(len(path)-1)]
        assert all(e in es for e in pe),(a,b,k,path,p)
        assert frozenset((x,y)) in pe
        p[k-1]+=1; assert p[k-1]<=n-k and is_tree(tuple(p)); nsl+=1
    slide(1,[2,1,3]); slide(2,[2,3,1,4])
    for r in range(1,a):
        R=2*r+2; J=2*r+2-a
        if 2*r<a+1:                                  # step (a)
            slide(1,[2*r+1,2*r,2,R] if r>1 else [3,2,4])
        # step (b): j=r+1
        slide(2*r+1,[2,R,1,R+1])
        if r<=a-2: slide(2*r+1,[3,R,2,R+1,1,R+2])
        for j in range(r,1,-1):
            q=R+1-2*j
            if j>=J: slide(2*j-1,[q+1,2,R,q,R+2,1,R+1])
            if j>J:  slide(2*j-1,[q+2,R,2,q+1,R+1,1,R+2])
        if 2*r<a:                                    # step (c)
            slide(1,[R,R-1,R+2,1,R+1])
        if 2*r+2<=n-2:                               # step (d)
            if 2*r<a: slide(R,[2,R,R+1,1,R+2])
            elif r==a-1: slide(R,[2,R+1,1,R+2])
            else: slide(R,[2,2*a-2*r,R+1,1,R+2])
        # invariant Sigma_r
        assert p[0]==min(a+1,2*r+2)
        for j in range(2,r+2): assert p[2*j-2]==min(a+2-j,2*r+5-2*j)
        for i in range(1,r+2):
            if 2*i<=n-2: assert p[2*i-1]==2
        for k in range(2*r+3,n): assert p[k-1]==1
    for k in range(2*a+1,n-1): slide(k,[2,k+1,1,k+2])
    from spider2_route import target,is_spider2
    assert tuple(p)==target(a,b) and (a+b<3 or is_spider2(tuple(p),a,b))
    assert nsl==sum(p)-(n-1)
A,B=int(sys.argv[1]),int(sys.argv[2])
for a in range(2,A+1):
    for b in range(0,B+1): check(a,b)
print("all path certificates verified for 2<=a<=%d, 0<=b<=%d"%(A,B))
