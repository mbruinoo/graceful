# armpieces.py maxb maxj -- "pieces" for the gluing theorem G on paths.
# Path with arms (b, j) around the root.  Labels 0..b+j+1 (one spare), root 0.  A PIECE is a one-spare relaxed growth
# labeling that is CROSSING (every edge joins a label <= a to a label > a for some threshold a; i.e. all even-depth
# labels are below all odd-depth labels) and in which the tip y of the j-arm is INNERMOST on its side
# (the least odd-depth label if j is odd, the greatest even-depth label if j is even).
# Exhaustive enumeration; prints the number of pieces and the first few.
import sys
def pieces(b,j):
    R=b+j+1; out=[]
    def arm(seq,used,lens,need,cb):
        if len(seq)==need+1: cb(seq,used,lens); return
        x=seq[-1]; last=abs(seq[-1]-seq[-2]) if len(seq)>1 else R+1
        for l in range(last-1,0,-1):
            if l in lens: continue
            for z in (x+l,x-l):
                if 0<=z<=R and z not in used:
                    seq.append(z); used.add(z); lens.add(l); arm(seq,used,lens,need,cb); seq.pop(); used.discard(z); lens.discard(l)
    def afterA(A,used,lens):
        A=A[:]
        def afterB(B,used2,lens2):
            low=[A[i] for i in range(0,b+1,2)]+[B[i] for i in range(2,j+1,2)]
            high=[A[i] for i in range(1,b+1,2)]+[B[i] for i in range(1,j+1,2)]
            if max(low)>min(high): return
            y=B[-1]
            if (j%2==1 and y==min(high)) or (j%2==0 and y==max(low)): out.append((A,B[:]))
        arm([0],used,lens,j,afterB)
    arm([0],{0},set(),b,afterA)
    return out
if __name__=="__main__":
    for j in range(1,int(sys.argv[2])+1):
        for b in range(1,int(sys.argv[1])+1):
            s=pieces(b,j); print("b=%d j=%d pieces=%d"%(b,j,len(s)), s[:2])
