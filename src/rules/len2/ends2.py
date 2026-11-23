# Design of caps WITH ONE DIFFERENCE EDGE (k = 2 mod 3):  C0(n) -> free deal for k = 3n+c, c = 2 mod 3.
# Cap labels: middle [n+1,2n+dd], top [3n+dd+1,6n+2c].  v-coordinates as in ends.py:
# low vertex n+v, high vertex 3n+c+j (j=1..h, h=n+h3, h3=(c+1)/3), high sums 4n+c+(j+v) fill the top 2h-1 labels.
# Difference edge: o* = 3n+c+j*, x* = n+v*, label i* = o*-x* (a low label that is not a vertex).
# Backbone j <-> v=j+beta, j+beta+g for j=J0+1..h-J1; finite end problems.
# Usage: ends2.py c dd beta g J0 J1
import itertools, sys
c,dd,beta,g,J0,J1=map(int,sys.argv[1:7])
h3=(c+1)//3; smin=c-2*h3+2
def local(jdeg, sums, cap):
    sols=[]; deg={j:0 for j in jdeg}; use={}; cur=[]
    def rec(i):
        if sols: return
        if i==len(sums):
            if all(use.get(v,0)==cc for v,cc in cap.items()) and all(deg[j]==jdeg[j] for j in jdeg): sols.append(tuple(cur))
            return
        s=sums[i]
        for j in jdeg:
            v=s-j
            if deg[j]>=jdeg[j] or use.get(v,0)>=cap.get(v,0): continue
            deg[j]+=1; use[v]=use.get(v,0)+1; cur.append((j,v))
            rec(i+1)
            cur.pop(); deg[j]-=1; use[v]-=1
    rec(0); return sols
bs=[s for s in range(smin, 2*J0+beta+g+2) if (s%2==beta%2 and s<2*(J0+1)+beta) or (s%2!=beta%2 and s<2*(J0+1)+beta+g)]
lastA=h3-J1+beta; lastB=lastA+g      # primed: s' = s-(2n+h3-J1), j = n+h3-J1+j', v = n+v'
ts=[s for s in range(lastA-2*g-4, c-h3+J1+1) if ((s-lastA)%2==0 and s>lastA) or ((s-lastA)%2!=0 and s>lastB)]
vb0=J0+1+beta
capb0={v:(2 if v<vb0 else 1) for v in range(1,vb0+g)}
vt=h3-J1+beta
capt0={v:(2 if v>vt+g else 1) for v in range(vt+1,dd+1)}
nhole=dd-(2*c-1)//3; ntop=c-dd
small=[(a,b) for a in capb0 for b in capb0 if a<=b]
cross=[(p,q,p+q) for p in capb0 for q in capt0 if dd+1<=p+q<=c]
diffs=[]
for jb in range(1,J0+1):
    for vs in capb0:                           # j* bottom, v* bottom: i* = 2n+(c+j*-v*), a hole of the middle near its top
        H=c+jb-vs
        if H in capt0: diffs.append(('B','B',jb,vs,('hole',H)))
    for vp in capt0:                           # j* bottom, v* top: i* = n+(c+j*-v'), a hole of the middle near its bottom
        H=c+jb-vp
        if H in capb0 and H<vb0: diffs.append(('B','T',jb,vp,('bhole',H)))
for jp in range(1,J1+1):
    for vs in capb0:                           # j* top, v* bottom: i* = 3n + r
        r=c+h3-J1+jp-vs
        if dd+1<=r<=c: diffs.append(('T','B',jp,vs,('top',r)))
    for vp in capt0:                           # j* top, v* top: i* = 2n + H, hole v-coord n+H
        H=c+h3-J1+jp-vp
        if H in capt0: diffs.append(('T','T',jp,vp,('hole',H)))
found=0
for (jside,vside,js,vs,(kind,val)) in diffs:
    nh=nhole-(kind in ('hole','bhole')); nt=ntop-(kind=='top')
    if nh<0 or nt<0: continue
    if len(bs)!=2*J0-(jside=='B') or len(ts)!=2*J1-(jside=='T'): continue
    for es in itertools.combinations(small,nh):
        holes=[a+b for a,b in es]+([val] if kind=='hole' else [])
        if len(set(holes))<len(holes) or any(H not in capt0 for H in holes): continue
        for xs in itertools.combinations(cross,nt):
            tl=[x[2] for x in xs]+([val] if kind=='top' else [])
            if len(set(tl))<len(tl): continue
            capb=dict(capb0); capt={v:cc for v,cc in capt0.items() if v not in holes}
            if kind=='bhole':
                if any(val in e for e in es) or any(val==x[0] for x in xs): continue
                del capb[val]
            ok=True
            if any(a not in capb or b not in capb for a,b in es) or any(x[0] not in capb for x in xs): continue
            for a,b in es: capb[a]-=1; capb[b]-=1
            for p,q,_ in xs:
                capb[p]-=1
                if q not in capt: ok=False; break
                capt[q]-=1
            if not ok: continue
            if vside=='B':
                if vs not in capb: continue
                capb[vs]-=1
            else:
                if vs not in capt: continue
                capt[vs]-=1
            if min(capb.values())<0 or min(capt.values())<0: continue
            if sum(capb.values())!=len(bs) or sum(capt.values())!=len(ts): continue
            jb_={j:2 for j in range(1,J0+1)}; jd={j:2 for j in range(1,J1+1)}
            if jside=='B': jb_[js]=1
            else: jd[js]=1
            sb=local(jb_, bs, capb)
            if not sb: continue
            stp=local(jd, ts, capt)
            if stp:
                found+=1
                print("diff: j* %s %d, v* %s %d, i* %s %d"%(jside,js,vside,vs,kind,val))
                print("   low edges (v-coords): small",es,"cross (p, n+q)",[(p,q) for p,q,_ in xs],"holes n+",holes)
                print("   bottom (j,v):",sb[0])
                print("   top (j',v') with j=n+%d+j', v=n+v':"%(h3-J1),stp[0],flush=True)
                if found>=3: sys.exit()
