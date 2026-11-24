# Independent check: P7 vertices that carry label 1 in a graceful labeling (labels 1..n,
# equivalently 0-rotatable) vs in a growth labeling (edges of length >= k connected for all k).
from itertools import permutations
n=7; E=[(i,i+1) for i in range(n-1)]
def connected(es):
    vs={v for e in es for v in e}; adj={v:set() for v in vs}
    for a,b in es: adj[a].add(b); adj[b].add(a)
    s=[next(iter(vs))]; seen={s[0]}
    while s:
        x=s.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); s.append(y)
    return seen==vs
zero=set(); anc=set()
for p in permutations(range(1,n+1)):
    L={e:abs(p[e[0]]-p[e[1]]) for e in E}
    if sorted(L.values())!=list(range(1,n)): continue
    v=p.index(1); zero.add(v)
    if all(connected([e for e in E if L[e]>=k]) for k in range(1,n)): anc.add(v)
print("label-1 vertices:",sorted(zero)); print("growth label-1 vertices:",sorted(anc))
