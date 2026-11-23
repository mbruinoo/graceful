# Hub theorem check.  For every rooted tree D on d vertices: find the least m (0..M) for which the randomised
# search finds a growth placement of T(D,m) (= D plus m new leaves at the root) with the ROOT labelled 1.
# By Lemma 6 (leaf extension at the vertex labelled 1) T(D,m') then has one for every m' >= m.
# Then check T(D,m') for each m' < m without the root restriction.
# usage: hubthm.py d [M=12] [L=3000] [rounds=7]
import sys, subprocess, functools, os
from fam import line
d=int(sys.argv[1]); M=int(sys.argv[2]) if len(sys.argv)>2 else 12
L=sys.argv[3] if len(sys.argv)>3 else "3000"; R=sys.argv[4] if len(sys.argv)>4 else "7"
@functools.lru_cache(None)
def rooted(k):
    if k==1: return ("()",)
    out=set()
    def parts(rem,maxs,acc):
        if rem==0: out.add("("+"".join(acc)+")"); return
        for s in range(min(rem,maxs),0,-1):
            for t in rooted(s):
                if acc and (len(acc[-1])//2==s) and t>acc[-1]: continue
                parts(rem-s,s,acc+[t])
    parts(k-1,k-1,[])
    return tuple(sorted(out))
def run(strs,root0):
    env=dict(os.environ); 
    if root0: env["ROOT0"]="1"
    else: env.pop("ROOT0",None)
    out=subprocess.run(["./gsolve",L,R,"1"],input="\n".join(line(s) for s in strs)+"\n",capture_output=True,text=True,env=env).stdout.strip().split("\n")
    assert len(out)==len(strs)+1, out[-3:]
    return [o.startswith("FOUND") for o in out[:-1]]
pending=list(rooted(d)); m0={}
for m in range(0,M+1):
    if not pending: break
    ok=run(["("+"()"*m+D[1:] for D in pending],True)
    nxt=[]
    for D,o in zip(pending,ok):
        if o: m0[D]=m
        else: nxt.append(D)
    pending=nxt
hist={}
for D,m in m0.items(): hist[m]=hist.get(m,0)+1
small=[ "("+"()"*mm+D[1:] for D,m in m0.items() for mm in range(m)]
ok=run(small,False) if small else []
print("d=%d rooted trees=%d  least m with root anchor found: %s  unresolved(root never found as anchor up to m=%d)=%d  smaller members checked=%d failing=%d"%(d,len(rooted(d)),sorted(hist.items()),M,len(pending),len(small),ok.count(False)))
for D in pending: print("  PENDING",D)
for s,o in zip(small,ok):
    if not o: print("  SMALL-FAIL",s)
