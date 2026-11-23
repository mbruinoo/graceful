from lib import *
from t_spider2 import target
import sys
def coreach(p):
    n=len(p)+1; seen={p}; st=[p]
    while st:
        x=st.pop()
        for k in range(1,n):
            if x[k-1]>1:
                y=x[:k-1]+(x[k-1]-1,)+x[k:]
                if y not in seen and is_tree(y): seen.add(y); st.append(y)
    return seen
def lex(p,C,order):
    n=len(p)+1; x=tuple([1]*(n-1)); r=[]
    while x!=p:
        for k in order(n):
            y=x[:k-1]+(x[k-1]+1,)+x[k:]
            if y in C: x=y; r.append(k); break
    return r
for a in range(3,int(sys.argv[1])+1):
    p=target(a,0); C=coreach(p); n=len(p)+1
    print(a,len(C),"star in C",tuple([1]*(n-1)) in C)
    print("  smallest-first:",lex(p,C,lambda n:range(1,n)))
    print("  largest-first: ",lex(p,C,lambda n:range(n-1,0,-1)))
