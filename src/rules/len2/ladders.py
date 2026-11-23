# Which k admit a zigzag deal made only of "ladder cycles"?  Iterative deepening on the number r of ladders.
# Ladder type 1: P=[p,p+t], Q=[q,q+t-1], sums [p+q,p+q+2t-1], closing sum 2p+t   (t>=0; t=0 is a loop at p)
# Ladder type 2: P=[p,p+t-1], Q=[q,q+t], sums [p+q,p+q+2t-1], closing sum 2q+t   (t>=1)
# With a 4th argument M the label set is [M+1,2k] (a 'cap' that can be put on top of any deal for M/2 legs).
# Usage: ladders.py kmin kmax rmax [M]
import sys
kmin,kmax,rmax=map(int,sys.argv[1:4]); M=int(sys.argv[4]) if len(sys.argv)>4 else 0
def solve(k,r):
    N=2*k; used=[False]*(N+2)
    for i in range(M+1): used[i]=True
    pend=[]; out=[]
    def free(lo,hi): return hi<=N and not any(used[lo:hi+1])
    def setr(lo,hi,v):
        for i in range(lo,hi+1): used[i]=v
    def rec(left,need):
        # need = number of labels still uncovered
        l=1
        while l<=N and used[l]: l+=1
        if l>N: return not pend
        # pending Q start
        for idx,(typ,p,t) in enumerate(pend):
            q=l
            if typ==1: Q=(q,q+t-1); c=None
            else: Q=(q,q+t); c=2*q+t
            S=(p+q,p+q+2*t-1)
            if S[0]<=Q[1]: continue
            if not free(*Q) or (t>0 and not free(*S)): continue
            if c is not None and (c>N or used[c] or Q[0]<=c<=Q[1] or S[0]<=c<=S[1]): continue
            setr(*Q,True); setr(*S,True)
            if c: used[c]=True
            pend.pop(idx); out.append((typ,p,q,t))
            if rec(left,0): return True
            out.pop(); pend.insert(idx,(typ,p,t))
            setr(*Q,False); setr(*S,False)
            if c: used[c]=False
        if left==0: return False
        p=l
        for typ in (1,2):
            for t in range(0 if typ==1 else 1, k):
                P=(p,p+t) if typ==1 else (p,p+t-1)
                if not free(*P): break
                c=2*p+t if typ==1 else None
                if c is not None and (c>N or used[c]): continue
                setr(*P,True)
                if c: used[c]=True
                if typ==1 and t==0:
                    out.append((1,p,0,0))
                    ok=rec(left-1,0)
                    if ok: return True
                    out.pop()
                else:
                    pend.append((typ,p,t))
                    if rec(left-1,0): return True
                    pend.pop()
                setr(*P,False)
                if c: used[c]=False
        return False
    return out if rec(r,0) else None
for k in range(kmin,kmax+1):
    res=None
    for r in range(1,rmax+1):
        res=solve(k,r)
        if res: break
    if res or M==0: print(k, res if res else "none with r<=%d"%rmax, flush=True)
