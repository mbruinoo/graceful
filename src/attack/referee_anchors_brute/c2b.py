# Lemma 0: v anchor of T'+d leaves at v  <=>  gapped labelling of T' in [0,m'+d]
import sys,networkx as nx
from lib import *
def gapped(n,v,E,top):
    adj={i:[] for i in range(n)}
    for a,b in E: adj[a].append(b); adj[b].append(a)
    order=[];par={v:None}
    st=[v]
    while st:
        u=st.pop(); order.append(u)
        for w in adj[u]:
            if w not in par: par[w]=u; st.append(w)
    lab={v:0}; ln={v:top+1}; usedL={0}; usedW=set()
    def rec(i):
        if i==len(order): return set(lab.values())-{0}==usedW
        u=order[i]; p=par[u]
        for w in range(1,min(ln[p],top+1)):
            if w in usedW: continue
            for x in (lab[p]+w,lab[p]-w):
                if 0<=x<=top and x not in usedL:
                    lab[u]=x; ln[u]=w; usedL.add(x); usedW.add(w)
                    if rec(i+1): return True
                    usedL.discard(x); usedW.discard(w); del lab[u]
        return False
    return rec(1)
N=int(sys.argv[1]); DMAX=int(sys.argv[2]); cnt=0; bad=0; pos=0
for n in range(1,N+1):
    for T in nx.nonisomorphic_trees(n) if n>1 else [nx.empty_graph(1)]:
        E=list(T.edges())
        for v in T.nodes():
            items=[]
            for d in range(0,DMAX+1):
                items.append((n+d,v,E+[(v,n+i) for i in range(d)]))
            R=solve(items) if n+DMAX>1 else None
            for d,r in enumerate(R):
                if n+d<2: continue
                g=gapped(n,v,E,n-1+d); cnt+=1; pos+= (r[0]=='1')
                if g!=(r[0]=='1'): bad+=1; print("MISMATCH",n,v,E,d,g,r[0])
    print("n'<=%d d<=%d: cases %d (anchor in %d), mismatches %d"%(n,DMAX,cnt,pos,bad)); sys.stdout.flush()
