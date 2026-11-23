# Structured trees with nlo <= n <= nhi, one per line "n u v ...", preceded on stderr by nothing.
# usage: gen_struct.py family nlo nhi
#   eq     : k >= 3 copies of every rooted tree B (2 <= |B| <= 8) hung on a centre           n = k|B|+1
#   eq2    : two adjacent centres, each carrying k >= 2 copies of B (2 <= |B| <= 7)          n = 2k|B|+2
#   eqp    : as eq, plus one extra pendant path of length 1..3 at the centre
#   sym    : spherically symmetric trees, every branching sequence with d_0 >= 2 (d_0 >= 3 if depth 1), depth >= 2
#   spider : spiders with k >= 3 legs, all of length L or L+-1 mixes: legs (L^a,(L+1)^b)
#   comb   : path of p vertices, each carrying a pendant copy of B (2 <= |B| <= 5)   ("generalised combs")
import sys, functools
from fam import line
fam,nlo,nhi=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
@functools.lru_cache(None)
def rooted(k):
    if k==1: return ("()",)
    out=set()
    def parts(rem,maxs,acc):
        if rem==0: out.add("("+"".join(acc)+")"); return
        for s in range(min(rem,maxs),0,-1):
            for t in rooted(s):
                if acc and (len(acc[-1])//2==s) and t>acc[-1]: continue
                parts(rem-s,s,acc+[t])
    parts(k-1,k-1,[])
    return tuple(sorted(out))
path=lambda k:"("*k+")"*k
out=[]
def put(s):
    n=len(s)//2
    if nlo<=n<=nhi: out.append(s)
if fam=="eq":
    for b in range(2,9):
        for B in rooted(b):
            for k in range(3,(nhi-1)//b+1): put("("+B*k+")")
elif fam=="eqp":
    for b in range(2,8):
        for B in rooted(b):
            for k in range(3,(nhi-1)//b+1):
                for r in (1,2,3): put("("+B*k+path(r)+")")
elif fam=="eq2":
    for b in range(2,8):
        for B in rooted(b):
            for k in range(2,(nhi-2)//(2*b)+1): put("("+B*k+"("+B*k+"))")
elif fam=="sym":
    def rec(seq,size,width):
        # size = vertices so far, width = vertices on last level
        if len(seq)>=2 and nlo<=size<=nhi:
            def build(i): return "("+(build(i+1)*seq[i] if i<len(seq) else "")+")"
            out.append(build(0))
        for d in range(1,nhi):
            if size+width*d>nhi: break
            if not seq and d<2: continue
            rec(seq+[d],size+width*d,width*d)
    rec([],1,1)
elif fam=="spider":
    for L in range(1,nhi):
        for a in range(0,nhi):
            for b in range(0,nhi):
                if a+b<3: continue
                n=1+a*L+b*(L+1)
                if n>nhi: break
                put("("+path(L)*a+path(L+1)*b+")")
elif fam=="comb":
    for b in range(2,6):
        for B in rooted(b):
            for p in range(3,nhi//(b+1)+1):
                s=""
                for i in range(p): s="("+B+s+")"
                put(s)
seen=set()
for s in out:
    if s in seen: continue
    seen.add(s); print(line(s))
