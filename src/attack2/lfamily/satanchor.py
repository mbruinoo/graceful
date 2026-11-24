#!/usr/bin/env python3
# satanchor.py [solver] < queries   -- anchor test by SAT (independent of the DFS programs).
# Query lines "n v u1 w1 u2 w2 ..." (as anchq / ascan2 q; text after the pattern "| " prefix is accepted too).
# v is an anchor  <=>  there is a graceful labelling (labels 0..n-1, v = 0) whose edge lengths strictly
# decrease along every path away from v (README Theorem 7).  Encoding: x[u][a] = "u has label a",
# y[w][k] = "the edge from w to its parent has length k"; exactly-one constraints for vertices, labels,
# lengths; x[p][a] & x[w][b] -> y[w][|a-b|]; y[w][k] -> not y[child][k'] for k' >= k; siblings with isomorphic
# subtrees are ordered by edge length (symmetry breaking, exact).  SAT answers are re-checked from the definition.
import sys, time
from pysat.solvers import Solver
def solve(n, v, edges, name):
    adj=[[] for _ in range(n)]
    for a,b in edges: adj[a].append(b); adj[b].append(a)
    par=[-1]*n; order=[v]; 
    for u in order:
        for w in adj[u]:
            if w!=par[u]: par[w]=u; order.append(w)
    ch=[[w for w in adj[u] if w!=par[u]] for u in range(n)]
    canon={}
    for u in reversed(order): canon[u]="("+"".join(sorted(canon[w] for w in ch[u]))+")"
    m=n-1
    X=lambda u,a: 1+u*n+a
    Y=lambda w,k: 1+n*n+w*n+k          # k in 1..m
    cl=[]
    def exactly_one(lits):
        cl.append(list(lits))
        for i in range(len(lits)):
            for j in range(i): cl.append([-lits[i],-lits[j]])
    cl.append([X(v,0)])
    for u in range(n): exactly_one([X(u,a) for a in range(n)])
    for a in range(n): exactly_one([X(u,a) for u in range(n)])
    nonroot=[w for w in range(n) if w!=v]
    for w in nonroot: exactly_one([Y(w,k) for k in range(1,n)])
    for k in range(1,n): exactly_one([Y(w,k) for w in nonroot])
    for w in nonroot:
        p=par[w]
        for a in range(n):
            for b in range(n):
                if a!=b: cl.append([-X(p,a),-X(w,b),Y(w,abs(a-b))])
        if p!=v:
            for k in range(1,n):
                for k2 in range(k,n): cl.append([-Y(p,k),-Y(w,k2)])
    for u in range(n):                      # isomorphic siblings: lengths increasing in vertex order
        for i,w1 in enumerate(ch[u]):
            for w2 in ch[u][i+1:]:
                if canon[w1]==canon[w2]:
                    for k in range(1,n):
                        for k2 in range(1,k): cl.append([-Y(w1,k),-Y(w2,k2)])
    s=Solver(name=name,bootstrap_with=cl); t=time.time(); r=s.solve()
    if r:
        mod=set(l for l in s.get_model() if l>0); lab=[next(a for a in range(n) if X(u,a) in mod) for u in range(n)]
        assert sorted(lab)==list(range(n)) and lab[v]==0
        ln={w:abs(lab[w]-lab[par[w]]) for w in nonroot}
        assert sorted(ln.values())==list(range(1,n))
        assert all(par[w]==v or ln[w]<ln[par[w]] for w in nonroot)
        return "ANCHOR", time.time()-t, lab
    return "NOT", time.time()-t, None
name=sys.argv[1] if len(sys.argv)>1 else "cadical153"
for line in sys.stdin:
    if "|" in line: line=line.split("|",1)[1]
    t=line.split()
    if len(t)<4: continue
    n=int(t[0]); v=int(t[1]); e=[(int(t[i]),int(t[i+1])) for i in range(2,len(t),2)]
    r,sec,lab=solve(n,v,e,name)
    print(r,"%.1fs"%sec,name,"|",line.strip(), ("| labels "+" ".join(map(str,lab))) if lab else ""); sys.stdout.flush()
