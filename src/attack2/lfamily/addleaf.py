#!/usr/bin/env python3
# addleaf.py < lines   -- for every non-anchor (T, v) given as "NOT n deg.. | edges | v=.." (ascan/ascan2 scan
# lines) or as "NOT deg.. nodes=.. | n v u1 w1 u2 w2 ..." (ascan2 q output) print the query "n+1 v edges v-new":
# is v still a non-anchor after one more leaf is added AT v?  (Leaf rule / README Lemma 6: every non-anchor v
# having a leaf neighbour arises this way from a non-anchor v of the tree without that leaf.)
import sys
for line in sys.stdin:
    if not line.startswith("NOT "): continue
    parts=line.split("|")
    if len(parts)==3:
        n=int(line.split()[1]); v=int(parts[2].split("=")[1]); ed=[]
        for e in parts[1].split(): x,y=e.split("-"); ed+=[x,y]
    else:
        t=parts[1].split(); n=int(t[0]); v=int(t[1]); ed=t[2:]
    print(" ".join([str(n+1),str(v)]+ed+[str(v),str(n)]))
