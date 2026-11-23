# Balance rule: when the bracket of length k is placed in a growth placement (fresh foot x, used foot y),
# (#used cells strictly between x and y) == (#unused cells outside the closed interval [x,y]).
# Conversely, playing the game by the balance rule alone (no lengths) generates exactly the growth placements.
from growslide import growth_cfgs
def game(n):
    # all move sequences of the balance game; returns set of edge sets
    out=set()
    def rec(used,edges):
        if len(used)==n: out.add(frozenset(edges)); return
        for x in range(1,n+1):
            if x in used: continue
            for y in used:
                lo,hi=min(x,y),max(x,y)
                ub=sum(1 for c in range(lo+1,hi) if c in used)
                uo=sum(1 for c in range(1,n+1) if c not in used and (c<lo or c>hi))
                if ub==uo: rec(used|{x},edges+[(lo,hi)])
    rec(frozenset({1,n}),[(1,n)])
    return out
for n in range(3,10):
    G={frozenset((p[k],p[k]+k) for k in range(1,n)) for p in growth_cfgs(n)}
    B=game(n)
    print(f"n={n}: growth placements={len(G)}  balance-game outcomes={len(B)}  identical={G==B}")
