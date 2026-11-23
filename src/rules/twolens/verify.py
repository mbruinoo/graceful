# Independent checker, straight from the definition of a valid deal.
def check_deal(legs_len, deal):
    """legs_len: list of leg lengths.  deal: list (in dealing order, numbers m, m-1, ..., 1) of (leg index, sign)
    sign = +1 / -1 (first number of a leg must be +1).  Returns (ok, reason)."""
    m=sum(legs_len)
    if len(deal)!=m: return False,"wrong number of moves"
    tip=[0]*len(legs_len); cnt=[0]*len(legs_len); seen=set()
    for idx,(leg,sg) in enumerate(deal):
        w=m-idx
        if cnt[leg]==0 and sg!=1: return False,"first move of a leg must go up"
        if sg not in (1,-1): return False,"bad sign"
        tip[leg]+=sg*w; cnt[leg]+=1
        if not (1<=tip[leg]<=m): return False,"label %d out of range"%tip[leg]
        if tip[leg] in seen: return False,"label %d twice"%tip[leg]
        seen.add(tip[leg])
    if cnt!=list(legs_len): return False,"leg sizes wrong"
    return True,"ok"
def deal_from_lists(legs_len, lists):
    """lists[i] = [(w, sign), ...] for leg i (numbers decreasing).  Builds the dealing order."""
    m=sum(legs_len); owner={}
    for i,l in enumerate(lists):
        prev=None
        for (w,s) in l:
            assert w not in owner, "number %d dealt twice"%w
            assert prev is None or w<prev, "list not decreasing"
            owner[w]=(i,s); prev=w
    assert sorted(owner)==list(range(1,m+1)), "not all numbers dealt"
    return [owner[w] for w in range(m,0,-1)]
