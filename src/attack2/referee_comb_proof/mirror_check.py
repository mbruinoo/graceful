# Independent check of the 'fails' claim: S = 2,1^14 has no mirror comb (REPORT Lemma M) with w <= 2.
# Mirror comb: [1,y-1] = disjoint union of heads t_i, teeth sets U_i (U_i = t_i - U_i, U_i in [1,t_i-1]),
# and W = y - W; sizes |U_i| given.  Largest uncovered number must be a head (or in W, chosen first).
import sys
def search(n1,n2,y,W):
    cov=[False]*(y)
    for x in W: cov[x]=True
    def dfs(n1,n2):
        m=y-1
        while m>=1 and cov[m]: m-=1
        if m==0: return n1==0 and n2==0
        cov[m]=True
        if n1 and m%2==0 and not cov[m//2]:
            cov[m//2]=True
            if dfs(n1-1,n2): return True
            cov[m//2]=False
        if n2:
            for u in range(1,(m+1)//2):
                if u!=m-u and not cov[u] and not cov[m-u]:
                    cov[u]=cov[m-u]=True
                    if dfs(n1,n2-1): return True
                    cov[u]=cov[m-u]=False
        cov[m]=False
        return False
    return dfs(n1,n2)
n1,n2=14,1
for w in range(3):
    y=n1+n2+n1+2*n2+w+1
    Ws=[]
    if w==0: Ws=[[]]
    elif w==1: Ws=[[y//2]] if y%2==0 else []
    else: Ws=[[x,y-x] for x in range(1,(y+1)//2) if x!=y-x]
    ok=any(search(n1,n2,y,W) for W in Ws)
    print("w=%d y=%d mirror comb exists: %s"%(w,y,ok))
