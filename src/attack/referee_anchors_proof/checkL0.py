# Lemma 0: v anchor of T'+d leaves  <=>  gapped self-labelling of T' into [0,m'+d]. Exhaustive both sides.
import sys, subprocess, networkx as nx
from fam import line
def gapped(T,v,top):
    order=[v]; par={v:None}
    for u in order:
        for w in T[u]:
            if w!=par[u]: par[w]=u; order.append(w)
    f={v:0}; ln={}
    def rec(i):
        if i==len(order):
            return set(f.values())-{0}==set(ln.values())
        x=order[i]; p=par[x]
        for L in range(1,top+1):
            if L in f.values(): continue
            k=abs(L-f[p])
            if k in ln.values(): continue
            if p!=v and k>=ln[p]: continue
            f[x]=L; ln[x]=k
            if rec(i+1): return True
            del f[x]; del ln[x]
        return False
    return rec(1)
N=int(sys.argv[1]); DM=int(sys.argv[2]); lines=[]; exp=[]
for n in range(2,N+1):
    for T in nx.nonisomorphic_trees(n):
        for v in T.nodes():
            for d in range(0,DM+1):
                e=list(T.edges())+[(v,n+i) for i in range(d)]
                lines.append(line(n+d,e,v)); exp.append(gapped(T,v,n-1+d))
out=subprocess.run(["./gen","0"],input="\n".join(lines)+"\n",capture_output=True,text=True).stdout.split("\n")
bad=sum(1 for o,x in zip(out,exp) if o.startswith("YES")!=x)
print("cases",len(lines),"mismatches",bad,"non-anchor cases",sum(1 for x in exp if not x))
