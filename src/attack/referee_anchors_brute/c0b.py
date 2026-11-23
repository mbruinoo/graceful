# independent second method for L(l;h1,h2) via Theorem 7 root form (vertex-first, not length-first)
import sys
from lib import *
sys.setrecursionlimit(10000)
def anchor_L(l,h1,h2):
    m=l+h1+h2+3; nodes=0
    for a in range(1,m+1):                 # label (= length) of c
        for s1 in (1,-1):
          for x1 in range(h1+1,a):         # length of c-g1, must exceed its h1 leaf lengths
            b1=a+s1*x1
            if not (0<b1<=m) : continue
            for s2 in (1,-1):
              for x2 in range(h2+1,a):
                if x2==x1: continue
                b2=a+s2*x2
                if not (0<b2<=m) or b2==b1: continue
                used={0,a,b1,b2}
                lens=[w for w in range(m,0,-1) if w not in (a,x1,x2)]
                cap=[l,h1,h2]
                def rec(i):
                    nonlocal nodes
                    nodes+=1
                    if i==len(lens): return True
                    w=lens[i]
                    if cap[0] and w not in used:
                        cap[0]-=1; used.add(w)
                        if rec(i+1): return True
                        cap[0]+=1; used.discard(w)
                    for j,(b,x) in ((1,(b1,x1)),(2,(b2,x2))):
                        if cap[j] and w<x:
                            for y in (b+w,b-w):
                                if 0<=y<=m and y not in used:
                                    cap[j]-=1; used.add(y)
                                    if rec(i+1): return True
                                    cap[j]+=1; used.discard(y)
                    return False
                # top length m must be c (a=m) or a root leaf: handled by rec
                if rec(0): return True,nodes
    return False,nodes
if __name__=="__main__":
    print("L(3;8,9)",anchor_L(3,8,9)); print("L(4;8,9)",anchor_L(4,8,9))
    for l in range(1,5): print(l,anchor_L(l,2*l+2,2*l+3),anchor_L(l+1,2*l+2,2*l+3)); sys.stdout.flush()
    # cross-check both methods on all L(l;h1,h2) with n<=17
    bad=0;cnt=0
    items=[];keys=[]
    for l in range(0,10):
        for h1 in range(0,12):
            for h2 in range(h1,12):
                if l+h1+h2+4<=17: items.append(Ltree(l,h1,h2)); keys.append((l,h1,h2))
    R=solve(items)
    for k,r in zip(keys,R):
        cnt+=1
        if (r[0]=='1')!=anchor_L(*k)[0]: bad+=1; print("MISMATCH",k)
    print("cross-check",cnt,"trees, mismatches",bad)
