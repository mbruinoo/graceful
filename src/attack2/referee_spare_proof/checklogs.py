# checklogs.py treefile logfile -- referee re-check (own definition check from referee.py) of FOUND lines at slack 1.
import sys
from referee import defcheck
trees={}
for line in open(sys.argv[1]):
    t=line.split()
    if not t: continue
    name=t[0]; n=int(t[1]); root=int(t[2]); e=list(map(int,t[3:3+2*(n-1)])); trees[name]=(n,root,list(zip(e[::2],e[1::2])))
ok=bad=0; seen=set()
for line in open(sys.argv[2]):
    t=line.split()
    if "FOUND" not in t: bad+=1; continue
    name=t[0]; n,root,edges=trees[name]; labs=list(map(int,t[t.index("labels:")+1:]))
    assert len(labs)==n
    try: ul,uk=defcheck(edges,dict(enumerate(labs)),root,1); ok+=1; seen.add(name)
    except AssertionError as ex: bad+=1; print("BAD",name,ex)
print("%s: trees in file %d, FOUND lines passing the definition at slack 1: %d, distinct trees covered %d, bad/non-FOUND %d"%(sys.argv[2].split('/')[-1],len(trees),ok,len(seen),bad))
