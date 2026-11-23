# Show a build of the spider with k legs of length L found by runsolve128 under a skip limit, as leg label lists and a tape.
import sys, subprocess, os
k,L,sk=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]); n=k*L+1
s=subprocess.run(["python3","hardfam.py",f"S{k}",str(L)],capture_output=True,text=True).stdout
e=subprocess.run(["python3","paren.py"],input=s,capture_output=True,text=True).stdout
env=dict(os.environ,SHOW="1"); 
if len(sys.argv)>4: env["ORDERED"]="1"
out=subprocess.run(["./runsolve128",str(n),str(sk+1),"200000","1"],input=e,capture_output=True,text=True,env=env).stdout
lab=None
for line in out.splitlines():
    if line.startswith("labels"): lab=list(map(int,line.split(":")[1].split()))
if not lab: print("no build found"); sys.exit()
x=list(map(int,e.split())); E=list(zip(x[::2],x[1::2])); adj=[[] for _ in range(n)]
for a,b in E: adj[a].append(b); adj[b].append(a)
c=max(range(n),key=lambda v:len(adj[v]))
legs=[]
for w in adj[c]:
    leg=[lab[w]]; prev,cur=c,w
    while True:
        nx=[u for u in adj[cur] if u!=prev]
        if not nx: break
        prev,cur=cur,nx[0]; leg.append(lab[cur])
    legs.append(leg)
legs.sort(key=lambda l:-abs(l[0]-lab[c]))
print(f"S({L}^{k}) n={n}: centre={lab[c]}   legs: "+"  ".join("-".join(map(str,l)) for l in legs))
# tape
pos={lab[v]:v for v in range(n)}; edges=sorted(((abs(lab[a]-lab[b]),lab[a],lab[b]) for a,b in E),reverse=True)
used=set(); 
for d,a,b in edges:
    new=[z for z in (a,b) if z not in used]; used|={a,b}
    print(f"  k={d:2d} "+"".join(("N" if (i in new and d!=n-1) else "#") if i in used else "." for i in range(1,n+1)))
