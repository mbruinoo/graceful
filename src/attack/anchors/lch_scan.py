# lch_scan.py validate HMAX NMAX : compare ./lch with ./anchq on L(l;h1,h2) and L(l;h1,h2,h3)
# lch_scan.py scan l HMAX        : list (h1,h2) for which the root of L(l;h1,h2) is NOT an anchor
import subprocess,sys
def lch(l,hs): return subprocess.run(["./lch",str(l)]+[str(h) for h in hs],capture_output=True,text=True).stdout.startswith("ANCHOR")
def tree(l,hs):
    e=[(0,1)]; nx=2; gs=[]
    for h in hs: e.append((1,nx)); gs.append(nx); nx+=1
    for g,h in zip(gs,hs):
        for j in range(h): e.append((g,nx)); nx+=1
    for j in range(l): e.append((0,nx)); nx+=1
    return nx,e
def anchq(l,hs):
    n,e=tree(l,hs); line="%d 0 "%n+" ".join("%d %d"%x for x in e)
    return subprocess.run(["./anchq"],input=line+"\n",capture_output=True,text=True).stdout.startswith("ANCHOR")
if sys.argv[1]=="validate":
    HM=int(sys.argv[2]); NM=int(sys.argv[3]); tot=0; bad=0; non=0
    for l in range(0,6):
        for h1 in range(0,HM+1):
            for h2 in range(h1,HM+1):
                for h3 in [None]+list(range(h2,HM+1)):
                    hs=[h1,h2]+([h3] if h3 is not None else [])
                    if tree(l,hs)[0]>NM: continue
                    A=lch(l,hs); B=anchq(l,hs); tot+=1; non+= (not A)
                    if A!=B: bad+=1; print("MISMATCH",l,hs,A,B)
    print("validated",tot,"trees (n<=%d): non-anchor roots %d, mismatches %d"%(NM,non,bad))
else:
    l=int(sys.argv[2]); HM=int(sys.argv[3]); res=[]
    for h1 in range(0,HM+1):
        for h2 in range(h1,HM+1):
            if not lch(l,[h1,h2]): res.append((h1,h2))
    print("l=%d, 0<=h1<=h2<=%d: non-anchor (h1,h2):"%(l,HM),res,flush=True)
