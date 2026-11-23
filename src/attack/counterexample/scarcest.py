# usage: alltrees n | scarcest.py K   -> the K scarcest non-caterpillar trees by exact growth-placement count
import sys, subprocess
K=int(sys.argv[1]); lines=[l for l in sys.stdin if l.strip()]
out=subprocess.run(["./gcount"],input="".join(lines),capture_output=True,text=True).stdout.split("\n")
res=[]
for l,o in zip(lines,out):
    t=list(map(int,l.split())); n=t[0]; E=list(zip(t[1::2],t[2::2]))
    adj=[[] for _ in range(n)]
    for a,b in E: adj[a].append(b); adj[b].append(a)
    deg=[len(a) for a in adj]
    cat=all(sum(1 for u in adj[v] if deg[u]>1)<=2 for v in range(n))
    c=int(o.split()[1].split("=")[1])
    def enc(v,p): return "("+"".join(sorted(enc(u,v) for u in adj[v] if u!=p))+")"
    res.append((c,cat,l.strip()))
nc=sorted(r for r in res if not r[1])
print("n=%d trees=%d min_all=%d min_noncat=%d median=%d"%(n,len(res),min(r[0] for r in res),nc[0][0],sorted(r[0] for r in res)[len(res)//2]))
for c,_,l in nc[:K]:
    t=list(map(int,l.split())); n=t[0]; par={b:a for a,b in zip(t[1::2],t[2::2])}
    ch={}
    for b,a in par.items(): ch.setdefault(a,[]).append(b)
    def enc(v): return "("+"".join(sorted(enc(u) for u in ch.get(v,[])))+")"
    print("  %6d  %s"%(c,enc(0)))
