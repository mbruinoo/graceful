# hub_check.py -- machine checks for the two hub theorems (see PROOFS.txt).
#  DH(p,q): path c1 - v - c2, c1 has p leaf children, c2 has q; m = p+q+2 edges.
#    Theorem H2: v is an anchor  iff  for x = p or x = q there is a divisor s >= 2 of m, t = m/s, with
#                0 <= x-(s-2) <= t-1  and  (t even or x-(s-2) even).
#  H(1,1,k): v with three neighbours c1,c2,c3; c1,c2 have one leaf child each, c3 has k; m = k+5.
#    Theorem H3: for odd m >= 11, v is an anchor iff 3|m or 5|m or m = 3 (mod 4).
# Checked against (a) ./anchq, the generic growth-placement search from the README definitions (small m), and
#                 (b) ./d2, the exact depth-2 search (larger m).  Explicit witnesses of H3 are checked by check_growth from mirror.py.
import subprocess,sys
from mirror import check_growth
def dh_formula(p,q):
    m=p+q+2
    for x in (p,q):
        for s in range(2,m+1):
            if m%s: continue
            t=m//s; j=x-(s-2)
            if 0<=j<=t-1 and (t%2==0 or j%2==0): return True
    return False
def h3_formula(m): return m%3==0 or m%5==0 or m%4==3
def gen(ks):
    r=len(ks); e=[]; nx=r+1
    for i,kk in enumerate(ks):
        e.append((0,i+1))
        for j in range(kk): e.append((i+1,nx)); nx+=1
    return nx,e
def anchq(ks):
    n,e=gen(ks); line="%d 0 "%n+" ".join("%d %d"%x for x in e)
    return subprocess.run(["./anchq"],input=line+"\n",capture_output=True,text=True).stdout.startswith("ANCHOR")
def d2(ks): return subprocess.run(["./d2"]+[str(k) for k in ks],capture_output=True,text=True).stdout.startswith("ANCHOR")
def h3_witness(m):
    # returns (hub labels [b_small1,b_small2,b_big], leaf labels per hub) or None
    k=m-5
    if m%4==3:
        c=m-1; b=(m-1)//2; w1=(b-1)//2; w0=w1+1
        L=[[m-w0],[b+w1],[c-w for w in range(1,c) if w not in (b,w0,w1)]]; return [m,b,c],L
    if m%3==0:
        c=m-1; b=(2*m-3)//3; w1=c-b; w0=b+1
        L=[[m-w0],[b-w1],[c-w for w in range(1,c) if w not in (b,w0,w1)]]; return [m,b,c],L
    if m%5==0:
        b=2*m//5; c=4*m//5
        L=[[b+m//5],[c-3*m//5],[m-w for w in range(1,m) if w not in (b,c,m//5,3*m//5)]]; return [b,c,m],L
    return None
A=int(sys.argv[1]); B=int(sys.argv[2]); C=int(sys.argv[3])
bad=0; cnt=0; nonA=0
for m in range(2,B+1):
    for q in range(0,(m-2)//2+1):
        p=m-2-q; f=dh_formula(p,q); cnt+=1; nonA+= (not f)
        if m<=A and anchq((p,q))!=f: bad+=1; print("H2 MISMATCH anchq",p,q)
        if d2((p,q))!=f: bad+=1; print("H2 MISMATCH d2",p,q)
print("H2: DH(p,q) for all m<=%d (%d trees, %d non-anchor): formula vs d2; and vs anchq for m<=%d; mismatches %d"%(B,cnt,nonA,A,bad),flush=True)
bad=0; non=[]
for m in range(11,C+1,2):
    f=h3_formula(m); k=m-5
    if m<=31 and anchq((1,1,k))!=f: bad+=1; print("H3 MISMATCH anchq",m)
    if d2((1,1,k))!=f: bad+=1; print("H3 MISMATCH d2",m)
    if not f: non.append(m)
    w=h3_witness(m)
    assert (w is not None)==f
    if w:
        hubs,L=w; labels=[0]+hubs; edges=[(0,1),(0,2),(0,3)]; nx=4
        for i in range(3):
            for x in L[i]: labels.append(x); edges.append((i+1,nx)); nx+=1
        assert [len(x) for x in L]==[1,1,k]
        check_growth(edges,labels,m+1)
print("H3: H(1,1,m-5) for odd 11<=m<=%d: formula vs d2 (and anchq for m<=31), explicit witnesses verified; mismatches %d"%(C,bad))
print("    non-anchor m:",non)
