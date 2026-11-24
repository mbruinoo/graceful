# Cross-check gs.c against naive permutation brute force for all trees n<=8, every vertex.
import itertools, subprocess, networkx as nx, sys
N=int(sys.argv[1]) if len(sys.argv)>1 else 8
lines=[];ref=[]
for n in range(2,N+1):
    for T in nx.nonisomorphic_trees(n):
        E=list(T.edges())
        G=[False]*n; A=[False]*n
        for perm in itertools.permutations(range(1,n+1)):
            d=sorted(abs(perm[a]-perm[b]) for a,b in E)
            if d!=list(range(1,n)): continue
            v=perm.index(1); G[v]=True
            # growth: edges of length>=k connected for every k
            ok=True
            for k in range(1,n):
                H=nx.Graph([e for e in E if abs(perm[e[0]]-perm[e[1]])>=k])
                if not nx.is_connected(H): ok=False;break
            if ok: A[v]=True
        for v in range(n):
            lines.append(f"{n} {v} "+" ".join(f"{a} {b}" for a,b in E)); ref.append((int(G[v]),int(A[v])))
out=subprocess.run(["./gs"],input="\n".join(lines)+"\n",capture_output=True,text=True).stdout.split("\n")
bad=sum(1 for o,r in zip(out,ref) if tuple(map(int,o.split()))!=r)
print(f"validate gs.c vs permutation brute force, all trees 2<=n<={N}, every vertex: {len(ref)} cases, mismatches {bad}")
print("0-centred-not-anchor cases:",sum(1 for r in ref if r==(1,0)), " anchor-not-0:",sum(1 for r in ref if r==(0,1)))
