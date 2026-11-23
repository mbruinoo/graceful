# Re-derive the hub-theorem base case for size d with the CLAIMANT's solver but the REFEREE's tree generator
# and the REFEREE's checker: for every rooted D on d vertices find m0<=M with a checked growth placement of
# T(D,m0) having root label 1, and for every m<m0 a checked growth placement of T(D,m) (no root restriction).
import sys, subprocess, os, time
from rooted import rooted, edges
from chk import growth
G=sys.argv[1]
def solve(items,root0):
    env=dict(os.environ,SHOW="1")
    if root0: env["ROOT0"]="1"
    else: env.pop("ROOT0",None)
    inp="\n".join(str(n)+" "+" ".join("%d %d"%e for e in E) for n,E in items)+"\n"
    out=subprocess.run([G,"3000","7","1"],input=inp,capture_output=True,text=True,env=env).stdout.split("\n")
    res=[]
    for (n,E),o in zip(items,out):
        good=False
        if o.startswith("FOUND") and "labels:" in o:
            lab=list(map(int,o.split("labels:")[1].split()))
            good = len(lab)==n and growth(n,E,lab) and (not root0 or lab[0]==1)
        res.append(good)
    assert len(res)==len(items)
    return res
B=100000   # trees per batch (keeps memory small)
for d in map(int,sys.argv[2:]):
    t0=time.time(); allD=rooted(d); hist={}; nsmall=0; sf=0; never=0
    ch=os.environ.get('CHUNK')   # 'i/k': only every k-th tree starting at i (to keep one run under the time limit)
    if ch: i,k=map(int,ch.split('/')); allD=allD[i::k]
    for b in range(0,len(allD),B):
        pending=allD[b:b+B]; small=[]
        for m in range(0,5):
            if not pending: break
            ok=solve([edges(D,m) for D in pending],True); nxt=[]
            for D,o in zip(pending,ok):
                if o:
                    hist[m]=hist.get(m,0)+1; small+=[edges(D,mm) for mm in range(m)]
                else: nxt.append(D)
            pending=nxt
        never+=len(pending); nsmall+=len(small)
        if small: sf+=solve(small,False).count(False)
    print("d=%d %s trees=%d  referee-checked root-anchored certificate at least m: %s  never found (m<=4): %d  smaller members=%d without checked certificate=%d  [%.0fs]"%(d,("chunk "+ch) if ch else "all",len(allD),sorted(hist.items()),never,nsmall,sf,time.time()-t0),flush=True)
