import sys
from explore import d4trees
from allup import allup
N=int(sys.argv[1]); lo=int(sys.argv[2])
for n in range(lo,N+1):
    bad=[]; tot=0
    for a in d4trees(n):
        if min(a)==0 or len(a)<3: continue
        tot+=1
        if not allup(a,1): bad.append(a)
    print(n,tot,'no all-up comb from largest hub:',bad,flush=True)
