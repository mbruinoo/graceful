# trace.py -- print a growth build step by step on the tape (referee tool). usage: python3 trace.py "edges" "labels"
import sys
el=list(map(int,sys.argv[1].split())); E=list(zip(el[0::2],el[1::2])); lab=list(map(int,sys.argv[2].split())); n=len(lab)
br={abs(lab[u]-lab[v]):tuple(sorted((lab[u],lab[v]))) for u,v in E}
assert sorted(br)==list(range(1,n)) and sorted(lab)==list(range(1,n+1)) and br[n-1]==(1,n)
used={1,n}
for t in range(n-2,0,-1):
    a,b=br[t]; assert (a in used)!=(b in used); x,y=(a,b) if b in used else (b,a)
    tape=''.join('x' if c==x else 'Y' if c==y else '#' if c in used else '.' for c in range(1,n+1))
    print(f't={t:2d}  {tape}'); used.add(x)
