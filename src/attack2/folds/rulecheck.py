# rulecheck.py RULE n idx [idx ...]  -- INDEPENDENT exhaustive search (Python; shares no code with tidy.cpp) for a growth
# placement of tree number idx (line of `gentrees.py n`, file given by env TREES or t<n>.txt in env TDIR) that obeys the
# vocabulary RULE (bitmask as in tidy.cpp / REPORT.txt section 5).  Prints FOUND (with labels, re-checked by
# lib.replay and verify.obeys) or NONE (search space exhausted).
import sys, os, lib
sys.setrecursionlimit(100000)
def search(n,E,adj,R):
    enc={}
    def shape(v,p):
        if (v,p) not in enc: enc[(v,p)]=lib.enc(adj,v,p)
        return enc[(v,p)]
    roots=set(); res=[None]
    lab=[0]*n; used=[False]*(n+2); age={}; dead=set(); nodes=[0]
    def key():
        fr=[]
        for u in range(n):
            if lab[u]:
                for w in adj[u]:
                    if not lab[w]: fr.append((lab[u],shape(w,u)))
        fr.sort()
        holes=tuple(sorted(age.items(),key=lambda kv:kv[1])) if R&24 else tuple(sorted(age))
        return (tuple(i for i in range(1,n+1) if used[i]),tuple(h for h,_ in holes) if R&24 else holes,tuple(fr))
    def rec(t,clock):
        if t==0: return True
        k=key()
        if k in dead: return False
        nodes[0]+=1
        for u in range(n):
            if not lab[u]: continue
            seen=set()
            for w in adj[u]:
                if lab[w]: continue
                s=shape(w,u)
                if s in seen: continue
                seen.add(s)
                for x in (lab[u]-t,lab[u]+t):
                    if x<1 or x>n or used[x]: continue
                    y=lab[u]; newhole=None; delhole=None
                    if x in age:
                        others=[h for h in age if h!=x]
                        if R&8 and any(age[h]<age[x] for h in others): continue
                        if R&16 and any(age[h]>age[x] for h in others): continue
                        if R&32 and any(h<x for h in others) and any(h>x for h in others): continue
                        delhole=(x,age[x])
                    else:
                        lo=x
                        while lo>1 and not used[lo-1] and (lo-1) not in age: lo-=1
                        hi=x
                        while hi<n and not used[hi+1] and (hi+1) not in age: hi+=1
                        r=(x-lo) if y>x else (hi-x); c=(hi-lo)-r
                        if r>=1 and c>=1:
                            if r==1: newhole=x-1 if y>x else x+1
                            elif c==1:
                                if R&2: continue
                                newhole=x+1 if y>x else x-1
                            else: continue
                        elif c==0 and r>=1 and (R&4): continue
                    lab[w]=x; used[x]=True
                    if newhole is not None: age[newhole]=clock
                    if delhole: del age[x]
                    ok=rec(t-1,clock+1)
                    if ok: return True
                    lab[w]=0; used[x]=False
                    if newhole is not None: del age[newhole]
                    if delhole: age[delhole[0]]=delhole[1]
        dead.add(k); return False
    for u in range(n):
        for w in adj[u]:
            rk=(shape(u,w),shape(w,u))
            if rk in roots: continue
            roots.add(rk)
            lab[u]=1; lab[w]=n; used[1]=used[n]=True
            if rec(n-2,1): return list(lab),nodes[0]
            lab[u]=0; lab[w]=0
    return None,nodes[0]
if __name__=='__main__':
    R=int(sys.argv[1])|1; n=int(sys.argv[2]); tdir=os.environ.get('TDIR','.')
    T=[l for l in open(os.environ.get('TREES',f'{tdir}/t{n}.txt')) if l.strip()]
    import subprocess
    for i in map(int,sys.argv[3:]):
        nn,E,adj=lib.parse(T[i]); f,nodes=search(nn,E,adj,R)
        if f is None: print(f'RULE={R} n={n} tree {i} {lib.canon(adj)}: NONE (exhausted, {nodes} states)')
        else:
            steps=lib.replay(nn,E,f)
            sys.argv_backup=None
            from verify_rule import obeys
            good,why=obeys(nn,steps,R); assert good,why
            print(f'RULE={R} n={n} tree {i} {lib.canon(adj)}: FOUND labels {" ".join(map(str,f))}')
