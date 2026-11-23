import sys
from allup_H import feasible
P=int(sys.argv[1])
for p in range(1,P+1):
    for q in range(1,p+1):
        a1=p; m=3+p+q+a1; sols=[]
        for y in range(m-a1, m+1):
            w=a1-(m-y)
            for h in range(1,y):
                for h2 in range(1,y):
                    if h==h2: continue
                    if (p+2)*h+(q+2)*h2!=2*y: continue
                    r=feasible(y,(h,h2),[p,q],w)
                    if r: sols.append((w,y,h,h2,r))
        sols.sort()
        print(p,q,len(sols),' ; '.join('w=%d y=%d hp=%d hq=%d'%s[:4] for s in sols[:6]))
