# check_thms.py -- build the explicit labelings of Theorems W (window, depth 2) and S (sidestep) and check each
# one from the definition of a relaxed growth labeling with ONE spare label:
#   labels injective in 0..n (n = number of vertices), root at 0, edge lengths pairwise distinct,
#   lengths strictly decreasing along every path away from the root.
# usage: python3 check_thms.py W maxleaves maxhubs | S maxO maxq maxh
import sys, itertools
def check(n, root, edges, lab):
    assert len(lab)==n and lab[root]==0 and len(set(lab))==n and all(0<=x<=n for x in lab), "labels"
    adj=[[] for _ in range(n)]
    for a,b in edges: adj[a].append(b); adj[b].append(a)
    par={root:None}; st=[root]; lens=set()
    while st:
        v=st.pop()
        for u in adj[v]:
            if u==par[v]: continue
            par[u]=v; d=abs(lab[u]-lab[v]); assert d not in lens, "repeat length"; lens.add(d)
            if par[v] is not None: assert d<abs(lab[v]-lab[par[v]]), "not decreasing"
            st.append(u)
    assert len(par)==n and len(lens)==n-1
    return sorted(set(range(n+1))-set(lab)), sorted(set(range(1,n+1))-lens)

def window(a, s):
    """Theorem W.  a = leaf counts a_0>=a_1>=...>=a_{r-1}>=0 of the r children of the root.  s = unused length."""
    r=len(a); K=sum(a)+1; M=K+r; d=sum(j*a[j] for j in range(r)); assert 1<=s<=K-d
    edges=[]; lab=[0]; hub=[]
    for j in range(r): hub.append(len(lab)); edges.append((0,len(lab))); lab.append(K+1+j)
    def leaf(j,w): edges.append((hub[j],len(lab))); lab.append(K+1+j-w)
    p=s
    for j in range(1,r):
        for _ in range(a[j]):
            for w in range(p+1,p+j): leaf(0,w)        # the j-1 lengths the block jumps over stay with x_0
            leaf(j,p+j); p+=j                         # top length of the block goes to x_j
    for w in list(range(1,s))+list(range(s+d+1,K+1)): leaf(0,w)
    n=len(lab); assert n==M
    ul,uk=check(n,0,edges,lab); assert uk==[s] and ul==[K+1-s-d], (ul,uk)
    return n

def partitions(total, maxpart, parts):
    if parts==0:
        if total==0: yield ()
        return
    for x in range(min(total,maxpart),-1,-1):
        for rest in partitions(total-x,x,parts-1): yield (x,)+rest

def staircases(R):
    """all staircase placements on labels 0..R (README Theorem 2, labels shifted to start at 0) with their threshold a:
       returns (edges as label pairs, a).  Root = vertex labelled 0.  Every bracket joins a label <= a to one > a."""
    for bits in itertools.product((0,1),repeat=R-1):
        lo,hi=0,R; e=[(0,R)]
        for b in bits:
            if b: lo+=1
            else: hi-=1
            e.append((lo,hi))
        yield e, lo            # low labels 0..lo, high labels lo+1..R  (hi == lo+1 at the end)

def anchored_examples(q):
    """a few trees with q edges and a growth placement tau with the root at 0: star (centre), path (end), broom."""
    out=[]
    out.append([(0,i) for i in range(1,q+1)])                       # star, centre at 0
    e=[];lo,hi,cur=0,q,0                                           # zigzag path from 0
    labs=[0]
    while lo<hi:
        nxt = hi if cur==lo else lo
        if cur==lo: e.append((cur,hi)); cur=hi; lo+=1
        else: e.append((cur,lo)); cur=lo; hi-=1
    out.append(e)
    if q>=3:                                                        # broom: 0 - q, then q has leaves 1..q-1
        out.append([(0,q)]+[(q,i) for i in range(1,q)])
    return out

def sidestep(R,maxq,maxh):
    cnt=0
    for e,a in staircases(R):
        for version in ("low","high"):
            if version=="low" and a<1: continue
            if version=="high" and a>R-2: continue
            for q in range(0,maxq+1):
                for te in (anchored_examples(q) if q else [[]]):
                    for h in range(0,maxh+1):
                        D=q+h+1; n=R+1+q+h
                        sh=lambda g: g if g<=a else g+D
                        # vertices are named by their final labels; build edge list on labels
                        E=[(sh(u),sh(v)) for u,v in e]
                        if version=="low":
                            y=a; x=a-1
                            E+=[(a+u,a+v) for u,v in te]
                            E+=[(x,x+q+1+i) for i in range(1,h+1)]
                            unused=a+D
                        else:
                            y=a+1+D; x=a+2+D
                            E+=[(y-u,y-v) for u,v in te]
                            E+=[(x,x-(q+1+i)) for i in range(1,h+1)]
                            unused=a+1
                        labs=sorted(set(u for ed in E for u in ed)); idx={L:i for i,L in enumerate(labs)}
                        ul,uk=check(len(labs),idx[0],[(idx[u],idx[v]) for u,v in E],labs)
                        assert len(labs)==n and ul==[unused] and uk==[q+1], (ul,uk,unused,q)
                        cnt+=1
    return cnt
if sys.argv[1]=="W":
    ML=int(sys.argv[2]); MH=int(sys.argv[3]); cnt=trees=skipped=0
    for r in range(1,MH+1):
        for tot in range(0,ML+1):
            for a in partitions(tot,tot,r):
                if sum((j-1)*a[j] for j in range(2,r))>a[0]: skipped+=1; continue
                K=tot+1; d=sum(j*a[j] for j in range(r)); trees+=1
                for s in range(1,K-d+1): window(a,s); cnt+=1
    print("Theorem W: %d rooted depth-2 trees (<=%d hubs, <=%d leaves) satisfying (C), %d labelings (all admissible s) built and verified; %d trees fail (C) and are not covered"%(trees,MH,ML,cnt,skipped))
elif sys.argv[1]=="S":
    tot=0
    for R in range(2,int(sys.argv[2])+1): tot+=sidestep(R,int(sys.argv[3]),int(sys.argv[4]))
    print("Theorem S: %d labelings built and verified (all staircases O with R<=%s, both versions, q<=%s, h<=%s)"%(tot,sys.argv[2],sys.argv[3],sys.argv[4]))

# ---------------- Theorem P (paths): pieces + zigzag gluing ----------------
def zig(start, lo, hi, edges, first_high):
    """continue a zigzag from label `start`: alternately take the next unused high label (hi, hi-1, ..) and the next
       unused low label (lo, lo+1, ..); returns the list of new labels."""
    out=[]; high=first_high
    for _ in range(edges):
        if high: out.append(hi); hi-=1
        else: out.append(lo); lo+=1
        high=not high
    return out
def piece(b):
    """(A, B): labels along the b-arm and along the j-arm, both starting at the root label 0.  None if no formula."""
    if b%4==1 and b>=5:
        t=b//4; R=4*t+3
        A=[0]+zig(0,1,R,2*t+2,True)+zig(t+1,t+2,3*t+1,2*t-1,True); return A,[0,2*t+1]
    if b%4==2:
        t=b//4; R=4*t+4
        A=[0]+zig(0,1,R,2*t+2,True)+zig(t+1,t+2,3*t+2,2*t,True); return A,[0,2*t+2]
    if b%4==0 and b>=4:
        t=b//4; R=4*t+3
        A=[0]+zig(0,1,R-1,2*t+1,True)+zig(3*t+2,t+2,3*t+1,2*t-1,False); return A,[0,R,2*t+2]
    if b==3: return [0,7,1,6],[0,4,2,3]
    if b==7: return [0,11,1,10,2,9,4,8],[0,6,3,5]
    if b==11: return [0,19,1,18,2,17,4,16,6,15,8,12],[0,14,3,11,5,10,7,9]
    if b==15: return [0,19,1,18,2,17,3,16,5,15,6,13,7,11,8,10],[0,12,4,9]
    return None
def glue_path(A,B,q):
    """Theorem G with T'' = zigzag path with q edges anchored at its end, glued at the tip y of B."""
    b=len(A)-1; j=len(B)-1; y=B[-1]
    low=[A[i] for i in range(0,b+1,2)]+[B[i] for i in range(2,j+1,2)]
    high=[A[i] for i in range(1,b+1,2)]+[B[i] for i in range(1,j+1,2)]
    a=max(low); assert a<min(high)                       # crossing
    assert (j%2==1 and y==min(high)) or (j%2==0 and y==a)  # y innermost on its side
    sh=lambda g: g if g<=a else g+q
    A2=[sh(g) for g in A]; B2=[sh(g) for g in B]; y2=B2[-1]
    if j%2==1: ext=zig(y2,y2-q,y2-1,q,False)             # y is the top of the block [y2-q, y2]
    else:      ext=zig(y2,y2+1,y2+q,q,True)              # y is the bottom of the block [y2, y2+q]
    return A2,B2+ext
def check_arms(A,B):
    n=len(A)+len(B)-1; lab=A+B[1:]; edges=[(i,i+1) for i in range(len(A)-1)]+[(0,len(A))]+[(i,i+1) for i in range(len(A),n-1)]
    return check(n,0,edges,lab)
if sys.argv[1]=="P":
    MB=int(sys.argv[2]); MQ=int(sys.argv[3]); cnt=0; covered=set()
    for b in range(2,MB+1):
        pc=piece(b)
        if pc is None: continue
        for q in range(0,MQ+1):
            A,B=glue_path(pc[0],pc[1],q); assert len(A)-1==b and len(B)-1==len(pc[1])-1+q
            ul,uk=check_arms(A,B); cnt+=1; covered.add((b,len(B)-1)); covered.add((len(B)-1,b))
    unc=[(b,c) for b in range(2,MB+1) for c in range(b,MB+1) if (b,c) not in covered]
    bad=[p for p in unc if not (p[0]%4==3 and p[1]%4==3 and p[0]>=19)]
    print("Theorem P: %d labelings built and verified (b <= %d, q <= %d); %d arm pairs 2 <= b <= c <= %d are not produced; all of them have b = c = 3 (mod 4), b >= 19: %s; every such pair is unproduced: %s"%(cnt,MB,MQ,len(unc),MB,not bad, len(unc)==sum(1 for b in range(19,MB+1,4) for c in range(b,MB+1,4))))
