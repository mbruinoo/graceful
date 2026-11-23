from lib import *
import sys
def left_ok(p,S):
    return any(p[k-1]>1 and (p[:k-1]+(p[k-1]-1,)+p[k:]) in S for k in range(1,len(p)+1))
for n in range(4,int(sys.argv[1])+1):
    S=set(all_tree_placements(n)); shapes={}
    for p in S: shapes.setdefault(canon(p),[]).append(p)
    mins=[p for p in S if not left_ok(p,S)]
    ms={canon(p) for p in mins}
    miss=[c for c in shapes if c not in ms]
    print(n,"local minima",len(mins),"shapes",len(ms),"of",len(shapes))
    for c in miss:
        ex=shapes[c][0]; adj={}
        for x,y in edges(ex): adj.setdefault(x,[]).append(y); adj.setdefault(y,[]).append(x)
        print("   missing shape, degree sequence",sorted((len(v) for v in adj.values()),reverse=True),"example edges",edges(ex),"#placements",len(shapes[c]))
