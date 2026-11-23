# Design problem behind the "top block" architecture:
#   Delta = offsets of skipped lengths below the top one (0 in Delta; gaps between runs are even = 2g),
#   Pi    = offsets of skipped labels (same runs, gaps g),
#   want a bijection i in 1..k -> (delta_i, pi_i) with i + delta_i + pi_i = c for all i.
import sys
from fractions import Fraction
def sets(k,a,g):
    D=list(range(0,a))+list(range(a+2*g,k+2*g)); P=list(range(0,a))+list(range(a+g,k+g)); return D,P
def matching(k,D,P,c):
    Ps=set(P); res=[]
    def rec(i,Dleft,Pleft):
        if i==0: return True
        for d in sorted(Dleft):
            p=c-i-d
            if p in Pleft:
                res.append((i,d,p))
                if rec(i-1,Dleft-{d},Pleft-{p}): return True
                res.pop()
        return False
    return res[::-1] if rec(k,frozenset(D),frozenset(P)) else None
if __name__=="__main__":
    for k in range(2,int(sys.argv[1])+1):
        for g in range(0,3):
            for a in range(1,k+1) if g else [k]:
                D,P=sets(k,a,g)
                c=Fraction(k*(k+1)//2+sum(D)+sum(P),k)
                if c.denominator!=1: continue
                mt=matching(k,D,P,int(c))
                print("k=%d a=%d g=%d c=%d c%%3=%d :"%(k,a,g,c,c%3), [d for i,d,p in mt] if mt else None)
