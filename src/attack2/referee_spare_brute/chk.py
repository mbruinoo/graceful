# verify ref output against tree file:  chk.py trees out slack
import sys
from common import *
trees=[parse_tree(l) for l in open(sys.argv[1]) if l.strip()]
slack=int(sys.argv[3]); st={}; bad=0
for (name,n,root,e),l in zip(trees,[l for l in open(sys.argv[2]) if l.strip()]):
    t=l.split(); assert t[0]==name,(t[0],name); s=t[1]; st[s]=st.get(s,0)+1
    if s=="FOUND":
        lab=list(map(int,l.split(":")[1].split())); ok,why=check(n,root,e,lab,n+slack)
        if not ok: bad+=1; print("BAD",name,why)
        if len(sys.argv)>4: print(name,"unused label/length",unused(n,e,lab,n+slack))
    elif s!="FOUND" and len(sys.argv)>4: print(name,s)
print(sys.argv[2],st,"bad",bad)
