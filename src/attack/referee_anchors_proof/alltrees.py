# all trees on n vertices, every vertex: anchor or not (gen).  Prints counts by degree.
import sys, subprocess, networkx as nx
from collections import Counter
from fam import line
for n in range(int(sys.argv[1]),int(sys.argv[2])+1):
    lines=[];deg=[];tid=[]
    for i,T in enumerate(nx.nonisomorphic_trees(n)):
        e=list(T.edges())
        for v in range(n): lines.append(line(n,e,v)); deg.append(T.degree(v)); tid.append(i)
    out=subprocess.run(["./gen","0"],input="\n".join(lines)+"\n",capture_output=True,text=True).stdout.split("\n")
    c=Counter(); hasanchor=set()
    for o,d,t in zip(out,deg,tid):
        if o.startswith("NO"): c[min(d,4)]+=1
        else: hasanchor.add(t)
    print(n,"vertices",len(lines),"non-anchors",sum(c.values()),"by degree(1,2,3,>=4)",[c[1],c[2],c[3],c[4]],"trees without anchor",i+1-len(hasanchor),flush=True)
