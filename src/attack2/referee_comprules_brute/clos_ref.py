# naive closure: staircases closed under C, T (h same or smaller), plus B or D or P
import sys
exec(open('ref.py').read().split('# ---- Rule T')[0])
exec(open('ref.py').read().split('# ---- Rule B')[1].split('cntB=badB=0')[0])
import networkx as nx
mode=sys.argv[1]; N=int(sys.argv[2])
def stairs(m):
    out=[]
    def rec(k,p):
        if k==0: out.append(tuple([0]+p[::-1])); return
        prev=p[-1]
        for d in (0,1):
            rec(k-1,p+[prev+d])
    rec(m-1,[0]); return out
def comp(f,m): return tuple([0]+[m-f[k]-k for k in range(1,m+1)])
def rcanon(T,r,par=None): return '('+''.join(sorted(rcanon(T,c,r) for c in T[r] if c!=par))+')'
def canon(f,m):
    T=nx.Graph([(f[k],f[k]+k) for k in range(1,m+1)]); return min(rcanon(T,c) for c in nx.center(T))
def frees(f,m):
    used={0,m}; res={}
    for k in range(m-1,0,-1):
        used|={f[k+1],f[k+1]+k+1}
        res[k]=frozenset(x for x in range(m+1) if x not in used)
    return res
S={}
for m in range(1,N):
    cur=set(stairs(m)) if m>=1 else set()
    if mode in('B','D'):
        for pm in range(1,m):
            if m%pm==0 and m//pm>=2:
                t=m//pm; p=pm+1
                for f in S[pm]:
                    if mode=='B': vs=designs(f,p)
                    else:
                        l=lens(f,pm); vs=[]
                        for w in range(1,p+1):
                            if all((l[i]>=w-2*i) if 2*i<=w-1 else (l[i]>=2*i-w+1) for i in range(1,w)):
                                vs.append(tuple((w-1-j) if j<w-1 else 0 for j in range(p-1)))
                    for v in vs:
                        br,M=bproduct(f,p,v,t); cur.add(tuple([0]+[br[k][0] for k in range(1,M+1)]))
    # index of h tails: key (k, normalized free) -> list of (h,mh,min free)
    def addidx(idx,h,mh):
        fr=frees(h,mh)
        for k in range(1,mh):
            F=fr[k]; x=min(F); idx.setdefault((k,frozenset(y-x for y in F)),set()).add((h,mh,x))
    idx={}
    for mm in range(1,m):
        for h in S[mm]: addidx(idx,h,mm)
    todo=list(cur); 
    for h in cur: addidx(idx,h,m)
    done=set()
    while todo:
        new=set()
        for f in todo:
            c=comp(f,m)
            if c not in cur: new.add(c)
        # T: recompute all pairs among f in cur, h in idx (naive fixpoint)
        for f in list(cur):
            fr=frees(f,m)
            for k in range(1,m):
                F=fr[k]; x=min(F); key=(k,frozenset(y-x for y in F))
                for (h,mh,xh) in idx.get(key,()):
                    s=x-xh
                    br=[f[i] for i in range(m+1)]
                    ok=True
                    for i in range(1,k+1):
                        a=h[i]+s
                        if a<0 or a+i>m: ok=False;break
                        br[i]=a
                    if ok:
                        g=tuple(br)
                        if g not in cur: new.add(g)
        for g in new: addidx(idx,g,m)
        cur|=new; todo=list(new)
    for f in cur:
        br={k:(f[k],f[k]+k) for k in range(1,m+1)}; assert isgrowth(br,m)
    S[m]=cur
    print(m+1,len(cur),len({canon(f,m) for f in cur}) if m>1 else 1, flush=True)
