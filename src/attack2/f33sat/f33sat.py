# f33sat.py -- SAT search for a growth placement obeying the "ends" rule (Conjecture F33, README section 19).
# usage: f33sat.py stems K A M | sph d1 d2 ... | edges u v u v ...     [env TIMEOUT seconds, FREE=1 drops the rule, NOSYM=1 drops symmetry breaking]
# Labels 0..m.  Variables: x[v][l] (vertex v has label l), P[k][l] (bracket k stands on l, l+k),
# u[k][c] (cell c is used once brackets m..k are placed), h[k][c] (cell c is a hole at that moment).
# The rule is rule 33 of ../folds (verify_rule.py): a step places at an end of the run, or one cell in from an end
# (the jumped cell becomes a hole), or fills the leftmost or rightmost hole.  Every FOUND is re-checked by
# ../folds/lib.replay and verify_rule.obeys, which share no code with this file.
import sys, os, itertools
from pysat.solvers import Cadical153
def tree(args):
    E=[]
    if args[0]=='stems':
        K,A,M=map(int,args[1:4]); n=1
        for _ in range(K):
            p=0
            for _ in range(A): E.append((p,n)); p=n; n+=1
            for _ in range(M): E.append((p,n)); n+=1
    elif args[0]=='sph':
        ds=list(map(int,args[1:])); layer=[0]; n=1
        for d in ds:
            nx=[]
            for p in layer:
                for _ in range(d): E.append((p,n)); nx.append(n); n+=1
            layer=nx
    else:
        a=list(map(int,args[1:])); E=list(zip(a[::2],a[1::2])); n=len(E)+1
    return n,E
def solve(n,E,rule=True,timeout=None,sym=False):
    m=n-1; cnt=[0]
    def new(): cnt[0]+=1; return cnt[0]
    x=[[new() for l in range(n)] for v in range(n)]
    P={(k,l):new() for k in range(1,n) for l in range(n-k)}
    u={(k,c):new() for k in range(1,n) for c in range(n)}
    h={(k,c):new() for k in range(1,n+1) for c in range(n)}
    S=Cadical153()
    for c in range(n): S.add_clause([-h[n,c]]); S.add_clause([-h[m,c]])
    for v in range(n):
        S.add_clause(x[v])
    for l in range(n):
        S.add_clause([x[v][l] for v in range(n)])
        for a,b in itertools.combinations(range(n),2): S.add_clause([-x[a][l],-x[b][l]])
    for (a,b) in E:
        for k in range(1,n):
            for l in range(n-k):
                S.add_clause([-x[a][l],-x[b][l+k],P[k,l]]); S.add_clause([-x[b][l],-x[a][l+k],P[k,l]])
    for k in range(1,n):
        ps=[P[k,l] for l in range(n-k)]; S.add_clause(ps)
        for a,b in itertools.combinations(ps,2): S.add_clause([-a,-b])
    for c in range(n): S.add_clause([u[m,c] if c in(0,m) else -u[m,c]])
    for k in range(m-1,0,-1):
        up=lambda c:u[k+1,c]
        for l in range(n-k):
            S.add_clause([-P[k,l],up(l),up(l+k)]); S.add_clause([-P[k,l],-up(l),-up(l+k)])
        for c in range(n):
            feet=[P[k,l] for l in (c,c-k) if 0<=l<n-k]
            S.add_clause([-u[k,c],up(c)]+feet); S.add_clause([u[k,c],-up(c)])
            for f in feet: S.add_clause([u[k,c],-f])
        if not rule: continue
        # helper variables on the state before the step
        pair=[new() for c in range(n-1)]            # c and c+1 both unused
        for c in range(n-1):
            S.add_clause([-pair[c],-up(c)]); S.add_clause([-pair[c],-up(c+1)]); S.add_clause([pair[c],up(c),up(c+1)])
        Lp=[new() for c in range(n-1)]; Rp=[new() for c in range(n-1)]   # a pair at <= c ; at >= c
        for c in range(n-1):
            S.add_clause([-pair[c],Lp[c]]); S.add_clause([-pair[c],Rp[c]])
            if c: S.add_clause([-Lp[c-1],Lp[c]]); S.add_clause([-Lp[c],Lp[c-1],pair[c]])
            else: S.add_clause([-Lp[c],pair[c]])
            if c<n-2: S.add_clause([-Rp[c+1],Rp[c]]); S.add_clause([-Rp[c],Rp[c+1],pair[c]])
            else: S.add_clause([-Rp[c],pair[c]])
        A=Lp[n-2]
        # at most one long run: a pair to the left of c (ending at <= c) and a pair to the right force c unused
        for c in range(1,n-1):
            S.add_clause([-Lp[c-1],-Rp[c],-up(c)])
        # STRICT=1: the rule exactly as in ../folds/verify_rule.py (rule 33): holes are the cells made by a skip,
        # tracked as state h[k][c]; the cell left when the run shrinks to one cell is not a hole.
        hp=(lambda c:h[k+1,c]); T=lambda c: up(c) if 0<=c<n else None   # None = off the tape = "used"
        def cl(lits):
            out=[]
            for x_ in lits:
                if x_=='T': return            # clause satisfied
                if x_=='F': continue
                out.append(x_)
            S.add_clause(out)
        pos=lambda c: 'T' if not 0<=c<n else up(c)
        neg=lambda c: 'F' if not 0<=c<n else -up(c)
        for c in range(n):
            cl([-h[k,c],-u[k,c]]); cl([-hp(c),u[k,c],h[k,c]])
        HL=[new() for c in range(n)]; HR=[new() for c in range(n)]
        for c in range(n):
            S.add_clause([-hp(c),HL[c]]); S.add_clause([-hp(c),HR[c]])
            if c: S.add_clause([-HL[c-1],HL[c]]); S.add_clause([-HL[c],HL[c-1],hp(c)])
            else: S.add_clause([-HL[c],hp(c)])
            if c<n-1: S.add_clause([-HR[c+1],HR[c]]); S.add_clause([-HR[c],HR[c+1],hp(c)])
            else: S.add_clause([-HR[c],hp(c)])
        for l in range(n-k):
            for f,far in ((l,-1),(l+k,1)):
                if not 1<=f<=n-2: continue
                fr=[-P[k,l],up(f)]
                if 2<=f<=n-3: cl(fr+[up(f-1),up(f+1),up(f-2),up(f+2)])
                cl(fr+[-hp(f),-HL[f-1],-HR[f+1]])
                a_,b_=f+far,f-far            # a_ = neighbour on the far side, b_ = on the parent's side
                # a_ becomes a hole iff both neighbours unused and the cell beyond a_ is used
                cl(fr+[up(f-1),up(f+1),neg(a_+far),h[k,a_]])
                cl(fr+[-h[k,a_],hp(a_),-up(f-1)]); cl(fr+[-h[k,a_],hp(a_),-up(f+1)]); cl(fr+[-h[k,a_],hp(a_),pos(a_+far)])
                # b_ becomes a hole iff both neighbours unused and the cell beyond a_ is unused
                cl(fr+[up(f-1),up(f+1),pos(a_+far),h[k,b_]])
                cl(fr+[-h[k,b_],hp(b_),-up(f-1)]); cl(fr+[-h[k,b_],hp(b_),-up(f+1)]); cl(fr+[-h[k,b_],hp(b_),neg(a_+far)])
                for c in range(n):
                    if c not in (a_,b_): S.add_clause(fr+[hp(c),-h[k,c]])
    if sym:   # stems / sph only: all children of a vertex carry isomorphic subtrees, so sort them by label
        ch={}
        for a,b in E: ch.setdefault(a,[]).append(b)
        for p,cs in ch.items():
            for a,b in zip(cs,cs[1:]):
                for l in range(n):
                    for l2 in range(l): S.add_clause([-x[a][l],-x[b][l2]])
    import threading
    if timeout:
        t=threading.Timer(timeout,S.interrupt); t.start(); r=S.solve_limited(expect_interrupt=True); t.cancel()
    else: r=S.solve()
    lab=None
    if r:
        mod=set(l for l in S.get_model() if l>0); lab=[next(l for l in range(n) if x[v][l] in mod) for v in range(n)]
    return r,lab
def check(n,E,lab,rule=True):
    sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','folds'))
    import lib; from verify_rule import obeys
    steps=lib.replay(n,E,[l+1 for l in lab])
    if rule:
        ok,why=obeys(n,steps,33); assert ok,why
    return True
if __name__=='__main__':
    n,E=tree(sys.argv[1:]); rule=not os.environ.get('FREE'); to=float(os.environ.get('TIMEOUT','0')) or None
    r,lab=solve(n,E,rule,to,sym=sys.argv[1] in('stems','sph') and not os.environ.get('NOSYM'))
    if r: check(n,E,lab,rule); print('FOUND',' '.join(sys.argv[1:4]),'n=%d'%n,'labels',' '.join(map(str,lab)),flush=True)
    else: print('NONE' if r is False else 'UNDECIDED',' '.join(sys.argv[1:4]),'n=%d'%n,flush=True)
