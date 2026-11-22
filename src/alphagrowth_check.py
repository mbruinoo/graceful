# Check Theorem 9: a placement that is a growth placement AND has all brackets jumping one common point is a staircase.
from growslide import growth_cfgs
for n in range(3,13):
    G=growth_cfgs(n); ag=0; bad=0
    for p in G:
        if max(p[1:]) < min(p[k]+k for k in range(1,n)):       # every left foot is left of every right foot
            ag+=1
            if not all(p[k]-p[k+1] in (0,1) for k in range(1,n-1)): bad+=1
    print(f"n={n}: growth placements={len(G)}  also alpha={ag}  (2^(n-2)={2**(n-2)})  of those not staircases={bad}")
