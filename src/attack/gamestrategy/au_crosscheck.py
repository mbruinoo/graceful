# Independent cross-check of au_scan.cpp for small n: find an all-up comb with allup.py (different code),
# turn it into a labeling and check it from the definitions (comb_rules.check_growth_placement) and against the tree.
import sys
from explore import d4trees
from allup import allup
from comb_rules import comb_to_labels, check_growth_placement, canon, target_tree
N=int(sys.argv[1])
for n in range(5,N+1):
    tot=0
    for a in d4trees(n):          # a sorted decreasing, zeros allowed (leaves of the centre)
        tot+=1
        sol=allup(a,1)
        assert sol, ('no all-up comb', a)
        y,hubs,U=sol[0]
        edges,nn=comb_to_labels(a[0],y,list(zip(hubs[1:],U[1:])),U[0])
        assert nn==n and check_growth_placement(edges,n) and canon(edges)==canon(target_tree(a)), a
    print('n=%d: %d diameter-4 trees, each has an all-up comb rooted at a largest hub; labelings re-checked from the definitions'%(n,tot),flush=True)
