#!/usr/bin/env python3
# construct.py S Q -- Theorem U (upper bound): for p = 2s (1 <= s <= S) and every 1 <= q <= Q, the explicit labelling
# of L(s; p, q) below is a growth placement with v at the smallest label.  Checked straight from the definition
# (README section 2): labels 0..m bijective, lengths 1..m each once, and taking brackets longest first each one
# has exactly one foot on a vertex already used; the first bracket starts at v (label 0).
import sys
S,Q=int(sys.argv[1]),int(sys.argv[2]); n_ok=0
for s in range(1,S+1):
    p=2*s
    for q in range(1,Q+1):
        m=s+p+q+3; a=m                       # c at the top label a = m = q+3+3s
        assert a==q+3+3*s
        edges=[(0,a),(a,2),(a,3)]            # v=0, c=a, hub Q at 2 (edge a-2), hub P at 3 (edge a-3)
        edges+=[(0,a-1-3*i) for i in range(s)]              # s leaves at v: a-1, a-4, ..., a-3s+2
        edges+=[(2,2+w) for w in range(3,q+3)]              # q leaves of Q: lengths 3..q+2, labels 5..q+4
        edges+=[(3,4),(3,1)]                                # P: length 1 up, length 2 down
        for i in range(1,s): edges+=[(3,a-3*i),(3,a-3*i+1)] # P: lengths a-3i-3, a-3i-2 (up)
        assert len(edges)==m
        labs={x for e in edges for x in e}; assert labs==set(range(m+1))
        lens=sorted(abs(x-y) for x,y in edges); assert lens==list(range(1,m+1))
        deg={}; 
        for x,y in edges: deg[x]=deg.get(x,0)+1; deg[y]=deg.get(y,0)+1
        # shape: v has s leaves + c; c has v, hubs 2 and 3; hub 2 has q leaves; hub 3 has p leaves
        assert deg[0]==s+1 and deg[a]==3 and deg[2]==q+1 and deg[3]==p+1 and sum(1 for x in deg if deg[x]==1)==s+p+q
        used={0}
        for x,y in sorted(edges,key=lambda e:-abs(e[0]-e[1])):
            assert (x in used)!=(y in used); used|={x,y}
        n_ok+=1
print("construction verified for p=2s, s<=%d, q<=%d: %d trees, all growth placements anchored at v"%(S,Q,n_ok))
