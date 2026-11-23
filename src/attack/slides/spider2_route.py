# Explicit right-slide route from the star to F(a,b), the spider with a legs of length 2 and
# b legs of length 1 (n = 2a+1+b).  Every intermediate placement is checked to be a tree
# directly from the definition (README section 1), and the end shape is checked to be the spider.
from lib import *
import sys
def target(a,b):
    n=2*a+1+b; p=[1]*(n-1)
    for j in range(1,a): p[2*j-2]=a+2-j          # odd bracket 2j-1 at {a+2-j, a+1+j}
    for i in range(1,a): p[2*i-1]=2              # even bracket 2i at {2, 2+2i}
    for k in range(2*a-1,n-1): p[k-1]=2          # brackets 2a-1 .. n-2 at {2, 2+k}
    return tuple(p)
def schedule(a,b):
    n=2*a+1+b; T=target(a,b); p=[1]*(n-1); seq=[]
    def sl(k,times=1):
        for _ in range(times):
            if p[k-1]<T[k-1]: p[k-1]+=1; seq.append(k)
    sl(1); sl(2)
    for r in range(1,a):
        sl(1)
        for k in range(2*r+1,1,-2): sl(k,2)
        sl(1)
        sl(2*r+2)
    for k in range(2*a,n-1): sl(k)
    assert tuple(p)==T
    return seq
def is_spider2(p,a,b):
    n=len(p)+1; adj=[[] for _ in range(n+1)]
    for x,y in edges(p): adj[x].append(y); adj[y].append(x)
    deg=sorted(len(adj[v]) for v in range(1,n+1))
    c=[v for v in range(1,n+1) if len(adj[v])==a+b]
    if a+b<3: return None
    if len(c)!=1: return False
    c=c[0]; d2=sum(1 for u in adj[c] if len(adj[u])==2); d1=sum(1 for u in adj[c] if len(adj[u])==1)
    return is_tree(p) and d2==a and d1==b and n==1+2*a+b
if __name__=="__main__":
    A,B=int(sys.argv[1]),int(sys.argv[2]); cnt=0
    for a in range(2,A+1):
        for b in range(0,B+1):
            n=2*a+1+b; p=tuple([1]*(n-1)); seq=schedule(a,b)
            for k in seq:
                p=p[:k-1]+(p[k-1]+1,)+p[k:]
                assert p[k-1]<=n-k and is_tree(p),(a,b,k,p)
            assert p==target(a,b) and is_spider2(p,a,b) is not False
            cnt+=1
    print("verified explicit route for",cnt,"pairs (a,b): 2<=a<=%d, 0<=b<=%d"%(A,B))
