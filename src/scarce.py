# Scarcest NON-caterpillar shapes by number of growth placements.
import sys, subprocess
def build(s):
    E=[]; cnt=[0]
    def parse(i,pa):
        v=cnt[0]; cnt[0]+=1
        if pa is not None: E.append((pa,v))
        i+=1
        while s[i]=='(' : i=parse(i,v)
        return i+1
    if '|' in s:
        a,b=s.split('|'); 
        s=a; parse(0,None); r2=cnt[0]; s=b; parse(0,None); E.append((0,r2))
    else: parse(0,None)
    return cnt[0],E
def descr(n,E):
    adj=[[] for _ in range(n)]
    for a,b in E: adj[a].append(b); adj[b].append(a)
    deg=[len(a) for a in adj]
    inner=[v for v in range(n) if deg[v]>1]
    cat=all(sum(1 for u in adj[v] if deg[u]>1)<=2 for v in inner)
    big=[v for v in range(n) if deg[v]>=3]
    spider=len(big)<=1
    return cat, spider, sorted(deg,reverse=True)
for n in map(int,sys.argv[1:]):
    out=subprocess.run(["./growcount",str(n),"100000"],capture_output=True,text=True).stdout.splitlines()
    print(out[0]); k=0
    for line in out[1:]:
        c,s=line.split(); nn,E=build(s); cat,sp,dg=descr(nn,E)
        if cat: continue
        print(f"  {c:>6}  {'spider ' if sp else '       '} degs={dg[:6]}  {s}"); k+=1
        if k>=8: break
