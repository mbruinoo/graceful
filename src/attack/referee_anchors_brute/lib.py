# shared helpers for the referee scripts
import subprocess, os
HERE=os.path.dirname(os.path.abspath(__file__))
def line(n,root,edges): return "%d %d "%(n,root)+" ".join("%d %d"%e for e in edges)
def check_growth(n,root,edges,lab):
    """README section 1 check with labels 0..m: bijection, lengths 1..m once,
    brackets longest first each have exactly one used foot, root at label 0."""
    m=n-1
    if lab[root]!=0 or sorted(lab)!=list(range(n)): return False
    L=sorted(((abs(lab[a]-lab[b]),lab[a],lab[b]) for a,b in edges),reverse=True)
    if [x[0] for x in L]!=list(range(m,0,-1)): return False
    used=set()
    for i,(k,a,b) in enumerate(L):
        if i==0: used|={a,b}; continue
        if (a in used)==(b in used): return False
        used|={a,b}
    return True
def solve(items,limit=None,prune=None):
    """items: list of (n,root,edges). returns list of (res,nodes,labels)"""
    inp="\n".join(line(*it) for it in items)+"\n"
    env=dict(os.environ)
    if prune is not None: env['PRUNE']=str(prune)
    cmd=[os.path.join(HERE,'ra')]+([str(limit)] if limit else [])
    out=subprocess.run(cmd,input=inp,capture_output=True,text=True,env=env).stdout.split("\n")
    res=[]
    for it,o in zip(items,out):
        t=o.split(); r=t[0]; nodes=int(t[1]); lab=list(map(int,t[2:]))
        if r=='1': assert check_growth(it[0],it[1],it[2],lab),("BAD WITNESS",it,lab)
        res.append((r,nodes,lab))
    return res
def Ltree(l,h1,h2):
    e=[(0,1),(1,2),(1,3)]; nxt=4
    for i in range(h1): e.append((2,nxt)); nxt+=1
    for i in range(h2): e.append((3,nxt)); nxt+=1
    for i in range(l): e.append((0,nxt)); nxt+=1
    return (nxt,0,e)
