# armfast.py b j [maxshow] -- same enumeration as armpieces.py (crossing one-spare pieces for path arms (b, j) with the
# tip of the j-arm innermost), but pruning non-crossing partial labelings early; agrees with armpieces.py for
# b <= 12, j <= 3 (checked).  Exhaustive.
import sys
def pieces(b,j,limit=None):
    R=b+j+1; out=[]
    used=[False]*(R+1); lens=[False]*(R+2); used[0]=True
    st={'ml':0,'mh':R+1}
    def arm(seq,need,cb):
        if limit and len(out)>=limit: return
        if len(seq)==need+1: cb(seq); return
        x=seq[-1]; last=abs(seq[-1]-seq[-2]) if len(seq)>1 else R+1
        high=(len(seq)%2==1)          # next vertex has odd depth -> high side
        for l in range(last-1,0,-1):
            if lens[l]: continue
            z = x+l if high else x-l
            if z<0 or z>R or used[z]: continue
            ml,mh=st['ml'],st['mh']
            if high:
                if z<=ml: continue
                st['mh']=min(mh,z)
            else:
                if z>=mh: continue
                st['ml']=max(ml,z)
            seq.append(z); used[z]=True; lens[l]=True
            arm(seq,need,cb)
            seq.pop(); used[z]=False; lens[l]=False; st['ml'],st['mh']=ml,mh
    def afterA(A):
        A=A[:]
        def afterB(B):
            y=B[-1]
            if (j%2==1 and y==st['mh']) or (j%2==0 and y==st['ml']): out.append((A,B[:]))
        arm([0],j,afterB)
    arm([0],b,afterA)
    return out
if __name__=="__main__":
    b,j=int(sys.argv[1]),int(sys.argv[2]); s=pieces(b,j); print("b=%d j=%d pieces=%d"%(b,j,len(s)), s[:int(sys.argv[3]) if len(sys.argv)>3 else 2])
