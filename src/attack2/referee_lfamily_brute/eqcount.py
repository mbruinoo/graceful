"""Count reduced solutions with equal hub sizes h1=h2 (N<=NMAX), to reconcile the claimant's ordered total."""
import sys, subprocess
from lgrid import L
NMAX=int(sys.argv[1]); c=0
for p in range(1,NMAX):
    for d in range(0,NMAX):
        if 2*p+2+d>NMAX: break
        n,E=L(d,p,p); inp=f"{n} 0 "+" ".join(f"{u} {v}" for u,v in E)+"\n"
        for line in subprocess.run(["./rsolve","a"],input=inp,capture_output=True,text=True).stdout.split("\n"):
            if line and not line.startswith("END") and int(line.split()[1])==n-1: c+=1
print("equal-hub reduced solutions (unordered hubs):",c)
