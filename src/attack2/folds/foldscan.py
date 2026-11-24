# foldscan.py trees.txt results.out [more pairs ...] -- where do the non-staircase steps of the tidiest builds sit?
# For every step of every build: fold type (show.stype), time, number of hole cells H, and what is being attached:
#   parent degree, number of non-leaf neighbours of the parent ("branches meeting there"), whether the fresh vertex is a
#   leaf, distance of the parent from the centre of the tree.  Non-staircase steps are compared with staircase steps.
# NOTE the builds are whatever optimal build the solver returned, so type frequencies are not canonical; see REPORT.
import sys, collections, lib
from show import stype
def dist_from_centre(adj):
    c=lib.centres(adj); d={v:0 for v in c}; q=list(c)
    for v in q:
        for u in adj[v]:
            if u not in d: d[u]=d[v]+1; q.append(u)
    return d
rows=[]; ntrees=0; costs=collections.Counter()
args=sys.argv[1:]
for k in range(0,len(args),2):
    trees=[l for l in open(args[k]) if l.strip()]; res=lib.read_results(args[k+1]); assert len(trees)==len(res)
    for t,r in zip(trees,res):
        if r['labels'] is None: continue
        n,E,adj=lib.parse(t); steps=lib.replay(n,E,r['labels']); assert sum(s['costA'] for s in steps)==r['ub']; ntrees+=1; costs[r['ub']]+=1
        dc=dist_from_centre(adj); deg=[len(a) for a in adj]; nl=[sum(1 for u in adj[v] if deg[u]>1) for v in range(n)]
        for s in steps:
            p,c=s['parent'],s['child']
            rows.append(dict(ty=stype(s),cost=s['costA'],tau=1-s['t']/(n-2) if n>2 else 0,H=s['H'],pdeg=deg[p],pbr=nl[p],leaf=deg[c]==1,pdc=dc[p],n=n,
                             off=abs(s['y']-(s['main'][1]+1 if s['y']>s['x'] else s['main'][0]-1)) if s['inM'] else -1))
print('builds',ntrees,'steps',len(rows),'non-staircase',sum(r['cost'] for r in rows),' cost distribution',dict(sorted(costs.items())))
def summ(sel,name):
    if not sel: return
    m=len(sel); av=lambda f: sum(f(r) for r in sel)/m
    print(f'  {name:14s} {m:8d}  mean time {av(lambda r:r["tau"]):.2f}  early/mid/late {sum(1 for r in sel if r["tau"]<1/3)/m:.2f}/{sum(1 for r in sel if 1/3<=r["tau"]<2/3)/m:.2f}/{sum(1 for r in sel if r["tau"]>=2/3)/m:.2f}'
          f'  mean H before {av(lambda r:r["H"]):.2f}  fresh vertex is a leaf {av(lambda r:r["leaf"]):.2f}  parent deg>=3 {av(lambda r:r["pdeg"]>=3):.2f}'
          f'  parent has >=3 non-leaf nbrs {av(lambda r:r["pbr"]>=3):.2f}  mean parent dist from centre {av(lambda r:r["pdc"]):.2f}')
print('by fold type:')
summ([r for r in rows if r['cost']==0],'S (staircase)')
summ([r for r in rows if r['cost']==1],'all non-stair')
for ty,_ in collections.Counter(r['ty'] for r in rows if r['cost']).most_common(): summ([r for r in rows if r['ty']==ty and r['cost']],ty)
# staircase steps by depth of the partner below the tip of the opposite block (offset rule: = H)
oc=collections.Counter(r['H'] for r in rows if r['cost']==0)
print('staircase steps by number of hole cells H (= how deep under the tip of the opposite block the partner sits):',dict(sorted(oc.items())))
# enrichment: P(non-staircase | feature)
print('share of non-staircase steps among steps with a given feature:')
for nm,f in (('fresh vertex is a leaf',lambda r:r['leaf']),('fresh vertex is not a leaf',lambda r:not r['leaf']),('parent has >=3 non-leaf nbrs',lambda r:r['pbr']>=3),
             ('parent has <=2 non-leaf nbrs',lambda r:r['pbr']<=2),('parent deg 2',lambda r:r['pdeg']==2),('parent deg >=3',lambda r:r['pdeg']>=3),
             ('first third',lambda r:r['tau']<1/3),('middle third',lambda r:1/3<=r['tau']<2/3),('last third',lambda r:r['tau']>=2/3)):
    sel=[r for r in rows if f(r)]
    if sel: print(f'  {nm:30s} {sum(r["cost"] for r in sel)/len(sel):.3f}  ({len(sel)} steps)')
