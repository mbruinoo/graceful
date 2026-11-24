# Referee's own checks of Theorems G, S, W, P (written from the statements, not from check_thms.py)
import sys, itertools
def check(par, f, N):
    """par: dict child->parent (root has par None). f: dict vertex->label. relaxed growth labeling with range N (labels 0..N-1)."""
    V=list(par.keys()); labs=[f[v] for v in V]
    if len(set(labs))!=len(V): return "not injective"
    if min(labs)<0 or max(labs)>=N: return "range"
    root=[v for v in V if par[v] is None]
    if len(root)!=1 or f[root[0]]!=0: return "root"
    ln={v:abs(f[v]-f[par[v]]) for v in V if par[v] is not None}
    if len(set(ln.values()))!=len(ln): return "lengths repeat"
    for v in ln:
        p=par[v]
        if par[p] is not None and not ln[v]<ln[p]: return "not decreasing"
    return None
def rooted_trees(n):
    L=list(range(1,n+1))
    while True:
        par={0:None}; last={}
        for i,l in enumerate(L):
            if i>0: par[i]=last[l-1]
            last[l]=i
        yield par
        p=n-1
        while p>=0 and L[p]<=2: p-=1
        if p<0: return
        q=p-1
        while L[q]!=L[p]-1: q-=1
        for i in range(p,n): L[i]=L[i-(p-q)]
def labelings(par, N):
    """all relaxed growth labelings (brute force with early pruning), vertices 0..n-1 in preorder, root 0"""
    n=len(par); f={0:0}; used={0}; lens=set(); res=[]
    def rec(i):
        if i==n: res.append(dict(f)); return
        p=par[i]; pl=None if par[p] is None else abs(f[p]-f[par[p]])
        for x in range(N):
            if x in used: continue
            l=abs(x-f[p])
            if l in lens: continue
            if pl is not None and l>=pl: continue
            f[i]=x; used.add(x); lens.add(l); rec(i+1); used.discard(x); lens.discard(l); del f[i]
    rec(1); return res
def thresholds(par,f):
    """all a such that every edge joins a label <= a to a label > a"""
    out=[]
    for a in range(-1,max(f.values())+1):
        if all((f[v]<=a)!=(f[par[v]]<=a) for v in par if par[v] is not None): out.append(a)
    return out

def test_G(nmax,qmax,smax):
    anch=[]   # (par, tau)
    for q in range(0,qmax+1):
        for par in rooted_trees(q+1):
            for tau in labelings(par,q+1): anch.append((par,tau))
    cnt=0; bad=0
    for n in range(1,nmax+1):
        for par in rooted_trees(n):
            for s in range(0,smax+1):
                R=n-1+s
                for g in labelings(par,R+1):
                    if n==1: ths=[0]
                    else: ths=thresholds(par,g)
                    for a in ths:
                        used=sorted(g.values()); lows=[x for x in used if x<=a]; highs=[x for x in used if x>a]
                        cands=[]
                        if highs: cands.append((min(highs),'high'))
                        if lows: cands.append((max(lows),'low'))
                        inv={g[v]:v for v in g}
                        for gy,side in cands:
                            y=inv[gy]
                            for tpar,tau in anch:
                                q=len(tpar)-1
                                # build T: O vertices ('O',v), T'' vertices ('T',z) with ('T',0) identified with y
                                P={('O',v):(None if par[v] is None else ('O',par[v])) for v in par}
                                f={('O',v):(g[v] if g[v]<=a else g[v]+q) for v in par}
                                for z in tpar:
                                    if z==0: continue
                                    P[('T',z)]=('O',y) if tpar[z]==0 else ('T',tpar[z])
                                    f[('T',z)]=gy+q-tau[z] if side=='high' else gy+tau[z]
                                e=check(P,f,R+q+1); cnt+=1
                                if e: 
                                    bad+=1
                                    if bad<5: print("G COUNTEREXAMPLE",par,g,a,side,tpar,tau,e)
    print("G: nmax=%d qmax=%d smax=%d  glued labelings checked=%d  bad=%d"%(nmax,qmax,smax,cnt,bad))

def test_S(nmax,qmax,hmax):
    anch=[]
    for q in range(0,qmax+1):
        for par in rooted_trees(q+1):
            for tau in labelings(par,q+1): anch.append((par,tau))
    cnt=0; bad=0; vers={'low':0,'high':0}
    for n in range(2,nmax+1):
        for par in rooted_trees(n):
            R=n-1
            for g in labelings(par,R+1):
                inv={g[v]:v for v in g}
                for a in thresholds(par,g):
                    for ver in ('low','high'):
                        if ver=='low':
                            if not a>=1: continue
                            x=inv[a-1]; y=inv[a]
                        else:
                            if not a<=R-2: continue
                            x=inv[a+2]; y=inv[a+1]
                        for tpar,tau in anch:
                            q=len(tpar)-1
                            for h in range(0,hmax+1):
                                D=q+h+1; nn=R+1+q+h
                                P={('O',v):(None if par[v] is None else ('O',par[v])) for v in par}
                                f={('O',v):(g[v] if g[v]<=a else g[v]+D) for v in par}
                                for z in tpar:
                                    if z==0: continue
                                    P[('T',z)]=('O',y) if tpar[z]==0 else ('T',tpar[z])
                                    f[('T',z)]=a+tau[z] if ver=='low' else a+1+D-tau[z]
                                for i in range(1,h+1):
                                    P[('H',i)]=('O',x)
                                    f[('H',i)]=a+q+i if ver=='low' else a+1+D-q-i
                                assert len(P)==nn
                                e=check(P,f,nn+1); cnt+=1; vers[ver]+=1
                                if not e:
                                    ul=set(range(nn+1))-set(f.values()); uk=set(range(1,nn+1))-set(abs(f[v]-f[P[v]]) for v in P if P[v] is not None)
                                    pl=a+D if ver=='low' else a+1
                                    if ul!={pl} or uk!={q+1}: e="unused label/length %s %s predicted %d %d"%(ul,uk,pl,q+1)
                                if e:
                                    bad+=1
                                    if bad<5: print("S COUNTEREXAMPLE",ver,par,g,a,tpar,tau,h,e)
    print("S: nmax=%d qmax=%d hmax=%d  labelings checked=%d (%s) bad=%d"%(nmax,qmax,hmax,cnt,vers,bad))

def test_S_cor(M):
    bad=0;cnt=0
    for p in range(0,M+1):
        for q in range(0,M+1):
            m=p+q+2; P={'v':None,'c1':'v','c2':'v'}; f={'v':0,'c1':m+1,'c2':m}
            for i in range(q): P[('b',i)]='c2'; f[('b',i)]=m-1-i
            for i in range(p): P[('a',i)]='c1'; f[('a',i)]=m-q-1-i
            n=len(P); e=check(P,f,n+1); cnt+=1
            if not e:
                if set(range(n+1))-set(f.values())!={1}: e="unused label"
                if set(range(1,n+1))-set(abs(f[v]-f[P[v]]) for v in P if P[v])!={q+1}: e="unused len"
                if (p>0 and min(f[('a',i)] for i in range(p))!=2): e="c1 leaves do not end at 2"
            if e: bad+=1; print("S1 cor bad",p,q,e)
    print("Corollary S1 (DH(p,q), 0<=p,q<=%d): %d checked, bad=%d"%(M,cnt,bad))
    bad=0;cnt=0
    for l in range(0,M//3+1):
        for h1 in range(0,M+1):
            for h2 in range(0,M+1):
                P={'v':None,'c':'v','g1':'c','g2':'c'}; f={'v':0,'g2':1,'g1':2,'c':h1+h2+4}
                for i in range(h1): P[('a',i)]='g1'; f[('a',i)]=3+i
                for i in range(h2): P[('b',i)]='g2'; f[('b',i)]=h1+3+i
                for i in range(l): P[('r',i)]='v'; f[('r',i)]=h1+h2+5+i
                n=len(P); e=check(P,f,n+1); cnt+=1
                if not e:
                    if set(range(n+1))-set(f.values())!={h1+h2+3}: e="unused label"
                    if set(range(1,n+1))-set(abs(f[v]-f[P[v]]) for v in P if P[v])!={h1+1}: e="unused len"
                if e: bad+=1; print("S2 cor bad",l,h1,h2,e)
    print("Corollary S2 (L(l;h1,h2), l<=%d, h1,h2<=%d): %d checked, bad=%d"%(M//3,M,cnt,bad))

def parts(n,mx):
    if n==0: yield []; return
    for k in range(min(n,mx),0,-1):
        for r in parts(n-k,k): yield [k]+r
def W_build(a,s):
    r=len(a); K=1+sum(a); d=sum(j*a[j] for j in range(1,r))
    P={'v':None}; f={'v':0}
    for j in range(r): P[('x',j)]='v'; f[('x',j)]=K+1+j
    cnt=[0]*r
    def leaf(j,w):
        P[('l',j,cnt[j])]=('x',j); f[('l',j,cnt[j])]=K+1+j-w; cnt[j]+=1
    p=s; inwin=set()
    for j in range(1,r):
        for _ in range(a[j]):
            for w in range(p+1,p+j): leaf(0,w); inwin.add(w)
            leaf(j,p+j); inwin.add(p+j); p+=j
    assert p==s+d
    for w in range(1,K+1):
        if w!=s and w not in inwin: leaf(0,w)
    return P,f,cnt,K,d
def test_W(nmax,rmax):
    tot=0;sat=0;lab=0;bad=0
    for n in range(3,nmax+1):
        for pt in parts(n-1,n-1):
            a=[k-1 for k in pt]; tot+=1; r=len(a); K=1+sum(a); d=sum(j*a[j] for j in range(1,r))
            C=sum((j-1)*a[j] for j in range(2,r))<=a[0]
            assert C==(d<=K-1)
            if not C: continue
            sat+=1
            if r>rmax: continue
            for s in range(1,K-d+1):
                P,f,cnt,K,d=W_build(a,s); lab+=1
                e=None
                if cnt!=a: e="leaf counts %s"%cnt
                if len(P)!=n: e="size"
                e=e or check(P,f,n+1)
                if not e:
                    if set(range(n+1))-set(f.values())!={K+1-s-d}: e="unused label"
                    if set(range(1,n+1))-set(abs(f[v]-f[P[v]]) for v in P if P[v])!={s}: e="unused len"
                if e: bad+=1; print("W bad",a,s,e)
    print("W: depth<=2 rooted trees 3<=n<=%d: %d; satisfying (C): %d; labelings built (r<=%d, all s): %d; bad=%d"%(nmax,tot,sat,rmax,lab,bad))
def test_W_H(kmax):
    bad=0
    for k in range(1,kmax+1):
        P={'v':None,'B':'v','s1':'v','s2':'v','l1':'s1','l2':'s2'}; f={'v':0,'B':k+4,'s1':k+5,'s2':k+6,'l1':k+3,'l2':k+2}
        P[('b',3)]='B'; f[('b',3)]=k+1
        for w in range(5,k+4): P[('b',w)]='B'; f[('b',w)]=k+4-w
        n=len(P); e=None
        if n!=k+6: e="size"
        e=e or check(P,f,n+1)
        if not e:
            if set(range(n+1))-set(f.values())!={k}: e="unused label"
            if set(range(1,n+1))-set(abs(f[v]-f[P[v]]) for v in P if P[v])!={1}: e="unused len"
        if e: bad+=1; print("W-H bad",k,e)
    print("explicit H(1,1,k) labeling, k=1..%d: bad=%d"%(kmax,bad))

# ---- Theorem P
def zig(start, lo, hi, first_high, steps):
    """continue a zigzag from cell `start`, taking alternately the next unused high (hi, descending) and low (lo, ascending) cell"""
    seq=[]; cur=start; high=first_high
    for _ in range(steps):
        if high: seq.append(hi); hi-=1
        else: seq.append(lo); lo+=1
        high=not high
    return seq,lo,hi
def piece(b):
    """returns (A,B,j): label sequences of the arms from the root (root label 0 first), or None"""
    if b%4==2:
        t=(b-2)//4; R=4*t+4
        s1,lo,hi=zig(0,1,R,True,2*t+2); assert s1[-1]==t+1 and hi==3*t+3
        s2,lo,hi=zig(s1[-1],lo,hi-1,True,2*t)
        return [0]+s1+s2,[0,2*t+2],1
    if b%4==1 and b>=5:
        t=(b-1)//4; R=4*t+3
        s1,lo,hi=zig(0,1,R,True,2*t+2); assert s1[-1]==t+1 and hi==3*t+2
        s2,lo,hi=zig(s1[-1],lo,hi-1,True,2*t-1)
        return [0]+s1+s2,[0,2*t+1],1
    if b%4==0 and b>=4:
        t=b//4; R=4*t+3
        s1,lo,hi=zig(0,1,R-1,True,2*t+1); assert s1[-1]==3*t+2 and lo==t+1
        s2,lo,hi=zig(s1[-1],lo+1,hi,False,2*t-1)
        return [0]+s1+s2,[0,R,2*t+2],2
    sp={3:([0,7,1,6],[0,4,2,3]),7:([0,11,1,10,2,9,4,8],[0,6,3,5]),11:([0,19,1,18,2,17,4,16,6,15,8,12],[0,14,3,11,5,10,7,9]),
        15:([0,19,1,18,2,17,3,16,5,15,6,13,7,11,8,10],[0,12,4,9])}
    if b in sp: A,B=sp[b]; return A,B,len(B)-1
    return None
def path_check(A,B,N):
    P={('A',0):None}; f={('A',0):0}
    for i in range(1,len(A)): P[('A',i)]=('A',i-1); f[('A',i)]=A[i]
    for i in range(1,len(B)): P[('B',i)]=('A',0) if i==1 else ('B',i-1); f[('B',i)]=B[i]
    return check(P,f,N)
def piece_ok(b):
    pc=piece(b)
    if pc is None: return None
    A,B,j=pc
    assert len(A)==b+1 and len(B)==j+1
    n=b+j+1
    e=path_check(A,B,n+1)
    if e: return "piece not one-spare: "+e
    # crossing: even depth low, odd depth high
    ev=[A[i] for i in range(0,len(A),2)]+[B[i] for i in range(2,len(B),2)]
    od=[A[i] for i in range(1,len(A),2)]+[B[i] for i in range(1,len(B),2)]
    if not max(ev)<min(od): return "not crossing"
    y=B[-1]
    if j%2==1:
        if y!=min(od): return "y not innermost"
    else:
        if y!=max(ev): return "y not innermost"
    return (A,B,j,max(ev),'high' if j%2 else 'low')
def glue(b,c):
    """one-spare labeling for arms (b,c) from the piece for b, or None"""
    r=piece_ok(b)
    if r is None: return None
    assert not isinstance(r,str), (b,r)
    A,B,j,a,side=r
    if c<j: return None
    q=c-j; y=B[-1]
    sh=lambda x: x if x<=a else x+q
    A2=[sh(x) for x in A]; B2=[sh(x) for x in B]
    tau=[]; lo=0; hi=q
    for i in range(q+1):   # zigzag 0,q,1,q-1,...
        if i%2==0: tau.append(lo); lo+=1
        else: tau.append(hi); hi-=1
    yy=sh(y)
    ext=[(y+q-t) if side=='high' else (y+t) for t in tau]
    assert ext[0]==yy
    return A2,B2+ext[1:]
def test_P(M):
    bad=0; built=0; unc=[]
    for b in range(0,M+1):
        r=piece_ok(b)
        if isinstance(r,str): print("PIECE BAD",b,r); bad+=1
    for b in range(0,M+1):
        for c in range(b,M+1):
            n=b+c+1; ok=False
            if b==0:
                # zigzag 0,n-1,1,n-2...
                s,_,_=zig(0,1,n-1,True,c); e=path_check([0],[0]+s,n); ok=(e is None); 
                if e: print("b=0 bad",c,e); bad+=1
            elif b==1:
                s,_,_=zig(0,1,n-2,True,c); e=path_check([0,n-1],[0]+s,n); ok=(e is None)
                if e: print("b=1 bad",c,e); bad+=1
            else:
                for (x,yv) in ((b,c),(c,b)):
                    g=glue(x,yv)
                    if g:
                        A,B=g; assert len(A)==x+1 and len(B)==yv+1
                        e=path_check(A,B,n+1); built+=1
                        if e: print("glue bad",x,yv,e); bad+=1
                        else: ok=True
            if not ok: unc.append((b,c))
    exp=[(b,c) for b in range(19,M+1,4) for c in range(b,M+1,4)]
    print("P: arms 0<=b<=c<=%d: glued labelings built and checked=%d bad=%d; uncovered pairs=%d; equal to {b=c=3 mod 4, b>=19}: %s (expected %d)"%(M,built,bad,len(unc),unc==exp,len(exp)))
if __name__=="__main__":
    w=sys.argv[1]
    if w=="G": test_G(*map(int,sys.argv[2:5]))
    if w=="S": test_S(*map(int,sys.argv[2:5])); 
    if w=="Scor": test_S_cor(int(sys.argv[2]))
    if w=="W": test_W(int(sys.argv[2]),int(sys.argv[3])); test_W_H(int(sys.argv[4]))
    if w=="P": test_P(int(sys.argv[2]))
