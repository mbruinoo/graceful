# referee: S(2,2,1) brute force; E2 counts; S1+ instance generation
import sys, itertools
import networkx as nx
from common import *
from thms import enum, trees, rooted
def growth_ok(n,edges,lab):
    # README sec 8 form: bijection onto 0..n-1, lengths 1..n-1 once each, brackets n-1..k connected for every k
    L=sorted(((abs(lab[a]-lab[b]),a,b) for a,b in edges),reverse=True)
    if [x[0] for x in L]!=list(range(n-1,0,-1)): return False
    comp={L[0][1],L[0][2]}
    for _,a,b in L[1:]:
        if (a in comp)==(b in comp): return False
        comp|={a,b}
    return True
def canon(adj,v,p): return "("+"".join(sorted(canon(adj,w,v) for w in adj[v] if w!=p))+")"
if sys.argv[1]=="S221":
    e=[(0,1),(1,2),(0,3),(3,4),(0,5)]; c={}; tot=0
    for perm in itertools.permutations(range(6)):
        if growth_ok(6,e,perm):
            tot+=1; k=[x for x in e if abs(perm[x[0]]-perm[x[1]])==1][0]; c[k]=c.get(k,0)+1
    print("S(2,2,1): growth placements",tot,"length-1 edge counts",c)
if sys.argv[1]=="E2":
    for n in range(4,int(sys.argv[2])+1):
        fails=0; small=None
        for e in trees(n):
            adj=[[] for _ in range(n)]
            for a,b in e: adj[a].append(b); adj[b].append(a)
            hang=set()   # leaves that can be hung by the length-1 bracket
            for r in range(n):
                for lab in enum(n,r,e,n):
                    a,b=[x for x in e if abs(lab[x[0]]-lab[x[1]])==1][0]
                    par,dep,ch=rooted(n,r,e)
                    hang.add(a if dep[a]>dep[b] else b)
            orb={}
            for x in range(n):
                if len(adj[x])==1: orb.setdefault(canon(adj,x,-1),[]).append(x)
            for k,xs in orb.items():
                if not any(x in hang for x in xs): fails+=1; small=small or (e,xs[0])
        print("E2 n=%d failing (tree, leaf-orbit) pairs: %d"%(n,fails), small if fails else "")
if sys.argv[1]=="S1P":   # read tree file + ref slack-0 output; for each NONE write the n trees T+leaf at w
    for l,o in zip(open(sys.argv[2]),open(sys.argv[3])):
        if " NONE " in o:
            name,n,r,e=parse_tree(l)
            for w in range(n): print("%s+%d"%(name,w),n+1,r," ".join("%d %d"%x for x in e+[(w,n)]))
if sys.argv[1]=="S1Psum":
    res={}; rr={}
    for o in open(sys.argv[2]):
        t=o.split(); name,w=t[0].rsplit("+",1); root=name.split("@")[1]
        res.setdefault(name,False); rr.setdefault(name,False)
        assert t[1] in ("FOUND","NONE"),o
        if t[1]=="FOUND":
            res[name]=True
            if w==root: rr[name]=True
    print(sys.argv[2],"non-anchor pairs",len(res),"some w works",sum(res.values()),"w=r works",sum(rr.values()))
