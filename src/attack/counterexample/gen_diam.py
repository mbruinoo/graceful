# All trees of diameter exactly 4 (centre with children carrying leaves) or 5 (two adjacent centres) on n vertices.
# usage: gen_diam.py 4|5 n
import sys
D,n=int(sys.argv[1]),int(sys.argv[2])
def parts(total,maxp):
    if total==0: yield []; return
    for p in range(min(total,maxp),0,-1):
        for r in parts(total-p,p): yield [p]+r
def build(root_parts_list):   # list of (root id handled by caller)
    pass
def emit(groups):
    # groups: list of partitions; group i hangs from centre i; part p = a child with p-1 leaves
    E=[]; nxt=len(groups)
    for i in range(1,len(groups)): E.append((0,i))
    for i,g in enumerate(groups):
        for p in g:
            c=nxt; nxt+=1; E.append((i,c))
            for _ in range(p-1): E.append((c,nxt)); nxt+=1
    assert nxt==n
    print(n," ".join("%d %d"%e for e in E))
if D==4:
    for g in parts(n-1,n-1):
        if sum(1 for p in g if p>=2)>=2: emit([g])       # at least two children with leaves -> diameter 4
else:
    for a in range(1,n-1):
        b=n-2-a
        if b<a: break
        for g in parts(a,a):
            if not any(p>=2 for p in g): continue
            for h in parts(b,b):
                if not any(p>=2 for p in h): continue
                if a==b and h>g: continue
                emit([g,h])
