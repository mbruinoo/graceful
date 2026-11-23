# Brute-force check of the step used by the hub theorem (README Lemma 6 at the vertex labelled 1):
# for EVERY growth placement on n <= NMAX vertices (enumerated from the definition), adding the bracket {1, n+1}
# gives a growth placement on n+1 vertices of the tree plus a leaf at the vertex labelled 1, with that vertex still
# labelled 1.  Also checks the count of growth placements against README section 4.
import sys
NMAX=int(sys.argv[1]) if len(sys.argv)>1 else 9
def growth(br,n):      # br: dict length -> left foot.  definition: brackets n-1..k connected for every k
    used={br[n-1],br[n-1]+n-1}
    for k in range(n-2,0,-1):
        a,b=br[k],br[k]+k
        if (a in used)==(b in used): return False
        used|={a,b}
    return len(used)==n
def allgrowth(n):
    out=[]
    def rec(k,br):
        if k==0:
            if growth(br,n): out.append(dict(br))
            return
        for p in range(1,n-k+1):
            br[k]=p; rec(k-1,br)
        del br[k]
    rec(n-1,{})
    return out
known={4:4,5:12,6:32,7:116,8:412,9:1764}
for n in range(4,NMAX+1):
    G=allgrowth(n); ok=True
    for br in G:
        nb=dict(br); nb[n]=1
        if not growth(nb,n+1): ok=False
        # the new vertex n+1 is a leaf joined to label 1
        deg=sum(1 for k,p in nb.items() if n+1 in (p,p+k))
        if deg!=1 or nb[n]!=1: ok=False
    print("n=%d growth placements=%d (README: %s)  extension by {1,n+1} always a growth placement: %s"%(n,len(G),known.get(n),ok))
