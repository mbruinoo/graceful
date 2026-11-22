# Spider with d legs of length 2, centre as root (label 0), labels 0..2d.
# A growth labeling = inner labels I, outer labels O (|I|=|O|=d, I u O = 1..2d) and a matching i<->o with
# differences |i-o| forming exactly the set O and |i-o| < i.   List solutions as pairs (inner,outer).
import sys
d=int(sys.argv[1]); show=int(sys.argv[2]) if len(sys.argv)>2 else 10; m=2*d
sols=[]
def rec(labels_left, pairs, used_diff):
    if not labels_left:
        I={i for i,o in pairs}; O={o for i,o in pairs}
        if set(used_diff)==O: sols.append(sorted(pairs,reverse=True))
        return
    x=max(labels_left)                 # largest remaining label: it is inner (paired below) or outer of a smaller inner
    rest=labels_left-{x}
    for y in sorted(rest):
        # x inner, y outer (y<x): diff x-y < x ok
        dd=x-y
        if dd not in used_diff: rec(rest-{y}, pairs+[(x,y)], used_diff|{dd})
        # y inner, x outer (x>y): need x-y < y
        if dd<y and dd not in used_diff: rec(rest-{y}, pairs+[(y,x)], used_diff|{dd})
rec(frozenset(range(1,m+1)),[],frozenset())
print(f"d={d}: {len(sols)} solutions")
for s in sols[:show]: print("   "+"  ".join(f"{i}-{o}" for i,o in s))
