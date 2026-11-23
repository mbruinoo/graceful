# Referee check of claim 0: rebuild the three families move by move from the proof text,
# check every move against README section 1/2 definitions, plus the spider corollary via section 7 gluing.
import sys
def zig(lo,hi,start_high):
    # alternate extremes of [lo,hi]
    out=[];a,b=lo,hi;h=start_high
    while a<=b:
        if h: out.append(b); b-=1
        else: out.append(a); a+=1
        h=not h
    return out
def fam(kind,s):
    if kind==3:
        m=3*s+2
        A=[0]; 
        for i in range(1,s+1): A+= [m-i,i]
        B=[0,m,2*s+1]
        A+=zig(s+1,2*s,True)
        # order of numbers: B:m ; A: m-1..m-2s ; B: s+1 ; A: s..1
        lensB=[m,s+1]
    elif kind==5:
        m=5*s+4
        A=[0]
        for i in range(0,s+1): A+=[m-i,i+1]
        for i in range(1,s+1): A+=[4*s+3-i,s+1+i]
        A+=zig(2*s+2,3*s+1,True)
        B=[0,3*s+2,4*s+3]; lensB=[3*s+2,s+1]
    else:
        m=7*s+3
        A=[0]
        for i in range(0,2*s): A+=[m-i,i+1]
        A+=[m-2*s]
        for i in range(1,s+1): A+=[2*s+1+i,5*s+3-i]
        A+=zig(3*s+3,4*s+2,False)
        B=[0,3*s+2,2*s+1]; lensB=[3*s+2,s+1]
    return m,A,B,lensB
def check_growth(m,edges):
    # edges: list of (u,v) on labels 0..m ; README s1/s2: each length once, longest first exactly one used foot
    L={}
    for u,v in edges:
        d=abs(u-v); assert 1<=d<=m and d not in L; L[d]=(u,v)
    assert len(L)==m
    used={0,m}; assert set(L[m])=={0,m}
    for k in range(m-1,0,-1):
        u,v=L[k]; assert (u in used)!=(v in used),(k,u,v); used|={u,v}
    assert used==set(range(m+1))
def run(S):
    for kind in (3,5,7):
        for s in range(1,S+1):
            m,A,B,lensB=fam(kind,s)
            assert len(A)==m-1 and len(B)==3
            assert sorted(A+B[1:])==list(range(m+1))
            dA=[abs(A[i+1]-A[i]) for i in range(len(A)-1)]
            dB=[abs(B[i+1]-B[i]) for i in range(2)]
            assert dB==lensB
            assert all(dA[i]>dA[i+1] for i in range(len(dA)-1)) and dB[0]>dB[1]
            edges=list(zip(A,A[1:]))+list(zip(B,B[1:]))
            check_growth(m,edges)
            # path: vertex sequence reversed(B)+A[1:], label 0 is third from end
            seq=B[::-1]+A[1:]; assert seq[2]==0 and len(set(seq))==m+1
    print("families ok s<=",S)
def glue(m,edgesT,c):
    # README s7 gluing: O = zigzag path on c edges (labels 1..c+1), x = largest low label a+1 at an end.
    # T' on labels 1..m+1 (shift by 1) with y at label 1.
    r=c
    seq=zig(1,r+1,False)  # 1,r+1,2,r,...
    if r%2==1: seq=[r+2-x for x in seq]
    lowmax=(r+2)//2 if r%2==0 else (r+1)//2
    assert seq[-1]==lowmax, (seq,lowmax)
    a=lowmax-1; M=m+1
    for u,v in zip(seq,seq[1:]): assert (u<=a+1)!=(v<=a+1)
    f=lambda x: x if x<=a+1 else x+M-1
    E=[(f(u),f(v)) for u,v in zip(seq,seq[1:])]
    E+=[(u+1+a,v+1+a) for u,v in edgesT]
    n=M+r
    E=[(u-1,v-1) for u,v in E]
    check_growth(n-1,E)
    # leg lengths from the centre (label a  after shift)
    adj={}
    for u,v in E: adj.setdefault(u,[]).append(v); adj.setdefault(v,[]).append(u)
    cen=a
    deg3=[x for x in adj if len(adj[x])>=3]
    legs=[]
    for nb in adj[cen]:
        p,q,l=cen,nb,1
        while len(adj[q])==2:
            p,q=q,[z for z in adj[q] if z!=p][0]; l+=1
        assert len(adj[q])==1; legs.append(l)
    return sorted(legs)
def spiders(S,C):
    cnt=0
    for kind in (3,5,7):
        for s in range(1,S+1):
            m,A,B,_=fam(kind,s)
            edges=list(zip(A,A[1:]))+list(zip(B,B[1:]))
            for c in range(1,C+1):
                legs=glue(m,edges,c)
                assert legs==sorted([m-2,2,c]),(legs,m,c); cnt+=1
    print("spider corollary ok cases",cnt)
run(int(sys.argv[1]) if len(sys.argv)>1 else 200)
spiders(15,40)
