# invariants.py N [treedir resultdir] -- tidy(T) against simple tree invariants, all trees on n <= N (cost A and B).
# Needs trees t<n>.txt (python3 ../../gentrees.py n) and data/all_{A,B}_<n>.txt (tidy.cpp output, same order).
import sys, collections, lib
def invs(n,adj):
    deg=[len(a) for a in adj]; L=sum(1 for d in deg if d==1); b3=sum(1 for d in deg if d>=3)
    inner=[v for v in range(n) if deg[v]>1]; iset=set(inner)
    d1={v:sum(1 for u in adj[v] if u in iset) for v in inner}          # degree in the derived tree T' = T minus leaves
    L1=sum(1 for v in inner if d1[v]<=1) if len(inner)>1 else len(inner)
    # longest path in T' (vertices)
    def far(s):
        dist={s:0}; st=[s]
        for v in st:
            for u in adj[v]:
                if u in iset and u not in dist: dist[u]=dist[v]+1; st.append(u)
        v=max(dist,key=dist.get); return v,dist[v]
    if inner:
        a,_=far(inner[0]); b,dd=far(a); lp=dd+1
    else: lp=0
    off=len(inner)-lp                                                   # vertices of T' off a longest path of T'
    maxbr=max((d1[v] for v in inner),default=0)                         # most non-leaf neighbours at one vertex
    inner2=[v for v in inner if d1[v]>1]                                # T'' = T' minus its leaves
    s2=set(inner2); d2={v:sum(1 for u in adj[v] if u in s2) for v in inner2}
    lobster=all(d<=2 for d in d2.values())
    b3d=sum(1 for v in inner if d1[v]>=3)                               # branch vertices of T'
    return dict(leaves_minus_2=L-2,branch_vertices=b3,derived_leaves_minus_2=max(0,L1-2),off_spine=off,max_branches=maxbr,
                derived_branch_vertices=b3d,lobster=int(lobster))
def spearman(xs,ys):
    def rank(v):
        o=sorted(range(len(v)),key=lambda i:v[i]); r=[0]*len(v); i=0
        while i<len(o):
            j=i
            while j+1<len(o) and v[o[j+1]]==v[o[i]]: j+=1
            for k in range(i,j+1): r[o[k]]=(i+j)/2
            i=j+1
        return r
    a,b=rank(xs),rank(ys); n=len(a); ma=sum(a)/n; mb=sum(b)/n
    va=sum((x-ma)**2 for x in a); vb=sum((y-mb)**2 for y in b)
    return sum((x-ma)*(y-mb) for x,y in zip(a,b))/(va*vb)**.5 if va*vb>0 else float('nan')
if __name__=='__main__':
    N=int(sys.argv[1]); tdir=sys.argv[2] if len(sys.argv)>2 else '.'; rdir=sys.argv[3] if len(sys.argv)>3 else 'data'
    rows=[]
    for n in range(4,N+1):
        trees=[l for l in open(f'{tdir}/t{n}.txt') if l.strip()]
        A=lib.read_results(f'{rdir}/all_A_{n}.txt'); B=lib.read_results(f'{rdir}/all_B_{n}.txt'); assert len(trees)==len(A)==len(B)
        for t,a,b in zip(trees,A,B):
            nn,E,adj=lib.parse(t); assert a['exact'] and b['exact']; d=invs(nn,adj); d.update(n=nn,cA=a['ub'],cB=b['ub']); rows.append(d)
    print(f'all trees on 4 <= n <= {N}: {len(rows)} trees')
    print('distribution of tidy by n (cost A | cost B):')
    for n in range(4,N+1):
        r=[x for x in rows if x['n']==n]; ca=collections.Counter(x['cA'] for x in r); cb=collections.Counter(x['cB'] for x in r)
        print(f'  n={n:2d} trees={len(r):6d}  A: '+' '.join(f'{k}:{ca[k]}' for k in sorted(ca))+'   B: '+' '.join(f'{k}:{cb[k]}' for k in sorted(cb)))
    names=['leaves_minus_2','branch_vertices','derived_leaves_minus_2','off_spine','max_branches','derived_branch_vertices','lobster']
    assert all((x['cA']==0)==(x['derived_leaves_minus_2']==0) for x in rows), 'tidy=0 iff caterpillar violated'
    print('tidy = 0 exactly for the caterpillars: holds for all',len(rows),'trees')
    for c in('cA','cB'):
        print(f'\n=== {c} against each invariant: equality, bounds, rank correlation; then the table (rows = invariant value) ===')
        for nm in names:
            eq=sum(1 for x in rows if x[c]==x[nm]); le=sum(1 for x in rows if x[c]<=x[nm]); ge=sum(1 for x in rows if x[c]>=x[nm])
            rho=spearman([x[c] for x in rows],[x[nm] for x in rows])
            nc=[x for x in rows if x['derived_leaves_minus_2']>0]; rho2=spearman([x[c] for x in nc],[x[nm] for x in nc])
            # is tidy a function of the invariant?  count values of the invariant on which tidy takes >1 value
            by=collections.defaultdict(collections.Counter)
            for x in rows: by[x[nm]][x[c]]+=1
            amb=sum(1 for v in by.values() if len(v)>1)
            print(f'{nm}: tidy==inv for {eq}/{len(rows)}; tidy<=inv for {le}; tidy>=inv for {ge}; Spearman rho={rho:.3f} (non-caterpillars only: {rho2:.3f}); invariant values with more than one tidy value: {amb}/{len(by)}')
            for k in sorted(by): print(f'      {nm}={k:2d}: '+'  '.join(f'tidy {t}: {by[k][t]}' for t in sorted(by[k])))
