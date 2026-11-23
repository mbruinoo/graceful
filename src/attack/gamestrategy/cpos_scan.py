import sys
from explore import *
def solve_c(par, root, cvert, clab, limit=1):
    n=len(par); m=n-1
    adj=[[] for _ in range(n)]
    for v,p in enumerate(par):
        if p>=0: adj[v].append(p); adj[p].append(v)
    lab=[-1]*n; used=[False]*n; res=[]
    lab[root]=0; used[0]=True
    def rec(k, frontier):
        if k==0: res.append(lab[:]); return len(res)>=limit
        seen=set()
        for idx,(v,p) in enumerate(frontier):
            if len(adj[v])==1:
                if lab[p] in seen: continue
                seen.add(lab[p])
            for x in (lab[p]+k, lab[p]-k):
                if 0<=x<=m and not used[x]:
                    if v==cvert and x!=clab: continue
                    if v!=cvert and x==clab and lab[cvert]<0: continue
                    lab[v]=x; used[x]=True
                    nf=frontier[:idx]+frontier[idx+1:]+[(c,v) for c in adj[v] if c!=p]
                    if rec(k-1,nf): return True
                    lab[v]=-1; used[x]=False
        return False
    rec(m,[(v,root) for v in adj[root]])
    return res
if __name__=='__main__':
    N=int(sys.argv[1]); lo=int(sys.argv[2])
    for n in range(lo,N+1):
        m=n-1
        for a in d4trees(n):
            if min(a)==0: continue
            par,kind=build(a)
            ok=[cl for cl in range(1,m+1) if solve_c(par,1,0,cl)]
            print(n,a,'c labels (m=%d):'%m,ok,flush=True)
