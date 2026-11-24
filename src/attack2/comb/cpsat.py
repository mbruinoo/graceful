#!/usr/bin/env python3
"""All-up comb for one multiset S by CP-SAT (ortools); used only for the few multisets on which the
exact-cover search combx is cut off.  The output is a certificate line in the combx format, to be
checked by verify.py; an answer "NONE" means CP-SAT reports infeasibility for every w tried (not used
as evidence anywhere unless stated).
Usage: cpsat.py [-w W | -wmax W] [-t seconds] [-j workers] s1 s2 ...
"""
import sys
from ortools.sat.python import cp_model
def solve(S,w,tlim=600,workers=4):
    S=sorted(S,reverse=True); k=len(S); y=k+sum(S)+w+1
    m=cp_model.CpModel(); R=range(1,y)
    x=[{h:m.NewBoolVar('') for h in R} for i in range(k)]
    L=[{u:m.NewBoolVar('') for u in R} if S[i] else {} for i in range(k)]
    C=[{z:m.NewBoolVar('') for z in R} if S[i] else {} for i in range(k)]
    Wb={z:m.NewBoolVar('') for z in R}
    for i in range(k):
        m.AddExactlyOne(x[i].values())
        if S[i]:
            m.Add(sum(L[i].values())==S[i]); m.Add(sum(C[i].values())==S[i])
            for h in R:
                for u in R:
                    if h+u<y: m.AddBoolOr([x[i][h].Not(),L[i][u].Not(),C[i][h+u]])
                    else: m.AddBoolOr([x[i][h].Not(),L[i][u].Not()])
    for l in R: m.AddExactlyOne([x[i][y-l] for i in range(k)]+[L[i][l] for i in range(k) if S[i]]+[Wb[l]])
    for z in R: m.AddExactlyOne([x[i][z] for i in range(k)]+[C[i][z] for i in range(k) if S[i]]+[Wb[z]])
    m.Add(sum(Wb.values())==w)
    hv=[]
    for i in range(k):
        v=m.NewIntVar(1,y-1,''); m.Add(v==sum(h*x[i][h] for h in R)); hv.append(v)
    for i in range(k-1):
        if S[i]==S[i+1]: m.Add(hv[i]<hv[i+1])
    m.Add(sum((S[i]+2)*hv[i] for i in range(k))==k*y)          # sum of cells = sum of lengths
    s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=tlim; s.parameters.num_workers=workers
    r=s.Solve(m)
    if r in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        hubs=sorted((s.Value(hv[i]),[u for u in R if S[i] and s.Value(L[i][u])]) for i in range(k))
        W=[z for z in R if s.Value(Wb[z])]
        return "S "+' '.join(map(str,S))+" | w %d y %d | "%(w,y)+' '.join("%d:%s"%(h,','.join(map(str,U))) for h,U in hubs)+" | W"+''.join(" %d"%z for z in W)
    return "NONE" if r==cp_model.INFEASIBLE else None
if __name__=="__main__":
    a=sys.argv[1:]; ws=None; wmax=None; t=600; j=4
    while a and a[0].startswith('-'):
        if a[0]=='-w': ws=[int(a[1])]
        elif a[0]=='-wmax': wmax=int(a[1])
        elif a[0]=='-t': t=float(a[1])
        elif a[0]=='-j': j=int(a[1])
        a=a[2:]
    S=list(map(int,a))
    if ws is None: ws=range(0,(max(S) if wmax is None else wmax)+1)
    for w in ws:
        r=solve(S,w,t,j)
        if r and r!="NONE": print(r); break
        print("# S %s w=%d: %s"%(' '.join(map(str,S)),w,"infeasible (CP-SAT)" if r=="NONE" else "time limit"),flush=True)
