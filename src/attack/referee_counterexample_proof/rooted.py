# Referee's own rooted-tree generator (nested tuples, children sorted non-increasing) and helpers.
import functools, itertools
@functools.lru_cache(None)
def rooted(k):
    if k==1: return [()]
    res=[]
    # forests of total size k-1 as multisets of rooted trees
    def forests(rem,maxsize,maxidx):
        # yield tuples of trees, ordered by (size desc, index desc)
        if rem==0: yield (); return
        for s in range(min(rem,maxsize),0,-1):
            L=rooted(s)
            top=len(L)-1 if s<maxsize else min(maxidx,len(L)-1)
            for i in range(top,-1,-1):
                for rest in forests(rem-s,s,i): yield (L[i],)+rest
    for f in forests(k-1,k-1,10**18): res.append(f)
    return res
def edges(t,extra=0):
    E=[]; cnt=[1]
    def rec(t,v):
        for c in t:
            w=cnt[0]; cnt[0]+=1; E.append((v,w)); rec(c,w)
    rec(t,0)
    for _ in range(extra):
        E.append((0,cnt[0])); cnt[0]+=1
    return cnt[0],E
def line(t,extra=0):
    n,E=edges(t,extra); return str(n)+" "+" ".join("%d %d"%e for e in E)
if __name__=="__main__":
    print([len(rooted(k)) for k in range(1,16)])
