import random,sys
random.seed(int(sys.argv[3])); n=int(sys.argv[1])
for t in range(int(sys.argv[2])):
    # random labelled tree: random attachment after random Pruefer decode
    pr=[random.randrange(n) for _ in range(n-2)]; deg=[1]*n
    for x in pr: deg[x]+=1
    e=[]
    for x in pr:
        l=min(i for i in range(n) if deg[i]==1); e.append((l,x)); deg[l]-=1; deg[x]-=1
    u,v=[i for i in range(n) if deg[i]==1]; e.append((u,v))
    for r in random.sample(range(n),5): print("#R%d_%d@%d %d %d "%(n,t,r,n,r)+" ".join("%d %d"%x for x in e))
