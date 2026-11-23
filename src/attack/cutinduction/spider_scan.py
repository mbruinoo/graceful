# Run spider_ck over all spiders on n vertices with a given number of legs (or all leg counts >=3) and list those NOT in C(K).
# Usage: python3 spider_scan.py K n [legs|0=all>=3] [timeout_s]
import subprocess, sys, os
K=int(sys.argv[1]); n=int(sys.argv[2]); legs=int(sys.argv[3]) if len(sys.argv)>3 else 0; to=int(sys.argv[4]) if len(sys.argv)>4 else 300
here=os.path.dirname(os.path.abspath(__file__))
def parts(total,maxpart,k):
    if k==0:
        if total==0: yield []
        return
    for p in range(min(total-(k-1),maxpart),0,-1):
        for rest in parts(total-p,p,k-1): yield [p]+rest
tot=0; bad=[]; unk=[]
for k in ([legs] if legs else range(3,n)):
    for p in parts(n-1,n-1,k):
        tot+=1
        try:
            out=subprocess.run([os.path.join(here,'spider_ck'),str(K)]+[str(x) for x in p],capture_output=True,text=True,timeout=to).stdout
        except subprocess.TimeoutExpired:
            unk.append(p); continue
        line=[l for l in out.splitlines() if l.startswith('spider')][0]
        if 'cap hit' in line: unk.append(p)
        elif 'NOT REACHED' in line: bad.append(p)
print(f"K={K} n={n} legs={'all>=3' if not legs else legs}: spiders={tot} not_in_C(K)={len(bad)} {bad} undecided={len(unk)} {unk}",flush=True)
