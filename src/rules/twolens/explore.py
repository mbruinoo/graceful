# Exploration: spiders (r, 2^k).  Long leg is a zigzag on the numbers NOT in N; N = union of <=nb intervals
# is the set of 2k numbers of the short legs.  Find all (N, pairing) that give a valid deal.
import sys, itertools
def long_labels(W):            # W decreasing; zigzag up, down, up ...
    t=0; out=[]
    for i,w in enumerate(W):
        t = t+w if i%2==0 else t-w
        out.append(t)
    return out
def match(N, P, m, plus):
    # N sorted desc numbers for short legs, P set of free labels.  Return list of (x,d,label2) or None
    N=sorted(N,reverse=True); k=len(N)//2
    res=[]
    def rec(avail, free):
        if not avail: return True
        x=avail[0]
        if x not in free: return False
        for d in avail[1:]:
            for y in ((x-d,x+d) if plus else (x-d,)):
                if y in free and y!=x:
                    res.append((x,d,y))
                    rest=[a for a in avail[1:] if a!=d]
                    if rec(rest, free-{x,y}): return True
                    res.pop()
        return False
    return res if rec(N,frozenset(P)) else None
def solve(r,k,nb=2,plus=False,first=True):
    m=r+2*k; sols=[]
    # interval decompositions of 2k into nb parts
    def comps(total,parts):
        if parts==1: yield (total,); return
        for a in range(1,total-parts+2):
            for c in comps(total-a,parts-1): yield (a,)+c
    for parts in range(1,nb+1):
        for sizes in comps(2*k,parts):
            for starts in itertools.combinations(range(1,m+1),parts):
                ok=True; N=[]
                for i in range(parts):
                    a=starts[i]; b=a+sizes[i]-1
                    if b>m or (i+1<parts and b+1>=starts[i+1]): ok=False;break
                    N+=range(a,b+1)
                if not ok: continue
                Ns=set(N); W=[w for w in range(m,0,-1) if w not in Ns]
                lab=long_labels(W)
                if min(lab)<1 or max(lab)>m or len(set(lab))<r: continue
                P=set(range(1,m+1))-set(lab)
                mt=match(N,P,m,plus)
                if mt:
                    sols.append(([(starts[i],starts[i]+sizes[i]-1) for i in range(parts)],mt))
                    if first: return sols
    return sols
if __name__=="__main__":
    kmax=int(sys.argv[1]); rmax=int(sys.argv[2]); nb=int(sys.argv[3]); plus=len(sys.argv)>4
    for k in range(1,kmax+1):
        row=""
        for r in range(3,rmax+1):
            s=solve(r,k,nb,plus)
            row+= "X" if s else "."
        print(k,row)
