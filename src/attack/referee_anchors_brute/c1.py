from lib import *
import sys,time
def DH(p,q):
    e=[(0,1),(0,2)]; nx=3
    for i in range(p): e.append((1,nx)); nx+=1
    for i in range(q): e.append((2,nx)); nx+=1
    return (nx,0,e)
def ruleH2(p,q):
    m=p+q+2
    for x in (p,q):
        for s in range(2,m+1):
            if m%s: continue
            t=m//s; j=x-(s-2)
            if 0<=j<=t-1 and (t%2==0 or j%2==0): return True
    return False
def H11k(k):
    e=[(0,1),(0,2),(0,3),(1,4),(2,5)]; nx=6
    for i in range(k): e.append((3,nx)); nx+=1
    return (nx,0,e)
def ruleH3(m): return m%3==0 or m%5==0 or m%4==3
MM=int(sys.argv[1]); M3=int(sys.argv[2])
t0=time.time()
keys=[(p,m-2-p) for m in range(2,MM+1) for p in range(0,(m-2)//2+1)]
R=solve([DH(*k) for k in keys])
bad=[(k,r[0]) for k,r in zip(keys,R) if (r[0]=='1')!=ruleH2(*k)]
non=sum(1 for r in R if r[0]=='0')
print("H2: DH(p,q) 2<=m<=%d: %d trees (p<=q, p>=0), non-anchors %d, rule mismatches %d %s  maxnodes %d  %.0fs"%(MM,len(keys),non,len(bad),bad[:10],max(r[1] for r in R),time.time()-t0))
pr=[(k) for k,r in zip(keys,R) if k[0]>=1 and all((sum(k)+2)%d for d in range(2,sum(k)+2)) and r[0]=='1']
print("   prime m, p,q>=1, anchor (should be none):",pr); sys.stdout.flush()
ms=list(range(5,M3+1))
R=solve([H11k(m-5) for m in ms])
bad=[(m,r[0]) for m,r in zip(ms,R) if m%2==1 and m>=11 and (r[0]=='1')!=ruleH3(m)]
print("H3: H(1,1,k) odd 11<=m<=%d: mismatches %s; non-anchor odd m: %s; (even m and m<11, not claimed: non-anchor m = %s)  maxnodes %d %.0fs"%(M3,bad,[m for m,r in zip(ms,R) if r[0]=='0' and m%2 and m>=11],[m for m,r in zip(ms,R) if r[0]=='0' and not(m%2 and m>=11)],max(r[1] for r in R),time.time()-t0))
