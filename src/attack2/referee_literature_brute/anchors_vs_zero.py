import subprocess, sys
def run(cases):
    inp="\n".join(f"{n} {v} "+" ".join(f"{a} {b}" for a,b in E) for n,v,E in cases)+"\n"
    out=subprocess.run(["./gs"],input=inp,capture_output=True,text=True).stdout.split()
    return [(int(out[2*i]),int(out[2*i+1])) for i in range(len(cases))]
# P7
E=[(i,i+1) for i in range(6)]
print("P7 vertex -> (0-centred graceful, anchor):",dict(zip(range(7),run([(7,v,E) for v in range(7)]))))
# H(1,1,k): centre 0 with hubs 1,2,3; hub1,hub2 one leaf each, hub3 k leaves
def H(k):
    E=[(0,1),(0,2),(0,3),(1,4),(2,5)]; n=6
    for i in range(k): E.append((3,n)); n+=1
    return n,0,E
for k in range(2,14):
    n,v,E=H(k); print(f"H(1,1,{k}) m={n-1}: centre (0-centred graceful, anchor) =",run([(n,v,E)])[0], flush=True)
# DH(p,q): v=0, c1=1, c2=2
def DH(p,q):
    E=[(0,1),(0,2)]; n=3
    for i in range(p): E.append((1,n)); n+=1
    for i in range(q): E.append((2,n)); n+=1
    return n,0,E
def h2(p,q):
    m=p+q+2
    for x in (p,q):
        for s in range(2,m+1):
            if m%s: continue
            t=m//s; j=x-(s-2)
            if 0<=j<=t-1 and (t%2==0 or j%2==0): return True
    return False
def vb(p,q):
    m=p+q+2
    for m1,m2 in ((p,q),(q,p)):
        for r in range(2,m//2+1):
            for x in range(0,min(r-1,m2)+1):
                if x%2 and r%2: continue
                if m1==(m2+2-x)*(r-1)-x: return True
    return False
dis=tot=non=0
for m in range(4,201):
    for p in range(1,m-2):
        q=m-2-p
        if q<p: continue
        tot+=1; non+= not h2(p,q); dis+= h2(p,q)!=vb(p,q)
print(f"DH(p,q) 1<=p<=q, m<=200: {tot} trees, {non} non-anchors by H2, H2 vs VB disagreements {dis}")
M=int(sys.argv[1]) if len(sys.argv)>1 else 18
cases=[];keys=[]
for m in range(4,M+1):
    for p in range(1,m-2):
        q=m-2-p
        if q<p: continue
        cases.append(DH(p,q)); keys.append((p,q))
res=run(cases); bad=[(k,r,h2(*k)) for k,r in zip(keys,res) if not (r[0]==r[1]==int(h2(*k)))]
print(f"brute force DH, m<={M}: {len(keys)} trees, cases where anchor/0-centred/H2 not all equal: {bad}")
