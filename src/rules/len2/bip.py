# Reduced search for C0 -> C0 caps.  Cap for sub-size n, k = 3n+c, middle [n+1, n+dd+n], top [3n+dd+1, 6n+2c].
# High vertices 3n+c+j (j=1..h, h=n+c/3), low vertices n+v (v in V), every high vertex has two low neighbours and the
# sums 4n+c+j+v fill [4n+4c/3+1, 6n+2c], i.e. j+v takes each value in [c/3+1, 2n+c] once.
# Low edges (sum <= 3n+c): given as pairs; a pair (a,b) of small constants has sum n+(n+a+b) (a hole of the middle),
# a pair (p,'N') means (n+p) + (2n+q) with p+q = c ... i.e. v-values p and n+c-p, sum 3n+c.
# We look for assignments with few translation pieces.  Usage: bip.py c dd maxbreaks n1,n2,...
import sys, itertools
c=int(sys.argv[1]); dd=int(sys.argv[2]); MB=int(sys.argv[3]); ns=[int(x) for x in sys.argv[4].split(',')]
def solve(n,holes,lowedges,MB):
    h=n+c//3; V=[v for v in range(1,n+dd+1) if v not in holes]
    need={v:2 for v in V}
    for (a,b) in lowedges:
        for x in (a,b):
            if x not in need: return None
            need[x]-=1
            if need[x]<0: return None
    smin,smax=c//3+1,2*n+c
    if sum(need.values())!=2*h: return None
    degJ=[0]*(h+2); jof={}
    def rec(s,br):
        if s<smin: return True
        cont = jof.get(s+2,None)
        cands=[]
        if cont is not None and cont-1>=1: cands.append((cont-1,0))
        if br<MB:
            for j in range(min(h,s-1),0,-1):
                if cont is not None and j==cont-1: continue
                cands.append((j,1))
        for j,cost in cands:
            v=s-j
            if j<1 or j>h or degJ[j]>=2 or need.get(v,0)<=0: continue
            degJ[j]+=1; need[v]-=1; jof[s]=j
            if rec(s-1,br+cost): return True
            degJ[j]-=1; need[v]+=1; del jof[s]
        return False
    if not rec(smax,0): return None
    # describe as pieces
    out=[]; 
    for par in (0,1):
        ss=[s for s in range(smax,smin-1,-1) if (smax-s)%2==par]
        cur=None
        for s in ss:
            j=jof[s]
            if cur and cur[1]-cur[3]==j and cur[0]-2*cur[3]==s: cur[3]+=1
            else:
                if cur: out.append(tuple(cur))
                cur=[s,j,s-j,1]
        out.append(tuple(cur))
    return sorted(out,reverse=True)
def lowsets():
    # two holes n+A, n+B from constant pairs, one edge with sum 3n+c: (p, n+c-p)
    em=dd-(c//3)*2  # number of holes: ell = n+2c/3 vertices in a middle of n+dd labels
    pairs=[(a,b) for a in range(1,9) for b in range(a,9) if a+b<=dd]
    for combo in itertools.combinations(pairs,em):
        hs=[a+b for a,b in combo]
        if len(set(hs))<em: continue
        for extra in itertools.product(range(1,dd+1),repeat=c//3-em):
            yield [n_h for n_h in hs], list(combo), list(extra)
for hs,combo,extra in lowsets():
    ok=True; res=[]
    for n in ns:
        holes={n+x for x in hs}
        low=list(combo)+[(p,n+c-p) for p in extra]
        r=solve(n,holes,low,MB)
        if r is None: ok=False; break
        res.append(r)
    if ok:
        print("holes n+",hs,"low edges",combo,"top-low p:",extra,flush=True)
        for n,r in zip(ns,res): print("   n=%d pieces (s,j,v,len):"%n,r)
