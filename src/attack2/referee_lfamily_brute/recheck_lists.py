"""Re-decide the claimant's listed queries with rsolve and check (a) same verdicts, (b) degrees,
(c) the 89 n=22 kinds are pairwise non-isomorphic as rooted trees.  Reads claimant files read-only."""
import re, subprocess, networkx as nx
D="../lfamily/"
def parse(line):
    body=line.split("|",1)[1].strip()
    if "v=" in body:
        es,v=body.rsplit("v=",1); E=[tuple(map(int,e.split("-"))) for e in es.split() if "-" in e]; return len(E)+1,int(v),E
    a=list(map(int,body.split())); n,r=a[0],a[1]; return n,r,[(a[2+2*i],a[3+2*i]) for i in range(n-1)]
def canon(adj,r):
    def f(x,p): return "("+"".join(sorted(f(y,x) for y in adj[x] if y!=p))+")"
    return f(r,-1)
for fn in ["n22_deg2_noleaf.txt","n22_deg2_leaf.txt","r23.txt","r24.txt"]:
    rows=[l for l in open(D+fn) if "|" in l]
    q=[];claims=[];cs=set();degs=set()
    for l in rows:
        n,r,E=parse(l); adj={i:[] for i in range(n)}
        for u,v in E: adj[u].append(v); adj[v].append(u)
        degs.add(len(adj[r])); cs.add(canon(adj,r)); claims.append(l.split()[0])
        q.append(f"{n} {r} "+" ".join(f"{u} {v}" for u,v in E))
    out=subprocess.run(["./rsolve","d","3000000000"],input="\n".join(q)+"\n",capture_output=True,text=True).stdout.split("\n")
    mine=[o.split()[0] for o in out if o]
    dis=sum(1 for a,b in zip(claims,mine) if a!=b)
    print(fn,"rows",len(rows),"distinct rooted",len(cs),"degrees",degs,"claimNOT",claims.count("NOT"),"myNOT",mine.count("NOT"),"disagree",dis,"CAP",mine.count("CAP"))
