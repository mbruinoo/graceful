# print all two-leg deals for (a,b): sequence of (leg, sign) for k=m..1, run-length compressed by leg, and the labelling
import sys
def deals(a,b):
    m=a+b; out=[]
    def go(k,tip,rem,used,hist):
        if k==0: out.append(list(hist)); return
        for l in (0,1):
            if not rem[l]: continue
            for d in (1,-1):
                x=tip[l]+d*k
                if x<0 or x>m or x in used: continue
                t=tip[l]; tip[l]=x; rem[l]-=1; used.add(x); hist.append((l,d,x))
                go(k-1,tip,rem,used,hist)
                hist.pop(); used.discard(x); rem[l]+=1; tip[l]=t
    go(m,[0,0],[a,b],{0},[])
    return out
if __name__=="__main__":
    a,b=int(sys.argv[1]),int(sys.argv[2])
    for h in deals(a,b):
        if a==b and h[0][0]==1: continue
        s=""; 
        runs=[]; 
        for (l,d,x) in h:
            if runs and runs[-1][0]==l: runs[-1][1]+=1
            else: runs.append([l,1])
        print("runs:", " ".join("%s%d"%("AB"[l],c) for l,c in runs))
        print("   A:", [0]+[x for (l,d,x) in h if l==0])
        print("   B:", [0]+[x for (l,d,x) in h if l==1])
