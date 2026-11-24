# referee: replay a labeling (labels of vertices 0..n-1) as a growth build; print the tape and
# check literal rule compliance: there must EXIST a classification of each step as S/B/K1/F
# (with K1 = cell one in from a gap end, that end cell becomes a hole) obeying rule bits.
import sys
def steps(edges,lab):
    n=len(lab); br={}
    for u,v in edges:
        a,b=lab[u],lab[v]; L=abs(a-b); assert 1<=L<=n-1 and L not in br; br[L]=(min(a,b),max(a,b))
    assert sorted(lab)==list(range(1,n+1)) and br[n-1]==(1,n)
    used={1,n}; out=[]
    for L in range(n-2,0,-1):
        a,b=br[L]; assert (a in used)!=(b in used), "not growth"
        x,y=(b,a) if a in used else (a,b); assert n-len(used)==L
        out.append((x,y,L)); used.add(x)
    return out
def literal_ok(n,st,R):
    # states: (gaplo,gaphi,holes tuple in creation order)
    states={(2,n-1,())}
    for (x,y,L) in st:
        new=set()
        for lo,hi,H in states:
            d=1 if y>x else -1
            if x in H:
                if R&8 and H[0]!=x: continue
                if R&16 and H[-1]!=x: continue
                if R&32 and not (x==min(H) or x==max(H)): continue
                new.add((lo,hi,tuple(h for h in H if h!=x))); continue
            if not (lo<=x<=hi): continue
            Lg=hi-lo+1
            if x==lo:
                isS = (Lg==1) or d>0
                if isS or not R&4: new.add((lo+1,hi,H))
            if x==hi and Lg>1:
                isS = d<0
                if isS or not R&4: new.add((lo,hi-1,H))
            if Lg>=2 and x==lo+1:
                across = d>0
                if across or not R&2: new.add((lo+2,hi,H+(lo,)))
            if Lg>=2 and x==hi-1:
                across = d<0
                if across or not R&2: new.add((lo,hi-2,H+(hi,)))
        states=new
        if not states: return False
    return True
if __name__=="__main__":
    edges=list(map(int,sys.argv[1].split())); edges=list(zip(edges[::2],edges[1::2]))
    lab=list(map(int,sys.argv[2].split())); R=int(sys.argv[3]); n=len(lab)
    st=steps(edges,lab); used={1,n}
    for x,y,L in st:
        print(''.join('x' if c==x else 'Y' if c==y else ('#' if c in used else '.') for c in range(1,n+1)), f"len {L}")
        used.add(x)
    print("literal rule",R,"ok:",literal_ok(n,st,R))
