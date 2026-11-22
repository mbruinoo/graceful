# Growth labelings of a spider with the CENTRE as root (label 0, labels 0..m), shown as signed weights down each leg.
# Usage: spiderview.py L1 L2 ... [--max K]
import sys
args=sys.argv[1:]; K=6
if "--max" in args: i=args.index("--max"); K=int(args[i+1]); args=args[:i]
L=list(map(int,args)); d=len(L); m=sum(L); n=m+1
tips=[0]*d; placed=[0]*d; legs=[[] for _ in range(d)]; used=[False]*(n); used[0]=True; sols=[]; count=[0]
def rec(k):
    if k==0:
        count[0]+=1
        if len(sols)<K: sols.append([list(x) for x in legs])
        return
    seen=set()
    for i in range(d):
        if placed[i]==L[i]: continue
        key=(L[i],tuple(legs[i]))            # identical legs in identical state are interchangeable
        if key in seen: continue
        seen.add(key)
        for s in (1,-1):
            x=tips[i]+s*k
            if 0<=x<n and not used[x]:
                old=tips[i]; used[x]=True; tips[i]=x; placed[i]+=1; legs[i].append(s*k)
                rec(k-1)
                legs[i].pop(); placed[i]-=1; tips[i]=old; used[x]=False
rec(m)
print(f"spider legs {L}: n={n}, growth labelings with centre at 0 (up to swapping equal legs): {count[0]}")
for s in sols:
    print("   "+"   |   ".join(" ".join(f"{w:+d}" for w in leg) for leg in s))
