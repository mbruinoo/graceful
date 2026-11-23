# Family F(a,b): spider with a legs of length 2 and b legs of length 1, n=2a+1+b. Centre labelled 2.
from lib import *
import sys
sys.setrecursionlimit(100000)
def target(a,b):
    n=2*a+1+b; E=[(1,n),(2,n)]
    E+=[(2,x) for x in range(2*a+1,n)]          # b leaves
    E+=[(2,2*a),(3,2*a)]
    for i in range(1,a-1):                        # mids 4..2a-2, reverse pairing with ends 5..2a-1
        E+=[(2,2*i+2),(2*i+2,2*(a-1-i)+3)]
    p=[0]*(n-1)
    for x,y in E:
        x,y=min(x,y),max(x,y); assert p[y-x-1]==0,(a,b,E); p[y-x-1]=x
    assert all(p); return tuple(p)
def back_reach(p):
    # is p reachable from the star by legal right slides?  search left slides from p with memo
    n=len(p)+1; star=tuple([1]*(n-1)); seen={p}; st=[p]; par={p:None}
    while st:
        x=st.pop()
        if x==star:
            r=[]; 
            while par[x]: x,k=par[x]; r.append(k)
            return r  # brackets slid right, in forward order from star
        for k in range(1,n):
            if x[k-1]>1:
                y=x[:k-1]+(x[k-1]-1,)+x[k:]
                if y not in seen and is_tree(y): seen.add(y); par[y]=(x,k); st.append(y)
    return None
if __name__=="__main__":
    for a in range(2,int(sys.argv[1])+1):
        for b in range(0,int(sys.argv[2])+1):
            p=target(a,b); assert is_tree(p)
            r=back_reach(p)
            print(a,b,p,"growth" if is_growth(p) else "", "REACH" if r is not None else "no", r if a<=5 and b<=1 else "")
