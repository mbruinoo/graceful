# mirror.py -- machine check of the "mirror labelling" theorem (leaf-rich anchors), straight from README section 1/2 definitions.
#
# Theorem checked.  T' rooted at v, every neighbour of v a non-leaf, r = deg(v) >= 1, D = eccentricity of v (>= 2), m' edges.
#   q_j (j=2..D) = smallest odd number >= max number of children of a vertex at depth j-1,  Q = prod q_j,
#   M = 2^(D-1) * ((2r+1)Q - 2).
# Then T' plus (M - m') new leaves at v has a growth placement with v at label 1 (label 0 in the 0-based convention used here),
# given explicitly:  S(i-th child of v) = (2i+1)Q - 2;   children of u at depth j-1>=1 get S = S(u) + 2*g_j*tau,
#   tau ranging over a symmetric set {-h..h} (0 used iff the number of children is odd), g_j = prod_{i>j} q_i;
#   label(x) = 2^(D-depth(x)) * S(x);  the new leaves get the labels in 1..M not used.
# The check: labels are a bijection onto 0..M; edge lengths are exactly 1..M; and, placing brackets longest first,
# every bracket has exactly one foot already used (definition of growth placement); v has label 0.
import sys
def rooted_trees(n):
    # all rooted trees on n vertices as canonical level sequences (Beyer-Hedetniemi)
    L=list(range(n))
    while True:
        yield L[:]
        p=n-1
        while p>0 and L[p]==1: p-=1
        if p==0: return
        q=p-1
        while L[q]!=L[p]-1: q-=1
        for i in range(p,n): L[i]=L[i-(p-q)]
def parents(L):
    par=[-1]*len(L); st=[]
    for i,l in enumerate(L):
        while st and L[st[-1]]>=l: st.pop()
        if st: par[i]=st[-1]
        st.append(i)
    return par
def mirror_labels(par,depth):
    n=len(par); ch=[[] for _ in range(n)]
    for i in range(1,n): ch[par[i]].append(i)
    D=max(depth); r=len(ch[0])
    q=[1]*(D+2)
    for j in range(2,D+1):
        k=max(len(ch[u]) for u in range(n) if depth[u]==j-1)
        q[j]=k if k%2==1 else k+1
    g=[1]*(D+2)
    for j in range(D-1,0,-1): g[j]=g[j+1]*q[j+1]
    Q=g[1]; S=[0]*n
    for i,c in enumerate(ch[0]): S[c]=(2*(i+1)+1)*Q-2
    order=sorted(range(1,n),key=lambda x:depth[x])
    for u in order:
        k=len(ch[u]); h=k//2; taus=[t for t in range(-h,h+1) if (t!=0 or k%2==1)]
        for x,t in zip(ch[u],taus): S[x]=S[u]+2*g[depth[x]]*t
    lab=[0]*n
    for x in range(1,n): lab[x]=2**(D-depth[x])*S[x]
    M=2**(D-1)*((2*r+1)*Q-2)
    return lab,M
def check_growth(edges,labels,N):
    # labels: list for vertices; N = number of vertices; labels must be 0..N-1; edges list of (a,b)
    assert sorted(labels)==list(range(N)), "labels not a bijection"
    lens=sorted(abs(labels[a]-labels[b]) for a,b in edges)
    assert lens==list(range(1,N)), "lengths not 1..N-1"
    used=set(); byLen=sorted(edges,key=lambda e:-abs(labels[e[0]]-labels[e[1]]))
    a,b=byLen[0]; used|={a,b}
    for a,b in byLen[1:]:
        assert (a in used)!=(b in used), "bracket does not have exactly one used foot"
        used|={a,b}
    return True
if __name__=="__main__":
    N=int(sys.argv[1]); tot=0; worst={}
    for n in range(3,N+1):
        cnt=0; mx=0
        for L in rooted_trees(n):
            par=parents(L); ch=[0]*n
            for i in range(1,n): ch[par[i]]+=1
            if any(par[i]==0 and ch[i]==0 for i in range(1,n)): continue   # v has a leaf neighbour: strip leaves first
            lab,M=mirror_labels(par,L)
            edges=[(par[i],i) for i in range(1,n)]
            usedl=set(lab); labels=lab[:]; nx=n
            for x in range(1,M+1):
                if x not in usedl: labels.append(x); edges.append((0,nx)); nx+=1
            assert nx==M+1
            check_growth(edges,labels,M+1); assert labels[0]==0
            cnt+=1; mx=max(mx,M-(n-1))
        tot+=cnt; print("n'=%d rooted trees (no leaf at root) checked: %d   largest number of leaves used: %d"%(n,cnt,mx),flush=True)
    print("ALL OK, total",tot)
