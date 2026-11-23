# filter: stdin tree lines (optionally "TAG: tree"); print trees that are NOT spiders with all legs <= 3
import sys
for l in sys.stdin:
    if ":" in l: l=l.split(":",1)[1]
    t=l.split()
    if not t or not t[0].isdigit(): continue
    n=int(t[0]); x=list(map(int,t[1:])); adj=[[] for _ in range(n)]
    for a,b in zip(x[0::2],x[1::2]): adj[a].append(b); adj[b].append(a)
    big=[v for v in range(n) if len(adj[v])>=3]
    ok=False
    if len(big)==1:
        c=big[0]; ok=True
        for u in adj[c]:
            L=1; p=c; w=u
            while len(adj[w])==2: p,w=w,[y for y in adj[w] if y!=p][0]; L+=1
            if L>3: ok=False
    if not ok: print(l.strip())
