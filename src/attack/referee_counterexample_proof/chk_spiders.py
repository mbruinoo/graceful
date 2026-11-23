import sys,re
from chk import growth
C="../counterexample/"
# (c) spdlx logs: lines "n1 n2 n3 OK legs: a,b,c ..." labels 0-based, centre 0
seen={}; bad=0
for f in ["run_spdlx_72.log","run_spdlx_105.log"]:
    for l in open(C+f):
        m=re.match(r"(\d+) (\d+) (\d+) OK legs:(.*)",l)
        if not m:
            print("non-OK line in",f,":",l.strip()[:120]); continue
        n1,n2,n3=map(int,m.groups()[:3]); legs=[list(map(int,p.split(","))) for p in m.group(4).split()]
        ls=sorted(map(len,legs))
        okshape = ls.count(1)==n1 and ls.count(2)==n2 and ls.count(3)==n3 and len(ls)==n1+n2+n3
        E=[]; lab=[1]; v=1
        for leg in legs:
            prev=0
            for x in leg: E.append((prev,v)); lab.append(x+1); prev=v; v+=1
        if okshape and growth(v,E,lab): seen[(n1,n2,n3)]=1
        else: bad+=1; print("BAD",f,n1,n2,n3)
want=[(n2,n3) for n3 in range(0,36) for n2 in range(0,53) if 0<2*n2+3*n3<=105]
miss=[p for p in want if (0,)+p not in seen]
print("spdlx: distinct (n1,n2,n3) verified centre-anchored=%d bad=%d ; pairs (n2,n3) with 0<2n2+3n3<=105: %d ; missing with n1=0: %s"%(len(seen),bad,len(want),miss))
print("  entries with n1>0:",sorted(k for k in seen if k[0]>0))
# zigzag deals S(2^k): "k=.. n=.. OK legs: a:o ..." centre 0, inner a, outer o.  zigzag: inner>0 (up), outer<inner (down)
ks=[]; bad=0
for l in open(C+"run_zz2dlx.log"):
    m=re.match(r"k=(\d+) n=(\d+) OK legs:(.*)",l)
    if not m:
        if l.strip() and not l.startswith("k=") : pass
        continue
    k=int(m.group(1)); legs=[tuple(map(int,p.split(":"))) for p in m.group(3).split()]
    E=[]; lab=[1]; v=1; zig=len(legs)==k
    for a,o in legs:
        E+=[(0,v),(v,v+1)]; lab+=[a+1,o+1]; v+=2
        if not (a>0 and o<a): zig=False
        if not (a>(a-o)): zig=False   # first number larger than second (decreasing outward)
    if zig and growth(v,E,lab): ks.append(k)
    else: bad+=1; print("BAD zz k",k)
want=[k for k in range(1,151) if k%3!=2]
print("zigzag deals S(2^k): verified %d values, bad=%d, missing from {k<=150, k!=2 mod 3}: %s, extra: %s"%(len(ks),bad,sorted(set(want)-set(ks)),sorted(set(ks)-set(want))))
