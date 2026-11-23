# Referee: direct checks from the definitions of two exhibited labelings (no search).
def runs(un):
    un=sorted(un); r=[]
    for x in un:
        if r and r[-1][-1]==x-1: r[-1].append(x)
        else: r.append([x])
    return r
def trace(n,edges,lab):
    assert sorted(lab.values())==list(range(1,n+1))
    br={}
    for u,v in edges:
        k=abs(lab[u]-lab[v]); assert k not in br; br[k]=(lab[u],lab[v])
    assert sorted(br)==list(range(1,n))
    used=set(); out=[]
    for k in range(n-1,0,-1):
        a,b=br[k]
        if k==n-1: assert not used
        else: assert (a in used)!=(b in used), "not growth"
        used|={a,b}; out.append(runs(set(range(1,n+1))-used))
    return out
# S(3,3,3), claim 1: centre 1, legs 1-10-3-8, 1-9-5-6, 1-7-4-2 (vertices named by label)
edges=[(1,10),(10,3),(3,8),(1,9),(9,5),(5,6),(1,7),(7,4),(4,2)]
tr=trace(10,edges,{i:i for i in range(1,11)})
def literal_ok(rs):   # exists main run, others single, at most one on each side
    for i,m in enumerate(rs):
        if all(len(r)==1 for j,r in enumerate(rs) if j!=i) and i<=1 and len(rs)-1-i<=1: return True
    return not rs
def leftmost_ok(rs):  # main = first run of maximal size
    if not rs: return True
    mx=max(map(len,rs)); i=[len(r) for r in rs].index(mx)
    return all(len(r)==1 for j,r in enumerate(rs) if j!=i) and i<=1 and len(rs)-1-i<=1
for rs in tr: print(rs, 'literal', literal_ok(rs), 'leftmost-main', leftmost_ok(rs))
print("S(3,3,3): growth placement, literal each-side rule holds:", all(literal_ok(r) for r in tr))
# 22-vertex tree of sec 11, claimed two-run certificate
e="0 1 1 2 2 3 3 4 4 5 4 6 4 7 4 8 4 9 4 10 0 11 11 12 12 13 13 14 13 15 13 16 13 17 13 18 13 19 12 20 20 21".split()
edges=[(int(e[i]),int(e[i+1])) for i in range(0,len(e),2)]
labs=list(map(int,"3 19 4 18 5 17 13 9 8 7 6 20 2 21 10 11 12 14 15 16 22 1".split()))
tr=trace(22,edges,dict(enumerate(labs)))
print("22-vertex tree: growth placement; max number of runs =",max(len(r) for r in tr))
