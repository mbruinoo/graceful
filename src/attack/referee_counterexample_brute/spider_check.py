#!/usr/bin/env python3
"""Referee: (1) exhaustive: for every (n1,n2,n3) with n=1+n1+2n2+3n3<=N is the centre an anchor? (from enumall data)
(2) independent re-check of claimant's spider certificates in run_spdlx_105.log / run_spdlx_72.log / run_spdlx_extra.log
(3) independent re-check of zigzag certificates run_zz2dlx.log"""
import sys,os
N=int(sys.argv[1])
def canon(t):
    ks=sorted((canon(c) for c in t),key=lambda x:(x[1],x[0]),reverse=True)
    b=1;l=1
    for cb,cl in ks: b=(b<<cl)|cb;l+=cl
    return (b<<1,l+1)
anch={}
for n in range(2,N+1):
    anch[n]={int(l.split()[0],16) for l in open('an_%d.txt'%n)}
leg={1:(),2:((),),3:(((),),)}
bad=[];tot=0
for n3 in range(0,6):
  for n2 in range(0,9):
    for n1 in range(0,17):
        n=1+n1+2*n2+3*n3
        if n<2 or n>N: continue
        t=(leg[1],)*n1+(leg[2],)*n2+(leg[3],)*n3
        tot+=1
        if canon(t)[0] not in anch[n]: bad.append((n1,n2,n3))
print("exhaustive n<=%d: spiders (n1,n2,n3) tested %d; centre NOT an anchor for:"%(N,tot),bad)
def check_deal(legs,zig=False):
    """legs: list of label lists outward from centre 0. returns error string or None"""
    m=sum(len(l) for l in legs)
    labs=[0]+[x for l in legs for x in l]
    if sorted(labs)!=list(range(m+1)): return "labels not 0..m once"
    E=[]
    for l in legs:
        p=0;prevlen=None;prevdir=None
        for x in l:
            L=abs(x-p)
            if prevlen is not None and L>=prevlen: return "lengths not decreasing outward"
            d=1 if x>p else -1
            if zig and prevdir is not None and d==prevdir: return "not zigzag"
            if zig and prevdir is None and d!=1: return "first move not up"
            prevlen=L;prevdir=d;E.append((p,x));p=x
    if sorted(abs(a-b) for a,b in E)!=list(range(1,m+1)): return "lengths not 1..m once"
    # definition: longest first, exactly one foot used
    used={0}
    for a,b in sorted(E,key=lambda e:-abs(e[0]-e[1])):
        if (a in used)==(b in used): return "growth order broken"
        used|={a,b}
    return None
C='../counterexample/'
seen=set();nbad=0;nlines=0
for f in ['run_spdlx_105.log','run_spdlx_72.log','run_spdlx_extra.log']:
    if not os.path.exists(C+f): continue
    for l in open(C+f):
        if 'legs:' not in l:
            if l.strip(): print("non-cert line in",f,":",l.strip()[:100])
            continue
        head,tail=l.split('legs:')
        h=head.split();n1,n2,n3=int(h[0]),int(h[1]),int(h[2])
        legs=[list(map(int,p.split(','))) for p in tail.split()]
        cntl=[sum(1 for g in legs if len(g)==k) for k in (1,2,3)]
        err=check_deal(legs)
        if cntl!=[n1,n2,n3]: err="leg counts differ from header"
        nlines+=1
        if err: nbad+=1;print("BAD",f,h,err)
        else: seen.add((n1,n2,n3))
want={(n2,n3) for n2 in range(0,53) for n3 in range(0,36) if 2*n2+3*n3<=105}
got={(b,c) for a,b,c in seen if a==0}
print("spider certs: lines %d bad %d ; pairs with 2n2+3n3<=105: %d ; certified with n1=0: %d ; missing:"%(nlines,nbad,len(want),len(want&got)),sorted(want-got))
print("certs with n1>0:",sorted(x for x in seen if x[0]>0))
ks=set();nb=0
for l in open(C+'run_zz2dlx.log'):
    if 'legs:' not in l:
        if l.strip(): print("zz non-cert line:",l.strip()[:100])
        continue
    head,tail=l.split('legs:')
    k=int(head.split()[0].split('=')[1])
    legs=[list(map(int,p.split(':'))) for p in tail.split()]
    err=check_deal(legs,zig=True)
    if len(legs)!=k or any(len(g)!=2 for g in legs): err="shape"
    if err: nb+=1;print("BAD zz k=",k,err)
    else: ks.add(k)
wantk={k for k in range(1,151) if k%3!=2}
print("zigzag S(2^k): certified k count %d bad %d; missing from k<=150,k!=2 mod 3:"%(len(ks),nb),sorted(wantk-ks),"extra:",sorted(ks-wantk))
