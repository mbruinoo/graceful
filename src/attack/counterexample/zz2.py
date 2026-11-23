# zigzag deals of S(2^k): sets O (|O|=k) of {1..2k} with a permutation pi of O such that {b+pi(b)} = complement.
# lists solutions whose O has the fewest "runs" (maximal intervals), to look for a pattern.
import sys, itertools
k=int(sys.argv[1]); N=2*k; S=k*(2*k+1)
if S%3: print("no solution (Lemma 11)"); sys.exit()
sols=[]
def runs(O):
    O=sorted(O); return 1+sum(1 for i in range(1,len(O)) if O[i]!=O[i-1]+1)
def perm(O,I):
    # find pi: backtrack over b in O assigning partner o with b+o in I unused, o unused as image
    O=sorted(O); res=[]
    def bt(i,usedo,useda,acc):
        if i==len(O): res.append(list(acc)); return True
        b=O[i]
        for o in O:
            if o in usedo: continue
            a=b+o
            if a in I and a not in useda:
                usedo.add(o); useda.add(a); acc.append((b,o,a))
                if bt(i+1,usedo,useda,acc): return True
                usedo.discard(o); useda.discard(a); acc.pop()
        return False
    bt(0,set(),set(),[]); return res[0] if res else None
cands=[]
for O in itertools.combinations(range(1,N+1),k):
    if 3*sum(O)!=S: continue
    cands.append((runs(O),O))
cands.sort()
shown=0
for r,O in cands:
    I=set(range(1,N+1))-set(O); p=perm(O,I)
    if p:
        print(r,O,sorted(I)," ".join("%d+%d=%d"%t for t in p)); shown+=1
        if shown>=int(sys.argv[2]): break
