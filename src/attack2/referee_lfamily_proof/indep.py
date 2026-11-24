# Independent referee check (written from README definitions; no project code reused).
# anchor(): graceful labelling 0..m with v=0 and edge lengths strictly decreasing away from v
# (README Theorem 7).  Edges are assigned longest first; each new edge hangs an unplaced
# neighbour y off a placed vertex x.  Unplaced leaves of the same x are interchangeable.
import sys, itertools
def anchor(n, edges, v):
    adj=[[] for _ in range(n)]
    for a,b in edges: adj[a].append(b); adj[b].append(a)
    m=n-1; lab=[-1]*n; used=[False]*(m+1); lab[v]=0; used[0]=True; placed=[v]
    def rec(k):
        if k==0: return True
        for x in list(placed):
            seenleaf=False
            for y in adj[x]:
                if lab[y]!=-1: continue
                if len(adj[y])==1:
                    if seenleaf: continue
                    seenleaf=True
                for ly in (lab[x]+k, lab[x]-k):
                    if 0<=ly<=m and not used[ly]:
                        lab[y]=ly; used[ly]=True; placed.append(y)
                        if rec(k-1): return True
                        placed.pop(); used[ly]=False; lab[y]=-1
        return False
    return rec(m)
def L(l,p,q):
    # v=0, c=1, P=2, Q=3
    e=[(0,1),(1,2),(1,3)]; k=4
    for _ in range(p): e.append((2,k)); k+=1
    for _ in range(q): e.append((3,k)); k+=1
    for _ in range(l): e.append((0,k)); k+=1
    return k,e
def R(p,q,d):
    # all solutions of reduced problem: returns list of (labelP,labelQ)
    N=p+q+2+d; a=N+1; out=set()
    for gP in range(1,N+1):
        for gQ in range(1,N+1):
            if gP==gQ: continue
            xP,xQ=a-gP,a-gQ
            # assign lengths 1..N: each either gap (label=length), xP, xQ, P-leaf (up/down), Q-leaf
            labused={gP,gQ}; lenused={xP,xQ}
            if xP==xQ: continue
            res=[]
            def rec(w,cp,cq,cd):
                if w==0:
                    return cp==p and cq==q and cd==d
                if w in lenused: return rec(w-1,cp,cq,cd)
                # gap
                if cd<d and w not in labused:
                    labused.add(w)
                    if rec(w-1,cp,cq,cd+1): return True
                    labused.discard(w)
                for (g,x,isP) in ((gP,xP,True),(gQ,xQ,False)):
                    if w>=x: continue
                    if isP and cp>=p: continue
                    if not isP and cq>=q: continue
                    for lb in (g+w,g-w):
                        if 1<=lb<=N and lb not in labused:
                            labused.add(lb)
                            if rec(w-1,cp+isP,cq+(not isP),cd): return True
                            labused.discard(lb)
                return False
            if rec(N,0,0,0): out.add((gP,gQ))
    return sorted(out)
if __name__=="__main__":
    cmd=sys.argv[1]
    if cmd=="L":
        l,p,q=map(int,sys.argv[2:5]); n,e=L(l,p,q); print(f"L({l};{p},{q}) n={n} v anchor={anchor(n,e,0)}")
    if cmd=="R":
        p,q,d=map(int,sys.argv[2:5]); print(f"R({p},{q},{d}) feasible (P,Q) hub labels:",R(p,q,d))
