# lib.py -- shared helpers: tree parsing, canonical code (same as brute.cpp), replay of a build, step classification
import sys
sys.setrecursionlimit(10000)
def parse(line):
    t=list(map(int,line.split())); E=[(t[i],t[i+1]) for i in range(0,len(t),2)]; n=max(max(e) for e in E)+1
    adj=[[] for _ in range(n)]
    for u,v in E: adj[u].append(v); adj[v].append(u)
    return n,E,adj
def enc(adj,v,p):
    return "("+"".join(sorted(enc(adj,u,v) for u in adj[v] if u!=p))+")"
def centres(adj):
    n=len(adj); deg=[len(a) for a in adj]; alive=[True]*n; left=n; lv=[i for i in range(n) if deg[i]<=1]
    while left>2:
        nx=[]
        for v in lv:
            alive[v]=False; left-=1
            for u in adj[v]:
                if alive[u]:
                    deg[u]-=1
                    if deg[u]==1: nx.append(u)
        lv=nx
    return [i for i in range(n) if alive[i]]
def canon(adj):
    c=centres(adj)
    if len(c)==1: return enc(adj,c[0],-1)
    a,b=enc(adj,c[0],c[1]),enc(adj,c[1],c[0])
    if a>b: a,b=b,a
    return a+"|"+b
def runs_of(used,n):
    """list of (lo,hi) runs of unused cells, left to right"""
    R=[]; i=1
    while i<=n:
        if not used[i]:
            j=i
            while j<n and not used[j+1]: j+=1
            R.append((i,j)); i=j+1
        else: i+=1
    return R
def replay(n,E,f):
    """f[v]=label 1..n.  Checks the growth placement FROM THE DEFINITION (labels a permutation, lengths 1..n-1 once
    each, every bracket taken longest first has exactly one used foot) and returns the list of steps
    dict(t,x,y,child,parent,runs(before),main,inM,r,c,H,costA,costB)."""
    assert sorted(f)==list(range(1,n+1)), "labels not a permutation"
    assert len(E)==n-1
    by={}
    for u,v in E:
        d=abs(f[u]-f[v]); assert d not in by, "repeated length"; by[d]=(u,v)
    assert sorted(by)==list(range(1,n)), "lengths not 1..n-1"
    u,v=by[n-1]; assert {f[u],f[v]}=={1,n}
    used=[False]*(n+2); used[1]=used[n]=True; steps=[]
    for t in range(n-2,0,-1):
        u,v=by[t]
        if used[f[v]]: u,v=v,u
        assert used[f[u]] and not used[f[v]], "not a growth placement"
        x,y=f[v],f[u]; R=runs_of(used,n); assert sum(b-a+1 for a,b in R)==t
        main=max(R,key=lambda ab:(ab[1]-ab[0],-ab[0]))      # longest, leftmost on ties
        own=[ab for ab in R if ab[0]<=x<=ab[1]][0]
        r=(x-own[0]) if y>x else (own[1]-x); c=(own[1]-own[0])-r
        inM=(own==main); H=t-(main[1]-main[0]+1)
        steps.append(dict(t=t,x=x,y=y,child=v,parent=u,runs=R,main=main,own=own,inM=inM,r=r,c=c,H=H,
                          costA=0 if (inM and r==0) else 1,costB=0 if r==0 else 1))
        used[x]=True
    return steps
def read_results(path):
    """lines 'T idx n=.. lb=.. ub=.. exact=.. nodes=.. time=.. labels: ...' -> list of dicts (in file order)"""
    out=[]
    for l in open(path):
        if not l.startswith('T '): continue
        p=l.split(); d=dict(kv.split('=') for kv in p[2:8]); d['idx']=int(p[1])
        d['labels']=list(map(int,l.split('labels:')[1].split())) if 'labels:' in l else None
        for k in('n','lb','exact'): d[k]=int(d[k])
        d['ub']=None if d['ub']=='NONE' else int(d['ub'])
        out.append(d)
    return out
