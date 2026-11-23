# Search for a parametric family of caps: two long translation pieces
#   P: (2n+aP-i, 4n+bP-i), i=0..n+eP-1      Q: (2n+aQ-i, 4n+bQ-i), i=0..n+eQ-1
# plus a bounded number of sporadic edges found by DFS, the same parameters working for several n.
# Cap label set: [n+1, n+delta] u [2n+delta+1, 6n+2c]; split threshold 3n+c (class C0 -> C0), delta = n+dd.
# Usage: capfamily.py c dd nlist(comma)
import sys, itertools
c=int(sys.argv[1]); dd=int(sys.argv[2]); ns=[int(x) for x in sys.argv[3].split(',')]
def rest(n,pre,maxspor=99):
    L=list(range(n+1,2*n+dd+1))+list(range(3*n+dd+1,6*n+2*c+1)); Ls=set(L); T=3*n+c
    deg={}; issum=set(); 
    for (u,w) in pre:
        s=u+w
        if u not in Ls or w not in Ls or s not in Ls or s in issum: return None
        if (u>T)+(w>T)!=(s>T): return None
        issum.add(s); deg[u]=deg.get(u,0)+1; deg[w]=deg.get(w,0)+1
    for v in deg:
        if deg[v]>2 or v in issum: return None
    if len(L)-len(issum)-sum(1 for v in deg if deg[v]==2) > 3*maxspor: return None
    L.sort(); out=[]
    def rec(i):
        if i<0: return True
        v=L[i]
        if v in issum: return rec(i-1)
        dv=deg.get(v,0)
        if dv==2: return rec(i-1)
        if dv==1: return False
        issum.add(v)
        for u in range(v//2,0,-1):
            w=v-u
            if u not in Ls or w not in Ls or u in issum or w in issum: continue
            if (u>T)+(w>T)!=(v>T): continue
            du=deg.get(u,0); dw=deg.get(w,0)
            if u==w:
                if du: continue
                deg[u]=2
            else:
                if du>=2 or dw>=2: continue
                deg[u]=du+1; deg[w]=dw+1
            out.append((u,w))
            if rec(i-1): return True
            out.pop()
            if u==w: deg[u]=0
            else: deg[u]=du; deg[w]=dw
        issum.discard(v); return False
    return list(out) if rec(len(L)-1) else None
def piece(n,a,b,e): return [(2*n+a-i,4*n+b-i) for i in range(n+e)]
def rel(n,x):
    j=(x+3)//n; return (j,x-j*n)
R=range(-3,10); B=range(2,16); E=range(-4,3)
maxspor=int(sys.argv[4]) if len(sys.argv)>4 else 10
for aP,bP,eP in itertools.product(R,B,E):
    for aQ,bQ,eQ in itertools.product(R,B,E):
        if (aP+bP)%2==0 or (aQ+bQ)%2==1: continue   # P odd sums, Q even sums
        ok=True; res=[]; sig=None
        for n in ns:
            r=rest(n,piece(n,aP,bP,eP)+piece(n,aQ,bQ,eQ),maxspor)
            if r is None or len(r)>maxspor: ok=False; break
            sg=sorted(tuple(sorted((rel(n,u),rel(n,w)))) for u,w in r)
            if sig is None: sig=sg
            elif sg!=sig: ok=False; break
        if ok:
            print("P",(aP,bP,eP),"Q",(aQ,bQ,eQ),"sporadic (j,r) means j*n+r:",sig,flush=True)
