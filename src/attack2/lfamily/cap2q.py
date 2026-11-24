#!/usr/bin/env python3
# cap2q.py [NOT] < scan output -- turns "CAP n deg | edges | v=.." lines (and NOT lines if the argument NOT is given)
# into query lines "n v u1 w1 ..." for ascan2 q / anchq / satanchor.py.
import sys
kinds=("CAP ","NOT ") if len(sys.argv)>1 else ("CAP ",)
for l in sys.stdin:
    if not l.startswith(kinds): continue
    p=l.split('|'); n=int(l.split()[1]); v=int(p[2].split('=')[1])
    print(n,v,' '.join(e.replace('-',' ') for e in p[1].split()))
