# Is every vertex of degree >= 4 an anchor?  (README section 7 observes this for n <= 14.)
# For every rooted tree D on d vertices whose root has degree >= DEG: is the root an anchor?  Randomised search first,
# then exhaustive (ordered, unlimited) for the rest.  usage: deg4.py DEG d...
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
def rootdeg(s):
    dep=0; c=0
    for ch in s:
        if ch=="(":
            dep+=1
            if dep==2: c+=1
        else: dep-=1
    return c
DEG=int(sys.argv[1])
for d in map(int,sys.argv[2:]):
    Ds=[D for D in rooted(d) if rootdeg(D)>=DEG]
    out=subprocess.run(["./gsolve","3000","7","1"],input="\n".join(line(D) for D in Ds)+"\n",capture_output=True,text=True,env=dict(os.environ,ROOT0="1")).stdout.strip().split("\n")
    rest=[D for D,o in zip(Ds,out) if not o.startswith("FOUND")]
    non=[]
    if rest:
        out=subprocess.run(["./gsolve","3000","3","0"],input="\n".join(line(D) for D in rest)+"\n",capture_output=True,text=True,env=dict(os.environ,ROOT0="1")).stdout.strip().split("\n")
        non=[D for D,o in zip(rest,out) if o.startswith("NONE")]
        assert all(o.startswith(("NONE","FOUND")) for o in out[:-1])
    print("d=%d rooted trees with root degree >= %d: %d   root is NOT an anchor (exhaustive): %d"%(d,DEG,len(Ds),len(non)),flush=True)
    for D in non[:10]: print("   ",D)
