from thm import *
def vecs(r,tot,mx):
    if r==0: yield []; return
    for a in range(min(tot,mx),-1,-1):
        for rest in vecs(r-1,tot-a,a): yield [a]+rest
for minr,zero in ((1,True),(1,False),(2,True)):
    nv=0;nl=0;bad=0
    for r in range(minr,7):
        for a in vecs(r,30,30):
            if not zero and a[-1]==0: continue
            K=1+sum(a); d=sum(j*a[j] for j in range(1,r))
            if d>K-1: continue
            nv+=1
            for s in range(1,K-d+1):
                P,f,cnt,K,d=W_build(a,s); nl+=1; n=len(P)
                e=check(P,f,n+1)
                if cnt!=a or e or set(range(n+1))-set(f.values())!={K+1-s-d} or set(range(1,n+1))-set(abs(f[v]-f[P[v]]) for v in P if P[v])!={s}: bad+=1
    print("r from",minr,"zeros allowed",zero,"vectors",nv,"labelings",nl,"bad",bad)
