from lib import *
import sys,time
t=Ltree(3,8,9)
assert t[2]==[(0,1),(1,2),(1,3)]+[(2,i) for i in range(4,12)]+[(3,i) for i in range(12,21)]+[(0,i) for i in (21,22,23)]
for pr in (1,0,-1):
    t0=time.time(); r=solve([t],prune=pr,limit=3*10**9); print("L(3;8,9) prune",pr,r[0][:2],"%.1fs"%(time.time()-t0)); sys.stdout.flush()
r=solve([Ltree(4,8,9)]); print("L(4;8,9)",r[0])
for l in range(1,6):
    t0=time.time()
    a=solve([Ltree(l,2*l+2,2*l+3)],limit=2*10**9)[0]; b=solve([Ltree(l+1,2*l+2,2*l+3)],limit=2*10**9)[0]
    print("l=%d L(l;2l+2,2l+3) n=%d: %s nodes %d | L(l+1;..): %s nodes %d  %.1fs"%(l,2*l+2+2*l+3+l+4,a[0],a[1],b[0],b[1],time.time()-t0)); sys.stdout.flush()
