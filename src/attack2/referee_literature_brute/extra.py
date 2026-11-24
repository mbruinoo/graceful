import subprocess
def run(cases,timeout=None):
    inp="\n".join(f"{n} {v} "+" ".join(f"{a} {b}" for a,b in E) for n,v,E in cases)+"\n"
    out=subprocess.run(["./gs"],input=inp,capture_output=True,text=True,timeout=timeout).stdout.split()
    return [(int(out[2*i]),int(out[2*i+1])) for i in range(len(cases))]
# L(3;8,9), v=0
E=[(0,1),(1,2),(1,3)]+[(2,i) for i in range(4,12)]+[(3,i) for i in range(12,21)]+[(0,i) for i in (21,22,23)]
print("L(3;8,9) v=0 (24 vertices): (0-centred graceful, anchor) =",run([(24,0,E)])[0],flush=True)
# brooms rooted at handle end: path r=0..h-1 then t leaves on vertex h-1 at depth h
bad=[];cnt=0
for n in range(3,21):
    for h in range(1,n):
        t=n-h
        if h==1 and t!=n-1: continue
        E=[(i,i+1) for i in range(h-1)]+[(h-1,h-1+j) for j in range(1,t+1)]
        r=run([(n,0,E)])[0]; cnt+=1
        if r[1]!=1: bad.append((n,h,t))
print(f"brooms rooted at the handle end (h+t_h=n), n<=20: {cnt} cases, root not an anchor in {bad}")
