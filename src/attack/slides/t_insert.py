# Test: "cut insertion". p on n labels, cut t (new label t, old labels >= t shift up),
# crossing brackets (a < t <= b) must be exactly the lengths >= k. New bracket k at {t-k,t} or {t,t+k}.
from lib import *
from collections import Counter
for n in range(4,10):
    S1=set(all_tree_placements(n+1)); R0=right_reach(n); R1=right_reach(n+1,S1)
    stat=Counter()
    for p in R0:
        for t in range(2,n+1):
            cross=[k for k in range(1,n) if p[k-1]<t<=p[k-1]+k]
            k=min(cross)
            if cross!=list(range(k,n)): continue
            # new placement q on n+1: lengths 1..n
            base=[0]*(n)  # q[j-1]
            for j in range(1,n):
                a=p[j-1]
                if j>=k: base[j]=a            # length j+1, left foot a (<t) unchanged
                else: base[j-1]=a if a+j<t else a+1
            for side,pos in (("L",t-k),("R",t)):
                if pos<1 or pos+k>n+1: continue
                q=base[:]; q[k-1]=pos; q=tuple(q)
                key=(side, "tree" if q in S1 else "nontree", "reach" if q in R1 else "no")
                stat[key]+=1
                # finer: record (side, whether hung-on vertex is t-1 / t+1 side info)
    print(n,dict(stat))
