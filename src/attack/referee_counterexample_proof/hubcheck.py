# For every rooted D on d vertices and m=0..3: exhaustive root-anchor / any-growth for T(D,m).
import sys, subprocess, time
from rooted import rooted, line
def run(lines):
    out=subprocess.run(["./ex"],input="\n".join(lines)+"\n",capture_output=True,text=True).stdout.split("\n")
    return [tuple(map(int,o.split())) for o in out if o]
for d in map(int,sys.argv[1:]):
    t0=time.time(); Ds=rooted(d); res={}
    for m in range(4):
        r=run([line(D,m) for D in Ds]); assert len(r)==len(Ds)
        for D,x in zip(Ds,r): res[D,m]=x
    hist={}; nomono=0; smallfail=0; deg4fail=0; deg3two=[]
    for D in Ds:
        ms=[m for m in range(4) if res[D,m][0]]
        m0=ms[0] if ms else None
        hist[m0]=hist.get(m0,0)+1
        if m0 is not None and any(not res[D,m][0] for m in range(m0,4)): nomono+=1
        if any(not res[D,m][1] for m in range(4)): smallfail+=1
        for m in range(4):
            if len(D)+m>=4 and not res[D,m][0]: deg4fail+=1
        if m0 is not None and m0>=2: print("   d=%d least m=%d D=%s  edges(m=%d): %s"%(d,m0,D,m0-1,line(D,m0-1)))
        # degree-3 root with (at least) two leaf neighbours, not an anchor
        for m in range(4):
            if len(D)+m==3 and sum(1 for c in D if c==())+m>=2 and not res[D,m][0]: deg3two.append((d+m,line(D,m)))
    print("d=%d rooted=%d least-m histogram=%s  monotonicity violations=%d  T(D,m) m<=3 with NO growth placement=%d  root-degree>=4 non-anchors (n<=%d)=%d  [%.0fs]"%(d,len(Ds),sorted(hist.items(),key=str),nomono,smallfail,d+3,deg4fail,time.time()-t0),flush=True)
    for x in deg3two: print("   degree-3 root with two leaf neighbours, NOT an anchor: n=%d  %s"%x)
