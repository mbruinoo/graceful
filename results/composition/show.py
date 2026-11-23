#!/usr/bin/env python3
"""Describe trees given as nested parentheses (one per line on stdin): degree sequence, spider legs if a spider."""
import sys
def parse(s):
    par=[]; st=[]
    for ch in s:
        if ch=='(':
            par.append(st[-1] if st else -1); st.append(len(par)-1)
        else: st.pop()
    return par
for line in sys.stdin:
    s=line.strip()
    if not s: continue
    par=parse(s); n=len(par); adj=[[] for _ in range(n)]
    for i,p in enumerate(par):
        if p>=0: adj[i].append(p); adj[p].append(i)
    deg=[len(a) for a in adj]; big=[v for v in range(n) if deg[v]>=3]
    desc=""
    if len(big)==1:
        c=big[0]; legs=[]
        for x in adj[c]:
            l=1; prev=c
            while deg[x]==2:
                x,prev=[y for y in adj[x] if y!=prev][0],x; l+=1
            legs.append(l)
        desc="spider S(%s)"%",".join(map(str,sorted(legs,reverse=True)))
    elif not big: desc="path"
    edges=" ".join("%d-%d"%(p,i) for i,p in enumerate(par) if p>=0)
    print("n=%d %s  %s  edges: %s"%(n,s,desc,edges))
