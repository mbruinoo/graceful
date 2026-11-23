# Read spider edge lists (centre = vertex 0, legs numbered consecutively) and print leg-length partitions.
import sys
for line in sys.stdin:
    x=list(map(int,line.split())); E=list(zip(x[::2],x[1::2])); n=len(E)+1
    adj=[[] for _ in range(n)]
    for a,b in E: adj[a].append(b); adj[b].append(a)
    c=max(range(n),key=lambda v:len(adj[v])); legs=[]
    for w in adj[c]:
        L=1; prev,cur=c,w
        while True:
            nx=[u for u in adj[cur] if u!=prev]
            if not nx: break
            prev,cur=cur,nx[0]; L+=1
        legs.append(L)
    print(tuple(sorted(legs,reverse=True)))
