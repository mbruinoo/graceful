# Shape search: each leg = one free first label f, then a tail of L-1 vertices that zigzags between
# two contiguous blocks of labels (start block of size A=ceil((L-1)/2), other block of size B=floor((L-1)/2)).
# A "shape" (word over s/A/B laying out the singles and the blocks along 1..m, pairing of blocks, which f goes
# with which tail) does not depend on L; we look for shapes that give a valid deal for every L tested.
# Usage: shapes.py k parity(0 even L /1 odd L) Lmax
import sys, itertools
k=int(sys.argv[1]); par=int(sys.argv[2]); Lmax=int(sys.argv[3])
Ls=[L for L in range(4,Lmax+1) if L%2==par]
def words():
    if par==1: base='s'*k+'A'*(2*k)
    else: base='s'*k+'A'*k+'B'*k
    return sorted(set(itertools.permutations(base)))
def layout(word,L):
    A=(L-1+1)//2; B=(L-1)//2
    pos=1; S=[];Ab=[];Bb=[]
    for ch in word:
        if ch=='s': S.append(pos); pos+=1
        elif ch=='A': Ab.append((pos,pos+A-1)); pos+=A
        else: Bb.append((pos,pos+B-1)); pos+=B
    return S,Ab,Bb
def check(L,S,Ab,Bb,pairs,fa):
    # pairs: list of (index of start block, index of other block) ; fa: perm, leg i uses single S[fa[i]]
    m=k*L; edges=set()
    for i,(a,b) in enumerate(pairs):
        st=Ab[a]; ot=Bb[b] if par==0 else Ab[b]
        f=S[fa[i]]
        if st[0]>ot[1]: v=st[1]; d=st[1]-ot[0]     # start block high
        else: v=st[0]; d=ot[1]-st[0]
        g=abs(f-v)
        if not (f>g>d): return False
        es=[f,g]+list(range(d,d-(L-2),-1))
        if es[-1]<1: return False
        for e in es:
            if e in edges: return False
            edges.add(e)
    return len(edges)==m
def pairings():
    if par==0:
        for p in itertools.permutations(range(k)): yield [(i,p[i]) for i in range(k)]
    else:
        idx=list(range(2*k))
        def rec(rem):
            if not rem: yield []; return
            a=rem[0]
            for b in rem[1:]:
                r2=[x for x in rem if x not in (a,b)]
                for rest in rec(r2):
                    yield [(a,b)]+rest; yield [(b,a)]+rest
        yield from rec(idx)
good=[]
P=list(pairings()); F=list(itertools.permutations(range(k)))
for w in words():
    lay={L:layout(w,L) for L in Ls}
    for pr in P:
        for fa in F:
            if all(check(L,*lay[L],pr,fa) for L in Ls[:2]) and all(check(L,*lay[L],pr,fa) for L in Ls):
                good.append((''.join(w),pr,fa))
print(f"k={k} parity={par} Ls={Ls}: shapes working for all: {len(good)}")
for g in good[:40]: print(g)
