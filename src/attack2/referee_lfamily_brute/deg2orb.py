"""Count non-anchor vertex orbits of a given degree on all n-vertex trees (orbit = rooted-isomorphism class within a tree).
Usage: python3 deg2orb.py n deg"""
import sys, subprocess, networkx as nx
n,dg=int(sys.argv[1]),int(sys.argv[2])
def canon(T,r):
    def f(x,p): return "("+"".join(sorted(f(y,x) for y in T[x] if y!=p))+")"
    return f(r,-1)
lines=[];meta=[]
for t,T in enumerate(nx.nonisomorphic_trees(n)):
    E=" ".join(f"{u} {v}" for u,v in T.edges()); seen=set()
    for r in T.nodes():
        if T.degree(r)!=dg: continue
        c=canon(T,r)
        if c in seen: continue
        seen.add(c); lines.append(f"{n} {r} {E}"); meta.append((t,r,any(T.degree(y)==1 for y in T[r])))
out=subprocess.run(["./rsolve","d","200000000"],input="\n".join(lines)+"\n",capture_output=True,text=True).stdout.split("\n")
nots=[m for m,o in zip(meta,out) if o.startswith("NOT")]
print(f"n={n} deg={dg} orbits={len(meta)} NOT orbits={len(nots)} with_leaf_nbr={sum(1 for m in nots if m[2])} CAP={sum(1 for o in out if o.startswith('CAP'))}")
