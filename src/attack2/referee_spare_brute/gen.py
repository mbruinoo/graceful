# referee generators (own code). usage: gen.py FAMILY args
import sys
def out(name,n,root,e): print(name,n,root," ".join("%d %d"%x for x in e))
def Ltree(l,h1,h2):
    # v=0 with l leaves and child c; c has children g1,g2 with h1,h2 leaves
    e=[(0,1),(1,2),(1,3)]; nx=4
    for g,h in ((2,h1),(3,h2)):
        for _ in range(h): e.append((g,nx)); nx+=1
    for _ in range(l): e.append((0,nx)); nx+=1
    return nx,e
def hubs(ks):
    e=[]; nx=1; hs=[]
    for k in ks: e.append((0,nx)); hs.append(nx); nx+=1
    for h,k in zip(hs,ks):
        for _ in range(k): e.append((h,nx)); nx+=1
    return nx,e
def prime(m): return m>1 and all(m%d for d in range(2,int(m**.5)+1))
def path(b,c):  # root 0, arm A = 1..b, arm B = b+1..b+c (tip = last vertex)
    e=[]; p=0
    for i in range(1,b+1): e.append((p,i)); p=i
    p=0
    for i in range(b+1,b+c+1): e.append((p,i)); p=i
    return b+c+1,e
def spider3(L,t): # S(L,L,L) rooted at distance t on leg 0
    e=[]; nx=1; r=0
    for leg in range(3):
        p=0
        for d in range(1,L+1):
            e.append((p,nx))
            if leg==0 and d==t: r=nx
            p=nx; nx+=1
    return nx,r,e
if __name__=="__main__":
    w=sys.argv[1]; a=list(map(int,sys.argv[2:]))
    if w=="L":
        n,e=Ltree(3,8,9); out("L(3;8,9)",n,0,e)
        for l in range(1,a[0]+1): n,e=Ltree(l,2*l+2,2*l+3); out("L(%d;%d,%d)"%(l,2*l+2,2*l+3),n,0,e)
    if w=="DH":
        for m in range(5,a[0]+1):
            if prime(m):
                for p in range(1,m-2):
                    q=m-2-p
                    if p<=q: n,e=hubs([p,q]); out("DH(%d,%d)"%(p,q),n,0,e)
    if w=="H3":
        for m in range(a[0],a[1]+1,2):
            if m%3 and m%5 and m%4!=3: n,e=hubs([1,1,m-5]); out("H(1,1,%d)m=%d"%(m-5,m),n,0,e)
    if w=="PATH":   # all (b,c), b<=c, lo<=n<=hi
        for n in range(a[0],a[1]+1):
            for b in range(0,(n-1)//2+1): nn,e=path(b,n-1-b); out("P(%d,%d)"%(b,n-1-b),nn,0,e)
    if w=="P33":
        lo,hi=a
        for b in range(lo,hi,4):
            for c in range(b,hi-b,4):
                if b+c+1<=hi: nn,e=path(b,c); out("P(%d,%d)"%(b,c),nn,0,e)
    if w=="PIECE": nn,e=path(a[0],a[1]); out("piece(%d,%d)"%(a[0],a[1]),nn,0,e)
    if w=="LLL":
        for L in range(a[0],a[1]+1):
            for t in (range(0,L+1) if len(a)<3 else [L]):
                n,r,e=spider3(L,t); out("S(%d^3)@%d"%(L,t),n,r,e)
    if w=="D2":   # partitions of n-1 into parts a_j+1 ; flag a[2]=1: only those violating (C)
        def parts(t,m):
            if t==0: yield (); return
            for x in range(min(t,m),0,-1):
                for r in parts(t-x,x): yield (x,)+r
        tot=0; okC=0
        for n in range(a[0],a[1]+1):
            for p in parts(n-1,n-1):
                ks=[x-1 for x in p]; tot+=1
                C = sum((j-1)*ks[j] for j in range(2,len(ks)))<=ks[0]; okC+=C
                if len(a)>2 and a[2]==1 and C: continue
                nn,e=hubs(ks); out("D2(%s)"%",".join(map(str,ks)),nn,0,e)
        print("D2 total",tot,"satisfy C",okC,file=sys.stderr)
    if w=="ALL":  # all free trees on n vertices, every root up to rooted isomorphism (a[1]=1) or all roots
        import networkx as nx
        n=a[0]
        def canon(adj,v,p): return "("+"".join(sorted(canon(adj,w,v) for w in adj[v] if w!=p))+")"
        for i,T in enumerate(nx.nonisomorphic_trees(n)):
            e=list(T.edges()); adj=[list(T[v]) for v in range(n)]; seen=set()
            for r in range(n):
                if len(a)>1 and a[1]==1:
                    c=canon(adj,r,-1)
                    if c in seen: continue
                    seen.add(c)
                out("T%d_%d@%d"%(n,i,r),n,r,e)
