#!/usr/bin/env python3
"""Enumerate, for n <= N, every pair (S, w) produced by Theorem C (caravans; moves Z, R(a,b), B(a), and for k <= KPERM every permutation move)
and by Theorem R (rounds with arbitrary admissible permutations in front of a paired comb).
Used by coverage.py.  families(N) returns {S (sorted tuple): {w: tag}}; a pair (S,w) serves the trees
D(a1; S) with a1 >= w, so it matters only if |S| + sum(S) + w + 2 <= N.
Every 37th generated pair is rebuilt as an explicit comb and checked with verify.check (when run as main).
"""
import sys, itertools
KPERM=6
def caravan_pairs(N):
    out={}
    for k in range(1,N):
        for l in range(1,N):
            w0=2*(l-1)
            if k+2+w0>N: break
            budget=N-k-2          # sum(S) + w <= budget
            labels=list(range(l,l+k))
            moves=[]              # (vector increments {label:inc}, wcost)
            if k in labels: moves.append(({k:1},0))
            for a in range(1,k):
                for b in range(1,k):
                    if k+a in labels and k-b in labels: moves.append(({k+a:b,k-b:a},0))
            for a in range(1,k):
                if k+a in labels: moves.append(({k+a:k},a))
            if k<=KPERM:                      # every permutation move (delta, pi) of Lemma C
                seen=set()
                for delta in range(0,budget-w0+1):
                    for r in ([k] if delta else range(1,k+1)):
                        if r>budget: continue
                        for pi in itertools.permutations(range(r)):
                            hs=[k+delta+pi[j]-j for j in range(r)]
                            if all(h in labels for h in hs):
                                inc={}
                                for h in hs: inc[h]=inc.get(h,0)+1
                                key=(tuple(sorted(inc.items())),delta)
                                if key not in seen: seen.add(key); moves.append((inc,delta))
            cur={(tuple([0]*k),w0)}
            for inc,wc in moves:          # unbounded knapsack: add this move any number of times
                new=set(cur); frontier=cur
                while frontier:
                    nxt=set()
                    for vec,w in frontier:
                        v=list(vec)
                        for h,d in inc.items(): v[h-l]+=d
                        if sum(v)+w+wc<=budget:
                            t=(tuple(v),w+wc)
                            if t not in new: new.add(t); nxt.add(t)
                    frontier=nxt
                cur=new
            for vec,w in cur:
                S=tuple(sorted(vec,reverse=True))
                out.setdefault(S,{}).setdefault(w,'C')
    return out
def round_vectors(k,B):
    """all label-count vectors of one round with shift B (labels B+2(pi(i)-i) in [1,2k-1])"""
    res=set()
    def rec(i,used,vec):
        if i==k: res.add(tuple(vec)); return
        for j in range(k):
            if not used>>j&1:
                h=B+2*(j-i)
                if 1<=h<=2*k-1:
                    vec[(h-1)//2]+=1; rec(i+1,used|1<<j,vec); vec[(h-1)//2]-=1
    rec(0,0,[0]*k); return res
def rounds_pairs(N,kmax=7):
    out={}
    for k in range(1,min(kmax,N)+1):
        budget0=N-k-2-(k-1)       # sum(S) + sum(B_t-k) <= budget0
        if budget0<0: break
        Bs=[B for B in range(1,2*k+2*budget0+2,2)]
        rv={B:round_vectors(k,B) for B in Bs if B-k<=budget0}
        rv={B:v for B,v in rv.items() if v}
        # states after t rounds: (lastB, vec, extra) ; T = 0 allowed
        states={(None,tuple([0]*k),0)}; allst=set(states)
        while states:
            nxt=set()
            for lastB,vec,ex in states:
                for B,vs in rv.items():
                    if lastB is not None and lastB+B<2*k: continue
                    if ex+(B-k)+sum(vec)+k>budget0 and True:
                        if sum(vec)+k+ex+(B-k)>budget0: continue
                    for v in vs:
                        t=(B,tuple(x+y for x,y in zip(vec,v)),ex+B-k)
                        if t not in allst: allst.add(t); nxt.add(t)
            states=nxt
        J=k//2
        def parts(total,n_):
            if n_==0:
                if total==0: yield ()
                return
            for f in range(total+1):
                for rest in parts(total-f,n_-1): yield (f,)+rest
        for lastB,vec,ex in allst:
            if ex<-(k-1): continue
            rem=budget0-sum(vec)-ex
            for tot in range(0,rem//2+1):
                for bs in parts(tot,J):
                    cs=[None] if k%2==0 else [c for c in range(0,rem-2*tot+1) if c%2==0 or c>=k]
                    for c in cs:
                        if lastB is not None and lastB<(k if (c is not None and c%2) else k-1): continue
                        v=list(vec)
                        for g,b in enumerate(bs): v[g]+=b; v[k-1-g]+=b
                        if c is not None: v[J]+=c
                        w=k-1+ex
                        if w<0: continue
                        S=tuple(sorted(v,reverse=True))
                        out.setdefault(S,{}).setdefault(w,'R')
    return out
def families(N):
    out=caravan_pairs(N)
    for S,d in rounds_pairs(N).items():
        for w,t in d.items(): out.setdefault(S,{}).setdefault(w,t)
    return out
if __name__=="__main__":
    N=int(sys.argv[1]); f=families(N)
    print("n <= %d: %d multisets S have a comb from Theorem C or Theorem R (some w)"%(N,len(f)))
