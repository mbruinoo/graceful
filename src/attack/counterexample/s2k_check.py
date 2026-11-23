# Spiders S(2^k) (k legs of length 2).  Reads zigzag deals "k=.. legs: a:o ..." (centre 0, inner label a, outer label o)
# from run_zz2dlx.log and writes certificates "tree | labels" (labels 1..n) for verify.py:
#  (1) k not 2 mod 3, k<=150: the deal itself (centre label 1).
#  (2) k = 2 mod 3: deal for k-1 shifted by 2, centre label 2, new leg centre - n - 1 (gluing statement, README 7/13).
#  (3) block lemma: from a deal for k' the deal for 5k'+1: keep the legs; add loops/shift on the interval
#      O-part [2k'+1, 6k'+1]:  x -> x+2k' (x <= 4k'+1),  x -> x-2k'-1 (x > 4k'+1); leg inner label x+pi(x), outer label pi(x).
import sys, re
deals={}
for l in open("run_zz2dlx.log"):
    m=re.match(r"k=(\d+) n=\d+ OK legs:(.*)",l)
    if m: deals[int(m.group(1))]=[tuple(map(int,p.split(":"))) for p in m.group(2).split()]
def cert(legs,shift,extra=None):
    # legs in 0-based labels with centre 0; vertex 0 = centre; output labels = label+shift
    k=len(legs)+(1 if extra else 0); n=2*k+1; E=[]; lab=[shift]
    v=1
    for a,o in legs:
        E+= [(0,v),(v,v+1)]; lab+=[a+shift,o+shift]; v+=2
    if extra: E+=[(0,v),(v,v+1)]; lab+=list(extra)
    print(n," ".join("%d %d"%e for e in E),"|"," ".join(map(str,lab)))
def block(legs):
    kp=len(legs); t=2*kp; c=t+1; new=list(legs)
    for x in range(c,c+2*t+1):
        p = x+t if x<=c+t else x-t-1
        new.append((x+p,p))
    return new
mode=sys.argv[1]
for k in sorted(deals):
    if mode=="deal": cert(deals[k],1)
    elif mode=="glue":
        K=k+1
        if K%3==2: cert(deals[k],2,extra=(2*K+1,1))
    elif mode=="block":
        cert(block(deals[k]),1)
    elif mode=="block2":
        if k<=30: cert(block(block(deals[k])),1)
