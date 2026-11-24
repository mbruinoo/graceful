# referee: recompute cost A/B of stored labelings (format: "T idx ... labels: ...") from the definition
import sys
from tape import steps
trees=open(sys.argv[1]).read().split('\n'); mode=sys.argv[3]
for line in open(sys.argv[2]):
    p=line.split(); i=int(p[1]); lab=list(map(int,p[p.index('labels:')+1:])); n=len(lab)
    e=list(map(int,trees[i].split()))
    try: st=steps(list(zip(e[::2],e[1::2])),lab)
    except AssertionError as ex: print(i,"NOT GROWTH"); continue
    used={1,n}; cost=0
    for x,y,L in st:
        lo=hi=x
        while lo-1>=1 and lo-1 not in used: lo-=1
        while hi+1<=n and hi+1 not in used: hi+=1
        r=(x-lo) if y>x else (hi-x); stair=(r==0)
        if mode=='A':
            runs=[];c=1
            while c<=n:
                if c not in used:
                    s=c
                    while c<=n and c not in used: c+=1
                    runs.append((c-s,-s,s))
                else: c+=1
            if max(runs)[2]!=lo: stair=False
        cost+= not stair; used.add(x)
    claimed=[q for q in p if q.startswith('ub=')][0]
    print(i,n,"recomputed",cost,claimed)
