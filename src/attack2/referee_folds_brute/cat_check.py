# referee: tidy==0 iff caterpillar, on ref outputs
import sys
for n in range(4,19):
    try: res=[l.split() for l in open(f"{sys.argv[1]}{n}.out")]
    except FileNotFoundError: continue
    bad=0
    for line,r in zip(open(f"t{n}.txt"),res):
        a=list(map(int,line.split())); adj={i:set() for i in range(n)}
        for u,v in zip(a[::2],a[1::2]): adj[u].add(v); adj[v].add(u)
        inner=[v for v in adj if len(adj[v])>1]
        cat = all(sum(1 for w in adj[v] if len(adj[w])>1)<=2 for v in inner)  # derived tree is a path (tree => max deg<=2)
        if cat != (r[2]=='0'): bad+=1
    print(sys.argv[1],n,"mismatches",bad)
