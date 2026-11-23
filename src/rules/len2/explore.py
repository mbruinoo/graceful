# Enumerate all zigzag deals for k legs of length 2 (set O, bijection d on O with {o+d(o)} = complement of O)
# and print those whose map o -> d(o) has the fewest affine pieces.  Usage: explore.py k [howmany]
import sys
k=int(sys.argv[1]); show=int(sys.argv[2]) if len(sys.argv)>2 else 5
m=2*k; target=k*(2*k+1)//3
sols=[]
def pieces(O,d):
    O=sorted(O); p=1
    for i in range(2,len(O)):
        if (O[i]-O[i-1],d[O[i]]-d[O[i-1]])!=(O[i-1]-O[i-2],d[O[i-1]]-d[O[i-2]]): p+=1
    return p
def solve_for(O):
    Os=sorted(O); I=set(range(1,m+1))-set(O); d={}; used=set(); sums=set()
    def rec(i):
        if i==len(Os): sols.append((pieces(Os,d),tuple(Os),dict(d))); return
        o=Os[i]
        for x in Os:
            if x in used: continue
            s=o+x
            if s>m: break
            if s in I and s not in sums:
                used.add(x); sums.add(s); d[o]=x
                rec(i+1)
                used.discard(x); sums.discard(s); del d[o]
    rec(0)
def subsets(start,left,s,cur):
    if left==0:
        if s==target: solve_for(cur)
        return
    for v in range(start,m+1):
        if s+v*left+left*(left-1)//2>target: break
        cur.append(v); subsets(v+1,left-1,s+v,cur); cur.pop()
if k*(2*k+1)%3==0: subsets(1,k,0,[])
print("k",k,"solutions",len(sols))
sols.sort(key=lambda t:(t[0],t[1]))
for p,O,d in sols[:show]:
    print(p,"O=",O," d=",[d[o] for o in O]," sums=",[o+d[o] for o in O])
