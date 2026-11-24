#!/usr/bin/env python3
# ext3.py L < NA-lines   -- for every non-anchor (T', c) listed by "NOT n deg.. | edges | v=c" (ascan) or
# "NA n ... | edges | v=c" (attack/anchors/anch) build T = T' + new vertex v joined to c + L leaves at v and
# print an anchq query line "n v edges" asking whether v (degree L+1) is an anchor of T.
import sys
L=int(sys.argv[1])
for line in sys.stdin:
    if not (line.startswith("NA ") or line.startswith("NOT ")): continue
    parts=line.split("|"); n=int(line.split()[1]); edges=parts[1].split(); c=int(parts[2].split("=")[1])
    v=n; out=[str(n+1+L),str(v)]
    for e in edges: x,y=e.split("-"); out+=[x,y]
    out+=[str(c),str(v)]
    for i in range(L): out+=[str(v),str(n+1+i)]
    print(" ".join(out))
