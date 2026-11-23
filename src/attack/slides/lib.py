# Common helpers, written from README section 1.
import itertools, sys
def edges(p): return [(p[k-1], p[k-1]+k) for k in range(1,len(p)+1)]
def is_tree(p):
    n=len(p)+1; par=list(range(n+1))
    def f(x):
        while par[x]!=x: x=par[x]
        return x
    for a,b in edges(p):
        a,b=f(a),f(b)
        if a==b: return False
        par[a]=b
    return True
def all_tree_placements(n):
    out=[]
    def rec(k,p,par):
        if k==0: out.append(tuple(p[1:])); return
        for q in range(1,n-k+1):
            pp=par[:]
            a,b=q,q+k
            while pp[a]!=a:a=pp[a]
            while pp[b]!=b:b=pp[b]
            if a==b: continue
            pp[a]=b; p[k]=q; rec(k-1,p,pp)
    rec(n-1,[0]*n,list(range(n+1)))
    return out
def is_growth(p):
    n=len(p)+1; used={p[-1],p[-1]+n-1}
    for k in range(n-2,0,-1):
        a,b=p[k-1],p[k-1]+k
        if (a in used)==(b in used): return False
        used|={a,b}
    return True
def is_interval_growth(p):
    n=len(p)+1
    if p[-1]!=1: return False
    lo,hi=1,n  # used = 1..lo and hi..n
    for k in range(n-2,0,-1):
        a,b=p[k-1],p[k-1]+k
        ua=(a<=lo or a>=hi); ub=(b<=lo or b>=hi)
        if ua==ub: return False
        new=b if ua else a
        if new==lo+1: lo+=1
        elif new==hi-1: hi-=1
        else: return False
    return True
def canon(p):
    n=len(p)+1; adj=[[] for _ in range(n+1)]
    for a,b in edges(p): adj[a].append(b); adj[b].append(a)
    def enc(v,pa): return "("+"".join(sorted(enc(u,v) for u in adj[v] if u!=pa))+")"
    return min(enc(v,0) for v in range(1,n+1))
def right_reach(n,S=None):
    S=S or set(all_tree_placements(n))
    star=tuple([1]*(n-1)); seen={star}; q=[star]
    for p in q:
        for k in range(1,n):
            if p[k-1]<n-k:
                r=p[:k-1]+(p[k-1]+1,)+p[k:]
                if r in S and r not in seen: seen.add(r); q.append(r)
    return seen
