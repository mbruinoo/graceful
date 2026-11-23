from lib import *
for n in range(4,11):
    S=set(all_tree_placements(n)); R=right_reach(n,S)
    I=[p for p in S if is_interval_growth(p)]
    bad=[p for p in I if p not in R]
    print(n,len(S),len(R),"interval",len(I),"not reachable",len(bad),sorted(bad)[:3], "shapes interval",len({canon(p) for p in I}),"shapes interval&reach",len({canon(p) for p in I if p in R}))
