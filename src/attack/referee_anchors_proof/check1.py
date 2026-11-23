# Referee check of claim 1 (H2, H3 rules) and claim 0 family against gen (definition-level search).
import subprocess, sys
from fam import *
def run(lines, limit=0):
    out=subprocess.run(["./gen",str(limit)],input="\n".join(lines)+"\n",capture_output=True,text=True).stdout.split("\n")
    return [o.split() for o in out if o]
def verify(n,e,labs):
    m=n-1
    assert sorted(labs)==list(range(n)) and labs[0]==0
    ln={abs(labs[a]-labs[b]):(a,b) for a,b in e}; assert sorted(ln)==list(range(1,n))
    used={labs[0]}  # must grow from... definition: each bracket longest first has exactly one used foot
    used=set()
    for k in range(m,0,-1):
        a,b=ln[k]
        if k==m: used|={labs[a],labs[b]}; continue
        assert (labs[a] in used)!=(labs[b] in used); used|={labs[a],labs[b]}
    return True
def H2rule(p,q):
    m=p+q+2
    for x in (p,q):
        for s in range(2,m+1):
            if m%s: continue
            t=m//s; j=x-(s-2)
            if 0<=j<=t-1 and (t%2==0 or j%2==0): return True
    return False
def H3rule(m): return m%3==0 or m%5==0 or m%4==3
M2=int(sys.argv[1]); M3=int(sys.argv[2])
trees=[];meta=[]
for m in range(2,M2+1):
    for p in range(0,(m-2)//2+1):
        q=m-2-p; n,e=hubs([p,q]); trees.append((n,e)); meta.append(("H2",p,q,H2rule(p,q)))
for m in range(11,M3+1,2):
    n,e=hubs([1,1,m-5]); trees.append((n,e)); meta.append(("H3",m,0,H3rule(m)))
res=run([line(n,e) for n,e in trees])
bad=0; non=[]
for (n,e),mt,r in zip(trees,meta,res):
    ok=(r[0]=="YES")
    if ok: verify(n,e,list(map(int,r[2:])))
    if ok!=mt[3]: bad+=1; print("MISMATCH",mt,r[:2])
    if not ok: non.append(mt[:3])
print("trees",len(trees),"mismatches",bad)
print("H2 non-anchors",sum(1 for x in non if x[0]=="H2"),"H3 non-anchor m:",[x[1] for x in non if x[0]=="H3"])
print("max nodes",max(int(r[1]) for r in res))
