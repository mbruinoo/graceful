# All spiders on n vertices (one per partition of n-1 into >=3 parts = leg lengths), as edge lists; centre is vertex 0.
import sys
n=int(sys.argv[1])
def parts(m,mx):
    if m==0: yield []; return
    for k in range(min(m,mx),0,-1):
        for r in parts(m-k,k): yield [k]+r
for P in parts(n-1,n-1):
    if len(P)<3: continue
    E=[]; v=1
    for L in P:
        prev=0
        for _ in range(L): E.append((prev,v)); prev=v; v+=1
    print(' '.join(f"{a} {b}" for a,b in E))
