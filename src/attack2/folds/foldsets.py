# foldsets.py N -- from data/brutefolds_<n>.txt (all growth placements, n <= N): for each vocabulary V of non-staircase
# fold types, how many trees (a) have any build using only S and V, (b) reach their true tidy number (cost A) with it.
import sys, itertools
N=int(sys.argv[1]); names={1:'K1',2:'K1*',4:'Kbig',8:'B',16:'F',32:'Fbig'}
rows=[]
for n in range(7,N+1):
    for l in open(f'data/brutefolds_{n}.txt'):
        p=l.split(); rows.append((n,[int(v) for v in p[1:]]))
nc=[r for r in rows if r[1][0]<0]      # non-caterpillars: no build with empty mask
print(f'non-caterpillar trees on 7 <= n <= {N}: {len(nc)} (of {len(rows)})')
def best(v,V):
    c=[v[m] for m in range(64) if (m & ~V)==0 and v[m]>=0]; return min(c) if c else None
print('vocabulary (besides S)            trees with a build   trees reaching tidy_A   smallest n with no build')
for V in sorted(range(1,64),key=lambda V:(bin(V).count('1'),V)):
    has=0; opt=0; first=None
    for n,v in nc:
        b=best(v,V); full=best(v,63)
        if b is not None:
            has+=1
            if b==full: opt+=1
        elif first is None or n<first: first=n
    nm='{'+','.join(names[b] for b in names if V&b)+'}'
    if bin(V).count('1')<=3 or V==63: print(f'  {nm:32s} {has:6d}              {opt:6d}                {first if first else "-"}')
