# equal hubs at odd labels 1,3,..,2d-1; each hub's lengths an AP of difference d; list start vectors
import sys
a=int(sys.argv[1]); d=int(sys.argv[2])
H=[2*i+1 for i in range(d)]; y=d*(a+2)
T={y-h for h in H}; C=set(range(1,y))-set(H); D=set(range(1,y))-T
def rec(i,usedU,usedC,acc):
    if i==d:
        rest=D-usedU
        if rest==C-usedC: print('d=%d a=%d y=%d starts=%s wild=%s'%(d,a,y,acc,sorted(rest)))
        return
    h=H[i]
    for s in range(1,y):
        U={s+j*d for j in range(a)}
        if not U<=D or U&usedU: continue
        Cc={u+h for u in U}
        if not Cc<=C or Cc&usedC: continue
        rec(i+1,usedU|U,usedC|Cc,acc+[s])
rec(0,set(),set(),[])
