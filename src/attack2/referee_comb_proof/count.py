# independent count of multisets S (entries>=0, max>=1) with |S|+sum+max+2 = n, via partitions
from functools import lru_cache
@lru_cache(None)
def P(total,parts,maxv):  # number of multisets of exactly `parts` entries in [0,maxv] summing to total
    if parts==0: return 1 if total==0 else 0
    return sum(P(total-f,parts-1,f) for f in range(0,min(total,maxv)+1))
tot=0
for n in range(5,45):
    c=0
    for k in range(1,n):
        for mx in range(1,n):
            rem=n-2-k-mx-mx   # remaining sum of k-1 other entries
            if rem<0: continue
            c+=P(rem,k-1,mx)
    tot+=c
    print(n,c)
print("total",tot)
