#!/usr/bin/env python3
# Machine check of rule.py against the definition (verify.py).   usage: check_rule.py KMAX RMAX
import sys
from rule import deal, designs
from verify import check_deal, deal_from_lists
KMAX=int(sys.argv[1]); RMAX=int(sys.argv[2]); bad=0; tot=0; cov=0
for k in range(1,KMAX+1):
    ds=designs(k); ok=[]; miss=[]
    for r in range(1,RMAX+1):
        tot+=1; L=deal(r,k)
        if L is None: miss.append(r); continue
        legs=[r]+[2]*k
        try: good,why=check_deal(legs,deal_from_lists(legs,L))
        except AssertionError as e: good,why=False,str(e)
        if good: ok.append(r); cov+=1
        else: bad+=1; print("INVALID r=%d k=%d: %s"%(r,k,why))
    # describe coverage
    res=sorted(ds); thr={}
    for rr in res:
        c=ds[rr][0]; thr[rr]=c-k
    missing_big=[r for r in miss if (r+k)%3 in ds and r>=max(1,thr[(r+k)%3])]
    print("k=%3d residues of r+k covered: %s  c=%s  valid for r=c-k+3l>=1: %s%s"%(k,res,[ds[x][0] for x in res],[max(1,thr[x]) for x in res]," UNEXPECTED MISS %s"%missing_big if missing_big else ""))
print("pairs (r,k) tried %d, deals produced and verified %d, invalid %d"%(tot,cov,bad))
# extra legs of length 1 (README section 13: deal the new longest numbers to the new legs first)
bad1=0; n1=0
for k in range(1,13):
    for j in range(1,6):
        for r in range(1,61):
            L=deal(r,k)
            if L is None: continue
            m=r+2*k; legs=[r]+[2]*k+[1]*j
            L2=L+[[(m+t,1)] for t in range(1,j+1)]
            good,why=check_deal(legs,deal_from_lists(legs,L2)); n1+=1
            if not good: bad1+=1; print("INVALID with ones",r,k,j,why)
print("with j=1..5 extra legs of length 1 (k<=12, r<=60): %d deals verified, %d invalid"%(n1,bad1))
