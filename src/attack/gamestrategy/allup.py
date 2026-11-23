# All-up comb solutions: root hub at 0 (a[0] leaves, wildcards), centre at y, hubs at h_i<y, every leaf of hub i at h_i+u.
import sys, itertools
def allup(a, limit=5, yrange=None):
    k=len(a); m=k+sum(a); out=[]
    others=a[1:]
    for y in (yrange or range(m, m-a[0]-1, -1)):
        w_in=a[0]-(m-y)   # wildcards inside
        for H in itertools.combinations(range(1,y), k-1):
            for perm in set(itertools.permutations(others)):
                # necessary: sum (a_i+2)h_i=(k-1)y
                if sum((ai+2)*h for ai,h in zip(perm,H))!=(k-1)*y: continue
                hubs=(0,)+H; cap=[w_in]+list(perm)
                T={y-h for h in H}; used=set(hubs); assign={}
                def rec(u):
                    while u>=1 and u in T: u-=1
                    if u==0: return True
                    for i,h in enumerate(hubs):
                        if cap[i]>0 and h+u<y and (h+u) not in used and y-h>u:
                            cap[i]-=1; used.add(h+u); assign[u]=i
                            if rec(u-1): return True
                            cap[i]+=1; used.discard(h+u); del assign[u]
                    return False
                if rec(y-1):
                    out.append((y,hubs,[sorted(u for u in assign if assign[u]==i) for i in range(k)]))
                    if len(out)>=limit: return out
    return out
if __name__=='__main__':
    a=tuple(int(x) for x in sys.argv[1].split(','))
    for y,hubs,U in allup(a, int(sys.argv[2]) if len(sys.argv)>2 else 5):
        print('y=%d'%y, ' | '.join('h=%d U=%s'%(h,u) for h,u in zip(hubs,U)))
