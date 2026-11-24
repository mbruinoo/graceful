# (1) S(2,2,1): all 720 bijections, growth property from README section 2 (brackets n-1..k connected for every k)
# (2) bridge equivalence, brute force for all trees with n<=7 and every leaf
import itertools
from thm import rooted_trees, labelings
def is_growth(n,edges,f):
    ln={}
    for (u,v) in edges:
        l=abs(f[u]-f[v])
        if l in ln: return None
        ln[l]=(u,v)
    if set(ln)!=set(range(1,n)): return None
    comp={f_:None for f_ in ()}
    used=set(ln[n-1])
    for k in range(n-2,0,-1):
        u,v=ln[k]
        if (u in used)==(v in used): return None
        used|={u,v}
    return ln
E=[(0,1),(1,2),(0,3),(3,4),(0,5)]
cnt=0; where={}
for perm in itertools.permutations(range(6)):
    ln=is_growth(6,E,perm)
    if ln: cnt+=1; where[ln[1]]=where.get(ln[1],0)+1
print("S(2,2,1): growth placements among 720 bijections:",cnt,"; length-1 bracket on edge:",where)
# bridge
def free_edges(par): return [(v,par[v]) for v in par if par[v] is not None]
bad=0;tot=0
for n in range(3,8):
    for par in rooted_trees(n):
        E=free_edges(par); deg=[0]*n
        for u,v in E: deg[u]+=1; deg[v]+=1
        gp=[]
        for perm in itertools.permutations(range(n)):
            ln=is_growth(n,E,perm)
            if ln: gp.append((perm,ln))
        for x in range(n):
            if deg[x]!=1: continue
            y=[u if v==x else v for (u,v) in E if x in (u,v)][0]
            lhs=any(set(ln[1])=={x,y} for perm,ln in gp)
            # rhs: T-x has a one-spare labeling (some root) with unused length 1 and unused label f(y)+-1
            rhs=False
            verts=[v for v in range(n) if v!=x]
            for r in verts:
                # root T-x at r
                adj={v:[] for v in verts}
                for u,v in E:
                    if x not in (u,v): adj[u].append(v); adj[v].append(u)
                order=[r]; p2={r:None}
                for u in order:
                    for w in adj[u]:
                        if w not in p2: p2[w]=u; order.append(w)
                idx={v:i for i,v in enumerate(order)}
                parr={idx[v]:(None if p2[v] is None else idx[p2[v]]) for v in order}
                for g in labelings(parr,n):       # n-1 vertices, labels 0..n-1 : slack 1
                    lens={abs(g[i]-g[parr[i]]) for i in parr if parr[i] is not None}
                    un=(set(range(n))-set(g.values())).pop()
                    if 1 not in lens and abs(un-g[idx[y]])==1: rhs=True; break
                if rhs: break
            tot+=1
            if lhs!=rhs: bad+=1; print("BRIDGE MISMATCH",n,E,x)
print("bridge equivalence: (rooted tree, leaf) cases n<=7 checked:",tot,"mismatches:",bad)
