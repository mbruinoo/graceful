# Referee check of Theorem M and Lemma 0 (claim 2), from the statement only.
import sys, itertools, subprocess, networkx as nx
from fam import line
def rooted(T,v):
    par={v:None}; depth={v:0}; order=[v]; ch={}
    for u in order:
        ch[u]=[w for w in T[u] if w!=par[u]]
        for w in ch[u]: par[w]=u; depth[w]=depth[u]+1; order.append(w)
    return par,depth,order,ch
def mirror(T,v):
    par,depth,order,ch=rooted(T,v)
    D=max(depth.values()); r=len(ch[v]); mp=T.number_of_edges()
    q={j:1 for j in range(2,D+1)}
    for u in order:
        j=depth[u]+1
        if j>=2 and ch[u]:
            k=len(ch[u]); q[j]=max(q[j], k if k%2 else k+1)
    Q=1
    for j in q: Q*=q[j]
    g={D:1}
    for j in range(D-1,0,-1): g[j]=g[j+1]*q[j+1]
    assert g[1]==Q
    M=2**(D-1)*((2*r+1)*Q-2)
    S={}
    for i,p in enumerate(ch[v],1): S[p]=(2*i+1)*Q-2
    for u in order:
        if u==v: continue
        k=len(ch[u]); h=k//2; j=depth[u]+1
        taus=[t for t in range(-h,h+1) if t!=0 or k%2]
        for w,t in zip(ch[u],taus): S[w]=S[u]+2*g[j]*t
    f={v:0}
    for x in S: f[x]=2**(D-depth[x])*S[x]
    return f,M,mp
def growth_check(edges,f,top):
    # README section 1 definition, labels 0..top
    labs=sorted(f.values()); assert labs==list(range(top+1))
    ln={}
    for a,b in edges:
        k=abs(f[a]-f[b]); assert k not in ln; ln[k]=(f[a],f[b])
    assert sorted(ln)==list(range(1,top+1))
    used=set(ln[top])
    for k in range(top-1,0,-1):
        a,b=ln[k]; assert (a in used)!=(b in used); used|={a,b}
N=int(sys.argv[1]); cnt=0; maxleaves=0
for n in range(3,N+1):
    for T in nx.nonisomorphic_trees(n):
        seen=set()
        for v in T.nodes():
            if any(T.degree(w)==1 for w in T[v]): continue
            # dedupe rooted shapes cheaply by canonical string
            def can(u,p): return "("+"".join(sorted(can(w,u) for w in T[u] if w!=p))+")"
            c=can(v,None)
            if c in seen: continue
            seen.add(c)
            f,M,mp=mirror(T,v)
            assert max(f.values())==M, (M,max(f.values()))
            for extra in (0,1,3):   # d = M-m' , and larger d (labelling into [0,m'+d])
                top=M+extra
                e=list(T.edges()); ff=dict(f); nxt=n
                for num in range(1,top+1):
                    if num not in set(f.values()):
                        e.append((v,nxt)); ff[nxt]=num; nxt+=1
                assert len(e)==top and len(e)-mp==M-mp+extra
                assert ff[v]==0
                growth_check(e,ff,top)
            cnt+=1; maxleaves=max(maxleaves,M-mp)
print("rooted trees checked",cnt,"max leaves",maxleaves,"all pass")
