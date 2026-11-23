# Referee's certificate checker: python3 ref_cert.py RULE "n a b ..." "labels..."  -> prints unused-run history and verdict
import sys
def runs(unused,n):
    r=[];i=1
    while i<=n:
        if i in unused:
            j=i
            while j<=n and j in unused: j+=1
            r.append((i,j-1)); i=j
        else: i+=1
    return r
def check(rule,tree,labs,verbose=True):
    t=list(map(int,tree.split())); n=t[0]; ed=list(zip(t[1::2],t[2::2])); lab=list(map(int,labs.split()))
    assert len(ed)==n-1 and sorted(lab)==list(range(1,n+1))
    byl={}
    for a,b in ed:
        d=abs(lab[a]-lab[b]); assert d not in byl; byl[d]=(lab[a],lab[b])
    assert sorted(byl)==list(range(1,n))
    used=set(); maxruns=0; maxsing=0; ok=True
    for k in range(n-1,0,-1):
        a,b=byl[k]
        if k==n-1: used|={a,b}
        else:
            assert (a in used)!=(b in used), "not growth at %d"%k
            used|={a,b}
        r=runs(set(range(1,n+1))-used,n)
        big=[x for x in r if x[1]>x[0]]
        maxruns=max(maxruns,len(r))
        if verbose: print(k,(a,b),r)
        if rule[0]=='R': ok&= len(r)<=int(rule[1])
        if rule[0]=='H': ok&= len(big)<=1 and len(r)<=int(rule[1])+1
        if rule=='EACH': ok&= len(big)<=1 and (len(r)<=2 or (len(r)==3 and (not big or big[0]==r[1])))
    print("growth placement OK; max runs",maxruns,"; rule",rule,"OK" if ok else "VIOLATED")
if __name__=="__main__": check(sys.argv[1],sys.argv[2],sys.argv[3])
