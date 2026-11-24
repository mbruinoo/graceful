# check claimant log labelings with referee checker; trees taken from claimant generator output (file 1),
# and compared (as rooted trees, canonical form) with the multiset of referee-generated trees (file 3)
import sys
from common import *
sys.setrecursionlimit(100000)
def canon(n,root,e):
    adj=[[] for _ in range(n)]
    for a,b in e: adj[a].append(b); adj[b].append(a)
    # iterative canonical form
    order=[]; par=[-1]*n; st=[root]
    while st:
        v=st.pop(); order.append(v)
        for w in adj[v]:
            if w!=par[v]: par[w]=v; st.append(w)
    c=[None]*n
    for v in reversed(order): c[v]="("+"".join(sorted(c[w] for w in adj[v] if w!=par[v]))+")"
    return c[root]
their=[parse_tree(l.lstrip("#")) for l in open(sys.argv[1]) if l.strip()]
logs=[l for l in open(sys.argv[2]) if l.startswith("#") and (" FOUND " in l or " NONE " in l or " CAP " in l)]
mine=sorted(canon(n,r,e) for _,n,r,e in (parse_tree(l) for l in open(sys.argv[3]) if l.strip()))
print("same instance multiset as referee generator:", mine==sorted(canon(n,r,e) for _,n,r,e in their), len(mine), len(their))
bad=0; found=0; byname={t[0]:t for t in their}; nolab=0
for l in logs:
    name=l.split()[0].lstrip("#")
    if " FOUND " not in l: print("not found:",l.strip()[:80]); continue
    found+=1
    if "labels:" not in l: nolab+=1; continue
    _,n,root,e=byname[name]; lab=list(map(int,l.split("labels:")[1].split()))
    ok,why=check(n,root,e,lab,n+1)
    if not ok: bad+=1; print("BAD",name,why)
    if len(sys.argv)>4: print(name,unused(n,e,lab,n+1))
print(sys.argv[2],"lines",len(logs),"found",found,"bad",bad,"without labels",nolab)
