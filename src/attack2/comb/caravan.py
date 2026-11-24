#!/usr/bin/env python3
"""Caravan combs (REPORT.txt, Lemma C and Theorem C): hub labels are a block L = [l, l+k-1].

A caravan is a list of moves.  State: an integer c; the k "tokens" are the cells c..c+k-1 (already used
as cells, not yet as lengths).  Start c = l (tokens = the hub cells).  A move (delta, pi), pi a permutation
of 0..r-1 (r = k whenever delta > 0), makes c+k..c+k+delta-1 inside fillers and gives the length c+j to
the hub with label k+delta+pi(j)-j (so its leaf sits at cell c+k+delta+pi(j)); then c += r+delta.
At the end y = c+l+k-1, and 1..l-1 and y-l+1..y-1 are fillers too.
Named moves:  Z = (0, id on 1)            one leaf for hub k
              R(a,b) = (0, rotation)      b leaves for hub k+a and a leaves for hub k-b
              B(a) = (a, id on k)         k leaves for hub k+a, a fillers
Usage: caravan.py test N      random caravans and the families of Theorem C with n <= N, checked by verify.check
       caravan.py show k l move move ...     moves: Z  Ra,b  Ba      e.g.  caravan.py show 3 2 R1,1 Z B1
"""
import sys, random
from verify import check
def build(k,l,moves):
    L=range(l,l+k); U={h:[] for h in L}; W=list(range(1,l)); c=l
    for delta,pi in moves:
        r=len(pi); assert sorted(pi)==list(range(r)) and (delta==0 or r==k) and r<=k
        W+=range(c+k,c+k+delta)
        for j in range(r):
            h=k+delta+pi[j]-j; assert h in U, "label %d not in block"%h
            U[h].append(c+j)
        c+=r+delta
    y=c+l+k-1; W+=range(y-l+1,y)
    S=sorted((len(u) for u in U.values()),reverse=True)
    return S,len(W),y,sorted(U.items()),sorted(W)
Z=(0,[0])
def R(a,b): return (0,[j+a for j in range(b)]+[j-b for j in range(b,a+b)])
def B(a,k): return (a,list(range(k)))
def from_counts(k,l,n0,x,z,rng=None):
    """n0 moves Z, x[(a,b)] moves R(a,b), z[a] moves B(a), in the given or a random order."""
    mv=[Z]*n0+[R(a,b) for (a,b),c in x.items() for _ in range(c)]+[B(a,k) for a,c in z.items() for _ in range(c)]
    if rng: rng.shuffle(mv)
    return build(k,l,mv)
def run(cert,extra=(0,1,7)):
    S,w,y,hubs,W=cert
    return [check(S,w,y,hubs,W,w+d) for d in extra][0]
if __name__=="__main__":
    if sys.argv[1]=="show":
        k=int(sys.argv[2]); l=int(sys.argv[3]); mv=[]
        for t in sys.argv[4:]:
            if t=="Z": mv.append(Z)
            elif t[0]=="R": a,b=map(int,t[1:].split(',')); mv.append(R(a,b))
            else: mv.append(B(int(t[1:]),k))
        S,w,y,hubs,W=build(k,l,mv); run((S,w,y,hubs,W))
        print("S",*S,"| w",w,"y",y,"|",' '.join("%d:%s"%(h,','.join(map(str,U))) for h,U in hubs),"| W",*W)
    else:
        N=int(sys.argv[2]); rng=random.Random(7)
        # (1) corollary C1: k = 3, labels 2,3,4, sizes (s, t, s+3z), w = 2+z, every member with n <= N at a1 = w
        cnt=0
        for s in range(0,N):
            for t in range(0,N):
                if 1+4+2*s+t+2>N: break
                for z in range(0,N):
                    if 1+4+2*s+t+3*z+2+z>N: break
                    for order in range(2):
                        cert=from_counts(3,2,t,{(1,1):s},{1:z},rng if order else None)
                        assert cert[0]==sorted([s,t,s+3*z],reverse=True) and cert[1]==2+z
                        run(cert); cnt+=1
        print("Corollary C1 (sizes s, t, s+3z; labels 2,3,4): every (s,t,z) with n <= %d at a1 = w, w+1, w+7, two move orders: %d combs, all pass"%(N,cnt))
        # (2) Theorem C: random k, l, random counts of Z, R(a,b), B(a)
        cnt=0
        while cnt<20000:
            k=rng.randint(1,12); l=rng.randint(1,k+2)
            pos=[a for a in range(1,k) if l<=k+a<=l+k-1]; neg=[b for b in range(1,k) if l<=k-b<=l+k-1]
            x={}; z={}
            for _ in range(rng.randint(0,6)):
                if pos and neg:
                    key=(rng.choice(pos),rng.choice(neg)); x[key]=x.get(key,0)+rng.randint(1,3)
            for _ in range(rng.randint(0,2)):
                if pos: a=rng.choice(pos); z[a]=z.get(a,0)+1
            n0=rng.randint(0,8) if l<=k<=l+k-1 else 0
            exp={h:0 for h in range(l,l+k)}
            if n0: exp[k]+=n0
            for (a,b),c in x.items(): exp[k+a]+=b*c; exp[k-b]+=a*c
            for a,c in z.items(): exp[k+a]+=k*c
            w=2*(l-1)+sum(a*c for a,c in z.items())
            if 1+(k+1)+sum(exp.values())+w>N: continue
            cert=from_counts(k,l,n0,x,z,rng)
            assert dict((h,len(u)) for h,u in cert[3])==exp and cert[1]==w
            run(cert); cnt+=1
        print("Theorem C: %d random caravans (k <= 12, moves Z, R(a,b), B(a) in random order) with n <= %d, all pass"%(cnt,N))
        # (2b) Corollary C3: sizes prescribed on the labels, moment = k*B, s_{k-1} >= sum_{a>=2} a*s_{k+a}
        cnt=0
        while cnt<20000:
            k=rng.randint(3,12); l=rng.randint(2,k-1); s={h:0 for h in range(l,l+k)}
            for h in s:
                if h not in (k-1,k+1): s[h]=rng.choice([0,0,1,1,2,3,rng.randint(0,9)])
            up=sum((h-k)*s[h] for h in s if h>=k+2); dn=sum((k-h)*s[h] for h in s if h<=k-2)
            t=rng.randint(0,6); Bz=rng.randint(0,3)
            s[k-1]=t+up; s[k+1]=t+dn+k*Bz
            assert sum(v*(h-k) for h,v in s.items())==k*Bz
            w=2*(l-1)+Bz
            if 1+(k+1)+sum(s.values())+w>N: continue
            x={(1,1):t}
            for h in s:
                if h>=k+2 and s[h]: x[(h-k,1)]=s[h]
                if h<=k-2 and s[h]: x[(1,k-h)]=s[h]
            cert=from_counts(k,l,s[k],x,{1:Bz},rng)
            assert dict((h,len(u)) for h,u in cert[3])==s and cert[1]==w
            run(cert); cnt+=1
        print("Corollary C3: %d random size assignments (k <= 12) with n <= %d, all pass"%(cnt,N))
        # (3) Lemma C with arbitrary permutation moves
        cnt=0
        while cnt<20000:
            k=rng.randint(1,10); l=rng.randint(1,k+1); mv=[]; ok=True
            for _ in range(rng.randint(1,10)):
                for tries in range(50):
                    delta=rng.choice([0,0,0,1,2]); r=k if delta else rng.randint(1,k)
                    pi=list(range(r)); rng.shuffle(pi)
                    if all(l<=k+delta+pi[j]-j<=l+k-1 for j in range(r)): mv.append((delta,pi)); break
            if not mv: continue
            cert=build(k,l,mv)
            if 1+(k+1)+sum(cert[0])+cert[1]>N: continue
            run(cert,(0,1)); cnt+=1
        print("Lemma C: %d random caravans with arbitrary permutation moves, n <= %d, all pass"%(cnt,N))
