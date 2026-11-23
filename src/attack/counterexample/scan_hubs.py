# Multi-hub families: every tree D on d vertices (from ./alltrees), every set of h vertices of D (up to
# isomorphism of the result); attach a_i new leaves to the i-th chosen vertex, for every size vector in
# the list.  Exact growth-placement counts via ./gcount.  Non-caterpillars only.
# usage: scan_hubs.py d h "a1,a2;a1,a2;..." [node limit]
import sys, subprocess, itertools, os
d,h=int(sys.argv[1]),int(sys.argv[2]); sizes=[tuple(map(int,s.split(","))) for s in sys.argv[3].split(";")]
lim=sys.argv[4] if len(sys.argv)>4 else "20000000"
def canon(n,E):
    adj=[[] for _ in range(n)]
    for a,b in E: adj[a].append(b); adj[b].append(a)
    def enc(v,p): return "("+"".join(sorted(enc(u,v) for u in adj[v] if u!=p))+")"
    return min(enc(r,-1) for r in range(n))
def iscat(n,E):
    adj=[[] for _ in range(n)]
    for a,b in E: adj[a].append(b); adj[b].append(a)
    return all(sum(1 for u in adj[v] if len(adj[u])>1)<=2 for v in range(n))
def attach(E,vs,sz):
    E=list(E); n=d
    for v,a in zip(vs,sz):
        for _ in range(a): E.append((v,n)); n+=1
    return n,E
trees=subprocess.run(["./alltrees",str(d)],capture_output=True,text=True).stdout.strip().split("\n")
seen=set(); fams=[]
for t in trees:
    x=list(map(int,t.split())); E=list(zip(x[1::2],x[2::2]))
    for vs in itertools.permutations(range(d),h):
        n,E2=attach(E,vs,tuple(range(2,2+h)))      # distinct sizes >=2 so every chosen vertex is a marked hub
        c=canon(n,E2)
        if c in seen: continue
        seen.add(c)
        n3,E3=attach(E,vs,sizes[0])
        if iscat(n3,E3): continue
        fams.append((E,vs))
inp=[]; keys=[]
for E,vs in fams:
    for sz in sizes:
        n,E2=attach(E,vs,sz); inp.append(str(n)+" "+" ".join("%d %d"%e for e in E2)); keys.append((tuple(E),vs,sz))
out=subprocess.run(["./gcount"],input="\n".join(inp)+"\n",capture_output=True,text=True,env=dict(os.environ,LIMIT=lim)).stdout.strip().split("\n")
res={}
for (E,vs,sz),o in zip(keys,out):
    f=o.split(); res.setdefault((E,vs),[]).append(f[1].split("=")[1]+("+" if "UNFINISHED" in o else ""))
def key(v):
    xs=[int(x.rstrip("+").lstrip(">")) for x in v[1] if not x.endswith("+")]
    return min(xs) if xs else 10**18
print("sizes:",sizes)
for (E,vs),c in sorted(res.items(),key=key): print(min([int(x) for x in c if not x.endswith("+")] or [-1]), "skeleton",E,"hubs at",vs,"counts"," ".join(c))
