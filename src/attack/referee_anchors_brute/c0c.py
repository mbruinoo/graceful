from lib import *
import sys,time
# (i) least l with v anchor == h1/2 for h1 even < h2 odd <= 17
t0=time.time(); bad=0; cases=0
for h1 in range(2,17,2):
    for h2 in range(h1+1,18,2):
        cases+=1
        items=[Ltree(l,h1,h2) for l in range(0,h1//2+1)]
        R=[r[0] for r in solve(items)]
        if R!=['0']*(h1//2)+['1']: bad+=1; print("FAIL",h1,h2,R)
print("least-l observation: cases",cases,"failures",bad,"%.0fs"%(time.time()-t0)); sys.stdout.flush()
# (ii) pattern of non-anchor pairs for fixed l
for l,H in ((0,14),(1,14),(2,18),(3,16),(4,15),(5,14)):
    keys=[(h1,h2) for h1 in range(0,H+1) for h2 in range(h1,H+1)]
    R=solve([Ltree(l,*k) for k in keys])
    non={k for k,r in zip(keys,R) if r[0]=='0'}
    pred={(h1,h2) for (h1,h2) in keys if h1%2==0 and h2%2==1 and h1<h2 and h1>=2*l+2}
    print("l=%d h<=%d: non-anchor pairs %d, predicted %d, equal %s; extra %s missing %s  %.0fs"%(l,H,len(non),len(pred),non==pred,sorted(non-pred)[:8],sorted(pred-non)[:8],time.time()-t0)); sys.stdout.flush()
