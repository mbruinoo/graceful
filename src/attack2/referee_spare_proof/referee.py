# referee.py -- proof-reading referee for line "spare".  Independent re-implementation, written from the PROSE of
# REPORT.txt section 2 (not from check_thms.py).  Everything is checked from the definition:
#   relaxed growth labeling with slack s of (T,r): injective into 0..n-1+s, f(r)=0, distinct edge lengths,
#   lengths strictly decreasing away from r.
import sys, itertools, random
def defcheck(edges, lab, root, slack):
    """edges: list of (u,v) vertex names; lab: dict vertex->label.  Returns (unused labels, unused lengths)."""
    V=set(lab); n=len(V); N=n+slack
    assert len(edges)==n-1, "edge count"
    assert lab[root]==0
    vals=list(lab.values()); assert len(set(vals))==n and min(vals)>=0 and max(vals)<=N-1, "labels"
    adj={v:[] for v in V}
    for u,v in edges: adj[u].append(v); adj[v].append(u)
    seen={root}; st=[(root,None,10**9)]; lens=[]
    while st:
        v,p,up=st.pop()
        for u in adj[v]:
            if u==p: continue
            assert u not in seen, "cycle"; seen.add(u)
            d=abs(lab[u]-lab[v]); assert d<up, "not decreasing"; lens.append(d); st.append((u,v,d))
    assert len(seen)==n, "connected"; assert len(set(lens))==n-1, "repeat length"
    return sorted(set(range(N))-set(vals)), sorted(set(range(1,N))-set(lens))
def is_crossing(edges, lab, a): return all(min(lab[u],lab[v])<=a<max(lab[u],lab[v]) for u,v in edges)

# ---- anchored test trees T'' (q edges, growth placement tau with tau(y'')=0), named by tau labels -------------
def anchored(q, rnd):
    out=[[(0,i) for i in range(1,q+1)]]                               # star
    seq=[0]; lo,hi=1,q
    while lo<=hi:
        seq.append(hi); hi-=1
        if lo<=hi: seq.append(lo); lo+=1
    out.append(list(zip(seq,seq[1:])))                                # zigzag path
    for _ in range(2):                                                # random staircase (caterpillar), root label 0
        lo,hi=0,q; e=[]
        if q: e.append((0,q))
        for _ in range(q-1):
            if rnd.random()<.5: lo+=1
            else: hi-=1
            e.append((lo,hi))
        out.append(e)
    for e in out:
        lab={i:i for i in range(q+1)}; ul,uk=defcheck(e,lab,0,0); assert ul==[] and uk==[]
    return out

# ---- Theorem G ---------------------------------------------------------------------------------------------------
def glue(edges, lab, root, slack, a, y, te, q):
    """as in the proof of Theorem G; returns new (edges, lab)."""
    assert is_crossing(edges,lab,a)
    used=sorted(lab.values()); high=lab[y]>a
    if high: assert lab[y]==min(x for x in used if x>a)
    else:    assert lab[y]==max(x for x in used if x<=a)
    f={z:(g if g<=a else g+q) for z,g in lab.items()}
    E=list(edges); names={0:y}
    for t in range(1,q+1): names[t]=('T',t); f[('T',t)] = lab[y]+q-t if high else lab[y]+t
    assert f[y]==(lab[y]+q if high else lab[y])
    E+=[(names[u],names[v]) for u,v in te]
    return E,f
def all_crossing_relaxed(n, slack):
    """every rooted tree on n vertices (as parent arrays), every relaxed growth labeling with given slack that is
       crossing for some threshold: yields (edges, lab, root=0, a)."""
    N=n+slack
    def trees(k, par):
        if k==n: yield list(par); return
        for p in range(k):
            par.append(p); yield from trees(k+1,par); par.pop()
    for par in trees(1,[None]):
        edges=[(par[v],v) for v in range(1,n)]
        depth=[0]*n
        for v in range(1,n): depth[v]=depth[par[v]]+1
        def rec(v, lab, usedl, usedlen, uplen):
            if v==n:
                lows=[lab[x] for x in range(n) if depth[x]%2==0]; highs=[lab[x] for x in range(n) if depth[x]%2==1]
                if highs and max(lows)<min(highs):
                    for a in range(max(lows),min(highs)): yield edges,dict(enumerate(lab)),a
                return
            p=par[v]
            for z in range(N):
                if z in usedl: continue
                d=abs(z-lab[p])
                if d in usedlen or d>=uplen[p]: continue
                lab.append(z); usedl.add(z); usedlen.add(d); uplen.append(d)
                yield from rec(v+1,lab,usedl,usedlen,uplen)
                lab.pop(); usedl.discard(z); usedlen.discard(d); uplen.pop()
        yield from rec(1,[0],{0},set(),[10**9])
def test_G(maxn, maxq):
    rnd=random.Random(1); cnt=0; wrong=[0]; ex=[]
    for n in range(1,maxn+1):
        for slack in (0,1,2):
            for edges,lab,a in all_crossing_relaxed(n,slack):
                ul0,uk0=defcheck(edges,lab,0,slack)
                used=sorted(lab.values()); ys=[]
                hi=[x for x in used if x>a]; lo=[x for x in used if x<=a]
                inv={g:z for z,g in lab.items()}
                if hi: ys.append(inv[min(hi)])
                ys.append(inv[max(lo)])
                for y in ys:
                    for q in range(0,maxq+1):
                        for te in anchored(q,rnd):
                            E,f=glue(edges,lab,0,slack,a,y,te,q)
                            ul,uk=defcheck(E,f,0,slack)
                            assert uk==[k+q for k in uk0], "unused lengths claim"
                            # REPORT.txt says "low ones unchanged, high ones + q" (relative to the threshold a).
                            # That is false when an unused cell lies strictly between g(y) and the threshold side
                            # boundary; the correct rule is relative to g(y):
                            assert ul==[u if u<lab[y] else u+q for u in ul0], "unused labels (corrected rule)"
                            if ul!=[u if u<=a else u+q for u in ul0] and q>0: wrong[0]+=1; ex.append((edges,dict(lab),a,y,q))
                            cnt+=1
    print("Theorem G: %d glued labelings (ALL rooted trees with <= %d vertices, ALL crossing relaxed labelings with slack 0,1,2, both innermost vertices, q <= %d, 4 kinds of T'') pass the definition; unused lengths = old + q as stated; unused labels follow the rule 'below g(y) unchanged, above g(y) + q'"%(cnt,maxn,maxq))
    print("  REPORT's side remark 'unused labels: low ones unchanged, high ones + q' (relative to threshold a) is violated in %d of these; first example (edges, g, a, y, q): %s"%(wrong[0], ex[0] if ex else None))

# ---- Theorem S ---------------------------------------------------------------------------------------------------
def all_crossing_growth(n):
    for edges,lab,a in all_crossing_relaxed(n,0): yield edges,lab,a
def test_S(maxn, maxq, maxh):
    rnd=random.Random(2); cnt=0
    for n in range(2,maxn+1):
        R=n-1
        for edges,g,a in all_crossing_growth(n):          # NOT only staircases: every crossing growth placement
            inv={v:k for k,v in g.items()}
            for version in ("low","high"):
                if version=="low" and a<1: continue
                if version=="high" and a>R-2: continue
                x=inv[a-1] if version=="low" else inv[a+2]; y=inv[a] if version=="low" else inv[a+1]
                for q in range(0,maxq+1):
                    for te in anchored(q,rnd):
                        for h in range(0,maxh+1):
                            D=q+h+1; f={z:(v if v<=a else v+D) for z,v in g.items()}; E=list(edges); nm={0:y}
                            for t in range(1,q+1): nm[t]=('T',t); f[('T',t)]=(a+t) if version=="low" else (a+1+D-t)
                            E+=[(nm[u],nm[v]) for u,v in te]
                            for i in range(1,h+1):
                                f[('L',i)]=(a-1)+(q+1+i) if version=="low" else (a+2+D)-(q+1+i); E.append((x,('L',i)))
                            ul,uk=defcheck(E,f,0,1)
                            assert uk==[q+1] and ul==[a+D if version=="low" else a+1], (ul,uk)
                            assert len(f)==R+1+q+h
                            cnt+=1
    print("Theorem S: %d labelings (ALL crossing growth placements of ALL rooted trees with <= %d vertices, not only staircases; both versions; q <= %d, h <= %d) pass; unused label/length as stated"%(cnt,maxn,maxq,maxh))
def test_S_cor(M):
    cnt=0
    for p in range(0,M+1):
        for q in range(0,M+1):                 # Corollary S1, explicit labels from the statement
            m=p+q+2; lab={'v':0,'c1':m+1,'c2':m}; E=[('v','c1'),('v','c2')]
            for i,z in enumerate(range(m-1,m-q-1,-1)): lab[('b',i)]=z; E.append(('c2',('b',i)))
            for i,z in enumerate(range(m-q-1,1,-1)): lab[('a',i)]=z; E.append(('c1',('a',i)))
            assert sum(1 for e in E if e[0]=='c1')==p and sum(1 for e in E if e[0]=='c2')==q
            ul,uk=defcheck(E,lab,'v',1); assert ul==[1] and uk==[q+1]; cnt+=1
    c2=0
    for l in range(0,M//2+1):
        for h1 in range(0,M+1):
            for h2 in range(0,M+1):            # Corollary S2, explicit labels from the statement
                lab={'v':0,'g2':1,'g1':2,'c':h1+h2+4}; E=[('v','c'),('c','g1'),('c','g2')]
                for i,z in enumerate(range(3,h1+3)): lab[('a',i)]=z; E.append(('g1',('a',i)))
                for i,z in enumerate(range(h1+3,h1+h2+3)): lab[('b',i)]=z; E.append(('g2',('b',i)))
                for i in range(l): lab[('r',i)]=h1+h2+5+i; E.append(('v',('r',i)))
                assert len(lab)==l+h1+h2+4
                ul,uk=defcheck(E,lab,'v',1); assert ul==[h1+h2+3] and uk==[h1+1]; c2+=1
    # the hand example
    print("Corollaries S1 (DH(p,q), 0<=p,q<=%d): %d pass.  S2 (L(l;h1,h2), l<=%d, h1,h2<=%d): %d pass (includes L(3;8,9): unused label 20, length 9)"%(M,cnt,M//2,M,c2))

# ---- Theorem W ---------------------------------------------------------------------------------------------------
def W_label(a, s, order):
    r=len(a); K=1+sum(a); d=sum(j*a[j] for j in range(1,r)); assert 1<=s<=K-d
    lab={'v':0}; E=[]
    for j in range(r): lab[('x',j)]=K+1+j; E.append(('v',('x',j)))
    blocks=[j for j in range(1,r) for _ in range(a[j])]
    if order=="rev": blocks.reverse()
    elif order=="rnd": random.Random(7).shuffle(blocks)
    c=[0]
    def leaf(j,w): lab[('l',c[0])]=K+1+j-w; E.append((('x',j),('l',c[0]))); c[0]+=1
    p=s; inwin=set()
    for j in blocks:
        for w in range(p+1,p+j): leaf(0,w); inwin.add(w)
        leaf(j,p+j); inwin.add(p+j); p+=j
    assert inwin==set(range(s+1,s+d+1))
    for w in range(1,K+1):
        if w!=s and w not in inwin: leaf(0,w)
    for j in range(r): assert sum(1 for e in E if e[0]==('x',j))==a[j], "leaf count"
    ul,uk=defcheck(E,lab,'v',1); assert uk==[s] and ul==[K+1-s-d], (a,s,ul,uk)
def partitions_upto(total, maxpart, parts):
    if parts==0:
        if total==0: yield ()
        return
    for x in range(min(total,maxpart),-1,-1):
        for rest in partitions_upto(total-x,x,parts-1): yield (x,)+rest
def test_W(maxleaves, maxhubs):
    cnt=trees=0; unsorted=0
    for r in range(1,maxhubs+1):
        for tot in range(0,maxleaves+1):
            for a in partitions_upto(tot,tot,r):
                K=1+sum(a); d=sum(j*a[j] for j in range(1,r))
                C=sum((j-1)*a[j] for j in range(2,r))<=a[0]
                assert C==(d<=K-1), "equivalence (C) <=> d<=K-1"
                if not C: continue
                trees+=1
                for s in range(1,K-d+1):
                    for order in ("fwd","rev","rnd"): W_label(a,s,order); cnt+=1
    # the proof never uses the ordering a_0>=a_1>=...: try unsorted vectors too
    rnd=random.Random(3)
    for _ in range(3000):
        r=rnd.randint(1,6); a=[rnd.randint(0,8) for _ in range(r)]; K=1+sum(a); d=sum(j*a[j] for j in range(1,r))
        if d<=K-1:
            for s in range(1,K-d+1): W_label(a,s,"rnd"); unsorted+=1
    print("Theorem W: %d sorted size vectors (<= %d hubs, <= %d leaves) with (C); %d labelings (every s, three block orders) pass; (C) <=> d<=K-1 confirmed on all vectors; %d labelings for unsorted vectors also pass (ordering is not needed by the proof)"%(trees,maxhubs,maxleaves,cnt,unsorted))
    for k in range(1,200):          # explicit H(1,1,k) from the statement
        lab={'v':0,'x0':k+4,'x1':k+5,'x2':k+6,'l1':k+3,'l2':k+2,('b',3):k+1}
        E=[('v','x0'),('v','x1'),('v','x2'),('x1','l1'),('x2','l2'),('x0',('b',3))]
        for w in range(5,k+4): lab[('b',w)]=k+4-w; E.append(('x0',('b',w)))
        if k==1: # statement gives big-hub leaves at k+1 and w=5..k+3: for k=1 that is 1 leaf (k+1=2) and the empty range
            pass
        assert sum(1 for e in E if e[0]=='x0')==k
        ul,uk=defcheck(E,lab,'v',1); assert ul==[k] and uk==[1]
    print("explicit H(1,1,k), k = 1..199: pass (unused label k, unused length 1)")
    # count for d2 family: rooted trees of height <= 2 with 3 <= n <= 30 = partitions of n-1
    def parts(total,maxp):
        if total==0: yield (); return
        for x in range(min(total,maxp),0,-1):
            for rest in parts(total-x,x): yield (x,)+rest
    tot=ok=0
    for n in range(3,31):
        for p in parts(n-1,n-1):
            a=[x-1 for x in p]; tot+=1
            if sum((j-1)*a[j] for j in range(2,len(a)))<=a[0]: ok+=1
    print("height<=2 rooted trees, 3<=n<=30: %d; satisfying (C): %d   (claimed 23,023 and 10,932)"%(tot,ok))

# ---- Theorem P ---------------------------------------------------------------------------------------------------
def zig(start, lo, hi, steps, first):
    """from 'start', alternately take the next unused high cell (hi, descending) and low cell (lo, ascending)."""
    seq=[start]; side=first
    for _ in range(steps):
        if side=='h': seq.append(hi); hi-=1; side='l'
        else: seq.append(lo); lo+=1; side='h'
    return seq
def piece(b):
    """returns (A, B, threshold a) from the prose of Theorem P, or None."""
    spor={3:([0,7,1,6],[0,4,2,3]),7:([0,11,1,10,2,9,4,8],[0,6,3,5]),
          11:([0,19,1,18,2,17,4,16,6,15,8,12],[0,14,3,11,5,10,7,9]),
          15:([0,19,1,18,2,17,3,16,5,15,6,13,7,11,8,10],[0,12,4,9])}
    if b in spor: return spor[b]
    if b%4==2:
        t=(b-2)//4; R=4*t+4
        A=zig(0,1,R,2*t+2,'h'); assert A[-1]==t+1 and (t+1>0)
        A+=zig(A[-1],t+2,3*t+2,2*t,'h')[1:]; B=[0,2*t+2]; return A,B
    if b%4==1 and b>=5:
        t=(b-1)//4; R=4*t+3
        A=zig(0,1,R,2*t+2,'h'); assert A[-1]==t+1
        A+=zig(A[-1],t+2,3*t+1,2*t-1,'h')[1:]; B=[0,2*t+1]; return A,B
    if b%4==0 and b>=4:
        t=b//4; R=4*t+3
        A=zig(0,1,R-1,2*t+1,'h'); assert A[-1]==3*t+2
        A+=zig(A[-1],t+2,3*t+1,2*t-1,'l')[1:]; B=[0,R,2*t+2]; return A,B
    return None
def check_piece(A,B):
    b=len(A)-1; j=len(B)-1; lab={('A',i):A[i] for i in range(1,b+1)}; lab.update({('B',i):B[i] for i in range(1,j+1)}); lab['r']=0
    nm=lambda arm,i: 'r' if i==0 else (arm,i)
    E=[(nm('A',i),nm('A',i+1)) for i in range(b)]+[(nm('B',i),nm('B',i+1)) for i in range(j)]
    ul,uk=defcheck(E,lab,'r',1)
    low=[A[i] for i in range(0,b+1,2)]+[B[i] for i in range(0,j+1,2)]; high=[A[i] for i in range(1,b+1,2)]+[B[i] for i in range(1,j+1,2)]
    assert max(low)<min(high), "crossing"; a=max(low)
    y=B[-1]; assert y==(min(high) if j%2 else max(low)), "innermost"
    return E,lab,a,nm('B',j),ul,uk
def test_P(maxb, maxq):
    cnt=0; covered=set()
    for b in range(2,maxb+1):
        pc=piece(b)
        if pc is None: assert b%4==3 and b>=19; continue
        A,B=pc; assert len(A)==b+1
        E,lab,a,y,ul,uk=check_piece(A,B); j=len(B)-1
        if b%4==2: t=(b-2)//4; assert ul==[3*t+3] and uk==[1] and j==1
        if b%4==1: t=(b-1)//4; assert ul==[3*t+2] and uk==[1] and j==1
        if b%4==0: t=b//4; assert ul==[t+1] and uk==[1] and j==2
        for q in range(0,maxq+1):
            seq=[0]; lo,hi=1,q
            while lo<=hi:
                seq.append(hi); hi-=1
                if lo<=hi: seq.append(lo); lo+=1
            te=list(zip(seq,seq[1:]))
            E2,f=glue(E,lab,'r',1,a,y,te,q); defcheck(E2,f,'r',1)
            # confirm the glued tree is the path with arms (b, j+q)
            deg={}
            for u,v in E2: deg[u]=deg.get(u,0)+1; deg[v]=deg.get(v,0)+1
            assert max(deg.values())<=2 and deg['r']==2 and len(E2)==b+j+q
            covered.add((b,j+q)); cnt+=1
    # base cases b=0, b=1 (slack 0)
    for n in range(2,maxb+maxq+2):
        seq=zig(0,1,n-1,n-1,'h'); lab={i:seq[i] for i in range(n)}; defcheck([(i,i+1) for i in range(n-1)],lab,0,0)
        if n>=3:
            seq=zig(0,1,n-2,n-2,'h'); lab={i:seq[i] for i in range(n-1)}; lab['leaf']=n-1
            defcheck([(i,i+1) for i in range(n-2)]+[(0,'leaf')],lab,0,0)
    M=min(maxb,maxq); un=[(b,c) for b in range(2,M+1) for c in range(b,M+1) if (b,c) not in covered and (c,b) not in covered]
    assert all(b%4==3 and c%4==3 and b>=19 for b,c in un)
    exp=[(b,c) for b in range(19,M+1,4) for c in range(b,M+1,4)]
    assert sorted(un)==sorted(exp)
    print("Theorem P: pieces built from the prose for every b <= %d (except b = 3 mod 4, b >= 19) pass definition+crossing+innermost with the stated unused label/length; %d glued paths pass; uncovered pairs 2<=b<=c<=%d: %d, exactly b=c=3 (mod 4), b>=19"%(maxb,cnt,M,len(un)))
def test_newpieces():
    """Referee's own finding (pieces.cpp): crossing pieces for b = 19..51, b = 3 mod 4, with j <= b."""
    new={19:([0,27,1,26,2,25,4,24,6,23,7,21,9,19,10,17,11,15,12,14],[0,22,3,18,5,16,8,13]),
     23:([0,39,1,38,2,37,3,36,4,35,6,34,7,33,9,32,11,31,13,29,16,26,18,22],[0,30,5,27,8,25,10,24,12,23,14,21,15,20,17,19]),
     27:([0,31,1,30,2,29,3,28,4,27,5,26,7,25,8,24,9,22,10,21,11,19,12,18,13,17,14,16],[0,20,6,15]),
     31:([0,39,1,38,2,37,3,36,4,35,5,34,6,33,8,32,9,31,10,30,12,28,13,27,15,25,16,23,17,21,18,20],[0,26,7,24,11,22,14,19]),
     35:([0,43,1,42,2,41,3,40,4,39,5,38,6,37,7,36,9,35,10,34,11,33,12,31,14,30,15,29,17,27,18,25,19,23,20,22],[0,28,8,26,13,24,16,21]),
     39:([0,43,1,42,2,41,3,40,4,39,5,38,6,37,7,36,9,35,10,34,11,33,12,31,13,30,14,29,15,27,16,26,17,25,18,24,19,23,20,22],[0,28,8,21]),
     43:([0,59,1,58,2,57,3,56,4,55,5,54,6,53,7,52,8,51,10,50,11,49,12,48,13,47,16,46,17,45,21,43,22,39,23,36,25,35,26,33,27,31,28,30],[0,42,9,41,14,40,15,38,18,37,19,34,20,32,24,29]),
     47:([0,63,1,62,2,61,3,60,4,59,5,58,6,57,8,56,9,55,10,54,12,53,13,52,15,51,16,49,18,48,20,46,21,44,22,42,24,40,25,39,27,37,28,35,29,33,30,32],[0,50,7,45,11,43,14,41,17,38,19,36,23,34,26,31]),
     51:([0,55,1,54,2,53,3,52,4,51,5,50,6,49,7,48,8,47,9,46,11,45,12,44,13,43,14,42,15,40,16,39,17,38,18,37,19,35,20,34,21,33,22,32,23,31,24,30,25,29,26,28],[0,36,10,27])}
    for b,(A,B) in sorted(new.items()):
        assert len(A)==b+1; E,lab,a,y,ul,uk=check_piece(A,B); j=len(B)-1; assert j<=b
        for q in (0,1,2,5,40):
            seq=[0]; lo,hi=1,q
            while lo<=hi:
                seq.append(hi); hi-=1
                if lo<=hi: seq.append(lo); lo+=1
            E2,f=glue(E,lab,'r',1,a,y,list(zip(seq,seq[1:])),q); defcheck(E2,f,'r',1)
        print("  new piece b=%d j=%d: passes definition, crossing, innermost; unused label %s, unused length %s"%(b,j,ul,uk))

# ---- Bridge and the S(2,2,1) counterexample ---------------------------------------------------------------------
def growth_placements(n, edges):
    """all bijections V->0..n-1 that are growth placements (definition: brackets n-1..k connected for every k)."""
    out=[]
    for perm in itertools.permutations(range(n)):
        ln={}
        ok=True
        for u,v in edges:
            d=abs(perm[u]-perm[v])
            if d in ln: ok=False; break
            ln[d]=(u,v)
        if not ok: continue
        seen=set(ln[n-1])
        for k in range(n-2,0,-1):
            u,v=ln[k]
            if (u in seen)==(v in seen): ok=False; break
            seen|={u,v}
        if ok: out.append((perm,ln[1]))
    return out
def test_bridge(maxn):
    import networkx as nx
    E=[(0,1),(1,2),(0,3),(3,4),(0,5)]; gp=growth_placements(6,E)
    from collections import Counter
    c=Counter(tuple(sorted(e)) for _,e in gp)
    print("S(2,2,1): %d growth placements among 720 bijections; length-1 bracket on edges: %s"%(len(gp),dict(c)))
    assert len(gp)==12 and c.get((0,5),0)==0
    for n in range(2,maxn+1):
        bad=0; pairs=0; bridge_fail=0
        for T in nx.nonisomorphic_trees(n):
            edges=list(T.edges()); deg=dict(T.degree()); gp=growth_placements(n,edges)
            hung=set()
            for perm,(u,v) in gp:
                for x in (u,v):
                    if deg[x]==1: hung.add(x)
            leaves=[x for x in range(n) if deg[x]==1]
            if n==2: leaves=leaves  # K2: both ends
            pairs+=len(leaves); bad+=sum(1 for x in leaves if x not in hung)
            # bridge: for each leaf x with neighbour y: exists growth placement with bracket 1 = {y,x}
            #   <=>  T-x has a one-spare labeling (some root) with unused length 1 and unused label f(y)+-1
            if n<=7 and n>=3:
                for x in leaves:
                    y=next(iter(T[x])); lhs = x in hung and any(set(e)=={x,y} for _,e in gp)
                    rest=[v for v in range(n) if v!=x]; e2=[e for e in edges if x not in e]; rhs=False
                    for labs in itertools.permutations(range(n),n-1):
                        lab=dict(zip(rest,labs))
                        if 0 not in labs: continue
                        root=[v for v in rest if lab[v]==0][0]
                        try: ul,uk=defcheck(e2,lab,root,1)
                        except AssertionError: continue
                        if uk==[1] and abs(ul[0]-lab[y])==1: rhs=True; break
                    if lhs!=rhs: bridge_fail+=1
        print("n=%d: (tree, leaf) pairs %d, leaf never hung by the length-1 bracket: %d%s"%(n,pairs,bad,("; bridge equivalence failures: %d"%bridge_fail) if 3<=n<=7 else ""))
def test_counts():
    def isprime(m): return m>1 and all(m%d for d in range(2,int(m**.5)+1))
    dh=sum(1 for m in range(2,152) if isprime(m) for p in range(1,m) for q in range(p,m) if p+q+2==m)
    h3=[m for m in range(11,198,2) if m%3 and m%5 and m%4!=3]
    pall=sum((n+1)//2 for n in range(3,201)); p33=sum(1 for b in range(15,400,4) for c in range(b,400,4) if b+c+1<=331)
    print("counts: DH prime m<=151, 1<=p<=q: %d (claimed 1,160); H3 list: %d (claimed 26) %s; rooted paths 3..200: %d (claimed 10,098); P33 pairs: %d (claimed 1,482); S(L,L,L) roots: %d (claimed 495)"%(dh,len(h3),h3[:4],pall,p33,sum(L+1 for L in range(1,31))))
if __name__=="__main__":
    w=sys.argv[1]
    if w=="G": test_G(int(sys.argv[2]),int(sys.argv[3]))
    if w=="S": test_S(int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4])); test_S_cor(30)
    if w=="W": test_W(int(sys.argv[2]),int(sys.argv[3]))
    if w=="P": test_P(int(sys.argv[2]),int(sys.argv[3])); test_newpieces()
    if w=="B": test_bridge(int(sys.argv[2]))
    if w=="C": test_counts()
