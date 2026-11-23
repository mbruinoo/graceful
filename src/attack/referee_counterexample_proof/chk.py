# Referee's own certificate checker (definition: README sections 1-2).
def growth(n,E,lab):
    """E: edges on vertices 0..n-1, lab: labels.  True iff a growth placement drawing exactly this tree."""
    if len(E)!=n-1 or sorted(lab)!=list(range(1,n+1)): return False
    by={}
    for a,b in E:
        d=abs(lab[a]-lab[b])
        if d in by: return False
        by[d]=(lab[a],lab[b])
    if sorted(by)!=list(range(1,n)): return False
    used=set(by[n-1])
    for k in range(n-2,0,-1):
        a,b=by[k]
        if (a in used)==(b in used): return False
        used|={a,b}
    return len(used)==n
