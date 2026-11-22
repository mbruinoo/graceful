# emit structured / random trees on exactly n vertices: "name" selects family
import sys, random
def emit(E): print(' '.join(f"{u} {v}" for u,v in E))
fam=sys.argv[1]; n=int(sys.argv[2]); cnt=int(sys.argv[3]) if len(sys.argv)>3 else 1
random.seed(1)
for _ in range(cnt):
    if fam=='random':   # uniform random labelled tree via random attachment of Prufer
        pr=[random.randrange(n) for _ in range(n-2)]
        deg=[1]*n
        for x in pr: deg[x]+=1
        E=[]
        import heapq
        leaves=[i for i in range(n) if deg[i]==1]; heapq.heapify(leaves)
        for x in pr:
            l=heapq.heappop(leaves); E.append((l,x)); deg[x]-=1
            if deg[x]==1: heapq.heappush(leaves,x)
        E.append((heapq.heappop(leaves),heapq.heappop(leaves))); emit(E)
    elif fam=='path': emit([(i,i+1) for i in range(n-1)])
    elif fam=='kary':  # complete k-ary tree truncated to n vertices, k = cnt arg reused
        k=int(sys.argv[4]); emit([((i-1)//k,i) for i in range(1,n)])
    elif fam=='spider': # legs of equal length L = argv[4]; n = 1 + legs*L
        L=int(sys.argv[4]); E=[]; v=1
        for leg in range((n-1)//L):
            prev=0
            for j in range(L): E.append((prev,v)); prev=v; v+=1
        emit(E)
