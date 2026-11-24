# gen.py -- test populations.  Output: one tree per line "u v u v ..." (0-based); with NAMES=1 a second file of names.
#   gen.py random n count seed          uniformly random LABELLED trees (Pruefer sequences), i.e. each labelled tree
#                                       equally likely; an unlabelled shape is weighted by n!/|Aut|.
#   gen.py sym nmin nmax                the symmetric population with nmin <= n <= nmax (names on stderr)
import sys, random, heapq, itertools
def emit(E): print(' '.join(f"{u} {v}" for u,v in E))
def prufer(n,rnd):
    pr=[rnd.randrange(n) for _ in range(n-2)]; deg=[1]*n
    for x in pr: deg[x]+=1
    E=[]; leaves=[i for i in range(n) if deg[i]==1]; heapq.heapify(leaves)
    for x in pr:
        l=heapq.heappop(leaves); E.append((l,x)); deg[x]-=1
        if deg[x]==1: heapq.heappush(leaves,x)
    E.append((heapq.heappop(leaves),heapq.heappop(leaves))); return E
def from_paren(s):
    """rooted tree from a parenthesis string; '|' joins two rooted trees by an edge between their roots"""
    E=[]; cnt=[0]
    def one(s):
        st=[]; root=None
        for ch in s:
            if ch=='(':
                v=cnt[0]; cnt[0]+=1
                if st: E.append((st[-1],v))
                else: root=v
                st.append(v)
            else: st.pop()
        return root
    parts=s.split('|'); roots=[one(p) for p in parts]
    for a,b in zip(roots,roots[1:]): E.append((a,b))
    return E
hub=lambda m:"("+"()"*m+")"
path=lambda k:"("*k+")"*k
def stem(a,inner):            # path of a edges ending in `inner` (a>=1): the rooted branch
    return "("*(a-1)+inner+")"*(a-1)
def sph(ds):
    def b(i): return "("+(b(i+1)*ds[i] if i<len(ds) else "")+")"
    return b(0)
def binary(d): return sph([2]*d)
def rooted_all(k):            # all rooted trees on k vertices as paren strings (canonical, sorted children)
    if k==1: return ["()"]
    res=set()
    def parts(m,mx):
        if m==0: yield []; return
        for a in range(min(m,mx),0,-1):
            for rest in parts(m-a,a): yield [a]+rest
    for p in parts(k-1,k-1):
        for combo in itertools.product(*[rooted_all_c(a) for a in p]):
            res.add("("+"".join(sorted(combo))+")")
    return sorted(res)
_cache={}
def rooted_all_c(k):
    if k not in _cache: _cache[k]=rooted_all(k)
    return _cache[k]
def sym_population(nmin,nmax):
    out=[]
    def add(name,s):
        E=from_paren(s) if isinstance(s,str) else s
        n=len(E)+1
        if nmin<=n<=nmax: out.append((name,E))
    # equal-leg spiders S(L^k)
    for k in range(3,13):
        for L in range(2,34): add(f"spider {k} legs of length {L}","("+path(L)*k+")")
    # k equal hubs on a centre, and k stems of length a ending in hubs of m leaves
    for k in range(3,9):
        for a in range(1,5):
            for m in range(2,16): add(f"{k} stems of length {a} ending in a hub of {m} leaves","("+stem(a,hub(m))*k+")")
    # k copies of each rooted tree on up to 7 vertices round a centre
    for k in range(3,7):
        for sz in range(3,8):
            for i,b in enumerate(rooted_all_c(sz)): add(f"{k} copies of rooted tree {b} round a centre","("+b*k+")")
    # two copies joined by an edge (bicentred symmetric)
    for sz in range(5,9):
        for b in rooted_all_c(sz): add(f"two copies of {b} joined at the roots",b+"|"+b)
    # spherically symmetric
    for ds in ([2,2,2],[2,2,2,2],[2,2,2,2,2],[3,3],[3,3,3],[4,4],[5,5],[3,3,3,2],[3,2,2],[3,2,2,2],[2,3,3],[3,3,2],[4,3],[3,4],[4,4,2],[2,4,4],[6,6],[7,7],[3,2,3],[2,2,3],[4,2,2],[5,2,2],[3,3,2,2],[2,2,2,3],[9,9],[4,4,4],[2,3,2,3]):
        add("spherically symmetric "+str(tuple(ds)),sph(ds))
    # complete k-ary trees truncated
    # trees named as failures in README sections 7, 11-13
    add("README 11: S(2,2,2,2) first R=1 failure","("+path(2)*4+")")
    add("README 11/12: S(3,3,3)","("+path(3)*3+")")
    for k in (5,8,11): add(f"README 12: S(2^{k}) no zigzag split","("+path(2)*k+")")
    def el(s): 
        E=[]
        for tok in s.split():
            a,b=tok.split('-'); E.append((int(a),int(b)))
        return E
    add("README 11: first R=2 failure at n=16 (a)",el("1-0 1-2 0-7 2-3 3-4 4-5 4-6 7-8 7-12 8-9 9-10 9-11 12-13 13-14 13-15"))
    add("README 11: first R=2 failure at n=16 (b)",el("1-0 1-2 0-6 0-11 2-3 2-4 2-5 6-7 7-8 7-9 7-10 11-12 12-13 12-14 12-15"))
    add("README 11: R=2 failure at n=18",el("1-0 1-2 1-6 1-10 0-14 2-3 2-4 2-5 6-7 6-8 6-9 10-11 10-12 10-13 14-15 15-16 15-17"))
    E=el("0-1 1-2 2-3 3-4 0-11 11-12 12-13 12-20 20-21")+[(4,i) for i in range(5,11)]+[(13,i) for i in range(14,20)]
    add("README 11: 22-vertex tree needing three skips",E)
    E=el("0-1 1-2 1-3")+[(2,i) for i in range(4,12)]+[(3,i) for i in range(12,21)]+[(0,i) for i in (21,22,23)]
    add("README 7: 24-vertex tree with a non-anchor of degree 4",E)
    for m in range(2,9): add(f"README 11: three arms of length 2 ending in hubs of {m} leaves","("+stem(2,hub(m))*3+")")
    for m in (5,10,20,30,60,90): add(f"README 18: H({m})","("+hub(m)+"(())(()))")
    return out
if __name__=='__main__':
    if sys.argv[1]=='random':
        n,cnt,seed=map(int,sys.argv[2:5]); rnd=random.Random(seed)
        for _ in range(cnt): emit(prufer(n,rnd))
    elif sys.argv[1]=='sym':
        for name,E in sym_population(int(sys.argv[2]),int(sys.argv[3])):
            emit(E); print(len(E)+1,name,file=sys.stderr)
