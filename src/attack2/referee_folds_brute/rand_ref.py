# referee: uniform random labelled trees via Pruefer sequences; args n count seed
import sys, random, heapq
n,cnt,seed=map(int,sys.argv[1:4]); rng=random.Random(seed)
for _ in range(cnt):
    p=[rng.randrange(n) for _ in range(n-2)]; deg=[1]*n
    for x in p: deg[x]+=1
    h=[i for i in range(n) if deg[i]==1]; heapq.heapify(h); E=[]
    for x in p:
        l=heapq.heappop(h); E.append((l,x)); deg[x]-=1
        if deg[x]==1: heapq.heappush(h,x)
    u=heapq.heappop(h); v=heapq.heappop(h); E.append((u,v))
    print(' '.join(f"{a} {b}" for a,b in E))
