# enumerate all valid deals for k equal legs of length L (legs unordered: leg receiving larger first number first)
import sys
def deals(k,L,zig=False,limit=None):
    m=k*L; cur=[0]*k; cnt=[0]*k; used=[False]*(m+1); lab=[[] for _ in range(k)]; ed=[[] for _ in range(k)]; out=[]
    def rec(t):
        if t==0:
            out.append(([l[:] for l in lab],[e[:] for e in ed])); return limit is not None and len(out)>=limit
        for i in range(k):
            if cnt[i]==L: continue
            if cnt[i]==0 and i>0 and cnt[i-1]==0: continue
            if cnt[i]==0: cands=[t]
            elif zig: cands=[cur[i]+t if cnt[i]%2==0 else cur[i]-t]
            else: cands=[cur[i]-t,cur[i]+t]
            for x in cands:
                if x<1 or x>m or used[x]: continue
                old=cur[i]; cur[i]=x; used[x]=True; cnt[i]+=1; lab[i].append(x); ed[i].append(t)
                if rec(t-1): return True
                lab[i].pop(); ed[i].pop(); cnt[i]-=1; used[x]=False; cur[i]=old
        return False
    rec(m); return out
if __name__=="__main__":
    k,L=int(sys.argv[1]),int(sys.argv[2]); zig=len(sys.argv)>3 and sys.argv[3]=='zig'
    D=deals(k,L,zig)
    print(f"k={k} L={L} zig={zig}: {len(D)} deals")
    for lab,ed in D[:int(sys.argv[4]) if len(sys.argv)>4 else 30]:
        print("  "+"  |  ".join(" ".join(map(str,l)) for l in lab))
