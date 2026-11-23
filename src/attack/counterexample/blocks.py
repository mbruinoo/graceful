# Block tilings.  A block (c,t): O-interval [c,c+2t] and I-interval [2c+t,2c+3t].
# For a prefix length t0 (even), find all N=2k <= NMAX such that (t0,N] is tiled exactly by blocks.
import sys
sys.setrecursionlimit(100000)
NMAX=int(sys.argv[1])
def ends(t0,NMAX):
    res={}
    occ=[0]*(3*NMAX+5)
    def rec(p,hi,blocks,cnt):
        # p: smallest position > t0 possibly uncovered; hi: largest covered position
        while p<=hi and occ[p]: p+=1
        if p>hi:
            if hi>t0 and hi%2==0 and hi not in res: res[hi]=list(blocks)
            # may also continue with a new block starting at p=hi+1
        if p>NMAX: return
        if cnt[0]>200000: return
        cnt[0]+=1
        t=0
        while True:
            if p+2*t>NMAX or 2*p+3*t>NMAX: break
            if any(occ[x] for x in range(p,p+2*t+1)): break
            if not any(occ[x] for x in range(2*p+t,2*p+3*t+1)) and 2*p+t>p+2*t:
                for x in range(p,p+2*t+1): occ[x]=1
                for x in range(2*p+t,2*p+3*t+1): occ[x]=1
                blocks.append((p,t)); rec(p+1,max(hi,2*p+3*t),blocks,cnt); blocks.pop()
                for x in range(p,p+2*t+1): occ[x]=0
                for x in range(2*p+t,2*p+3*t+1): occ[x]=0
            t+=1
    rec(t0+1,t0,[],[0])
    return res
if __name__=="__main__":
    for t0 in range(0,int(sys.argv[2])+1,2):
        r=ends(t0,NMAX)
        print("prefix k'=%d -> k in"%(t0//2), sorted(x//2 for x in r))
