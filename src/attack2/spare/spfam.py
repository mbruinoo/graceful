# spfam.py mode ... -- spiders, every vertex up to symmetry as root.
#  LLL maxL : S(L,L,L), root at distance t from the centre, t = 0..L          (t = L is the leaf)
#  ABC maxleg : every S(a,b,c), 1<=a<=b<=c<=maxleg, every vertex
import sys
def spider(legs):
    e=[]; nx=1; pos={}
    for i,L in enumerate(legs):
        prev=0
        for t in range(1,L+1): e.append((prev,nx)); pos[(i,t)]=nx; prev=nx; nx+=1
    return nx,e,pos
if sys.argv[1]=="LLL":
    for L in range(1,int(sys.argv[2])+1):
        n,e,pos=spider([L,L,L])
        for t in range(0,L+1):
            r=0 if t==0 else pos[(0,t)]
            print("#S(%d,%d,%d)@dist%d %d %d "%(L,L,L,t,n,r)+" ".join("%d %d"%x for x in e))
else:
    M=int(sys.argv[2])
    for a in range(1,M+1):
        for b in range(a,M+1):
            for c in range(b,M+1):
                n,e,pos=spider([a,b,c])
                for r in range(n): print("#S(%d,%d,%d)@v%d %d %d "%(a,b,c,r,n,r)+" ".join("%d %d"%x for x in e))
