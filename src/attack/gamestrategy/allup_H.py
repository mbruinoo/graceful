# for equal hubs a^k (root size a1), list which (y,H') admit all-up solutions
import sys, itertools
def feasible(y,H,caps,w_in):
    hubs=(0,)+tuple(H); cap=[w_in]+list(caps)
    T={y-h for h in H}; used=set(hubs); assign={}
    def rec(u):
        while u>=1 and u in T: u-=1
        if u==0: return True
        for i,h in enumerate(hubs):
            if cap[i]>0 and h+u<y and (h+u) not in used:
                cap[i]-=1; used.add(h+u); assign[u]=i
                if rec(u-1): return True
                cap[i]+=1; used.discard(h+u); del assign[u]
        return False
    if rec(y-1): return [sorted(u for u in assign if assign[u]==i) for i in range(len(hubs))]
    return None
if __name__=='__main__':
    a=int(sys.argv[1]); k=int(sys.argv[2]); a1=int(sys.argv[3]) if len(sys.argv)>3 else a
    m=k+a*(k-1)+a1
    for y in range(m, m-a1-1, -1):
        if ((k-1)*y)%(a+2): continue
        S=(k-1)*y//(a+2)
        for H in itertools.combinations(range(1,y),k-1):
            if sum(H)!=S: continue
            r=feasible(y,H,[a]*(k-1),a1-(m-y))
            if r: print('y=%d H=%s'%(y,H), r)
