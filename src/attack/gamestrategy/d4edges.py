import sys
from explore import d4trees, build
n=int(sys.argv[1]); full=len(sys.argv)>2
for a in d4trees(n):
    if not full and min(a)==0: continue
    par,_=build(a)
    print(' '.join(f"{p} {v}" for v,p in enumerate(par) if p>=0))
