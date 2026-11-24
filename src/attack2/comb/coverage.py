#!/usr/bin/env python3
"""Which diameter-4 trees are covered by a written proof?  (REPORT.txt, section 7.)
A tree is the multiset Sigma of leaf counts of the centre's neighbours (>= 2 positive entries).
Covered if it is a caterpillar (Rosa 1967), or some neighbour r can be the root with S = Sigma - {r}:
  T3  S has two entries p >= q >= 1 and r >= p                       (three-hub theorem, gamestrategy)
  EQ  S = a^d, a >= 1, r >= d-1                                      (equal-hub theorem, gamestrategy)
  P   S = pairs of equal sizes (+ one more size c, even or odd >= |S|), r >= |S|-1      (Theorem P)
  Q   S = 2^k, r >= w(k) = 0,0,1,2 for k = 0,1,2,3 mod 4                (Theorem Q)
  O   S = 1^k, r >= w(k) = 0,0,1 for k = 0,1,2 mod 3                    (Theorem O)
  C   Theorem C (caravans, moves Z, R(a,b), B(a)) and
  R   Theorem R (rounds in front of a paired comb): the pairs (S, w) enumerated by covergen.py, r >= w
  Z   Sigma = Sigma' + zeros, where Sigma' is covered with the root's leaves all inside the comb
      (w = r exactly: P or EQ with r = |S|-1; Q or O with r = w(k); C or R
      with some w = r), by Lemma 6 at the centre (the centre then carries the largest label).
The root r may be ANY neighbour of the centre (this file is about growth placements, not about the
all-up comb conjecture, which wants a largest hub as root).
Usage: coverage.py N [list|all] [cert=M]
  cert=M: a tree with no rule counts as 'certified' (not open) if the tree minus one largest hub, S, has
          |S|+sum(S)+max(S)+2 <= M (the range of the certificate run, REPORT.txt section 2).      (N <= 24 is quick)"""
import sys, collections
from covergen import families
FAM={}
def gen(total,k,maxv):
    if k==0:
        if total==0: yield []
        return
    for f in range(min(total,maxv),-1,-1):
        for rest in gen(total-f,k-1,f): yield [f]+rest
def P_ok(S,r):
    k=len(S)
    if r<k-1: return False
    odd=[s for s,c in collections.Counter(S).items() if c%2]
    if k%2==0: return not odd
    return len(odd)==1 and (odd[0]%2==0 or odd[0]>=k)
def rooted(S,r,closed=False):
    k=len(S)
    if k==0: return None
    f=FAM.get(tuple(sorted(S,reverse=True)),{})
    if closed:
        if r in f: return f[r]
        if P_ok(S,r) and r==k-1: return 'P'
        if all(s==2 for s in S) and r==(0,0,1,2)[k%4]: return 'Q'
        if all(s==1 for s in S) and r==(0,0,1)[k%3]: return 'O'
        if len(set(S))==1 and S[0]>=1 and r==k-1: return 'EQ'
        return None
    if k==2 and S[1]>=1 and r>=S[0]: return 'T3'
    if len(set(S))==1 and S[0]>=1 and r>=k-1: return 'EQ'
    if P_ok(S,r): return 'P'
    if all(s==2 for s in S) and r>=(0,0,1,2)[k%4]: return 'Q'
    if all(s==1 for s in S) and r>=(0,0,1)[k%3]: return 'O'
    for w in f:
        if w<=r: return f[w]
    return None
def covered(Sig):
    if sum(1 for s in Sig if s>0)<=2: return 'caterpillar'
    for r in sorted(set(Sig),reverse=True):
        S=list(Sig); S.remove(r); c=rooted(S,r)
        if c: return c
    z=Sig.count(0)
    if z:
        core=[s for s in Sig if s>0]
        for r in sorted(set(Sig),reverse=True):          # the root may also be a leaf of the centre (r = 0)
            rest=list(core); zr=z
            if r>0: rest.remove(r)
            else: zr-=1
            for keep in range(0,zr):                     # keep some zeros as hubs of the comb, add zr-keep >= 1 by Lemma 6
                if rooted(rest+[0]*keep,r,True): return 'Z'
    return None
N=int(sys.argv[1]); show=len(sys.argv)>2
CERT=0
for t in sys.argv[2:]:
    if t.startswith('cert='): CERT=int(t[5:])
FAM.update(families(N))
for n in range(5,N+1):
    tot=0; by=collections.Counter(); unc=[]
    for k in range(2,n):
        for Sig in gen(n-1-k,k,n):
            if sum(1 for s in Sig if s>0)<2: continue
            tot+=1; c=covered(Sig)
            if c is None and CERT:
                srt=sorted(Sig,reverse=True)          # tree minus one largest hub: S = srt[1:]
                if len(srt)-1+sum(srt[1:])+srt[1]+2<=CERT: c='cert'
            by[c]+=1
            if c is None: unc.append(Sig)
    print("n=%d trees=%d caterpillars=%d covered non-caterpillars=%d (T3 %d EQ %d P %d Q %d O %d C %d R %d Z %d) open=%d %s"%(n,tot,by['caterpillar'],tot-by['caterpillar']-by[None]-by['cert'],by['T3'],by['EQ'],by['P'],by['Q'],by['O'],by['C'],by['R'],by['Z'],by[None],
          ("" if not CERT else " [no rule but certified: %d]"%by['cert'])+("  smallest open: "+'; '.join(' '.join(map(str,s)) for s in (unc if sys.argv[2:]==['all'] else unc[:6]))) if show and unc else ""))
