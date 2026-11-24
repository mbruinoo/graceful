# extras.py E1 n | E2 n      (uses ./spare and ../../gentrees.py)
# E1: for every non-anchor pair (T,r) on n vertices: is r an anchor of T + one new leaf at some vertex w?
#     (equivalently: has (T,r) a one-spare labeling whose unused label u and unused length k satisfy u = f(w)+-k with
#      k shorter than the edge above w, or w = r)   Prints the pairs for which NO w works, and how often w = r works.
# E2: for every tree T on n vertices and every leaf x: is there a growth placement of T (any root) in which the
#     bracket of length 1 hangs x?   Prints the (tree, leaf) pairs for which there is none.
import sys, subprocess
def run(lines, slack, extra=()):
    return subprocess.run(["./spare",str(slack),"0","0",*extra],input="\n".join(lines)+"\n",capture_output=True,text=True).stdout.split("\n")
mode=sys.argv[1]; n=int(sys.argv[2])
trees=[l for l in subprocess.run([sys.executable,"../../gentrees.py",str(n)],capture_output=True,text=True).stdout.split("\n") if l.strip()]
if mode=="E1":
    lines=["#t%d@%d %d %d %s"%(i,r,n,r,t) for i,t in enumerate(trees) for r in range(n)]
    non=[l.split()[0] for l in run(lines,0) if " NONE " in l]
    q=[]
    for name in non:
        i,r=name[2:].split("@"); i=int(i); r=int(r)
        for w in range(n): q.append("#t%d@%d+%d %d %d %s %d %d"%(i,r,w,n+1,r,trees[i],w,n))
    res={}
    for l in run(q,0):
        if not l.strip(): continue
        name=l.split()[0]; base,w=name.split("+"); res.setdefault(base,[]).append((int(w)," FOUND " in l))
    none=[b for b,v in res.items() if not any(f for _,f in v)]
    atroot=sum(1 for b,v in res.items() if any(f for w,f in v if w==int(b.split("@")[1])))
    print("E1 n=%d: non-anchor pairs %d; anchor after one leaf somewhere: %d; of these with the leaf at the root itself: %d; NO single leaf works: %d %s"%(n,len(non),len(non)-len(none),atroot,len(none),[ (b,trees[int(b[2:].split('@')[0])]) for b in none][:5]))
else:
    q=[]; pairs=0
    for i,t in enumerate(trees):
        e=list(map(int,t.split())); deg=[0]*n
        for v in e: deg[v]+=1
        for x in range(n):
            if deg[x]!=1: continue
            pairs+=1
            for r in range(n): q.append("#t%d/%d@%d %d %d %s %d"%(i,x,r,n,r,t,x))
    ok=set()
    for l in run(q,0,("last",)):
        if " FOUND " in l: ok.add(l.split()[0].split("@")[0])
    allp=set(l.split()[0].split("@")[0] for l in q); bad=sorted(allp-ok)
    print("E2 n=%d: (tree, leaf) pairs %d; leaf can be hung by the length-1 bracket: %d; cannot: %d %s"%(n,pairs,len(ok),len(bad),[(b,trees[int(b[2:].split('/')[0])]) for b in bad][:6]))
