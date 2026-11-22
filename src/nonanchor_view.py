# Show each non-anchor vertex as the multiset of branches hanging off it (each branch as a nested-paren rooted tree).
import sys, subprocess, re, collections
def enc(adj,v,pa): return "("+"".join(sorted(enc(adj,u,v) for u in adj[v] if u!=pa))+")"
def size(s): return s.count("(")
for n in range(6,int(sys.argv[1])+1):
    trees=subprocess.run(["python3","gentrees.py",str(n)],capture_output=True,text=True).stdout
    out=subprocess.run(["./anchors",str(n),"v"],input=trees,capture_output=True,text=True).stdout
    rows=set()
    for line in out.splitlines():
        if "non-anchors" not in line: continue
        e,bad=line.split(" | non-anchors:"); x=list(map(int,e.split())); adj=collections.defaultdict(list)
        for i in range(0,len(x),2): adj[x[i]].append(x[i+1]); adj[x[i+1]].append(x[i])
        for m in re.finditer(r"(\d+)\(deg",bad):
            v=int(m.group(1)); br=sorted((enc(adj,u,v) for u in adj[v]),key=lambda s:(size(s),s))
            rows.add((len(br),tuple(size(b) for b in br),"  ".join(br)))
    print(f"n={n}: {len(rows)} non-anchor vertex types")
    if n<=int(sys.argv[2]):
        for r in sorted(rows): print("   deg",r[0],"branch sizes",r[1],"  ",r[2])
    else:
        c=collections.Counter((r[0],r[1]) for r in rows)
        print("   by (deg, branch sizes):",dict(sorted(c.items())))
