#!/usr/bin/env python3
"""Independent check of comb certificates, from the README section 1 definitions only.

Reads lines   S s.. | w W y Y | h:u,u,.. h:u.. | W x x ..     (as printed by combx / symx / rules.py)
For each line builds the tree D(a1; S) with a1 = max(S) (and also a1 = w, the smallest root the comb
allows, when w>=1... the root must have at least w leaves) on labels 1..n and checks:
  * vertex labels are 1..n, each once;  * edge lengths are 1..n-1, each once (a placement);
  * growth: taking brackets longest first, each has exactly one foot already used (first: none used);
  * the graph is the tree D(a1; S): the centre's neighbours carry exactly the leaf counts a1, S;
  * the a1-hub has README label 1.
Lines starting with '#' are ignored; a line starting with FAIL is an error.
Usage: verify.py [--complete LO HI] file [file ...]      (files may be .gz)\n--complete: also check that the files contain a certificate for EVERY multiset S with |S|+sum+max+2 = n, LO<=n<=HI.
"""
import sys, gzip
def check(S, w, y, hubs, W, a1):
    k=len(S); m=1+k+sum(S)+a1          # edges; labels 0..m
    assert y==k+sum(S)+w+1 and a1>=w and len(W)==w
    edges=[(0,y)]
    for x in W: edges.append((0,x))
    for x in range(y+1,m+1): edges.append((0,x))
    for h,U in hubs:
        edges.append((y,h))
        for u in U: edges.append((h,h+u))
    edges=[(a+1,b+1) for a,b in edges]; n=m+1
    # placement
    assert len(edges)==n-1
    lens=sorted(abs(a-b) for a,b in edges); assert lens==list(range(1,n)), "lengths"
    verts=set(v for e in edges for v in e); assert verts==set(range(1,n+1)), "labels"
    # growth
    used=set()
    for a,b in sorted(edges,key=lambda e:-abs(e[0]-e[1])):
        if not used: used|={a,b}; continue
        assert (a in used)!=(b in used), "growth"
        used|={a,b}
    # shape
    adj={v:set() for v in verts}
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    c=y+1; counts=[]
    for h in adj[c]:
        leaves=adj[h]-{c}; assert all(len(adj[l])==1 for l in leaves), "shape"
        counts.append(len(leaves))
    assert sorted(counts)==sorted(list(S)+[a1]), "shape"
    assert len(adj[1])==a1+1 and c in adj[1], "root"
    return n
def allS(n):
    """every multiset S (non-increasing, entries >= 0, max >= 1) with |S| + sum(S) + max(S) + 2 = n"""
    def gen(total,k,maxv):
        if k==0:
            if total==0: yield ()
            return
        for f in range(min(total,maxv),-1,-1):
            for rest in gen(total-f,k-1,f): yield (f,)+rest
    for k in range(1,n):
        mx=1
        while k+2*mx+2<=n:
            for p in gen(n-2-k-2*mx,k-1,mx): yield (mx,)+p
            mx+=1
def main():
    tot=0; byn={}; args=sys.argv[1:]; complete=None; seen=set()
    if args[0]=='--complete': complete=(int(args[1]),int(args[2])); args=args[3:]
    for fn in args:
        f=gzip.open(fn,'rt') if fn.endswith('.gz') else open(fn)
        for line in f:
            if line.startswith('#') or not line.strip(): continue
            assert not line.startswith('FAIL'), line
            p=[x.strip() for x in line.split('|')]
            S=list(map(int,p[0].split()[1:])); t=p[1].split(); w=int(t[1]); y=int(t[3])
            hubs=[]
            for tok in p[2].split():
                h,_,us=tok.partition(':'); hubs.append((int(h),[int(u) for u in us.split(',')] if us else []))
            assert sorted(len(U) for h,U in hubs)==sorted(S), "sizes"
            W=list(map(int,p[3].split()[1:]))
            assert w<=max(S), "w > max(S)"
            n=check(S,w,y,hubs,W,max(S)); tot+=1; byn[n]=byn.get(n,0)+1; seen.add(tuple(sorted(S,reverse=True)))
            if w<max(S) and w>=1: check(S,w,y,hubs,W,w)
    print("verified %d certificates; by n (with a1 = max S):"%tot, sorted(byn.items()))
    if complete:
        for n in range(complete[0],complete[1]+1):
            need=set(allS(n)); miss=need-seen
            print("n=%d: %d multisets S with |S|+sum+max+2=n, certified %d, missing %d%s"%(n,len(need),len(need)-len(miss),len(miss),"" if not miss else "  e.g. "+str(sorted(miss)[:3])))
if __name__=='__main__': main()
