# Referee: Theorem S2. Replay the stated schedule, tree-test after every slide,
# check invariant S_t, and check every path certificate named in the proof.
import sys
def is_tree(p,n):
    par=list(range(n+1))
    def f(x):
        while par[x]!=x:
            par[x]=par[par[x]];x=par[x]
        return x
    for k in range(1,n):
        a,b=f(p[k]),f(p[k]+k)
        if a==b:return False
        par[a]=b
    return True
def run(a,b,certs=True):
    n=2*a+1+b
    F=[0]+[2]*(n-2)+[1]
    for j in range(1,a):F[2*j-1]=a+2-j
    T=lambda j:a+2-j
    p=[0]+[1]*(n-1)
    cnt=[0]
    def edges():
        return {frozenset((p[k],p[k]+k)):k for k in range(1,n)}
    def slide(k,path=None):
        assert p[k]<n-k,("off rail",a,b,k)
        if certs:
            assert path is not None,("no cert",a,b,k)
            E=edges()
            assert path[0]==p[k]+1 and path[-1]==p[k]+k+1,("cert ends",a,b,k,path)
            assert len(set(path))==len(path)
            ks=[E.get(frozenset(e)) for e in zip(path,path[1:])]
            assert None not in ks,("cert edge missing",a,b,k,path)
            assert k in ks,("cert misses bracket",a,b,k,path)
        p[k]+=1;cnt[0]+=1
        assert is_tree(p,n),("not tree",a,b,k)
    def tgt(k):  # target of odd bracket 2j-1
        return F[k]
    # Start
    slide(1,[2,1,3]); slide(2,[2,3,1,4])
    def inv(t):
        for k in range(1,n):
            if k==1: e=min(a+1,2*t+2)
            elif k%2==1 and 2<=(k+1)//2<=t+1:
                j=(k+1)//2; e=min(T(j),2*t+5-2*j)
            elif k%2==0 and k//2<=t+1 and k<=n-2: e=2
            else: e=1
            assert p[k]==e,("invariant",a,b,t,k,p[k],e)
    inv(0)
    for r in range(1,a):
        R=2*r+2; J=2*r+2-a
        # (a)
        if p[1]<a+1:
            assert 2*r<=a
            slide(1,[2*r+1,2*r,2,R] if r>1 else [3,2,4])
        else: assert not 2*r<=a
        # (b)
        for j in range(r+1,1,-1):
            k=2*j-1
            for s in range(2):
                if p[k]>=tgt(k):continue
                if j==r+1:
                    path=[2,R,1,R+1] if s==0 else [3,R,2,R+1,1,R+2]
                    if s==1: assert r<=a-2
                else:
                    q=R+1-2*j
                    # first slide from {q,R}
                    if p[k]==q:
                        path=[q+1,2,R,q,R+2,1,R+1]
                    else:
                        assert p[k]==q+1 and j>J
                        path=[q+2,R,2,q+1,R+1,1,R+2]
                slide(k,path)
        # (c)
        if p[1]<a+1:
            assert 2*r<a
            slide(1,[R,R-1,R+2,1,R+1])
        else: assert not 2*r<a
        # (d)
        if R<=n-2:
            if 2*r<a: path=[2,R,R+1,1,R+2]
            elif r==a-1: path=[2,R+1,1,R+2]
            else: path=[2,2*a-2*r,R+1,1,R+2]
            slide(R,path)
        inv(r)
    for k in range(2*a+1,n-1):
        slide(k,[2,k+1,1,k+2])
    assert p==F,("end",a,b)
    assert cnt[0]==(a-1)*(a+2)//2+a+b,("count",a,b,cnt[0])
    # shape: spider with a legs of length 2, b of length 1, centre 2
    adj={v:set() for v in range(1,n+1)}
    for k in range(1,n):
        adj[p[k]].add(p[k]+k);adj[p[k]+k].add(p[k])
    l1=l2=0
    for v in adj[2]:
        if len(adj[v])==1:l1+=1
        else:
            assert len(adj[v])==2
            w=(adj[v]-{2}).pop(); assert len(adj[w])==1; l2+=1
    assert (l2,l1)==(a,b) and len(adj[2])==a+b,("shape",a,b)
A=int(sys.argv[1]);B=int(sys.argv[2]);c=0
for a in range(2,A+1):
    for b in range(0,B+1):
        run(a,b);c+=1
print("S2 replay+certs+invariant OK for 2<=a<=%d, 0<=b<=%d (%d pairs)"%(A,B,c))
