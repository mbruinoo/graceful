#!/usr/bin/env python3
"""Closed-form all-up combs (no search) and their check from the README section 1 definitions.

  paired(bs, c)   Paired-hub theorem (REPORT.txt, Theorem P): non-root hubs = pairs of equal sizes
                  bs[0],bs[0],bs[1],bs[1],... plus optionally one more hub of size c (c even, or c odd >= k
                  where k = 2*len(bs)+1).  w = k-1.
  twos(k)         Theorem Q: k hubs with two leaves each; w = 0 (k = 0,1 mod 4), 1 (k = 2 mod 4), 2 (k = 3 mod 4).
  ones(k)         Theorem O: k hubs with one leaf each; w = 0 (k = 0,1 mod 3), 1 (k = 2 mod 3).

Each returns (S, w, y, hubs, W) with hubs = [(label, [leaf lengths])]; verify.check then builds the tree
D(a1; S) on labels 1..n and checks: labels 1..n once, lengths 1..n-1 once, growth order, tree shape, root.

Usage: rules.py paired-all N      every (bs, c) with n <= N (a1 = k-1 and a1 = k), bs in every order for n<=Nsmall
       rules.py two N             every member with at most two distinct non-root sizes, n <= N
       rules.py twos N | ones N   every k with n <= N
       rules.py random N count    random members of the paired family with n <= N
       rules.py show b1,b2,.. [c] print one comb
"""
import sys, random, itertools
from verify import check

def paired(bs, c=None):
    J=len(bs); k=2*J+(0 if c is None else 1)
    if c is not None: assert c%2==0 or c>=k, "middle hub must be even or odd >= k"
    e=0 if c is None else (c//2 if c%2==0 else (c-k)//2)
    odd = c is not None and c%2==1
    N=sum(bs)+e
    y = 3*k+2*N if odd else 2*k+2*N
    U={h:[] for h in range(1,2*k,2)}
    i=0; inter=set()
    runs=[(g,b) for g,b in enumerate(bs)]
    if c is not None: runs.append((J,e))
    for g,cnt in runs:
        for _ in range(cnt):
            i+=1; x=2*i-1; h=2*g+1; z=x+h
            U[h].append(x); U[2*k-h].append(z); inter.add(z)      # chain x -> x+h -> x+2k
    if odd:
        for z in range(2*N+1,2*N+2*k,2): U[k].append(z)            # k single steps of the middle hub
        W=[z for z in range(2,y-2*k,2) if z not in inter]+list(range(y-k+1,y-1,2))
    else:
        W=[z for z in range(2,y-1,2) if z not in inter]
    S=sorted([b for b in bs for _ in (0,1)]+([c] if c is not None else []),reverse=True)
    return S,len(W),y,sorted(U.items()),sorted(W)

def skolem(n):
    """Skolem sequence of order n = 0,1 (mod 4): pairs (a_i,b_i), b_i-a_i=i, covering 1..2n (Skolem 1957)."""
    if n==1: return {1:(1,2)}
    if n==4: P=[(1,2),(5,7),(3,6),(4,8)]
    elif n==5: P=[(8,9),(1,3),(4,7),(2,6),(5,10)]
    elif n%4==0:
        s=n//4
        P=[(4*s+r-1,8*s-r+1) for r in range(1,2*s+1)]+[(r,4*s-r-1) for r in range(1,s-1)]
        P+=[(s+r+1,3*s-r) for r in range(1,s-1)]+[(s-1,3*s),(s,s+1),(2*s,4*s-1),(2*s+1,6*s)]
    else:
        s=n//4
        P=[(4*s+r+1,8*s-r+3) for r in range(1,2*s+1)]+[(r,4*s-r+1) for r in range(1,s+1)]
        P+=[(s+r+2,3*s-r+1) for r in range(1,s-1)]+[(s+1,s+2),(2*s+1,6*s+2),(2*s+2,4*s+1)]
    return {b-a:(a,b) for a,b in P}

def hooked_skolem(n):
    """Hooked Skolem sequence of order n = 2,3 (mod 4): pairs covering 1..2n+1 except 2n (O'Keefe 1961)."""
    if n==2: P=[(1,2),(3,5)]
    elif n==3: P=[(2,3),(5,7),(1,4)]
    elif n%4==2:
        s=n//4
        P=[(r,4*s-r+2) for r in range(1,2*s+1)]+[(4*s+r+3,8*s-r+4) for r in range(1,s)]
        P+=[(5*s+r+2,7*s-r+3) for r in range(1,s)]+[(2*s+1,6*s+2),(4*s+2,6*s+3),(4*s+3,8*s+5),(7*s+3,7*s+4)]
    else:
        s=(n+1)//4
        P=[(4*s+r,8*s-r-2) for r in range(1,2*s-1)]+[(r,4*s-r-1) for r in range(1,s-1)]
        P+=[(s+r+1,3*s-r) for r in range(1,s-1)]+[(s-1,3*s),(s,s+1),(2*s,4*s-1),(2*s+1,6*s-1),(4*s,8*s-1)]
    return {b-a:(a,b) for a,b in P}

def pair_search(n, positions):
    """Pairs (a_i, a_i+i), i=1..n, tiling the given positions; depth-first with restarts (used only for
    Rosa / hooked Rosa sequences, whose existence is classical: Rosa 1966)."""
    sys.setrecursionlimit(10000)
    rng=random.Random(n)
    order=sorted(positions); limit=20000
    while True:
        free=set(positions); sol={}; cnt=[0]
        def rec(d):
            if d==0: return True
            cnt[0]+=1
            if cnt[0]>limit: return False
            for a in order:
                if a in free and a+d in free:
                    free.discard(a); free.discard(a+d); sol[d]=(a,a+d)
                    if rec(d-1): return True
                    free.add(a); free.add(a+d)
            return False
        if rec(n): return sol
        rng.shuffle(order); limit=int(limit*1.3)

def heffter(k):
    """k = 0 or 1 (mod 3), k != 4.  Returns (c, triples): c = 2k+1 and disjoint triples (p,q,r) with
    p+q+r = c, which together with the fixed point c/3 (k = 1 mod 3) contain exactly one number of each
    pair {z, c-z}, 1 <= z <= k.  (Heffter's difference problems; Peltesohn 1939.)"""
    j=k//3; c=2*k+1
    if j==0: return c,[]
    if k%3==0:
        P=skolem(j) if j%4 in (0,1) else hooked_skolem(j)
    else:
        if j%4 in (0,3): P=pair_search(j,[x for x in range(1,2*j+2) if x!=j+1])           # Rosa sequence
        else: P=pair_search(j,[x for x in range(1,2*j+3) if x not in (j+1,2*j+1)])       # hooked Rosa
    tr=[]
    for i,(a,b) in P.items():
        z=b+j                                   # i + (a+j) = z
        tr.append((i,a+j,c-z))                  # i + (a+j) + (c-z) = c
    return c,tr

def ones(k):
    """Theorem O: k hubs with one leaf each.  w = 0 (k = 0,1 mod 3), w = 1 (k = 2 mod 3)."""
    if k==4: return [1]*4,0,9,[(1,[2]),(2,[6]),(4,[3]),(5,[1])],[]
    if k%3!=2:
        c,tr=heffter(k); y=c; hubs=[]
        for p,q,r in tr: hubs+=[(q,[p]),(r,[q]),(p,[r])]      # frog at p jumps by q to y-r, and cyclically
        if k%3==1: hubs.append((c//3,[c//3]))
        return [1]*k,0,y,sorted(hubs),[]
    K=k+1; c,tr=heffter(K); y=2*K; hubs=[]; W=[]
    for t in tr:
        for p,q in ((t[0],t[1]),(t[1],t[2]),(t[2],t[0])):       # head c-q owns the length p
            if q==1: W=[p]
            else: hubs.append((q-1,[p]))
    return [1]*k,1,y,sorted(hubs),W

def twos(k):
    if k%4==0:
        P=skolem(k); y=3*k+1; W=[]
        hubs=[(y-(b+k),[i,a+k]) for i,(a,b) in P.items()]
    elif k%2==0:    # nested: even differences round the hole k/2+1, odd differences in a second nest
        P={}
        for r in range(1,k//2+1):
            P[2*r]=(k//2+1-r,k//2+1+r); P[2*r-1]=(3*k//2+2-r,3*k//2+1+r)
        y=3*k+2; W=[y//2]
        hubs=[(y-(b+k),[i,a+k]) for i,(a,b) in P.items()]
    elif k%4==1:
        P=skolem(k); y=3*k+1; W=[]
        hubs=[(y-(b+k),[i,a+k]) for i,(a,b) in P.items()]
    else:
        K=k+1; P=skolem(K); y=3*K; W=[]; hubs=[]
        for i,(a,b) in P.items():
            if b+K==y: W=[i,a+K]
            else: hubs.append((y-(b+K),[i,a+K]))
    return [2]*k,len(W),y,sorted(hubs),sorted(W)

def test(cert, extra=(0,1)):
    S,w,y,hubs,W=cert
    assert sorted(len(U) for h,U in hubs)==sorted(S)
    ns=[]
    for d in extra: ns.append(check(S,w,y,hubs,W,w+d))
    return ns[0]

def partitions(total, parts, maxv):
    if parts==0:
        if total==0: yield []
        return
    for f in range(min(total,maxv),-1,-1):
        for rest in partitions(total-f,parts-1,f): yield [f]+rest

if __name__=="__main__":
    cmd=sys.argv[1]
    if cmd=="show":
        bs=list(map(int,sys.argv[2].split(','))) if sys.argv[2] else []
        c=int(sys.argv[3]) if len(sys.argv)>3 else None
        S,w,y,hubs,W=paired(bs,c); test((S,w,y,hubs,W))
        print("S",*S,"| w",w,"y",y,"|",' '.join("%d:%s"%(h,','.join(map(str,U))) for h,U in hubs),"| W",*W)
    elif cmd=="twos":
        N=int(sys.argv[2]); cnt=0; k=1
        while True:
            S,w,y,hubs,W=twos(k)
            if 1+(k+1)+2*k+2>N: break
            a1max=N-(1+(k+1)+2*k)
            for a1 in sorted(set([w,2,3,a1max])):
                if a1>=w: check(S,w,y,hubs,W,a1); cnt+=1
            k+=1
        print("Theorem Q: D(a1; 2^k) checked for every k = 1..%d with a1 = w, 2, 3 and the largest a1 with n <= %d: %d trees, all pass"%(k-1,N,cnt))
    elif cmd=="ones":
        N=int(sys.argv[2]); cnt=0; k=1
        while 2*k+2+1<=N:
            S,w,y,hubs,W=ones(k)
            assert w==(1 if k%3==2 else 0)
            for a1 in sorted(set([w,1,2,N-2*k-2])):
                if a1>=w: check(S,w,y,hubs,W,a1); cnt+=1
            k+=1
        print("Theorem O: D(a1; 1^k) checked for every k = 1..%d with a1 = w, 1, 2 and the largest a1 with n <= %d: %d trees, all pass"%(k-1,N,cnt))
    elif cmd=="paired-all":
        N=int(sys.argv[2]); Nsmall=int(sys.argv[3]) if len(sys.argv)>3 else 0; cnt=0; fam=0
        for J in range(0,N):
            for hasc in (0,1):
                k=2*J+hasc
                if k==0: continue
                # n = 1 + (k+1) + sum S + a1, a1 = k-1  ->  sum S <= N-2k-1
                budget=N-2*k-1
                if budget<0: continue
                for tot in range(0,budget//2+1):
                    for bs in partitions(tot,J,tot):
                        cs=[None] if not hasc else [c for c in range(0,budget-2*tot+1) if c%2==0 or c>=k]
                        for c in cs:
                            orders=[bs]
                            if 1+(k+1)+2*tot+(c or 0)+k-1<=Nsmall: orders=set(itertools.permutations(bs))
                            for o in orders:
                                test(paired(list(o),c)); cnt+=1
                            fam+=1
        print("Theorem P: every member (pairs b_1..b_J, optional middle c) with n <= %d at a1 = k-1 and a1 = k: %d size patterns, %d combs (all orders of the pairs for n <= %d), all pass"%(N,fam,cnt,Nsmall))
    elif cmd=="two":
        N=int(sys.argv[2]); cnt=0
        # non-root sizes a^d b^e (a>b>=0, d>=1, e>=0); needs: d,e not both odd; if exactly one is odd that size is the middle
        for a in range(0,N):
            for d in range(1,N):
                if 1+(d+1)+d*a+(d-1)>N: break
                for b in range(0,a):
                    for e in range(0,N):
                        if e==0 and b>0: continue
                        k=d+e
                        if 1+(k+1)+d*a+e*b+(k-1)>N: break
                        if d%2 and e%2: continue
                        c=None
                        if d%2: c=a
                        if e%2: c=b
                        if c is not None and not (c%2==0 or c>=k): continue
                        bs=[a]*(d//2)+[b]*(e//2)
                        test(paired(bs,c)); cnt+=1
                        if d>=2 and e>=2: test(paired(bs[::-1],c)); 
        print("Theorem P, at most two distinct non-root sizes: every admissible (a,d,b,e) with n <= %d at a1 = k-1 and k: %d size patterns, all pass"%(N,cnt))
    elif cmd=="random":
        N=int(sys.argv[2]); R=int(sys.argv[3]); rng=random.Random(1); cnt=0
        while cnt<R:
            J=rng.randint(0,12); hasc=rng.randint(0,1); k=2*J+hasc
            if k==0: continue
            bs=[rng.choice([0,1,2,3,5,8,rng.randint(0,30)]) for _ in range(J)]
            c=None
            if hasc:
                c=rng.randint(0,40)
                if c%2 and c<k: c+=k+ (k+c)%2*0
                if c%2 and c<k: continue
            if 1+(k+1)+2*sum(bs)+(c or 0)+k-1>N: continue
            test(paired(bs,c)); cnt+=1
        print("Theorem P: %d random members with n <= %d, all pass"%(cnt,N))
