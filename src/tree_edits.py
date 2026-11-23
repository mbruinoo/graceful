# tree_edits.py N -- for every tree on n <= N vertices and every single-edge edit (unhook edge ab, hook uv across the two pieces):
# is there a tree placement of that tree in which the edit is one slide?  "rehang" = the new edge keeps an end of the old one.
import sys
def canon(n, edges, col=None):
    col=col or ['']*n
    adj=[[] for _ in range(n)]
    for a,b in edges: adj[a].append(b); adj[b].append(a)
    deg=[len(x) for x in adj]; layer=[v for v in range(n) if deg[v]<=1]; rem=n; gone=set()
    while rem>2:
        nx=[]
        for v in layer:
            gone.add(v); rem-=1
            for u in adj[v]:
                if u not in gone:
                    deg[u]-=1
                    if deg[u]==1: nx.append(u)
        layer=nx
    def enc(v,p): return '('+col[v]+''.join(sorted(enc(u,v) for u in adj[v] if u!=p))+')'
    return min(enc(c,-1) for c in range(n) if c not in gone)
def marked(n,E,i,u,v):
    a,b=E[i]; rest=E[:i]+E[i+1:]+[(a,n),(n,b)]
    col=['']*(n+1); col[n]='e'; col[u]+='x'; col[v]+='x'
    return canon(n+1,rest,col)
def istree(n,p):
    par=list(range(n+1))
    def f(x):
        while par[x]!=x: par[x]=par[par[x]]; x=par[x]
        return x
    for k in range(1,n):
        a,b=f(p[k]),f(p[k]+k)
        if a==b: return False
        par[a]=b
    return True
for n in range(5,int(sys.argv[1])+1):
    done=set(); rep={}; p=[0]*n
    def rec(k):
        if k==n:
            if not istree(n,p): return
            E=[(p[j]-1,p[j]+j-1) for j in range(1,n)]; rep.setdefault(canon(n,E),E)
            for j in range(1,n):
                for d in (-1,1):
                    q=p[j]+d
                    if 1<=q<=n-j:
                        p[j]=q; ok=istree(n,p); p[j]=q-d
                        if ok: done.add(marked(n,E,j-1,q-1,q+j-1))
            return
        for q in range(1,n-k+1): p[k]=q; rec(k+1)
    rec(1)
    tot={'rehang':set(),'both':set()}
    for c,E in rep.items():
        for i,(a,b) in enumerate(E):
            rest=E[:i]+E[i+1:]
            adj=[[] for _ in range(n)]
            for x,y in rest: adj[x].append(y); adj[y].append(x)
            A={a}; st=[a]
            while st:
                w=st.pop()
                for u in adj[w]:
                    if u not in A: A.add(u); st.append(u)
            for u in A:
                for v in range(n):
                    if v not in A and (u,v)!=(a,b):
                        kind='rehang' if (u==a or v==b) else 'both'
                        tot[kind].add(marked(n,E,i,u,v))
    print(n,{k:(len(s&done),len(s)) for k,s in tot.items()},flush=True)
