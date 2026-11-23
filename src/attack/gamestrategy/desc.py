import sys
from collections import Counter
for line in sys.stdin:
    t=list(map(int,line.split())); par={}
    for i in range(0,len(t),2): par[t[i+1]]=t[i]
    ch=Counter(par.values())
    print(sorted((ch.get(v,0) for v in par if par[v]==0),reverse=True))
