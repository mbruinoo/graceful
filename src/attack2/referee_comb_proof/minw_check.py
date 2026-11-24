# Independent brute force: for multisets S whose logged least w exceeds the Lemma G bound,
# confirm no comb exists for any smaller w (comb defined by (L),(C) of REPORT section 1).
import sys, gzip, math, itertools
from functools import reduce
def feasible(S, w):
    k=len(S); y=k+sum(S)+w+1; N=y-1
    sizes=sorted(S)
    for H in itertools.combinations(range(1,y), k):
        hublen=set(y-h for h in H)
        for perm in set(itertools.permutations(sizes)):
            cap=dict(zip(H,perm))
            cell=[False]*(y)
            for h in H: cell[h]=True
            def dfs(u, fill):
                if u==y: return fill==w
                if u in hublen: return dfs(u+1, fill)
                # filler
                if fill<w and not cell[u]:
                    cell[u]=True
                    if dfs(u+1, fill+1): return True
                    cell[u]=False
                for h in H:
                    c=h+u
                    if cap[h]>0 and c<=y-1 and not cell[c]:
                        cap[h]-=1; cell[c]=True
                        if dfs(u+1, fill): return True
                        cap[h]+=1; cell[c]=False
                return False
            if dfs(1,0): return True
    return False
ex=[]
for line in gzip.open(sys.argv[1],'rt'):
    if not line.startswith('S'): continue
    p=line.split('|'); S=list(map(int,p[0].split()[1:])); w=int(p[1].split()[1])
    k=len(S); g=reduce(math.gcd,[s+2 for s in S]); w0=0
    while (k*(k+sum(S)+1+w0))%g: w0+=1
    if w>w0: ex.append((S,w))
print(len(ex),"exceptions")
bad=0
for S,w in ex:
    for w2 in range(w):
        if feasible(S,w2): print("FOUND comb with smaller w",S,w2,"logged",w); bad+=1
print("done; contradictions:",bad)
