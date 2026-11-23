# Emit certificates "tree | labels" for the hub theorem at size d: for each rooted D, T(D,m) for the first m where
# the root-anchored search succeeds.  usage: hubcert.py d | verify.py root0
import sys, subprocess, os
sys.argv=[sys.argv[0],sys.argv[1]]
import importlib.util
from fam import line
import functools
d=int(sys.argv[1])
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
pending=list(rooted(d))
for m in range(0,13):
    if not pending: break
    lines=[line("("+"()"*m+D[1:]) for D in pending]
    out=subprocess.run(["./gsolve","3000","7","1"],input="\n".join(lines)+"\n",capture_output=True,text=True,env=dict(os.environ,ROOT0="1",SHOW="1")).stdout.strip().split("\n")
    nxt=[]
    for D,l,o in zip(pending,lines,out):
        if o.startswith("FOUND"): print(l,"|",o.split("labels:")[1])
        else: nxt.append(D)
    pending=nxt
print("pending",len(pending),file=sys.stderr)
