# streaming version: all trees on n vertices; vertices of degree >= mindeg; node limit per search (TIMEOUT reported)
import sys, subprocess, networkx as nx
from collections import Counter
from fam import line
n=int(sys.argv[1]); mindeg=int(sys.argv[2]); limit=sys.argv[3]
p=subprocess.Popen(["./gen",limit],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
import threading
degs=[]; c=Counter(); to=[0]; tot=[0]; maxnodes=[0]
def reader():
    i=0
    for o in p.stdout:
        d=degs[i]; i+=1; tot[0]+=1
        s=o.split(); maxnodes[0]=max(maxnodes[0],int(s[1]))
        if s[0]=="NO": c[min(d,4)]+=1
        elif s[0]=="TIMEOUT": to[0]+=1
th=threading.Thread(target=reader); th.start()
nt=0
for T in nx.nonisomorphic_trees(n):
    nt+=1; e=list(T.edges())
    for v in range(n):
        d=T.degree(v)
        if d>=mindeg: degs.append(d); p.stdin.write(line(n,e,v)+"\n")
p.stdin.close(); th.join()
print(n,"trees",nt,"vertices searched",tot[0],"(degree >=",mindeg,") non-anchors by degree(1,2,3,>=4)",[c[1],c[2],c[3],c[4]],"timeouts",to[0],"max nodes",maxnodes[0])
