import sys
from explore import *
a=tuple(int(x) for x in sys.argv[1].split(','))
rootkind=sys.argv[2]  # c or h<i>
lim=int(sys.argv[3]) if len(sys.argv)>3 else 20
par,kind=build(a)
root=0 if rootkind=='c' else [v for v in range(len(par)) if kind[v]==('h',int(rootkind[1:]))][0]
sols=solve(par,root,lim)
hubs=[v for v in range(len(par)) if kind[v]!='c' and kind[v][0]=='h']
seen=set()
for lab in sols:
    desc=[]
    for h in hubs:
        lv=sorted(lab[v] for v in range(len(par)) if par[v]==h)
        desc.append((lab[h],tuple(lv)))
    desc.sort(reverse=True)
    key=(lab[0],tuple(desc))
    if key in seen: continue
    seen.add(key)
    print('c=%d'%lab[0],'  '.join('%d:%s'%(w,list(l)) for w,l in desc))
print(len(seen))
