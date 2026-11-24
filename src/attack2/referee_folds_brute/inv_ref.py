# referee: invariants vs tidy (my outputs), Spearman among non-caterpillars, pooled over given n
import sys
from collections import deque
def rank(v):
    idx=sorted(range(len(v)),key=lambda i:v[i]); r=[0]*len(v); i=0
    while i<len(v):
        j=i
        while j+1<len(v) and v[idx[j+1]]==v[idx[i]]: j+=1
        for k in range(i,j+1): r[idx[k]]=(i+j)/2
        i=j+1
    return r
def corr(a,b):
    n=len(a); ma=sum(a)/n; mb=sum(b)/n
    sa=sum((x-ma)**2 for x in a)**.5; sb=sum((y-mb)**2 for y in b)**.5
    return sum((x-ma)*(y-mb) for x,y in zip(a,b))/(sa*sb) if sa*sb>0 else float('nan')
def sp(a,b): return corr(rank(a),rank(b))
def far(adj,s,S):
    d={s:0};q=deque([s]);par={s:None}
    while q:
        x=q.popleft()
        for w in adj[x]:
            if w in S and w not in d: d[w]=d[x]+1;par[w]=x;q.append(w)
    t=max(d,key=d.get); return t,par
def invs(n,a):
    adj={i:set() for i in range(n)}
    for u,v in zip(a[::2],a[1::2]): adj[u].add(v); adj[v].add(u)
    leaves=[v for v in adj if len(adj[v])==1]; D=set(v for v in adj if len(adj[v])>1)
    dd={v:sum(1 for w in adj[v] if w in D) for v in D}
    dleaves=sum(1 for v in D if dd[v]<=1)
    if D:
        s=next(iter(D)); t,_=far(adj,s,D); u,par=far(adj,t,D); path=set(); x=u
        while x is not None: path.add(x); x=par[x]
        off=len(D)-len(path)
    else: off=0
    maxnl=max([sum(1 for w in adj[v] if len(adj[w])>1) for v in adj])
    dbranch=sum(1 for v in D if dd[v]>=3)
    # lobster: removing leaves of derived tree gives a path
    D2=set(v for v in D if dd[v]>1)
    lob = all(sum(1 for w in adj[v] if w in D2)<=2 for v in D2)
    cat = all(dd[v]<=2 for v in D)
    return cat,{'leaves-2':len(leaves)-2,'branch':sum(1 for v in adj if len(adj[v])>=3),'dleaves-2':dleaves-2,'offspine':off,'maxnonleafnbr':maxnl,'dbranch':dbranch,'lobster':int(lob)}
ns=list(map(int,sys.argv[1:]))
rows=[]
for n in ns:
    A=[l.split() for l in open(f"A{n}.out")]; B=[l.split() for l in open(f"B{n}.out")]
    for line,a,b in zip(open(f"t{n}.txt"),A,B):
        cat,I=invs(n,list(map(int,line.split()))); rows.append((cat,int(a[2]),int(b[2]),I))
print("trees",len(rows))
for key in rows[0][3]:
    for ci,c in ((1,'A'),(2,'B')):
        nc=[r for r in rows if not r[0]]
        rho=sp([r[ci] for r in nc],[r[3][key] for r in nc]); rall=sp([r[ci] for r in rows],[r[3][key] for r in rows])
        le=sum(1 for r in rows if r[ci]<=r[3][key]); eq=sum(1 for r in rows if r[ci]==r[3][key])
        print(f"{key:14s} {c}: rho_all={rall:.3f} rho_noncat={rho:.3f} tidy<=inv fails={len(rows)-le} tidy==inv {eq}")
