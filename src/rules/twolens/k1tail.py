# k=1: legs (r,2).  Long leg alternates on numbers > T, free signs on numbers <= T.  Short leg (x,d,sign).
import sys
def sols(r,T,maxs=50):
    m=r+2; out=[]
    for x in range(2,m+1):
        for d in range(1,x):
            for y in (x-d,x+d):
                if y>m: continue
                W=[w for w in range(m,0,-1) if w!=x and w!=d]
                used={x,y}; 
                # deterministic part
                t=0; ok=True; path=[]; i=0
                def rec(i,t,up_last):
                    if i==len(W): return [[]]
                    w=W[i]; res=[]
                    if i==0: cands=[1]
                    elif w>T: cands=[-up_last]
                    else: cands=[-up_last,up_last]
                    for s in cands:
                        nt=t+s*w
                        if 1<=nt<=m and nt not in used:
                            used.add(nt)
                            for tail in rec(i+1,nt,s):
                                res.append([(w,s)]+tail)
                            used.discard(nt)
                    return res
                for p in rec(0,0,1):
                    out.append((x,d,y,[ (w,s) for (w,s) in p if w<=T]))
                    if len(out)>=maxs: return out
    return out
if __name__=="__main__":
    T=int(sys.argv[1])
    for r in range(4,60):
        s=sols(r,T)
        print(r,r+2,len(s),[ (x,d,y,"".join("+" if sg>0 else "-" for w,sg in tl)) for x,d,y,tl in s[:6]])
