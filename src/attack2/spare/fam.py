# fam.py -- write test trees, one per line: "#name n root a b a b ..."
import sys
def out(name,n,root,edges): print("#%s %d %d "%(name,n,root)+" ".join("%d %d"%e for e in edges))
def Lfam(l,hs):   # v=0, c=1, g_i=2.., leaves
    e=[(0,1)]; nx=2; gs=[]
    for h in hs: e.append((1,nx)); gs.append(nx); nx+=1
    for g,h in zip(gs,hs):
        for _ in range(h): e.append((g,nx)); nx+=1
    for _ in range(l): e.append((0,nx)); nx+=1
    return nx,e
def hub(ks):
    r=len(ks); e=[]; nx=r+1
    for i,k in enumerate(ks):
        e.append((0,i+1))
        for _ in range(k): e.append((i+1,nx)); nx+=1
    return nx,e
def isprime(m): return m>1 and all(m%d for d in range(2,int(m**.5)+1))
w=sys.argv[1]
if w=="L":
    out("L(3;8,9)",*(lambda n,e:(n,0,e))(*Lfam(3,[8,9])))
    for l in range(1,9): n,e=Lfam(l,[2*l+2,2*l+3]); out("L(%d;%d,%d)"%(l,2*l+2,2*l+3),n,0,e)
elif w=="DH":     # all (p,q), p<=q, p>=1, m=p+q+2 prime, m<=M
    M=int(sys.argv[2])
    for m in range(5,M+1):
        if not isprime(m): continue
        for p in range(1,(m-2)//2+1): n,e=hub([p,m-2-p]); out("DH(%d,%d)m=%d"%(p,m-2-p,m),n,0,e)
elif w=="H3":     # odd m in [11,M] that are non-anchors by rule H3
    M=int(sys.argv[2])
    for m in range(11,M+1,2):
        if m%3 and m%5 and m%4!=3: n,e=hub([1,1,m-5]); out("H(1,1,%d)m=%d"%(m-5,m),n,0,e)
elif w=="P":      # three middle vertices of P_n
    M=int(sys.argv[2])
    for n in range(5,M+1):
        e=[(i,i+1) for i in range(n-1)]
        for r in sorted(set([(n-1)//2-1,(n-1)//2,n//2,n//2+1])):
            if 0<=r<=(n-1)//2+1: out("P%d@%d"%(n,r),n,r,e)   # r 0-based position; includes floor/ceil middle and neighbours
elif w=="S":      # a leaf of S(L,L,L)
    M=int(sys.argv[2])
    for L in range(1,M+1):
        e=[]; nx=1; leaf=None
        for leg in range(3):
            prev=0
            for _ in range(L): e.append((prev,nx)); prev=nx; nx+=1
            leaf=prev
        out("S(%d,%d,%d)leaf"%(L,L,L),nx,leaf,e)
if w=="Pall":   # every vertex (up to reflection) of P_n, lo <= n <= hi;  root = distance from the nearer end
    for n in range(int(sys.argv[2]),int(sys.argv[3])+1):
        e=[(i,i+1) for i in range(n-1)]
        for r in range((n+1)//2): out("P%d@%d"%(n,r),n,r,e)
if w=="P33":    # arms (b,c), b <= c, both = 3 mod 4, both >= 15, n = b+c+1 <= maxn
    M=int(sys.argv[2])
    for b in range(15,M,4):
        for c in range(b,M-b,4):
            n=b+c+1; out("P%d@%d(arms%d,%d)"%(n,b,b,c),n,b,[(i,i+1) for i in range(n-1)])
if w=="RAND":   # RAND n trees roots seed : uniform random labelled trees (Pruefer), `roots` random roots each
    import random
    n=int(sys.argv[2]); T=int(sys.argv[3]); RR=int(sys.argv[4]); random.seed(int(sys.argv[5]))
    for t in range(T):
        pr=[random.randrange(n) for _ in range(n-2)]; deg=[1]*n
        for x in pr: deg[x]+=1
        e=[]; import heapq; leaves=[i for i in range(n) if deg[i]==1]; heapq.heapify(leaves)
        for x in pr:
            l=heapq.heappop(leaves); e.append((l,x)); deg[x]-=1
            if deg[x]==1: heapq.heappush(leaves,x)
        e.append((heapq.heappop(leaves),heapq.heappop(leaves)))
        for r in random.sample(range(n),RR): out("R%d_%d@%d"%(n,t,r),n,r,e)
