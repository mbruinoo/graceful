# edge lists ("s : u v u v ...") -> canonical nested-paren form rooted at the centre
import sys
for line in sys.stdin:
    s,e=line.split(":"); x=list(map(int,e.split())); E=list(zip(x[::2],x[1::2])); n=len(E)+1
    adj=[[] for _ in range(n)]
    for a,b in E: adj[a].append(b); adj[b].append(a)
    deg=[len(a) for a in adj]; layer=[v for v in range(n) if deg[v]<=1]; rem=n; gone=[0]*n
    while rem>2:
        nx=[]
        for v in layer:
            gone[v]=1; rem-=1
            for u in adj[v]:
                if not gone[u]:
                    deg[u]-=1
                    if deg[u]==1: nx.append(u)
        layer=nx
    def enc(v,pa): return "("+"".join(sorted((enc(u,v) for u in adj[v] if u!=pa),key=lambda t:(-len(t),t)))+")"
    c=enc(layer[0],-1) if len(layer)==1 else enc(layer[0],layer[1])+" | "+enc(layer[1],layer[0])
    print(s.strip(),n,c)
