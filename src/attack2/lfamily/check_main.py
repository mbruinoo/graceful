#!/usr/bin/env python3
# check_main.py PMAX QMAX -- existence-level check of the Main Theorem with the C++ solver lred:
# for all 1 <= p < q <= QMAX, p <= PMAX and all d with 2d < p, every (gP,gQ) for which the reduced problem
# R(p,q,d) is solvable has gQ = 1 or (gP,gQ) = (1,3); and for p even, q odd there is none at all.
import subprocess,re,sys
PM,QM=int(sys.argv[1]),int(sys.argv[2]); cases=0; feas=0; bad=0; evenodd=0
for p in range(1,PM+1):
    for q in range(p+1,QM+1):
        for d in range(0,(p+1)//2):
            if 2*d>=p: continue
            out=subprocess.run(["./lred",str(p),str(q),str(d)],capture_output=True,text=True).stdout
            pairs=[(int(x),int(y)) for x,y in re.findall(r"\((\d+),(\d+)\)",out)]
            cases+=1; feas+=len(pairs)
            if p%2==0 and q%2==1:
                evenodd+=1
                if pairs: bad+=1; print("EVEN/ODD FEASIBLE",p,q,d,pairs)
            for gp,gq in pairs:
                if not (gq==1 or (gp,gq)==(1,3)): bad+=1; print("EXCEPTION",p,q,d,gp,gq)
    print("p<=%d done: cases %d, feasible hub pairs %d, violations %d"%(p,cases,feas,bad),flush=True)
print("p<=%d, q<=%d: %d triples (p,q,d) with 2d<p; %d feasible (gP,gQ); %d even/odd triples (none feasible); violations %d"%(PM,QM,cases,feas,evenodd,bad))
