# verify.py treefile logfile slack -- independent check, from the definition, of every FOUND line of spare.cpp.
# Relaxed growth labeling, labels 0..N-1 (N=n+slack), root at 0: injective, edge lengths pairwise distinct,
# lengths strictly decreasing along every path away from the root.  Also reports the unused labels/lengths.
import sys
trees={}
for l in open(sys.argv[1]):
    t=l.split(); 
    if not t: continue
    name=t[0]; n=int(t[1]); r=int(t[2]); e=[(int(t[3+2*i]),int(t[4+2*i])) for i in range(n-1)]; trees[name]=(n,r,e)
s=int(sys.argv[3]); ok=bad=other=0; show=len(sys.argv)>4
for l in open(sys.argv[2]):
    t=l.split()
    if not t: continue
    if "FOUND" not in t: other+=1; continue
    name=t[0]; n,r,e=trees[name]; lab=list(map(int,t[t.index("labels:")+1:])); N=n+s
    adj=[[] for _ in range(n)]
    for a,b in e: adj[a].append(b); adj[b].append(a)
    good = len(lab)==n and lab[r]==0 and len(set(lab))==n and all(0<=x<N for x in lab)
    par={r:None}; st=[r]; lens=set()
    while st and good:
        v=st.pop()
        for u in adj[v]:
            if u==par[v]: continue
            par[u]=v; d=abs(lab[u]-lab[v])
            if d in lens or d==0: good=False
            lens.add(d)
            if par[v] is not None and not d<abs(lab[v]-lab[par[v]]): good=False
            st.append(u)
    good = good and len(par)==n and len(lens)==n-1
    if good: ok+=1
    else: bad+=1; print("BAD",name)
    if show: print(name,"unused labels",sorted(set(range(N))-set(lab)),"unused lengths",sorted(set(range(1,N))-lens))
print("verified %d labelings, %d bad, %d lines without a labeling"%(ok,bad,other))
