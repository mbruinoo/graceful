# Independent referee checks (labels 0..m; placement p[k]=left foot of bracket length k)
import sys, itertools
from functools import lru_cache
sys.setrecursionlimit(10000)

def growth(m):
    out=[]; p=[0]*(m+1)
    def rec(k,used):
        if k==0: out.append(tuple(p)); return
        for a in range(0,m-k+1):
            b=a+k
            if (a in used)!=(b in used):
                p[k]=a; rec(k-1, used|{a,b})
    p[m]=0; rec(m-1,{0,m}) if m>=1 else None
    if m==0: out.append((0,))
    return out
G={m:growth(m) for m in range(0,8)}
def isgrowth(br,m):
    # br: dict length->(a,b)
    if sorted(br)!=list(range(1,m+1)): return False
    used=None
    for k in range(m,0,-1):
        a,b=br[k]
        if min(a,b)<0 or max(a,b)>m or abs(a-b)!=k: return False
        if used is None: used={a,b}; continue
        if (a in used)==(b in used): return False
        used|={a,b}
    return True
def free(p,m,k):  # labels unused at time k (brackets >k placed)
    used={0,m}
    for i in range(m,k,-1): used|={p[i],p[i]+i}
    return frozenset(set(range(m+1))-used), used

# ---- Rule T
cntT=cnt1n2=0; bad=0
for mf in range(2,7):
  for mh in range(2,7):
    for f in G[mf]:
      for h in G[mh]:
        for k in range(1,min(mf,mh)):
          Ff,Uf=free(f,mf,k); Fh,Uh=free(h,mh,k)
          if len(Ff)!=len(Fh) or not Ff: 
              if not Ff and not Fh: pass
          if len(Ff)!=len(Fh): continue
          s=min(Ff)-min(Fh)
          if {x+s for x in Fh}!=Ff: continue
          touched={a for i in range(1,k+1) for a in (h[i],h[i]+i) if a in Uh}
          h2=all((a+s) in Uf for a in touched)
          br={i:(f[i],f[i]+i) for i in range(k+1,mf+1)}
          br.update({i:(h[i]+s,h[i]+i+s) for i in range(1,k+1)})
          g=isgrowth(br,mf)
          if h2: cntT+=1; bad+= (not g)
          else: cnt1n2+=1; bad+= g
print("RuleT", cntT, cnt1n2, "mismatch", bad)

# ---- Rule P
cntP=badP=0
for mf in range(2,7):
  for f in G[mf]:
    for k in range(1,mf):
      Ff,_=free(f,mf,k)
      x=min(Ff)
      if Ff!=frozenset(range(x,x+k)): continue
      for g in G[k]:
        for off in (x-1,x):
          br={i:(f[i],f[i]+i) for i in range(k+1,mf+1)}
          br.update({i:(g[i]+off,g[i]+i+off) for i in range(1,k+1)})
          cntP+=1; badP+= not isgrowth(br,mf)
print("RuleP", cntP, "bad", badP)

# ---- Rule B
def lens(f,m):
    l={0:None}
    used={0}
    for k in range(m,0,-1):
        a,b=f[k],f[k]+k
        new=b if a in used else a
        l[new]=k; used|={a,b}
    return l
def designs(f,p):
    m=p-1; l=lens(f,m); res=[]; v=[0]*(p-1)
    def rec(j,usedb):
        if j==p-1: res.append(tuple(v)); return
        for o in range(p):
            be= j-o if o<=j else o-j-1
            if be in usedb: continue
            if o!=0 and not be<l[o]: continue
            v[j]=o; rec(j+1,usedb|{be})
    rec(0,frozenset()); return res
def bproduct(f,p,v,t):
    m=p-1; M=(p-1)*t; br={}
    for k in range(1,m+1): br[k*t]=(t*f[k],t*(f[k]+k))
    for j in range(p-1):
        for d in range(1,t):
            leaf=j*t+d; o=t*v[j]; L=abs(leaf-o)
            if L in br: return None
            br[L]=(min(leaf,o),max(leaf,o))
    return br,M
cntB=badB=0
for p in range(2,8):
  for f in G[p-1]:
    for v in designs(f,p):
      for t in range(2,6):
        r=bproduct(f,p,v,t)
        cntB+=1
        if r is None or not isgrowth(*r): badB+=1
print("RuleB", cntB, "bad", badB)
# condition (2) necessity for t=2, p<=6
c1=viol=badv=0
for p in range(2,7):
  for f in G[p-1]:
    l=lens(f,p-1)
    for v in itertools.product(range(p),repeat=p-1):
      bs=[j-o if o<=j else o-j-1 for j,o in enumerate(v)]
      if sorted(bs)!=list(range(p-1)): continue
      c1+=1
      ok=all(o==0 or bs[j]<l[o] for j,o in enumerate(v))
      r=bproduct(f,p,v,2); g= r is not None and isgrowth(*r)
      if not ok: viol+=1
      if ok!=g: badv+=1
print("RuleB t=2 cond1",c1,"viol2",viol,"mismatch",badv)

# ---- Rule D
cntD=badD=0
for p in range(2,8):
  for f in G[p-1]:
    l=lens(f,p-1)
    for w in range(1,p+1):
      hyp=all((l[i]>=w-2*i) if 2*i<=w-1 else (l[i]>=2*i-w+1) for i in range(1,w))
      v=tuple((w-1-j) if j<w-1 else 0 for j in range(p-1))
      bs=[j-o if o<=j else o-j-1 for j,o in enumerate(v)]
      assert sorted(bs)==list(range(p-1))
      c2=all(o==0 or bs[j]<l[o] for j,o in enumerate(v))
      if c2!=hyp: badD+=1
      if hyp:
        for t in range(2,6):
          cntD+=1; r=bproduct(f,p,v,t); badD+= not isgrowth(*r)
print("RuleD", cntD, "bad", badD)

# ---- Lemma S: star K_{1,d}, leaves own exactly one block each
def star_designs(d):
    p=d+1; c=0
    for f in G[d]:
        # star placements only
        edges=[(f[k],f[k]+k) for k in range(1,d+1)]
        deg={}
        for a,b in edges: deg[a]=deg.get(a,0)+1; deg[b]=deg.get(b,0)+1
        if max(deg.values())!=d: continue
        cen=max(deg,key=deg.get)
        for v in designs(f,p):
            if cen in v: continue
            if sorted(v)==sorted(x for x in range(p) if x!=cen): c+=1
    return c
print("LemmaS", [star_designs(d) for d in range(1,7)])

# ---- Lemma B1
def oddleaf(M):
    out=set(); p=[0]*(M+1)
    def rec(k,used,deg):
        if k==0: out.add(tuple(p)); return
        for a in range(0,M-k+1):
            b=a+k
            if (a in used)!=(b in used):
                if any(x%2 and deg.get(x,0)>=1 for x in (a,b)): continue
                d2=dict(deg); d2[a]=d2.get(a,0)+1; d2[b]=d2.get(b,0)+1
                p[k]=a; rec(k-1,used|{a,b},d2)
    if M%2==0: p[M]=0; rec(M-1,{0,M},{0:1,M:1})
    return out
for p in range(2,7):
    M=2*(p-1); A=oddleaf(M); B=set()
    for f in G[p-1]:
        for v in designs(f,p):
            br,_=bproduct(f,p,v,2); B.add(tuple([0]+[br[k][0] for k in range(1,M+1)]))
    print("B1 p",p,len(A),len(B),A==B)

# ---- Lemma N1 check: h growth with m_h<=8 edges, truncation to lengths>=j with g<=j  -> star at 0
bad=0;tot=0
for mh in range(1,8):
  for h in G[mh] if mh<8 else []:
    for j in range(1,mh+1):
      g=mh-j+1
      # require labels 1..j-1 last j-1 added
      l=lens(h,mh); 
      if any(l[x]>=j for x in range(1,j)): continue
      if g>j: continue
      tot+=1
      if any(0 not in (h[i],h[i]+i) for i in range(j,mh+1)): bad+=1
print("N1", tot, "nonstar", bad)
