# For rooted trees D on d vertices: exact least m such that the root of T(D,m) is an anchor
# (exhaustive: ./gsolve with ROOT0=1 and unlimited ordered search for the failures).  Prints D with m >= 2.
import sys, subprocess, os, functools
from fam import line
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
for d in map(int,sys.argv[1:]):
    pending=list(rooted(d)); hist={}
    for m in range(0,8):
        if not pending: break
        lines=[line("("+"()"*m+D[1:]) for D in pending]
        out=subprocess.run(["./gsolve","3000","5","0"],input="\n".join(lines)+"\n",capture_output=True,text=True,env=dict(os.environ,ROOT0="1")).stdout.strip().split("\n")
        nxt=[]
        for D,o in zip(pending,out):
            if o.startswith("FOUND"):
                hist[m]=hist.get(m,0)+1
                if m>=2: print("  d=%d exact least m=%d  D=%s"%(d,m,D))
            else:
                assert o.startswith("NONE"), o
                nxt.append(D)
        pending=nxt
    print("d=%d exact least m histogram: %s"%(d,sorted(hist.items())))
