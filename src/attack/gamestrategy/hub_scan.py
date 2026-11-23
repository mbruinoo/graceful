import sys
from explore import *
N=int(sys.argv[1]); lo=int(sys.argv[2])
for n in range(lo,N+1):
    tot=0; nomax=[]; nomin=[]; noany=[]; nocl=[]
    for a in d4trees(n):
        tot+=1
        par,kind=build(a)
        res={}
        for v in range(1,n):
            if kind[v][0]=='h' and a[kind[v][1]] not in res:
                res[a[kind[v][1]]]=bool(solve(par,v,1))
        pos=[x for x in res if x>0]
        if not res[max(pos)]: nomax.append(a)
        if not res[min(pos)]: nomin.append(a)
        if not any(res[x] for x in pos): noany.append(a)
    print(n,tot,'largest hub not anchor:',nomax,'| smallest nontrivial hub not anchor:',nomin,'| no hub anchor',noany,flush=True)
