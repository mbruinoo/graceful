# equal hubs: all-up solutions in which each hub's length set is an AP with difference d=k-1 (residue dealing)
import sys, itertools
a=int(sys.argv[1]); k=int(sys.argv[2]); a1=int(sys.argv[3]) if len(sys.argv)>3 else a
d=k-1; m=k+a*(k-1)+a1
for y in range(m, m-a1-1, -1):
    if ((k-1)*y)%(a+2): continue
    S=(k-1)*y//(a+2); w=a1-(m-y)
    for H in itertools.combinations(range(1,y),k-1):
        if sum(H)!=S: continue
        T={y-h for h in H}; C=set(range(1,y))-set(H); D=set(range(1,y))-T
        # choose start s_h for each hub
        def rec(i,usedU,usedC,acc):
            if i==len(H):
                rest=D-usedU
                if rest==C-usedC and len(rest)==w: print('y=%d H=%s starts=%s wild=%s'%(y,H,acc,sorted(rest)))
                return
            h=H[i]
            for s in range(1,y):
                U={s+j*d for j in range(a)}
                if not U<=D or U&usedU: continue
                Cc={u+h for u in U}
                if not Cc<=C or Cc&usedC: continue
                rec(i+1,usedU|U,usedC|Cc,acc+[s])
        rec(0,set(),set(),[])
