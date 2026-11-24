#!/usr/bin/env python3
"""Exploration tool: all-up combs in which every hub's leaf lengths are a union of prescribed arithmetic
progressions.  spec: list of (hub_label, [(diff,count),...]);  w = number of inside fillers.
Prints up to `limit` solutions as  hub: [start..] ...  W=...   Used to find the rules in rules.py."""
import sys, itertools
def search(spec, w, limit=5, show=True):
    k=len(spec); tot=sum(c for h,aps in spec for d,c in aps); y=k+tot+w+1
    full=(1<<y)-2
    usedL=0; usedC=0
    for h,aps in spec:
        if h>=y: return []
        usedL|=1<<(y-h); usedC|=1<<h
    items=[(h,d,c) for h,aps in spec for d,c in aps if c>0]
    # order: longest APs first
    items.sort(key=lambda t:-t[2]*t[1])
    sols=[]; choice=[]
    def rec(i,uL,uC):
        if len(sols)>=limit: return
        if i==len(items):
            fl=full&~uL; fc=full&~uC
            if fl==fc: sols.append((list(choice),[x for x in range(1,y) if fl>>x&1]))
            return
        h,d,c=items[i]
        # symmetry: equal items on same hub in increasing start
        lo=1
        if i>0 and items[i-1]==items[i]: lo=choice[-1]+1
        for s in range(lo,y-h-d*(c-1)):
            mL=0; mC=0
            for j in range(c): mL|=1<<(s+d*j); mC|=1<<(s+d*j+h)
            if mL&uL or mC&uC: continue
            choice.append(s); rec(i+1,uL|mL,uC|mC); choice.pop()
    rec(0,usedL,usedC)
    if show:
        for ch,W in sols:
            print("  y=%d "%y+' '.join("%d:%d+%dx%d"%(items[i][0],ch[i],items[i][1],items[i][2]) for i in range(len(items))),"W=",W)
    return sols
if __name__=="__main__":
    # two sizes: e outer b-hubs (e even), d middle a-hubs, odd labels
    d=int(sys.argv[1]); e=int(sys.argv[2]); a=int(sys.argv[3]); b=int(sys.argv[4]); D=d+e
    labs=[2*i+1 for i in range(D)]
    spec=[]
    for i,h in enumerate(labs):
        if e//2<=i<e//2+d: spec.append((h,[(D,b),(d,a-b)]))
        else: spec.append((h,[(D,b)]))
    for w in range(0,3*D):
        s=search(spec,w,3)
        if s: print("w=",w); break
        else: print("w=",w,"none")
