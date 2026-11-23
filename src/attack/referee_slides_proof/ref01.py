# Referee checks for claims 0 and 1, written from README section 1 (own tree test, own path test).
import sys, itertools
def edges(p): return {frozenset((p[k-1], p[k-1]+k)) for k in range(1,len(p)+1)}
def adj(p):
    n=len(p)+1; A={v:set() for v in range(1,n+1)}
    for k in range(1,n): A[p[k-1]].add(p[k-1]+k); A[p[k-1]+k].add(p[k-1])
    return A
def is_tree(p):          # BFS connectivity + n-1 edges on n vertices
    n=len(p)+1
    if any(not(1<=p[k-1]<=n-k) for k in range(1,n)): return False
    A=adj(p); seen={1}; st=[1]
    while st:
        v=st.pop()
        for u in A[v]:
            if u not in seen: seen.add(u); st.append(u)
    return len(seen)==n
def F(a,b):
    n=2*a+1+b; p=[2]*(n-1); p[n-2]=1
    for j in range(1,a): p[2*j-2]=a+2-j
    return p
def is_spider2(p,a,b):
    A=adj(p); n=len(p)+1
    if len(A[2])!=a+b: return False
    legs2=legs1=0
    for u in A[2]:
        if len(A[u])==1: legs1+=1
        elif len(A[u])==2:
            w=(A[u]-{2}).pop()
            if len(A[w])==1: legs2+=1
            else: return False
        else: return False
    return legs2==a and legs1==b and 1+a*2+b==n
# ---------- claim 0, part 1: backward search from F to the star (left slides), no schedule
def back_reach(p):
    n=len(p)+1; star=tuple([1]*(n-1)); seen={tuple(p)}; st=[tuple(p)]
    while st:
        q=st.pop()
        if q==star: return True
        for k in range(1,n):
            if q[k-1]>1:
                r=q[:k-1]+(q[k-1]-1,)+q[k:]
                if r not in seen and is_tree(r): seen.add(r); st.append(r)
    return False
# ---------- claim 0, part 2: replay schedule, with the proof's named paths checked
class Bad(Exception): pass
def replay(a,b,certs=True):
    n=2*a+1+b; p=[1]*(n-1); T=lambda j:a+2-j; count=[0]
    def slide(k,path=None,capped_target=None):
        if capped_target is not None and p[k-1]>=capped_target: 
            if path is not None: raise Bad("proof says slide happens but capped k=%d"%k)
            return False
        old=frozenset((p[k-1],p[k-1]+k))
        if certs:
            if path is None: raise Bad("slide happens with no certificate k=%d a=%d b=%d"%(k,a,b))
            E=edges(p)
            if len(set(path))!=len(path): raise Bad("path repeats vertex")
            pe=[frozenset(x) for x in zip(path,path[1:])]
            if any(e not in E for e in pe): raise Bad("path edge missing %r k=%d a=%d b=%d p=%r"%(path,k,a,b,p))
            if old not in pe: raise Bad("path misses bracket")
            if path[0]!=p[k-1]+1 or path[-1]!=p[k-1]+1+k: raise Bad("path ends wrong %r k=%d"%(path,k))
        p[k-1]+=1; count[0]+=1
        if not is_tree(p): raise Bad("not a tree a=%d b=%d k=%d"%(a,b,k))
        return True
    slide(1,[2,1,3]); slide(2,[2,3,1,4])
    def inv(t):
        want=[1]*(n-1); want[0]=min(a+1,2*t+2)
        for j in range(2,t+2): want[2*j-2]=min(T(j),2*t+5-2*j)
        for i in range(1,t+2):
            if 2*i<=n-2: want[2*i-1]=2
        if want!=p: raise Bad("invariant fails t=%d a=%d b=%d"%(t,a,b))
    inv(0)
    for r in range(1,a):
        R=2*r+2; J=2*r+2-a
        # (a)
        if 2*r<=a: slide(1,[2*r+1,2*r,2,R] if r>1 else [3,2,4],a+1)
        else: slide(1,None,a+1)
        if 2*r<=a and (p[0],p[0]+1)!=(R-1,R): raise Bad("br1 after (a)")
        # (b) j=r+1
        k=2*r+1
        slide(k,[2,R,1,R+1],T(r+1))
        if r<=a-2: slide(k,[3,R,2,R+1,1,R+2],T(r+1))
        else: slide(k,None,T(r+1))
        for j in range(r,1,-1):
            k=2*j-1; q=R+1-2*j
            if j>=J:
                slide(k,[q+1,2,R,q,R+2,1,R+1],T(j))
                if j>J: slide(k,[q+2,R,2,q+1,R+1,1,R+2],T(j))
                else: slide(k,None,T(j))
            else:
                slide(k,None,T(j)); slide(k,None,T(j))
        # (c)
        if 2*r<a: slide(1,[R,R-1,R+2,1,R+1],a+1)
        else: slide(1,None,a+1)
        # (d)
        if 2*r+2<=n-2:
            if 2*r<a: path=[2,R,R+1,1,R+2]
            elif r==a-1: path=[2,R+1,1,R+2]
            else: path=[2,2*a-2*r,R+1,1,R+2]
            slide(2*r+2,path)
        inv(r)
    for k in range(2*a+1,n-1): slide(k,[2,k+1,1,k+2])
    if p!=F(a,b): raise Bad("end state")
    if count[0]!=(a-1)*(a+2)//2+a+b: raise Bad("count")
    return True
if __name__=="__main__":
    what=sys.argv[1]
    if what=="back":
        N=int(sys.argv[2])
        for a in range(2,N):
            for b in range(0,N):
                n=2*a+1+b
                if n>N: continue
                p=F(a,b); assert is_tree(p) and is_spider2(p,a,b),(a,b)
                assert back_reach(p),(a,b)
                print("a=%d b=%d n=%d: tree, spider, right-reachable (backward search)"%(a,b,n)); sys.stdout.flush()
    if what=="replay":
        A=int(sys.argv[2]); B=int(sys.argv[3]); c=0
        for a in range(2,A+1):
            for b in range(0,B+1):
                p=F(a,b); assert is_tree(p) and is_spider2(p,a,b),(a,b)
                replay(a,b); c+=1
        print("replay with proof certificates + invariant OK for 2<=a<=%d, 0<=b<=%d (%d pairs)"%(A,B,c))
    if what=="island":
        N=int(sys.argv[2])
        for n in range(5,N+1):
            res=[]
            for p1 in (2,3):
                p=[1]*(n-1); p[0]=p1; p[1]=n-3; p[n-3]=2
                ok=is_tree(p); nb=[]
                for k in range(1,n):
                    for s in (-1,1):
                        q=p[:]; q[k-1]+=s
                        if is_tree(q): nb.append((k,s))
                res.append((ok,nb))
            good = res[0]==(True,[(1,1)]) and res[1]==(True,[(1,-1)])
            print("n=%d island {P,P'}: %s %r"%(n,"OK" if good else "FAILS",res if not good else ""))
