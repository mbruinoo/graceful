from indep import R
bad=0;cnt=0
for N in range(4,17):
  for p in range(1,N):
    for q in range(p+1,N):
      d=N-p-q-2
      if d<0 or 2*d>=p: continue
      for (P,Q) in R(p,q,d):
        cnt+=1
        if not (Q==1 or (P,Q)==(1,3)): bad+=1; print("VIOLATION",p,q,d,P,Q)
        if p%2==0 and q%2==1: bad+=1; print("PARITY",p,q,d,P,Q)
print("feasible pairs",cnt,"violations",bad)
