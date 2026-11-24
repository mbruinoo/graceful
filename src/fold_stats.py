# fold_stats.py trees.txt labels.txt -- classify every step of longest-first builds (output of SHOW=1 runsolve128 n 3)
# step type = where the used foot is / where the fresh foot lands, relative to the longest run of unused labels
import sys, collections
trees=[list(map(int,l.split())) for l in open(sys.argv[1]) if l.strip()]
labs=[list(map(int,l.split(':')[1].split())) for l in open(sys.argv[2]) if l.startswith('labels by vertex')]
assert len(trees)==len(labs)
tot=collections.Counter(); third=[collections.Counter() for _ in range(3)]; exc=[]; maxisl=collections.Counter()
for t,f in zip(trees,labs):
    n=len(f); E=sorted(((abs(f[t[i]]-f[t[i+1]]),f[t[i]],f[t[i+1]]) for i in range(0,len(t),2)),reverse=True)
    assert [e[0] for e in E]==list(range(n-1,0,-1))
    used=[False]*(n+2); used[E[0][1]]=used[E[0][2]]=True; ne=0
    for idx,(k,a,b) in enumerate(E[1:]):
        if used[b]: a,b=b,a
        assert used[a] and not used[b]
        # longest unused run
        best=(0,0,0); i=1
        while i<=n:
            if not used[i]:
                j=i
                while j<n and not used[j+1]: j+=1
                if j-i+1>best[0]: best=(j-i+1,i,j)
                i=j+1
            else: i+=1
        _,lo,hi=best
        src='L' if a<lo else 'R' if a>hi else '?'
        if lo<=b<=hi: dst='l' if b==lo else 'r' if b==hi else 'i'
        else: dst='h'
        if lo==hi and b==lo: dst='l' if src=='R' else 'r'
        ty=src+dst; tot[ty]+=1; third[min(2,3*idx//(n-2))][ty]+=1
        if ty not in('Lr','Rl'): ne+=1
        used[b]=True
    exc.append(ne/(n-2))
N=sum(tot.values())
print('trees',len(trees),'steps',N)
for ty,c in tot.most_common(): print(f'  {ty}: {100*c/N:5.1f}%   early {100*third[0][ty]/sum(third[0].values()):5.1f}  middle {100*third[1][ty]/sum(third[1].values()):5.1f}  late {100*third[2][ty]/sum(third[2].values()):5.1f}')
exc.sort(); print('  share of steps that are not plain across-steps (Lr, Rl): median %.1f%%  min %.1f%%  max %.1f%%'%(100*exc[len(exc)//2],100*exc[0],100*exc[-1]))
