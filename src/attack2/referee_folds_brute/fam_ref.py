# referee: hard symmetric families, n<=NMAX: stems ending in hubs, spherically symmetric, spiders, hubs on a path pair
import sys, itertools
NMAX=int(sys.argv[1]); out=[]; names=[]
def emit(E,name):
    n=len(E)+1
    if 10<=n<=NMAX: out.append(' '.join(f"{a} {b}" for a,b in E)); names.append(f"{n} {name}")
for k in range(2,9):
    for a in range(0,5):
        for m in range(1,20):
            E=[];c=1
            for _ in range(k):
                prev=0
                for _ in range(a): E.append((prev,c)); prev=c; c+=1
                E.append((prev,c)); hub=c; c+=1
                for _ in range(m): E.append((hub,c)); c+=1
            emit(E,f"{k} stems len {a} hub {m}")
for depth in (2,3,4):
    for ds in itertools.product(range(2,10),repeat=depth):
        E=[];c=1;level=[0]
        for d in ds:
            nl=[]
            for v in level:
                for _ in range(d): E.append((v,c)); nl.append(c); c+=1
            level=nl
            if c>NMAX: break
        if c<=NMAX: emit(E,f"sph {ds}")
for k in range(3,9):
    for l in range(2,30):
        E=[];c=1
        for _ in range(k):
            prev=0
            for _ in range(l): E.append((prev,c)); prev=c; c+=1
        emit(E,f"spider {k}x{l}")
open(sys.argv[2],'w').write('\n'.join(out)+'\n'); open(sys.argv[2]+'.names','w').write('\n'.join(names)+'\n')
print(len(out))
