# kappa (least clean step size) for every spider with exactly `legs` legs on n vertices, n in [n0,n1].  Usage: kappa_scan.py legs n0 n1
import subprocess, sys, os, re
legs,n0,n1=map(int,sys.argv[1:4]); here=os.path.dirname(os.path.abspath(__file__))
def parts(total,maxpart,k):
    if k==0:
        if total==0: yield []
        return
    for p in range(min(total-(k-1),maxpart),0,-1):
        for rest in parts(total-p,p,k-1): yield [p]+rest
for n in range(n0,n1+1):
    hist={}; worst=[]
    for p in parts(n-1,n-1,legs):
        out=subprocess.run([os.path.join(here,'spider_kappa')]+[str(x) for x in p],capture_output=True,text=True).stdout
        k=int(re.search(r'kappa\(T\)=(-?\d+)',out).group(1)); hist[k]=hist.get(k,0)+1
        if k>=3: worst.append((k,p))
    print(f"n={n} legs={legs}: kappa histogram {dict(sorted(hist.items()))}  spiders with kappa>=3: {worst}",flush=True)
