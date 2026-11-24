# Independent check: does D(a;1,1) (centre with hubs of sizes a,1,1) have a growth placement
# (README sec.1: brackets longest first, each after the first adds exactly one new vertex)
# with the centre at label 1?  Exhaustive DFS.
import sys
def shape_ok(edges,n,c,sizes):
    adj={v:set() for v in range(1,n+1)}
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    cnt=[]
    for h in adj[c]:
        L=adj[h]-{c}
        if any(len(adj[l])!=1 for l in L): return False
        cnt.append(len(L))
    return sorted(cnt)==sorted(sizes)
def search(sizes):
    global N_; 
    n=1+len(sizes)+sum(sizes); c=1; found=[0]
    deg={v:0 for v in range(1,n+1)}
    target_c=len(sizes)
    def dfs(k,used,edges):
        if k==0:
            if shape_ok(edges,n,c,sizes): found[0]+=1
            return found[0]>0
        for p in range(1,n-k+1):
            a,b=p,p+k
            if (a in used)!=(b in used):
                new=b if a in used else a
                deg[a]+=1; deg[b]+=1
                if deg[c]<=target_c and max(deg[a],deg[b])<=max(sizes)+1:
                    used.add(new); edges.append((a,b))
                    if dfs(k-1,used,edges): return True
                    used.discard(new); edges.pop()
                deg[a]-=1; deg[b]-=1
        return False
    # first bracket (length n-1) is {1,n}: both new
    deg[1]+=1; deg[n]+=1
    dfs(n-2,{1,n},[(1,n)])
    return found[0]
for a in map(int,sys.argv[1:]):
    print("D(%d;1,1) n=%d centre-at-1 growth placements found:"%(a,a+5), search([a,1,1]))
