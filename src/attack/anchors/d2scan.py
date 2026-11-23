# scan depth-2 trees with r hubs: sizes small^(r-1) x big, using ./d2 ; optional validation against ./anchq
import subprocess,sys
from itertools import combinations_with_replacement
mode=sys.argv[1]
def d2(ks): return subprocess.run(["./d2"]+[str(k) for k in ks],capture_output=True,text=True).stdout.split()[0]
def gen(ks):
    r=len(ks); e=[]; nx=r+1
    for i,kk in enumerate(ks):
        e.append((0,i+1))
        for j in range(kk): e.append((i+1,nx)); nx+=1
    return "%d 0 "%nx+" ".join("%d %d"%x for x in e)
if mode=="validate":
    M=int(sys.argv[2]); bad=0; tot=0; nn=0
    def parts(total,r,mn=0):
        if r==1:
            if total>=mn: yield (total,)
            return
        for a in range(mn,total//r+1):
            for rest in parts(total-a,r-1,a): yield (a,)+rest
    for m in range(2,M+1):
        for r in range(1,m+1):
            for ks in parts(m-r,r):
                a=d2(ks); g=subprocess.run(["./anchq"],input=gen(ks)+"\n",capture_output=True,text=True).stdout.split()[0]
                tot+=1; nn+= (a=="NOT")
                if a!=g: bad+=1; print("MISMATCH",ks,a,g)
    print("validated",tot,"hub trees with m<=",M,"non-anchors:",nn,"mismatches:",bad)
else:
    r=int(sys.argv[2]); mx=int(sys.argv[3]); K=int(sys.argv[4]); cnt=0
    for small in combinations_with_replacement(range(0,mx+1),r-1):
        res=[]
        for k in range(max(small),K+1):
            cnt+=1
            if d2(small+(k,))=="NOT": res.append((k,sum(small)+k+r))
        if res: print(small,"non-anchor (k,m):",res,flush=True)
    print("done",cnt)
