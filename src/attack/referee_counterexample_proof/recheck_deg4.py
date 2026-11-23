# D4 evidence: every rooted tree on d vertices with root degree >= 4 (referee's generator), claimant's solver with ROOT0,
# referee's checker (growth placement of exactly this tree, root label 1).
import sys, subprocess, os, time
from rooted import rooted, edges
from chk import growth
G=sys.argv[1]
for d in map(int,sys.argv[2:]):
    t0=time.time(); items=[edges(D) for D in rooted(d) if len(D)>=4]
    inp="\n".join(str(n)+" "+" ".join("%d %d"%e for e in E) for n,E in items)+"\n"
    out=subprocess.run([G,"3000","7","0"],input=inp,capture_output=True,text=True,env=dict(os.environ,SHOW="1",ROOT0="1")).stdout.split("\n")
    bad=0
    for (n,E),o in zip(items,out):
        if not(o.startswith("FOUND") and growth(n,E,list(map(int,o.split("labels:")[1].split()))) and int(o.split("labels:")[1].split()[0])==1): bad+=1
    print("d=%d rooted trees with root degree>=4: %d  without referee-checked root-anchored certificate: %d [%.0fs]"%(d,len(items),bad,time.time()-t0),flush=True)
