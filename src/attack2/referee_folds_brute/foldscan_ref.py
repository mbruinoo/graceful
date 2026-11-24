# referee: location statistics of non-staircase steps (cost A) in stored builds
import sys
from tape import steps
trees=open(sys.argv[1]).read().split('\n'); res=open(sys.argv[2]).read().split('\n')
D={}; tot=[0,0]; ns=[0,0]; types={}; thirds=[0,0,0]; thirdsall=[0,0,0]; Bthird=[0,0,0]; Fleaf=[0,0]; K1deg3=[0,0]; leafrate=[[0,0],[0,0]]
for line in res:
    p=line.split()
    if 'labels:' not in p: continue
    i=int(p[1]); lab=list(map(int,p[p.index('labels:')+1:])); n=len(lab)
    e=list(map(int,trees[i].split())); adj={v:set() for v in range(n)}
    for u,v in zip(e[::2],e[1::2]): adj[u].add(v); adj[v].add(u)
    cell={lab[v]:v for v in range(n)}
    st=steps(list(zip(e[::2],e[1::2])),lab); used={1,n}
    for k,(x,y,L) in enumerate(st):
        lo=x; hi=x
        while lo-1>=1 and lo-1 not in used: lo-=1
        while hi+1<=n and hi+1 not in used: hi+=1
        runs=[]; c=1
        while c<=n:
            if c not in used:
                s=c
                while c<=n and c not in used: c+=1
                runs.append((c-s,-s,s))
            else: c+=1
        main=max(runs)[2]
        r=(x-lo) if y>x else (hi-x); cc=(hi-lo)-r
        stair = (main==lo and r==0)
        if hi==lo and main!=lo: typ='F'
        elif main!=lo: typ='other-run'
        elif r==0: typ='S'
        elif cc==0: typ='B'
        else: typ='K%d'%min(r,cc)
        if stair: typ='S'
        pv=cell[y]; xv=cell[x]; nl=sum(1 for w in adj[pv] if len(adj[w])>1)
        g=1 if nl>=3 else 0; tot[g]+=1; ns[g]+= (not stair)
        th=min(2,3*k//len(st)); thirdsall[th]+=1; thirds[th]+=(not stair)
        lf=1 if len(adj[xv])==1 else 0; leafrate[lf][0]+=1; leafrate[lf][1]+=(not stair)
        if not stair:
            types[typ]=types.get(typ,0)+1
            if typ=='B': Bthird[th]+=1
            if typ=='F': Fleaf[0]+=1; Fleaf[1]+=lf
            if typ=='K1': K1deg3[0]+=1; K1deg3[1]+=g; sub=('across' if r==1 else 'back'); D.setdefault(sub,[0,0,0]); D[sub][0]+=1; D[sub][1]+=g; D[sub][2]+=(len(adj[pv])>=3)
        used.add(x)
print("steps",sum(tot),"nonstair",sum(ns))
print("rate parent>=3 nonleaf nbrs: %.3f  else %.3f"%(ns[1]/tot[1],ns[0]/tot[0]))
print("rate fresh leaf %.3f nonleaf %.3f"%(leafrate[1][1]/leafrate[1][0],leafrate[0][1]/leafrate[0][0]))
print("thirds",[round(a/b,3) for a,b in zip(thirds,thirdsall)])
print("types",types); print("B thirds",Bthird,"F leaf",Fleaf,"K1 parent deg>=3",K1deg3)
print('K1 split [count, nonleafnbr>=3, deg>=3]',D)
