#!/usr/bin/env python3
"""Theorem R (REPORT.txt): rounds in front of a paired comb.  Hub labels 1,3,..,2k-1 (token i <-> 2i+1).

rounds(k, R, bs, c): R = [(B_1,pi_1),...,(B_T,pi_T)], B_t odd, pi_t a permutation of 0..k-1.
  Round t gives the length sigma_{t-1}+2i+1 to the hub with label B_t+2(pi_t(i)-i) (sigma_t = B_1+..+B_t);
  its leaf sits at cell sigma_t+2pi_t(i)+1.  After the rounds comes the mirror image (x -> y-x) of the
  paired comb paired(bs,c) of rules.py, shifted by sigma_T.
  Conditions (asserted): labels in {1,3,..,2k-1};  B_t+B_{t+1} >= 2k;  B_T >= k-1 (>= k if c is odd).
  Result: sizes = paired sizes + round counts,  w = k-1 + sum(B_t-k).
Usage: rounds.py two N          Corollary R1, every member with n <= N
       rounds.py test N         random members with n <= N, and the family P+ exhaustively for n <= Nsmall
       rounds.py show k "B:p0,p1,..;B:..." b1,b2,.. [c]
"""
import sys, random
from verify import check
from rules import paired
def dual(cert):
    S,w,y,hubs,W=cert
    return S,w,y,[(h,sorted(y-h-u for u in U)) for h,U in hubs],sorted(y-x for x in W)
def rounds(k,R,bs,c=None):
    S0,w0,y0,hubs0,W0=dual(paired(bs,c))
    assert len(hubs0)==k and [h for h,U in hubs0]==list(range(1,2*k,2))
    U={h:[] for h in range(1,2*k,2)}; sig=0; used=set(range(1,2*k,2))
    for t,(B,pi) in enumerate(R):
        assert B%2==1 and sorted(pi)==list(range(k))
        if t+1<len(R): assert B+R[t+1][0]>=2*k
        for i in range(k):
            h=B+2*(pi[i]-i); assert h in U, "label"
            U[h].append(sig+2*i+1)
        sig+=B
    if R: assert R[-1][0]>=(k if (c is not None and c%2) else k-1)
    for h,Us in hubs0: U[h]+=[u+sig for u in Us]
    y=y0+sig
    tok=set(s+2*i+1 for s in [sum(B for B,_ in R[:t]) for t in range(len(R))] for i in range(k))   # A_0..A_{T-1}
    W=sorted(set(range(1,sig+1))-tok)+[x+sig for x in W0 if x+sig not in tok]
    S=sorted((len(u) for u in U.values()),reverse=True)
    return S,len(W),y,sorted(U.items()),W
def run(cert,extra=(0,1,5)):
    S,w,y,hubs,W=cert
    return [check(S,w,y,hubs,W,w+d) for d in extra][0]
def randperm(k,B,rng):
    """random permutation with all labels B+2(pi(i)-i) in [1,2k-1]"""
    for _ in range(200):
        pi=list(range(k))
        for _ in range(rng.randint(0,2*k)):
            i=rng.randrange(k); j=rng.randrange(k); pi[i],pi[j]=pi[j],pi[i]
        if all(1<=B+2*(pi[i]-i)<=2*k-1 for i in range(k)): return pi
    return list(range(k)) if 1<=B<=2*k-1 else None
if __name__=="__main__":
    if sys.argv[1]=="show":
        k=int(sys.argv[2]); R=[]
        for tok in sys.argv[3].split(';'):
            if tok: B,_,p=tok.partition(':'); R.append((int(B),list(map(int,p.split(','))) if p else list(range(k))))
        bs=list(map(int,sys.argv[4].split(','))) if len(sys.argv)>4 and sys.argv[4] else [0]*(k//2)
        c=int(sys.argv[5]) if len(sys.argv)>5 else (0 if k%2 else None)
        S,w,y,hubs,W=rounds(k,R,bs,c); run((S,w,y,hubs,W))
        print("S",*S,"| w",w,"y",y,"|",' '.join("%d:%s"%(h,','.join(map(str,U))) for h,U in hubs),"| W",*W)
    elif sys.argv[1]=="two":
        # Corollary R1: non-root sizes (b+k*j)^d b^e with d, e odd, k = d+e, j >= 1; w = k-1+j
        N=int(sys.argv[2]); cnt=0
        for d in range(1,N,2):
            for e in range(1,N,2):
                k=d+e
                if 1+(k+1)+d*k+k-1+1>N: break
                for j in range(1,N):
                    if 1+(k+1)+d*k*j+k-1+j>N: break
                    for b in range(0,N):
                        if 1+(k+1)+d*(b+k*j)+e*b+k-1+j>N: break
                        bs=[b]*((e-1)//2)+[b+k*j]*((d-1)//2)+[b]          # last pair = labels k-1, k+1
                        cert=rounds(k,[(k+1,list(range(k)))]*j,bs,None)
                        assert cert[0]==sorted([b+k*j]*d+[b]*e,reverse=True) and cert[1]==k-1+j
                        run(cert,(0,1)); cnt+=1
        print("Corollary R1: every (b,j,d,e), d and e odd, with n <= %d at a1 = w and w+1: %d size patterns, all pass"%(N,cnt))
    else:
        N=int(sys.argv[2]); Nsmall=int(sys.argv[3]) if len(sys.argv)>3 else 40; rng=random.Random(11)
        # (1) family P+ : every pair (b, b + k*j) , rounds with pi = id and B = an upper label > k (or = k: middle hub)
        cnt=0
        def parts(total,parts_,maxv):
            if parts_==0:
                if total==0: yield []
                return
            for f in range(min(total,maxv),-1,-1):
                for rest in parts(total-f,parts_-1,f): yield [f]+rest
        for k in range(1,Nsmall):
            J=k//2
            uppers=[h for h in range(k,2*k,2)] if k%2 else [h for h in range(k+1,2*k,2)]
            for T in range(0,4):
                import itertools
                for Bs in itertools.combinations_with_replacement(uppers,T):
                    wr=k-1+sum(B-k for B in Bs)
                    base=1+(k+1)+k*T+wr
                    if base>Nsmall: continue
                    for tot in range(0,(Nsmall-base)//2+1):
                        for bs in parts(tot,J,tot):
                            cs=[None] if k%2==0 else [c for c in range(0,Nsmall-base-2*tot+1) if c%2==0 or c>=k]
                            for c in cs:
                                for order in set(itertools.permutations(Bs)):
                                    cert=rounds(k,[(B,list(range(k))) for B in order],bs,c)
                                    assert cert[1]==wr; run(cert); cnt+=1
        print("Theorem R with identity rounds (family P+): every member with n <= %d and at most 3 rounds: %d combs, all pass"%(Nsmall,cnt))
        # (2) random rounds
        cnt=0; tries=0
        while cnt<30000:
            tries+=1
            k=rng.randint(1,14); T=rng.randint(1,6); R=[]; ok=True
            for t in range(T):
                lo=1 if t==0 else max(1,2*k-R[-1][0])
                B=rng.choice([b for b in range(lo|1,2*k+4,2) if b>=lo][:4])
                pi=randperm(k,B,rng)
                if pi is None: ok=False; break
                R.append((B,pi))
            if not ok: continue
            J=k//2; bs=[rng.choice([0,0,1,2,3,rng.randint(0,12)]) for _ in range(J)]
            c=None
            if k%2:
                c=rng.randint(0,20)
                if c%2 and c<k: c+=1
            if R[-1][0]<(k if (c is not None and c%2) else k-1): continue
            wr=k-1+sum(B-k for B,_ in R)
            if wr<0 or 1+(k+1)+k*T+2*sum(bs)+(c or 0)+wr>N: continue
            cert=rounds(k,R,bs,c); assert cert[1]==wr
            run(cert); cnt+=1
        print("Theorem R: %d random members (k <= 14, up to 6 rounds, random permutations) with n <= %d, all pass"%(cnt,N))
