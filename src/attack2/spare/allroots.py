# allroots.py n  -- every (tree, vertex) pair on n vertices as spare.cpp input (trees from ../../gentrees.py)
import sys, subprocess
n=int(sys.argv[1])
for i,l in enumerate(subprocess.run([sys.executable,"../../gentrees.py",str(n)],capture_output=True,text=True).stdout.split("\n")):
    if not l.strip(): continue
    for r in range(n): print("#t%d@%d %d %d %s"%(i,r,n,r,l))
