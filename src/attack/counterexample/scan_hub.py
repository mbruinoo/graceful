# One-hub families: for every rooted tree D on d vertices, T(D,m) = D plus m new leaves at the root of D.
# Exact growth-placement counts (./gcount) for m in a range; prints per D the counts, sorted by the last count.
# usage: scan_hub.py d m_lo m_hi [node limit]
import sys, subprocess, functools
from fam import line, edges
d,lo,hi=map(int,sys.argv[1:4]); lim=sys.argv[4] if len(sys.argv)>4 else "20000000"
@functools.lru_cache(None)
def rooted(k):      # canonical paren strings of rooted trees on k vertices
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
def iscat(s):
    n,E=edges(s); adj=[[] for _ in range(n)]
    for a,b in E: adj[a].append(b); adj[b].append(a)
    return all(sum(1 for u in adj[v] if len(adj[u])>1)<=2 for v in range(n))
import os
rows=[]; inp=[]; keys=[]
for D in rooted(d):
    for m in range(lo,hi+1):
        s="("+"()"*m+D[1:]
        if iscat(s): continue
        inp.append(line(s)); keys.append((D,m))
out=subprocess.run(["./gcount"],input="\n".join(inp)+"\n",capture_output=True,text=True,env=dict(os.environ,LIMIT=lim)).stdout.strip().split("\n")
res={}
for (D,m),o in zip(keys,out):
    f=o.split(); res.setdefault(D,[]).append(f[1].split("=")[1]+("+" if "UNFINISHED" in o else ""))
def key(v):
    x=v[1][-1]; return (x.endswith("+"), int(x.rstrip("+").lstrip(">")))
for D,c in sorted(res.items(),key=key): print(D, " ".join(c))
