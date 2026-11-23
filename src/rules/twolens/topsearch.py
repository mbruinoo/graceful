# X = top block (numbers and labels B+1..m, B=r+k).  Long leg: zigzag on [1,B] minus D.  D = k-subset inside a window of width k+extra.
import sys, itertools
from explore import long_labels, match
def topsearch(r,k,extra,all_=False):
    m=r+2*k; B=r+k; out=[]
    X=list(range(B+1,m+1))
    for width in range(k,k+extra+1):
      for a in range(1,B-width+2):
        for mid in itertools.combinations(range(a+1,a+width-1),k-2) if k>=2 else [()]:
            D=[a]+list(mid)+([a+width-1] if k>=2 else [])
            if k==1 and width>1: continue
            Ds=set(D); W=[w for w in range(B,0,-1) if w not in Ds]
            lab=long_labels(W)
            if min(lab)<1 or len(set(lab))<r: continue
            P=set(range(1,m+1))-set(lab)
            mt=match(X+D,P,m,False)
            if mt:
                out.append((a,[d-a for d in D],sorted(P-set(X)),mt))
                if not all_: return out
    return out
if __name__=="__main__":
    k=int(sys.argv[1]); extra=int(sys.argv[3])
    for r in eval(sys.argv[2]):
        s=topsearch(r,k,extra,True)
        print("r",r,"B",r+k)
        for a,pat,P,mt in s:
            print("    a=%d D-a=%s  P=%s P-min=%s  pairs(i,j)=%s"%(a,pat,P,[p-P[0] for p in P],[(x-r-k,d-a) for x,d,y in mt]))
