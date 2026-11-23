#!/usr/bin/env python3
"""Explicit deals for the spider with one leg of length r and k legs of length 2  (legs (r,2,...,2), m = r+2k).

TOP-BLOCK RULE.  B = r+k.  The k short legs get the top numbers B+1..m as first numbers (labels B+1..m).
A *design* for k is  (c, delta_1..delta_k):  distinct offsets delta_i >= 0 such that, writing
    Delta = {delta_i},   rank(d) = #{e in Delta : e < d},   pi(d) = (d + rank(d))/2,
  (a) d - rank(d) is even for every d in Delta        (runs of Delta are separated by gaps of even length),
  (b) i -> c - i - delta_i  is a bijection from {1..k} onto {pi(d) : d in Delta}.
Given a design with c = B (mod 3) and l = (B-c)/3 >= 0, v = B-2l, v - max(Delta) >= 1:
    short leg i (i=1..k):  numbers  B+i, then v - delta_i  (up, then down)   -> labels B+i, 2l+i+delta_i
    long leg:  all other numbers of 1..B, in decreasing order, alternately up, down, up, ...
Designs:
    odd(k)      k odd,  c=(3k-1)/2          closed form
    even(k)     k even, c=3k/2+1            closed form        (both have c = 1 mod 3)
    tower(k,t)  k divisible by 3, t=0,1,2   closed form, c = 1 + t*q (mod 3)  -> all three residues
    gap(k,a)    Delta=[0,a-1] u [a+2,k+1]    matching by a fixed greedy order (no backtracking); optional (GREEDY=1),
                gives smaller c for many k divisible by 3 but gets stuck first at k=63
"""
import sys
from fractions import Fraction

def is_design(k, c, delta):
    if len(delta)!=k or len(set(delta))!=k or min(delta)<0: return False
    srt=sorted(delta); pi={}
    for rank,d in enumerate(srt):
        if (d-rank)%2: return False
        pi[d]=(d+rank)//2
    return sorted(c-(i+1)-delta[i] for i in range(k))==sorted(pi.values())

def design_odd(k):          # k odd
    c=(3*k-1)//2
    return c,[k-2*i if i<=(k-1)//2 else 2*k-2*i for i in range(1,k+1)]

def design_even(k):         # k = 2h
    h=k//2; d=[None]*(k+1)
    for s in range(h): d[2*h-1-2*s]=h+2+s
    for j in range(1,h+1): d[2*j]=h-j
    return 3*h+1,d[1:]

def design_tower(k,t):
    """k divisible by 3, t in {0,1,2}.  q = k with all factors 2 and 3 removed, Q = 3q, T = k/Q.
    inner:  odd(q).   middle (size Q): three shifted copies of odd(q), c_mid = (3+t)q + (3q-1)/2.
    outer (size k): T copies of the middle design, copy J (J=0..T-1) shifted by 3Q(T-1-J);  c = 3Q(T-1) + c_mid.
    c = 1 + t*q (mod 3), and q is prime to 3, so t = 0,1,2 give the three residues."""
    q=k
    while q%2==0: q//=2
    while q%3==0: q//=3
    Q=3*q; T=k//Q; c0,d0=design_odd(q)
    D,al = [((0,q,2*q),(1,2,0)), ((0,q,4*q),(2,0,1)), ((0,3*q,4*q),(1,2,0))][t]
    mid=[D[al[j]]+d0[i2] for j in range(3) for i2 in range(q)]; cmid=(3+t)*q+c0
    return 3*Q*(T-1)+cmid, [3*Q*(T-1-J)+mid[i] for J in range(T) for i in range(Q)]

def gap_sets(k,a):
    return list(range(0,a))+list(range(a+2,k+2)), list(range(0,a))+list(range(a+1,k+1))

def design_gap_greedy(k,a):
    """Delta=[0,a-1] u [a+2,k+1], Pi=[0,a-1] u [a+1,k].  Even i ascending, then odd i ascending; each i takes the
    largest free delta whose partner pi=c-i-delta is free.  Returns None if the greedy gets stuck."""
    D,P=gap_sets(k,a); c=Fraction(k*(k+1)//2+sum(D)+sum(P),k)
    if c.denominator!=1: return None
    c=int(c); Df=set(D); Pf=set(P); res=[None]*(k+1)
    for i in list(range(2,k+1,2))+list(range(1,k+1,2)):
        for d in sorted(Df,reverse=True):
            if c-i-d in Pf: Df.discard(d); Pf.discard(c-i-d); res[i]=d; break
        else: return None
    return c,res[1:]

def mirror(k,cd):
    """(i,delta,pi) -> (k+1-i, maxDelta-delta, maxPi-pi) maps gap(k,a) to gap(k,k-a)."""
    if cd is None: return None
    c,d=cd; mx=max(d); srt=sorted(d); mp=(mx+k-1)//2
    return (k+1)+mx+mp-c, [mx-d[k-i] for i in range(1,k+1)]

import os
GREEDY=bool(os.environ.get("GREEDY"))    # optional: also try the greedy gap designs (smaller c, so smaller first r); not needed
_cache={}
def designs(k):
    """dict residue (c mod 3) -> (c, delta, name); among available designs for a residue the smallest c is kept"""
    if k in _cache: return _cache[k]
    out={}
    def add(cd,name):
        if cd is None: return
        c,d=cd
        assert is_design(k,c,d),(k,name)
        if c%3 not in out or c<out[c%3][0]: out[c%3]=(c,d,name)
    add(design_odd(k) if k%2 else design_even(k), "odd" if k%2 else "even")
    if k%3==0:
        for t in range(3): add(design_tower(k,t),"tower")
        if GREEDY:
            for a in ([k//3,2*k//3] if k%2 else [k//6,5*k//6]):
                add(design_gap_greedy(k,a),"gap greedy")
                add(mirror(k,design_gap_greedy(k,k-a)),"gap mirrored greedy")
    _cache[k]=out; return out

def deal(r,k):
    """Return per-leg lists [(number, sign), ...] (long leg first) or None if the rule does not apply."""
    B=r+k; ds=designs(k)
    if B%3 not in ds: return None
    c,delta,name=ds[B%3]
    if B<c: return None
    l=(B-c)//3; v=B-2*l
    if v-max(delta)<1: return None
    Dset={v-d for d in delta}
    W=[w for w in range(B,0,-1) if w not in Dset]
    lists=[[(w,1 if j%2==0 else -1) for j,w in enumerate(W)]]
    for i in range(1,k+1): lists.append([(B+i,1),(v-delta[i-1],-1)])
    return lists

if __name__=="__main__":
    r,k=int(sys.argv[1]),int(sys.argv[2]); L=deal(r,k)
    if L is None: print("rule does not apply to r=%d k=%d"%(r,k)); sys.exit(1)
    for leg in L:
        t=0; labs=[]
        for w,s in leg: t+=s*w; labs.append(t)
        print("leg %d  numbers: %s   labels: %s"%(len(leg)," ".join(map(str,[w for w,s in leg]))," ".join(map(str,labs))))
