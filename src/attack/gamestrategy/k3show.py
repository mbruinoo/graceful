import sys
from allup_H import feasible
h,h2=int(sys.argv[1]),int(sys.argv[2])
for arg in sys.argv[3:]:
    P,Q=map(int,arg.split(','))   # size at hub h is P, at h2 is Q
    y2=(P+2)*h+(Q+2)*h2
    y=y2//2; w=y-3-P-Q
    r=feasible(y,(h,h2),[P,Q],w) if y2%2==0 and w>=0 else None
    print('sizes',P,Q,'y=%d w=%d'%(y,w), r)
