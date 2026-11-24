# referee checks of Theorems G, S, W, P (constructions re-implemented from the claim text) -- thms.py G|S|W|P|COR
import sys, itertools, random
import networkx as nx
from common import *
def rooted(n,root,edges):
    adj=[[] for _ in range(n)]
    for a,b in edges: adj[a].append(b); adj[b].append(a)
    par=[-1]*n; dep=[0]*n; ch=[[] for _ in range(n)]; st=[root]; seen={root}
    while st:
        v=st.pop()
        for w in adj[v]:
            if w not in seen: seen.add(w); par[w]=v; dep[w]=dep[v]+1; ch[v].append(w); st.append(w)
    return par,dep,ch
def enum(n,root,edges,N):
    """all relaxed growth labelings with labels 0..N-1 (longest-first; complete because parent edges are longer)"""
    par,dep,ch=rooted(n,root,edges); lab=[-1]*n; lab[root]=0; used=[False]*N; used[0]=True
    def rec(L,cnt):
        if cnt==n: yield list(lab); return
        if n-cnt>L: return
        for u in range(n):
            if lab[u]<0: continue
            for c in ch[u]:
                if lab[c]>=0: continue
                for p in (lab[u]-L,lab[u]+L):
                    if 0<=p<N and not used[p]:
                        lab[c]=p; used[p]=True
                        yield from rec(L-1,cnt+1)
                        lab[c]=-1; used[p]=False
        yield from rec(L-1,cnt)
    yield from rec(N-1,1)
def trees(n):
    if n==1: return [[]]
    return [list(T.edges()) for T in nx.nonisomorphic_trees(n)]
def crossing(n,root,edges,lab):
    par,dep,ch=rooted(n,root,edges)
    ev=[lab[v] for v in range(n) if dep[v]%2==0]; od=[lab[v] for v in range(n) if dep[v]%2==1]
    if not od: return None
    return (max(ev),min(od)) if max(ev)<min(od) else None
def glue(nO,eO,y,q,eT,yT):
    """identify vertex y of O with yT of T''; returns n, edges, map of T'' vertices"""
    m={}; nxt=nO
    for z in range(q+1):
        if z==yT: m[z]=y
        else: m[z]=nxt; nxt+=1
    return nxt, eO+[(m[a],m[b]) for a,b in eT], m
def anchored(maxq):
    res=[]
    for q in range(0,maxq+1):
        for e in trees(q+1):
            for r in range(q+1):
                for tau in enum(q+1,r,e,q+1): res.append((q,e,r,tau))
    return res
def testG(maxn,maxq):
    A=anchored(maxq); cnt=0; inst=0
    for n in range(2,maxn+1):
        for e in trees(n):
            for r in range(n):
                for s in (0,1,2):
                    R=n-1+s
                    for g in enum(n,r,e,R+1):
                        cr=crossing(n,r,e,g)
                        if not cr: continue
                        inst+=1; mx,mn=cr
                        for a in range(mx,mn):          # every admissible threshold
                            for yl,high in ((mn,True),(mx,False)):
                                y=g.index(yl)
                                for q,eT,yT,tau in A:
                                    N2,e2,m=glue(n,e,y,q,eT,yT); f=[None]*N2
                                    for z in range(n): f[z]=g[z] if g[z]<=a else g[z]+q
                                    for z in range(q+1):
                                        val=g[y]+q-tau[z] if high else g[y]+tau[z]
                                        if m[z]==y: assert f[y]==val,("y mismatch",n,e,r,g,a,high)
                                        f[m[z]]=val
                                    ok,why=check(N2,r,e2,f,R+q+1)
                                    assert ok,("G FAILS",n,e,r,g,a,high,q,eT,yT,tau,f,why)
                                    cnt+=1
    print("G: crossing labelings",inst,"glued labelings checked",cnt,"all ok (O n<=%d, slack 0..2, q<=%d)"%(maxn,maxq))
def testS(maxn,maxq,maxh):
    A=anchored(maxq); cnt=0
    for n in range(2,maxn+1):
        R=n-1
        for e in trees(n):
            for r in range(n):
                for g in enum(n,r,e,n):
                    cr=crossing(n,r,e,g)
                    if not cr: continue
                    a=cr[0]; assert cr[1]==a+1
                    for ver in ("low","high"):
                        if ver=="low":
                            if a<1: continue
                            x=g.index(a-1); y=g.index(a)
                        else:
                            if a>R-2: continue
                            x=g.index(a+2); y=g.index(a+1)
                        for q,eT,yT,tau in A:
                            for h in range(maxh+1):
                                D=q+h+1; N2,e2,m=glue(n,e,y,q,eT,yT); f=[None]*(N2+h)
                                for z in range(n): f[z]=g[z] if g[z]<=a else g[z]+D
                                for z in range(q+1):
                                    val=a+tau[z] if ver=="low" else a+1+D-tau[z]
                                    if m[z]==y: assert f[y]==val
                                    f[m[z]]=val
                                e3=list(e2)
                                for i in range(1,h+1):
                                    e3.append((x,N2+i-1)); f[N2+i-1]=(a-1)+(q+1+i) if ver=="low" else (a+2+D)-(q+1+i)
                                nn=N2+h; assert nn==R+1+q+h
                                ok,why=check(nn,r,e3,f,nn+1)
                                assert ok,("S FAILS",ver,n,e,r,g,q,eT,yT,tau,h,f,why)
                                ul,uk=unused(nn,e3,f,nn+1)
                                assert uk==[q+1] and ul==[a+q+h+1 if ver=="low" else a+1],("S unused wrong",ver,ul,uk)
                                cnt+=1
    print("S: labelings checked",cnt,"all ok incl. unused label/length (O n<=%d any crossing growth placement, q<=%d any anchored T'', h<=%d)"%(maxn,maxq,maxh))
def hubs(ks):
    e=[]; nxt=1; hs=[]
    for k in ks: e.append((0,nxt)); hs.append(nxt); nxt+=1
    lv=[]
    for h,k in zip(hs,ks):
        l=[]
        for _ in range(k): e.append((h,nxt)); l.append(nxt); nxt+=1
        lv.append(l)
    return nxt,e,hs,lv
def testCOR(M):
    c=0
    for p in range(0,M+1):
        for q in range(0,M+1):
            n,e,hs,lv=hubs([p,q]); m=p+q+2; f=[None]*n; f[0]=0; f[hs[0]]=m+1; f[hs[1]]=m
            for i,z in enumerate(lv[1]): f[z]=m-1-i
            for i,z in enumerate(lv[0]): f[z]=m-q-1-i
            ok,why=check(n,0,e,f,n+1); assert ok,("S1 fails",p,q,why)
            ul,uk=unused(n,e,f,n+1); assert (ul,uk)==([1],[q+1]),("S1 unused",p,q,ul,uk); c+=1
    print("Cor S1 (DH(p,q) explicit): ok for all 0<=p,q<=%d (%d)"%(M,c)); c=0
    for l in range(0,12):
        for h1 in range(0,22):
            for h2 in range(0,22):
                # v=0,c=1,g1=2,g2=3
                e=[(0,1),(1,2),(1,3)]; f=[0,h1+h2+4,2,1]; nxt=4
                for i in range(h1): e.append((2,nxt)); f.append(3+i); nxt+=1
                for i in range(h2): e.append((3,nxt)); f.append(h1+3+i); nxt+=1
                for i in range(l): e.append((0,nxt)); f.append(h1+h2+5+i); nxt+=1
                ok,why=check(nxt,0,e,f,nxt+1); assert ok,("S2 fails",l,h1,h2,why)
                ul,uk=unused(nxt,e,f,nxt+1); assert (ul,uk)==([h1+h2+3],[h1+1]),("S2 unused",ul,uk); c+=1
    print("Cor S2 (L(l;h1,h2) explicit): ok for l<12, h1,h2<22 (%d)"%c); c=0
    for k in range(1,200):
        n,e,hs,lv=hubs([k,1,1]); f=[None]*n; f[0]=0; f[hs[0]]=k+4; f[hs[1]]=k+5; f[hs[2]]=k+6
        f[lv[1][0]]=k+3; f[lv[2][0]]=k+2; bl=[k+1]+[k+4-w for w in range(5,k+4)]
        assert len(bl)==k
        for z,v in zip(lv[0],bl): f[z]=v
        ok,why=check(n,0,e,f,n+1); assert ok,("H11k fails",k,why)
        ul,uk=unused(n,e,f,n+1); assert (ul,uk)==([k],[1]),("H unused",k,ul,uk); c+=1
    print("explicit H(1,1,k): ok for k=1..199")
def testW(maxr,maxleaves):
    def vecs(r,tot,mx):
        if r==0:
            yield (); return
        for x in range(min(tot,mx),-1,-1):
            for rest in vecs(r-1,tot-x,x): yield (x,)+rest
    cnt=0; nv=0; rnd=random.Random(1)
    for r in range(1,maxr+1):
        for tot in range(0,maxleaves+1):
            for a in vecs(r,tot,tot):
                if sum(a)!=tot: continue
                K=1+sum(a); d=sum(j*a[j] for j in range(1,r))
                C=sum((j-1)*a[j] for j in range(2,r))<=a[0]
                assert C==(d<=K-1)
                if not C: continue
                nv+=1; n,e,hs,lv=hubs(a); assert n==K+r
                for s in range(1,K-d+1):
                    for order in range(3):
                        blocks=[j for j in range(1,r) for _ in range(a[j])]
                        if order==1: blocks.reverse()
                        if order==2: rnd.shuffle(blocks)
                        f=[None]*n; f[0]=0
                        for j in range(r): f[hs[j]]=K+1+j
                        leaf=[[] for _ in range(r)]; p=s; inwin=set()
                        for j in blocks:
                            leaf[j].append(K+1+j-(p+j))
                            for w in range(p+1,p+j): leaf[0].append(K+1-w)
                            inwin.update(range(p+1,p+j+1)); p+=j
                        assert p==s+d
                        for w in range(1,K+1):
                            if w not in inwin and w!=s: leaf[0].append(K+1-w)
                        assert [len(x) for x in leaf]==list(a),("W counts",a,s)
                        for j in range(r):
                            for z,v in zip(lv[j],leaf[j]): f[z]=v
                        ok,why=check(n,0,e,f,n+1); assert ok,("W FAILS",a,s,f,why)
                        ul,uk=unused(n,e,f,n+1); assert (ul,uk)==([K+1-s-d],[s]),("W unused",a,s,ul,uk)
                        cnt+=1
    print("W: size vectors with (C):",nv,"labelings checked",cnt,"all ok (r<=%d, leaves<=%d, every s, 3 block orders)"%(maxr,maxleaves))
def pathtree(b,c):
    e=[]; p=0; A=[0]; B=[0]
    for i in range(1,b+1): e.append((p,i)); p=i; A.append(i)
    p=0
    for i in range(b+1,b+c+1): e.append((p,i)); p=i; B.append(i)
    return b+c+1,e,A,B
def zig(first_high,lows,highs,k):
    seq=[]; hi=iter(highs); lo=iter(lows)
    for i in range(k): seq.append(next(hi) if i%2==0 else next(lo))
    return seq
def piece(b):
    """returns (j, labels of arm A after root, labels of arm B after root) or None"""
    if b%4==2:
        t=(b-2)//4; R=4*t+4
        return 1, zig(True,range(1,R),[x for x in range(R,0,-1) if x!=3*t+3],b), [2*t+2]
    if b%4==1 and b>=5:
        t=(b-1)//4; R=4*t+3
        return 1, zig(True,range(1,R),[x for x in range(R,0,-1) if x!=3*t+2],b), [2*t+1]
    if b%4==0 and b>=4:
        t=b//4; R=4*t+3
        return 2, zig(True,[x for x in range(1,R) if x!=t+1],range(R-1,0,-1),b), [R,2*t+2]
    sp={3:([7,1,6],[4,2,3]),7:([11,1,10,2,9,4,8],[6,3,5]),11:([19,1,18,2,17,4,16,6,15,8,12],[14,3,11,5,10,7,9]),
        15:([19,1,18,2,17,3,16,5,15,6,13,7,11,8,10],[12,4,9])}
    if b in sp: return len(sp[b][1]),sp[b][0],sp[b][1]
    return None
def testP(M):
    cnt=0; covered=set(); pc=0
    for b in range(2,M+1):
        pz=piece(b)
        if not pz: continue
        j,LA,LB=pz; assert len(LA)==b and len(LB)==j
        n,e,A,B=pathtree(b,j); g=[None]*n; g[0]=0
        for v,l in zip(A[1:],LA): g[v]=l
        for v,l in zip(B[1:],LB): g[v]=l
        R=b+j+1
        ok,why=check(n,0,e,g,R+1); assert ok,("piece fails",b,g,why)
        cr=crossing(n,0,e,g); assert cr,("piece not crossing",b,g)
        y=B[-1]; high=(j%2==1); assert g[y]==(cr[1] if high else cr[0]),("tip not innermost",b,g)
        ul,uk=unused(n,e,g,R+1); pc+=1
        if b%4!=3:
            t=b//4; exp={2:(3*t+3,1),1:(3*t+2,1),0:(t+1,1)}[b%4]; assert (ul,uk)==([exp[0]],[exp[1]]),("piece unused",b,ul,uk)
        a=cr[0]
        for q in range(0,M+1):
            c=j+q
            n2,e2,A2,B2=pathtree(b,c); f=[None]*n2; f[0]=0
            sh=lambda x: x if x<=a else x+q
            for v,l in zip(A2[1:],LA): f[v]=sh(l)
            for v,l in zip(B2[1:j+1],LB): f[v]=sh(l)
            tau=[0]+zig(True,range(1,q+1),range(q,0,-1),q)   # zigzag growth placement of P_{q+1} from its end
            for i in range(1,q+1):
                f[B2[j+i]]= g[y]+q-tau[i] if high else g[y]+tau[i]
            ok,why=check(n2,0,e2,f,n2+1); assert ok,("P glued fails",b,c,f,why)
            cnt+=1; covered.add((b,c)); covered.add((c,b))
    # b=0,1 cases
    for n in range(2,2*M):
        for b in (0,1):
            c=n-1-b
            if c<b: continue
            n2,e2,A2,B2=pathtree(b,c); f=[None]*n2; f[0]=0
            top=n-1
            if b==1: f[A2[1]]=n-1; top=n-2
            hs=iter(range(top,0,-1)); ls=iter(range(1,n))
            for i,v in enumerate(B2[1:]): f[v]=next(hs) if i%2==0 else next(ls)
            ok,why=check(n2,0,e2,f,n2); assert ok,("b<=1 fails",b,c,f,why)
    unc=[(b,c) for b in range(2,M+1) for c in range(b,M+1) if (b,c) not in covered]
    exp=[(b,c) for b in range(2,M+1) for c in range(b,M+1) if b%4==3 and c%4==3 and b>=19]
    print("P: pieces ok",pc,"glued labelings checked",cnt,"; uncovered pairs 2<=b<=c<=%d:"%M,len(unc),"== predicted set:",unc==exp)
if __name__=="__main__":
    w=sys.argv[1]; a=list(map(int,sys.argv[2:]))
    {"G":testG,"S":testS,"W":testW,"P":testP,"COR":testCOR}[w](*a)
