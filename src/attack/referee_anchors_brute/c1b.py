# Brute-force check of the skeleton of the H3 proof: for each odd m, enumerate hub label
# triples of H(1,1,k) (root 0; hub label = hub length), decide solvability of each triple by
# backtracking (Theorem 7 form), and record which proof cases actually occur.
import sys
def solvable(m,C,b1,b2):
    used={0,C,b1,b2}; lens=[w for w in range(m,0,-1) if w not in (C,b1,b2)]
    cap=[1,1]; hubs=((0,b1),(1,b2))
    def rec(i):
        if i==len(lens): return cap==[0,0]
        w=lens[i]
        rem=len(lens)-i
        if w<C and rem>cap[0]+cap[1]:
            for y in (C+w,C-w):
                if 0<=y<=m and y not in used:
                    used.add(y)
                    if rec(i+1): return True
                    used.discard(y)
        for j,b in hubs:
            if cap[j] and w<b:
                for y in (b+w,b-w):
                    if 0<=y<=m and y not in used:
                        cap[j]=0; used.add(y)
                        if rec(i+1): return True
                        cap[j]=1; used.discard(y)
        return False
    return rec(0)
for m in range(int(sys.argv[1]),int(sys.argv[2])+1,2):
    classes=set()
    for C in range(1,m+1):
        for b1 in range(1,m+1):
            for b2 in range(b1+1,m+1):
                if C in (b1,b2) or m not in (C,b1,b2): continue
                if solvable(m,C,b1,b2):
                    if C==m: classes.add("A")
                    else:
                        b=b1 if b2==m else b2
                        classes.add(("B1" if b<C else "B2")+" t=%d"%(m-C))
    pred=set()
    if m%5==0: pred.add("A")
    ok = ("A" in classes)<=(m%5==0) and all(c in("A","B1 t=1") for c in classes) and (("B1 t=1" in classes)<=(m%3==0 or m%4==3))
    print(m,sorted(classes),"consistent with proof case analysis:",ok, "| anchor:",bool(classes),"rule:",m%3==0 or m%5==0 or m%4==3); sys.stdout.flush()
