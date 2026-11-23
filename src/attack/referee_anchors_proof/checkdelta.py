# least l making v an anchor of L(l;h1,h2), by gen; compare with h1/2 when h1 even < h2 odd
import sys, subprocess
from fam import *
H=int(sys.argv[1]); LM=int(sys.argv[2])
cases=[(l,h1,h2) for h1 in range(1,H+1) for h2 in range(h1,H+1) for l in range(0,LM+1)]
out=subprocess.run(["./gen","0"],input="\n".join(line(*L(*c)) for c in cases)+"\n",capture_output=True,text=True).stdout.split("\n")
res={c:o.startswith("YES") for c,o in zip(cases,out)}
bad=0; npar=0; mono=0
for h1 in range(1,H+1):
    for h2 in range(h1,H+1):
        ys=[res[(l,h1,h2)] for l in range(LM+1)]
        if any(ys[i] and not ys[i+1] for i in range(LM)): mono+=1
        least=ys.index(True) if True in ys else None
        par=(h1%2==0 and h2%2==1 and h1<h2)
        if par:
            npar+=1
            exp=h1//2 if h1//2<=LM else None
            if least!=exp: bad+=1; print("MISMATCH",h1,h2,least)
        # non-anchor pairs for fixed l>=2 should be exactly parity pairs with h1>=2l+2
        for l in range(2,LM+1):
            if (not ys[l]) != (par and h1>=2*l+2): bad+=1; print("PAIR MISMATCH",l,h1,h2,ys[l])
print("H",H,"parity pairs",npar,"mismatches",bad,"monotonicity violations",mono)
