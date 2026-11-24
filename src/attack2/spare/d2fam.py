# d2fam.py lo hi -- every tree of depth <= 2 rooted at its centre with lo <= n <= hi vertices: the root's children
# have a_1 >= a_2 >= ... >= a_r >= 0 leaf children, n = 1 + r + sum a.  (partitions of n-1 into parts a_j+1)
import sys
def parts(total,maxp):
    if total==0: yield (); return
    for x in range(min(total,maxp),0,-1):
        for rest in parts(total-x,x): yield (x,)+rest
lo,hi=int(sys.argv[1]),int(sys.argv[2])
for n in range(lo,hi+1):
    for p in parts(n-1,n-1):
        e=[]; nx=len(p)+1
        for i,x in enumerate(p):
            e.append((0,i+1))
            for _ in range(x-1): e.append((i+1,nx)); nx+=1
        print("#D2(%s) %d 0 "%(",".join(str(x-1) for x in p),n)+" ".join("%d %d"%t for t in e))
