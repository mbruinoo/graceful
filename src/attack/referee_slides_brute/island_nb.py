# Referee: Theorem I. For each n, P and P' are trees and the only tree among
# their rail neighbours (p_k +-1) is the other one.
import sys
def is_tree(p,n):
    par=list(range(n+1))
    def f(x):
        while par[x]!=x:
            par[x]=par[par[x]];x=par[x]
        return x
    for k in range(1,n):
        if not 1<=p[k]<=n-k:return False
        a,b=f(p[k]),f(p[k]+k)
        if a==b:return False
        par[a]=b
    return True
bad=[]
for n in range(5,int(sys.argv[1])+1):
    P=[0]+[1]*(n-1);P[1]=2;P[2]=n-3;P[n-2]=2;P[n-1]=1
    Q=P[:];Q[1]=3
    ok=is_tree(P,n) and is_tree(Q,n)
    for X,Y in ((P,Q),(Q,P)):
        for k in range(1,n):
            for d in(-1,1):
                Z=X[:];Z[k]+=d
                if is_tree(Z,n) and Z!=Y: ok=False
    if not ok:bad.append(n)
print("n with {P,P'} NOT an isolated pair:",bad)
