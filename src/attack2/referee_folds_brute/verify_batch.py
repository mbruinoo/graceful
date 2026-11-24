# referee: verify ref outputs: growth placement + literal rule compliance (tape.py)
import sys
from tape import steps, literal_ok
trees=open(sys.argv[1]).read().split('\n'); R=int(sys.argv[3]); ok=bad=skip=0
for line in open(sys.argv[2]):
    p=line.split()
    if 'labels:' not in p: skip+=1; continue
    i=int(p[0]); lab=list(map(int,p[p.index('labels:')+1:]))
    e=list(map(int,trees[i].split())); E=list(zip(e[::2],e[1::2]))
    try:
        st=steps(E,lab); good=literal_ok(len(lab),st,R) if R>=0 else True
    except AssertionError: good=False
    if good: ok+=1
    else: bad+=1; print("BAD",i)
print("verified",ok,"bad",bad,"no-labeling",skip)
