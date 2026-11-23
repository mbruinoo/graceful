# Design of C0(n) -> C0(3n+c) caps with middle [n+1,2n+dd], top [3n+dd+1,6n+2c]  (c = 0 mod 3, dd = 2 mod 3).
# v-coordinates: low vertex n+v (v in [1,n+dd]), high vertex 3n+c+j (j in [1,h], h=n+c/3), high sum 4n+c+(j+v),
# j+v takes every value in [c/3+1, 2n+c] once, every j twice.
# Backbone: j <-> v=j+beta and v=j+beta+g (g odd) for j = J0+1 .. h-J1; the two ends are finite problems independent of n.
# Low edges: pairs of small v (a,b) whose sum 2n+a+b is a hole n+(n+a+b)... i.e. hole v = n+a+b <= n+dd,
#            and pairs (p, n+q) with p+q = c (sum 3n+c... generally sum 3n+r for r in [dd+1,c], p+q=r).
# Usage: ends.py c dd beta g J0 J1
import itertools, sys
c,dd,beta,g,J0,J1=map(int,sys.argv[1:7])
h3=c//3
def local(js_range, sums, cap):
    sols=[]; deg={j:0 for j in js_range}; use={}; cur=[]
    def rec(i):
        if len(sols)>3: return
        if i==len(sums):
            if all(use.get(v,0)==cc for v,cc in cap.items()): sols.append(tuple(cur))
            return
        s=sums[i]
        for j in js_range:
            v=s-j
            if deg[j]>=2 or use.get(v,0)>=cap.get(v,0): continue
            deg[j]+=1; use[v]=use.get(v,0)+1; cur.append((j,v))
            rec(i+1)
            cur.pop(); deg[j]-=1; use[v]-=1
    rec(0); return sols
# bottom sums: s >= h3+1 not produced by the backbone and below it
bs=[s for s in range(h3+1, 2*J0+beta+g+2) if (s%2==beta%2 and s<2*(J0+1)+beta) or (s%2!=beta%2 and s<2*(J0+1)+beta+g)]
# top, primed: j = h-J1+j' (j'=1..J1), v = n+v', s = 2n+h3-J1+(j'+v'); backbone last j=h-J1: sums 2n+2h3-2J1+beta (+g)
# s' = j'+v' = s-(2n+h3-J1), smax' = 2n+c-(2n+h3-J1) = 2h3+J1
lastA=h3-J1+beta      # 2(h-J1)+beta      - (2n+h3-J1)  -> s' value of last 'beta' sum
lastB=lastA+g
ts=[s for s in range(lastA-2*g-4, 2*h3+J1+1) if ((s-lastA)%2==0 and s>lastA) or ((s-lastA)%2!=0 and s>lastB)]
if len(bs)!=2*J0 or len(ts)!=2*J1: print("count mismatch",len(bs),len(ts)); sys.exit()
vb0=J0+1+beta                                # first backbone v
capb0={v:(2 if v<vb0 else 1) for v in range(1,vb0+g)}
vt=h3-J1+beta                                # primed: last backbone v' of first kind
capt0={v:(2 if v>vt+g else 1) for v in range(vt+1,dd+1)}
nhole=dd-2*h3; ntop=h3-nhole                 # holes in the middle; low sums in the top (3n+dd+1..3n+c)
small=[(a,b) for a in capb0 for b in capb0 if a<=b]
cross=[(p,q,p+q) for p in capb0 for q in capt0 if dd+1<=p+q<=c]   # (n+p)+(2n+q) = 3n+p+q
for es in itertools.combinations(small,nhole):
    holes=[a+b for a,b in es]
    if len(set(holes))<nhole or any(H not in capt0 for H in holes): continue
    for xs in itertools.combinations(cross,ntop):
        if len({x[2] for x in xs})<ntop: continue
        capb=dict(capb0); capt={v:cc for v,cc in capt0.items() if v not in holes}
        ok=True
        for a,b in es: capb[a]-=1; capb[b]-=1
        for p,q,_ in xs:
            capb[p]-=1
            if q not in capt: ok=False; break
            capt[q]-=1
        if not ok or min(capb.values())<0 or min(capt.values())<0: continue
        if sum(capb.values())!=2*J0 or sum(capt.values())!=2*J1: continue
        sb=local(range(1,J0+1), bs, capb)
        if not sb: continue
        stp=local(range(1,J1+1), ts, capt)
        if stp:
            print("low edges (v-coords): small",es,"cross (p, n+q)",[(p,q) for p,q,_ in xs],"holes n+",holes)
            print("   bottom (j,v):",sb[0])
            print("   top (j',v') with j=n+%d+j', v=n+v':"%(h3-J1),stp[0])
