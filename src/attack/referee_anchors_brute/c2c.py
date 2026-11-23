# Theorem M on random larger rooted trees (no leaf at root), skipping those with M > 3e5
import random,sys
sys.argv=['c2',  '3']
import importlib.util
src=open('c2.py').read().split("N=int(sys.argv[1])")[0]
exec(src)
random.seed(1); done=0; fails=0; maxM=0
def rnd(n):
    par=[None]+[random.randrange(0,i) if random.random()<0.6 else max(0,i-1-random.randrange(0,3)) for i in range(1,n)]
    ch=[[] for _ in range(n)]
    for i in range(1,n): ch[min(par[i],i-1)].append(i)
    def nest(u): return tuple(sorted(nest(c) for c in ch[u]))
    return nest(0)
while done<3000:
    t=rnd(random.randrange(5,26))
    if any(s==() for s in t): continue
    # cheap M estimate
    ok,M,info=test(t) if True else None
    done+=1; maxM=max(maxM,M)
    if not ok: fails+=1; print("FAIL",t,M,info)
print("random rooted trees (5..25 vertices):",done,"fails",fails,"max M",maxM)
