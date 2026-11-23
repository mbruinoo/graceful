# Which feature of a tree predicts the least number of skips it needs?   Usage: skipfeat.py file...
import sys, collections
def feats(n,E):
    adj=[[] for _ in range(n)]
    for a,b in E: adj[a].append(b); adj[b].append(a)
    deg=[len(a) for a in adj]
    def bfs(s):
        d=[-1]*n; d[s]=0; q=[s]
        for u in q:
            for v in adj[u]:
                if d[v]<0: d[v]=d[u]+1; q.append(v)
        return d
    d0=bfs(0); a=max(range(n),key=lambda v:d0[v]); da=bfs(a); b=max(range(n),key=lambda v:da[v]); db=bfs(b); diam=da[b]
    path={v for v in range(n) if da[v]+db[v]==diam}
    # distance of each vertex from the longest path (one of them)
    dist=[min(1 if any(u in path for u in adj[v]) else 9 for _ in [0]) if v not in path else 0 for v in range(n)]
    far=0
    q=list(path); dd={v:0 for v in path}
    for u in q:
        for v in adj[u]:
            if v not in dd: dd[v]=dd[u]+1; q.append(v)
    far=max(dd.values())
    branch=sum(1 for v in range(n) if deg[v]>=3)
    inner=[v for v in range(n) if deg[v]>1]
    nonleafnb=max((sum(1 for u in adj[v] if deg[u]>1) for v in range(n)),default=0)
    b3=sum(1 for v in range(n) if sum(1 for u in adj[v] if deg[u]>1)>=3)      # vertices with >=3 non-leaf neighbours
    leaves=deg.count(1)
    return dict(diam=diam,far=far,branch=branch,maxdeg=max(deg),leaves=leaves,nonleafnb=nonleafnb,b3=b3,inner=len(inner))
rows=[]
for f in sys.argv[1:]:
    for line in open(f):
        s,e=line.split(":"); x=list(map(int,e.split())); E=list(zip(x[::2],x[1::2])); n=len(E)+1
        r=feats(n,E); r['s']=int(s); r['n']=n; rows.append(r)
print(len(rows),"trees")
for key in ["far","b3","nonleafnb","branch","maxdeg","diam"]:
    tab=collections.defaultdict(collections.Counter)
    for r in rows: tab[r[key]][r['s']]+=1
    print(f"\nby {key}:")
    for k in sorted(tab):
        c=tab[k]; tot=sum(c.values()); print(f"  {key}={k:2d}: n={tot:6d}  " + "  ".join(f"s={s}: {c[s]} ({100*c[s]/tot:.0f}%)" for s in sorted(c)))
