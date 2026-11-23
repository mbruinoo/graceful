# Referee: spiders as tree lines "n a b ...". usage: equal | all N   (all: every partition of N-1 with >=3 parts)
import sys
def line(legs):
    e=[];v=1
    for L in legs:
        p=0
        for _ in range(L): e.append((p,v)); p=v; v+=1
    return "%d "%v+" ".join("%d %d"%x for x in e)
def parts(r,mx):
    if r==0: yield []; return
    for x in range(min(r,mx),0,-1):
        for t in parts(r-x,x): yield [x]+t
if sys.argv[1]=="equal":
    for L in range(1,7):
        for k in (3,4,5,6,8): print(line([L]*k))
else:
    N=int(sys.argv[2])
    for p in parts(N-1,N-1):
        if len(p)>=3: print(line(p))
