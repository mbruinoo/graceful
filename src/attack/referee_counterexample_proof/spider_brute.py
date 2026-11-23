# Exhaustive (referee's ex.cpp): centre-anchored growth placement for every leg multiset with legs in {1,2,3}, n<=NMAX.
import sys, subprocess
N=int(sys.argv[1]); items=[]
for n3 in range(0,6):
    for n2 in range(0,9):
        for n1 in range(0,N):
            n=1+n1+2*n2+3*n3
            if n<2 or n>N: continue
            E=[]; v=1
            for L,c in ((3,n3),(2,n2),(1,n1)):
                for _ in range(c):
                    p=0
                    for _ in range(L): E.append((p,v)); p=v; v+=1
            items.append(((n1,n2,n3),str(n)+" "+" ".join("%d %d"%e for e in E)))
out=subprocess.run(["./ex"],input="\n".join(l for _,l in items)+"\n",capture_output=True,text=True).stdout.split()
r=out[0::2]
print("leg multisets (n1,n2,n3) with n<=%d: %d ; centre NOT an anchor: %s"%(N,len(items),[k for (k,_),x in zip(items,r) if x=="0"]))
