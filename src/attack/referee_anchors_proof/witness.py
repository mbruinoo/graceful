# Explicit witnesses of claim 1 checked from the growth definition (labels 0..m, v=0).
import sys
def check(m,edges):  # edges: list of (labelA,labelB) ; tree shape checked separately by degree profile
    labs=set(); ln={}
    for a,b in edges:
        k=abs(a-b); assert k not in ln,(m,k); ln[k]=(a,b); labs|={a,b}
    assert labs==set(range(m+1)) and sorted(ln)==list(range(1,m+1)),m
    used=set(ln[m])
    for k in range(m-1,0,-1):
        a,b=ln[k]; assert (a in used)!=(b in used),(m,k); used|={a,b}
def shape(edges,expect):
    from collections import Counter
    ch=Counter(a for a,b in edges)   # edges written (parent,child)
    hubs=sorted(ch[b] for a,b in edges if a==0)
    assert hubs==sorted(expect),(hubs,expect)
    assert all(a==0 or (0,a) in edges for a,b in edges)
def H3(m):
    out=[]
    if m%4==3:
        b=(m-1)//2; c=m-1; w1=(b-1)//2; w0=w1+1
        e=[(0,m),(0,b),(0,c),(b,b+w1),(m,m-w0)]+[(c,c-w) for w in range(1,m) if w not in (b,c,w0,w1)]
        out.append(e)
    if m%3==0:
        b=(2*m-3)//3; c=m-1; w1=m//3; w0=b+1
        e=[(0,m),(0,b),(0,c),(b,b-w1),(m,m-w0)]+[(c,c-w) for w in range(1,m) if w not in (b,c,w0,w1)]
        assert m-w0==m//3
        out.append(e)
    if m%5==0:
        b=2*m//5; c=4*m//5
        e=[(0,m),(0,b),(0,c),(b,b+m//5),(c,c-3*m//5)]+[(m,m-w) for w in range(1,m) if w not in (b,c,m//5,3*m//5)]
        out.append(e)
    return out
n3=0
for m in range(11,int(sys.argv[1])+1,2):
    for e in H3(m): check(m,e); shape(e,[1,1,m-5]); n3+=1
print("H3 witnesses verified",n3)
# H2: build the labelling of proof steps (2)-(4) for every (x,s,j) allowed by the rule, incl. all gamma-choices counts
def H2(m,s,j):
    t=m//s; b=m-t; N=b
    e=[(0,m),(0,b)]+[(m,m-w) for w in range(b+1,m)]
    gam=set()
    # choose j bottoms: pairs {r,t-r} then t/2
    need=j
    if j%2: gam.add(t//2); need-=1
    r=1
    while need>0: gam|={r,t-r}; need-=2; r+=1
    assert len(gam)==j and all(1<=w<=t-1 for w in gam)
    for w in range(1,N):
        if w%t==0: e.append((b,b-w))          # beta
        elif w in gam: e.append((b,b+w))      # gamma
        else: e.append((m,m-w))               # alpha
    return e
n2=0
for m in range(2,int(sys.argv[2])+1):
    for s in range(2,m+1):
        if m%s: continue
        t=m//s
        for j in range(0,t):
            if t%2 and j%2: continue
            x=s-2+j; e=H2(m,s,j); check(m,e); shape(e,[x,m-2-x]); n2+=1
print("H2 constructions verified",n2)
