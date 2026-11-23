import sys
from explore import *
N=int(sys.argv[1]); lo=int(sys.argv[2]) if len(sys.argv)>2 else 5
for n in range(lo,N+1):
    bad=[];tot=0
    for a in d4trees(n):
        if min(a)==0: continue
        tot+=1
        par,kind=build(a)
        if not solve(par,0,1): bad.append(a)
    print(n,tot,'no centre anchor:',bad,flush=True)
