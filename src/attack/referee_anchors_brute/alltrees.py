# all trees on n vertices (networkx generator, not the claimant's): for every vertex
# (mode all) or every vertex of degree >= 4 (mode deg4) decide anchor-ness with ./ra
import sys,networkx as nx,subprocess,os,collections
from lib import *
n=int(sys.argv[1]); mode=sys.argv[2]
items=[];meta=[]
ntrees=0
for T in nx.nonisomorphic_trees(n):
    ntrees+=1
    E=list(T.edges())
    for v in T.nodes():
        d=T.degree(v)
        if mode=='deg4' and d<4: continue
        items.append((n,v,E)); meta.append((ntrees,d))
R=solve(items)
non=collections.Counter(); tot=collections.Counter(); nodesmax=0
treeHasMaxdegAnchor=collections.defaultdict(bool); allanch=collections.defaultdict(lambda:True)
for it,(ti,d),r in zip(items,meta,R):
    tot[d]+=1; nodesmax=max(nodesmax,r[1])
    if r[0]=='0':
        non[d]+=1; allanch[ti]=False
        if d>=3: print("  non-anchor deg",d,"root",it[1],"edges",it[2])
    else: allanch[ti]=True and allanch[ti]
print("n=%d mode=%s trees=%d vertices tested=%d non-anchors by degree=%s total non=%d trees all-anchor=%d maxnodes=%d"%(n,mode,ntrees,len(items),dict(sorted(non.items())),sum(non.values()),sum(1 for t in range(1,ntrees+1) if allanch[t]) if mode=='all' else -1,nodesmax))
