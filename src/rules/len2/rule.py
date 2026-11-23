#!/usr/bin/env python3
"""Explicit recursive rule for deals of the spider with k legs of length 2 (labels 0..2k, centre 0).  Every k >= 1.

Status (see check): the rule is a deterministic recursion with no search.  The argument in the comments below is
complete for n >= cap_threshold(c); the finitely many smaller cases are stored tables or are checked directly by
`rule.py check`.  Machine-checked from the definition of a deal for every k <= 1500.

Picture.  A zigzag deal is a set O of k outer labels in 1..2k together with a graph on O in which every vertex has
degree 2 (a loop counts 2): the edges are {o, d(o)}, and the edge sums o+d(o) must be exactly the other k labels
(the inner labels).  Leg of o: numbers (o+d(o), d(o)), labels o+d(o) then o.

Shift lemma.  T is a *split* of such a graph if every edge {u,w} satisfies [u>T] + [w>T] = [u+w>T].
Then adding one constant delta to every label >T keeps all edge equations, and frees the labels T+1..T+delta.

Class C0(k) (k = 0 mod 3): graphs on 1..2k for which T = k is a split.

Caps.  cap_c(n) is an explicit graph on the label set  [n+1, 2n+dd] u [3n+dd+1, 6n+2c]   (dd = c-1).
For c = 3, 6, 9 it has split 3n+c, so   G in C0(n)  ==>  shift(G; T=n, delta=n+dd) + cap_c(n)  is in C0(3n+c).

  k = 0 mod 3:  k = 3n+c with n = 0 mod 3 and c = 3, 6, 9 for k = 3, 6, 0 mod 9;  recurse on n (down to n = 0).
  k = 1 mod 3:  graph for k-1 (in C0), labels >k-1 shifted by 1, plus a loop at k (sum 2k).
  k = 2 mod 3:  no zigzag deal exists (README Lemma 11).  k = 3n+c with n = 0 mod 3 and c = 2, 5, 8: the graph of
                C0(n) shifted as before, plus a cap that contains ONE 'difference edge' o* - x* = i*
                (the leg of o* gets the numbers i* > x* and goes up twice; every other leg alternates).

Each cap is a ladder-like 'backbone' (two long runs of parallel edges) between a low interval and a high interval,
closed up at its two ends by a fixed finite table; see CAP_DATA.  cap_3 is the plain ladder, cap_2 the plain ladder
path closed by the difference edge.

Run:  rule.py show k      print the graph and the deal for k
      rule.py check K     verify, straight from the definition of a deal, every k <= K; check every cap by itself
"""
import sys

# ---------------------------------------------------------------- caps
# A cap is given in "v-coordinates":  low vertex n+v,  high vertex 3n+c+j  (j = 1..h, h = n+h3, h3 = (c+1)//3),
# so a low-high edge (j,v) has sum 4n+c+(j+v).
#   backbone : j <-> v = j+beta and v = j+beta+g      for j = J0+1 .. h-J1            (the part that grows with n)
#   bottom   : list of (j,v)                           (j in 1..J0;  the same for every n)
#   top      : list of (j',v') meaning j = h-J1+j', v = n+v'   (j' in 1..J1;  the same for every n)
#   small    : low-low edges (a,b) = {n+a, n+b}, sum 2n+(a+b)      (an unused label of the middle block)
#   cross    : low-low edges (p,q) = {n+p, 2n+q}, sum 3n+(p+q)     (a label of the top block that is <= 3n+c)
#   diff     : (side, j or j', v) = difference edge from o* = high vertex to x* = n+v, label o*-x*
CAP_DATA={
 3: dict(dd=2, beta=0,  g=1, J0=0, J1=0, small=[], cross=[(1,2)], bottom=[], top=[]),
 6: dict(dd=5, beta=0,  g=3, J0=1, J1=2, small=[(1,3)], cross=[(1,5)], bottom=[(1,2),(1,4)], top=[(1,1),(2,2),(2,3),(1,5)]),
 9: dict(dd=8, beta=-1, g=7, J0=5, J1=5, small=[(1,4),(1,6)], cross=[(3,6)],
         bottom=[(1,3),(1,4),(4,2),(5,2),(3,5),(2,7),(2,8),(3,9),(4,10),(5,11)],
         top=[(1,-2),(1,0),(4,-1),(2,3),(5,1),(5,2),(4,4),(3,6),(2,8),(3,8)]),
 2: dict(dd=1, beta=0,  g=1, J0=0, J1=1, small=[], cross=[], bottom=[], top=[(1,1)], diff=('top',1,1)),
 5: dict(dd=4, beta=0,  g=3, J0=1, J1=2, small=[(1,3)], cross=[], bottom=[(1,2),(1,4)], top=[(1,1),(2,2),(2,3)], diff=('top',1,1)),
 8: dict(dd=7, beta=-2, g=7, J0=5, J1=5, small=[(1,3)], cross=[(3,5)],
         bottom=[(2,2),(3,2),(5,1),(1,6),(1,7),(4,5),(3,8),(4,9),(5,10)],
         top=[(1,-3),(1,-1),(4,-2),(2,2),(5,0),(5,1),(4,3),(3,5),(2,7),(3,7)], diff=('bottom',2,4)),
}
# Small n where the general pattern has no room (found by search, checked like everything else).  '-' marks the difference edge.
CAP_SMALL={
 (6,0):"5+7 3+8 2+8 2+7 1+5 1+3",
 (9,0):"8+10 6+11 6+10 4+11 2+12 1+12 1+8 3+4 2+3",
 (9,3):"11+25 13+22 10+24 11+22 7+25 10+21 6+24 9+20 7+21 8+19 6+20 4+19 5+13 5+9 4+8",
 (9,6):"18+36 17+35 17+36 18+33 15+35 14+34 13+33 12+32 11+31 10+30 15+34 19+28 14+31 11+32 12+29 9+30 8+29 10+28 7+9 7+13 8+19",
 (5,0):"5+5 3+6 4+4 1+6 3-1",
 (8,0):"8+8 5+10 5+9 4+9 6+6 1+10 3+4 3-1",
 (8,3):"17+17 13+20 11+21 7+24 8+22 7+22 4+24 6+21 6+20 12+13 11+12 9+10 8+10 9-4",
 (8,6):"26+26 19+32 19+31 18+31 12+36 11+36 9+37 11+34 7+37 9+34 10+32 13+28 13+27 12+27 10+28 17+18 16+17 14+16 14+15 15-7",
}
def cap_threshold(c):
    D=CAP_DATA[c]; return max(0, D['g']+D['J0']+D['J1']-(c+1)//3)

def cap(c,n):
    """edge list (u, w, kind) of cap_c(n); kind '+' (label u+w) or '-' (label u-w)"""
    if (c,n) in CAP_SMALL:
        return [tuple(map(int,e.split(ch)))+(ch,) for e in CAP_SMALL[(c,n)].split() for ch in '+-' if ch in e]
    D=CAP_DATA[c]; h=n+(c+1)//3; J0,J1,beta,g=D['J0'],D['J1'],D['beta'],D['g']
    lo=lambda v: n+v
    hi=lambda j: 3*n+c+j
    E =[(lo(a),lo(b),'+') for (a,b) in D['small']]
    E+=[(lo(p),lo(n+q),'+') for (p,q) in D['cross']]
    E+=[(lo(v),hi(j),'+') for (j,v) in D['bottom']]
    E+=[(lo(n+v),hi(h-J1+j),'+') for (j,v) in D['top']]
    for j in range(J0+1,h-J1+1): E+=[(lo(j+beta),hi(j),'+'),(lo(j+beta+g),hi(j),'+')]
    if 'diff' in D:
        side,j,v=D['diff']
        E.append((hi(j) if side=='bottom' else hi(h-J1+j), lo(v), '-'))
    return E

# ---------------------------------------------------------------- the rule
def shift(E,T,delta): return [(u+delta*(u>T), w+delta*(w>T), kd) for (u,w,kd) in E]

def build(k):
    """edge list for k legs of length 2; for k = 0 mod 3 the result lies in C0(k)"""
    if k==0: return []
    if k%3==1: return shift(build(k-1),k-1,1)+[(k,k,'+')]
    c={3:3,6:6,0:9,2:2,5:5,8:8}[k%9]
    n=(k-c)//3
    return shift(build(n),n,n+CAP_DATA[c]['dd'])+cap(c,n)

# ---------------------------------------------------------------- from graph to deal, and the check from the definition
def deal_from_graph(E):
    """orient every cycle (the difference edge from o* to x*); return legs [w1,w2] and their signs"""
    adj={}
    for i,(u,w,kd) in enumerate(E):
        adj.setdefault(u,[]).append((w,i)); adj.setdefault(w,[]).append((u,i))
    assert all(len(a)==2 for a in adj.values()), "a vertex does not have degree 2"
    used=[False]*len(E); legs=[]; signs=[]
    def walk(start,first):
        cur=start; e=first
        while True:
            used[e]=True; u,w,kd=E[e]
            nxt = w if u==cur else u
            if kd=='+': legs.append([cur+nxt,nxt]); signs.append([1,-1])
            else:
                assert (cur,nxt)==(u,w); legs.append([cur-nxt,nxt]); signs.append([1,1])
            cur=nxt
            if cur==start: return
            e=[i for (_,i) in adj[cur] if not used[i]][0]
    for i,(u,w,kd) in enumerate(E):
        if kd=='-': walk(u,i)
    for v in sorted(adj):
        for (_,i) in adj[v]:
            if not used[i]: walk(v,i)
    return legs,signs

def check_deal(lengths, legs, signs):
    """the definition: numbers m..1 each dealt once, each leg strictly decreasing, first move up, all labels in 1..m distinct"""
    m=sum(lengths)
    assert sorted(len(l) for l in legs)==sorted(lengths)
    assert sorted(x for l in legs for x in l)==list(range(1,m+1)), "numbers 1..m not each dealt once"
    seen=set()
    for l,sg in zip(legs,signs):
        assert all(l[j]>l[j+1] for j in range(len(l)-1)), "leg not decreasing"
        assert sg[0]==1
        tip=0
        for w,s in zip(l,sg):
            tip+=s*w
            assert 1<=tip<=m and tip not in seen, ("label",tip)
            seen.add(tip)
    assert len(seen)==m
    return True

def is_split(E,T): return all(kd=='+' and (u>T)+(w>T)==(u+w>T) for (u,w,kd) in E)

def check_cap(c,n):
    """cap_c(n) is a graph with all degrees 2 on exactly the label set [n+1,2n+dd] u [3n+dd+1,6n+2c] (split 3n+c if c=0 mod 3)"""
    dd=CAP_DATA[c]['dd']
    try: E=cap(c,n)
    except Exception: return False
    L=set(range(n+1,2*n+dd+1))|set(range(3*n+dd+1,6*n+2*c+1))
    deg={}; lab=[]
    for (u,w,kd) in E:
        deg[u]=deg.get(u,0)+1; deg[w]=deg.get(w,0)+1; lab.append(u+w if kd=='+' else u-w)
    return (all(x==2 for x in deg.values()) and len(set(lab))==len(lab) and not set(lab)&set(deg)
            and set(lab)|set(deg)==L and (c%3!=0 or is_split(E,3*n+c))
            and sum(1 for e in E if e[2]=='-')==(c%3==2))

def prove_cap(c):
    """The n-free bookkeeping behind cap_c(n) for n >= cap_threshold(c): checks the two end tables once and for all.
    Bottom region = low vertices v <= J0+beta+g and high vertices j <= J0; top region = v' >= h3-J1+beta+1, j' in 1..J1
    (v = n+v', j = n+h3-J1+j'); everything in between is backbone and has degree 2 from the backbone alone."""
    D=CAP_DATA[c]; dd,beta,g,J0,J1=D['dd'],D['beta'],D['g'],D['J0'],D['J1']; h3=(c+1)//3
    diff=D.get('diff'); small=D['small']; cross=D['cross']; bottom=D['bottom']; top=D['top']
    smin=c-2*h3+1+(diff is not None)                       # high sums are 4n+c+s, s = smin .. 2n+c
    bs=[s for s in range(smin,2*J0+beta+g+3) if (s-beta)%2==0 and s<2*(J0+1)+beta or (s-beta)%2==1 and s<2*(J0+1)+beta+g]
    lastA=h3-J1+beta; lastB=lastA+g; smaxp=c-h3+J1          # primed sums s' = s-(2n+h3-J1)
    ts=[s for s in range(lastA-2,smaxp+1) if (s-lastA)%2==0 and s>lastA or (s-lastA)%2==1 and s>lastB]
    ok = sorted(j+v for j,v in bottom)==bs and sorted(j+v for j,v in top)==ts
    dj_b={j:2 for j in range(1,J0+1)}; dj_t={j:2 for j in range(1,J1+1)}
    holes={a+b for a,b in small}; toplow=[p+q for p,q in cross]; xv=None
    if diff:
        side,j,v=diff; xv=v
        if side=='bottom': dj_b[j]-=1; holes.add(c+j-v)                 # label 2n+(c+j-v)
        else: dj_t[j]-=1; toplow.append(c+h3-J1+j-v)                    # label 3n+(c+h3-J1+j-v)
    ok &= all(sum(1 for jj,_ in bottom if jj==j)==d for j,d in dj_b.items()) and all(1<=j<=J0 for j,_ in bottom)
    ok &= all(sum(1 for jj,_ in top if jj==j)==d for j,d in dj_t.items()) and all(1<=j<=J1 for j,_ in top)
    vb=range(1,J0+beta+g+1)                                              # bottom low vertices
    used_b=[v for _,v in bottom]+[x for e in small for x in e]+[p for p,_ in cross]+([xv] if diff else [])
    ok &= all(v in vb for v in used_b) and all(used_b.count(v)+(v>=J0+1+beta)==2 for v in vb)
    vt=range(h3-J1+beta+1,dd+1)                                          # top low vertices / unused labels, primed
    used_t=[v for _,v in top]+[q for _,q in cross]
    ok &= all(v in vt for v in used_t) and all(used_t.count(v)+(v<=h3-J1+beta+g)==(0 if v in holes else 2) for v in vt)
    ok &= holes<=set(vt) and len(holes)==len(small)+(diff is not None and diff[0]=='bottom')
    ok &= sorted(toplow)==list(range(dd+1,c+1))                          # labels 3n+dd+1 .. 3n+c
    return ok

if __name__=="__main__":
    if sys.argv[1]=="show":
        k=int(sys.argv[2]); E=build(k); legs,signs=deal_from_graph(E)
        print("edges:"," ".join("%d%s%d=%d"%(u,kd,w,u+w if kd=='+' else u-w) for u,w,kd in sorted(E,key=lambda e:-(e[0]+e[1]))))
        print("legs (numbers dealt; a leg marked ++ goes up twice):"," ".join("(%d,%d)%s"%(l[0],l[1],"++" if s[1]==1 else "") for l,s in zip(legs,signs)))
        print("valid:",check_deal([2]*k,legs,signs))
    elif sys.argv[1]=="check":
        K=int(sys.argv[2]); done=[]; missing=[]
        for k in range(1,K+1):
            try: E=build(k)
            except KeyError: missing.append(k); continue
            assert len(E)==k
            legs,signs=deal_from_graph(E); check_deal([2]*k,legs,signs)
            nonzig=sum(1 for s in signs if s[1]==1)
            assert nonzig==(1 if k%3==2 else 0)
            if k%3==0: assert is_split(E,k)
            done.append(k)
        print("deals verified from the definition for",len(done),"values of k <=",K)
        print("  k = 0,1 mod 3 covered:",all(k in done for k in range(1,K+1) if k%3!=2))
        print("  k = 2 mod 3 covered:",sum(1 for k in done if k%3==2),"of",sum(1 for k in range(1,K+1) if k%3==2),"; not covered:",missing[:12],"..." if len(missing)>12 else "")
        for c in sorted(CAP_DATA):
            bad=[n for n in range(0,K+1) if not check_cap(c,n)]
            print("  cap_%d: end tables consistent (n-free check): %s, valid from n >= %d by that check;"%(c,prove_cap(c),cap_threshold(c)),
                  "direct check for all n <= %d fails only for n in"%K,bad)
