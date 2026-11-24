# re-check pieces found by 'rs piece' from the definition (Python), and glue them (Theorem G) for a few q
import sys,re
from thm import *
for line in open(sys.argv[1]):
    m=re.match(r"piece b=(\d+) j=(\d+) FOUND: (.*)",line)
    if not m: continue
    b,j=int(m.group(1)),int(m.group(2)); L=list(map(int,m.group(3).split()))
    A=L[:b+1]; B=[0]+L[b+1:]; n=b+j+1
    assert len(B)==j+1
    e=path_check(A,B,n+1)
    ev=[A[i] for i in range(0,len(A),2)]+[B[i] for i in range(2,len(B),2)]
    od=[A[i] for i in range(1,len(A),2)]+[B[i] for i in range(1,len(B),2)]
    cross=max(ev)<min(od); inner=(B[-1]==min(od)) if j%2 else (B[-1]==max(ev))
    a=max(ev); side='high' if j%2 else 'low'; okg=True
    for q in range(0,60):
        sh=lambda x: x if x<=a else x+q
        tau=[]; lo=0; hi=q
        for i in range(q+1):
            if i%2==0: tau.append(lo); lo+=1
            else: tau.append(hi); hi-=1
        ext=[(B[-1]+q-t) if side=='high' else (B[-1]+t) for t in tau]
        if path_check([sh(x) for x in A],[sh(x) for x in B]+ext[1:],n+q+1): okg=False
    print("b=%d j=%d one-spare:%s crossing:%s tip innermost:%s glued q<60 ok:%s"%(b,j,e is None,cross,inner,okg))
