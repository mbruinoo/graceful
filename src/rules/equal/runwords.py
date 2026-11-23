# Collect run-structured deals (from ./runsearch k L R all) for a range of L, reduce each to its "word"
# (sequence of legs receiving each run) and print words that occur for several L together with run lengths.
import sys, subprocess, collections
k=int(sys.argv[1]); R=int(sys.argv[2]); Ls=list(map(int,sys.argv[3].split(','))); minocc=int(sys.argv[4]) if len(sys.argv)>4 else 3
db=collections.defaultdict(list)
for L in Ls:
    try: out=subprocess.run(["./runsearch",str(k),str(L),str(R),"all"],capture_output=True,text=True,timeout=1500).stdout
    except subprocess.TimeoutExpired: print("timeout",L); continue
    deals=out.split("deal ")[1:]
    print(f"L={L}: {len(deals)} deals with <= {R} runs",file=sys.stderr)
    for d in deals:
        lines=[l for l in d.splitlines() if 'edges' in l]
        owner={}
        for i,l in enumerate(lines):
            for e in l.split("edges:")[1].split(): owner[int(e)]=i
        m=k*L; word=[]; lens=[]
        labs=[list(map(int,l.split("edges:")[0].split("labels:")[1].split())) for l in lines]
        eds=[list(map(int,l.split("edges:")[1].split())) for l in lines]
        # run boundaries: need directions too
        dirs={}
        for i in range(k):
            p=0
            for x,e in zip(labs[i],eds[i]): dirs[e]=1 if x>p else -1; p=x
        t=m
        while t>=1:
            i=owner[t]; n=1
            while t-n>=1 and owner[t-n]==i and dirs[t-n]==-dirs[t-n+1]: n+=1
            word.append("ABCDEFGH"[i]+("+" if dirs[t]>0 else "-")); lens.append(n); t-=n
        db[" ".join(word)].append((L,lens))
for wd,occ in sorted(db.items(),key=lambda z:-len(set(o[0] for o in z[1]))):
    if len(set(o[0] for o in occ))<minocc: continue
    print(wd)
    for L,lens in occ: print("    L=%d: %s"%(L," ".join(map(str,lens))))
