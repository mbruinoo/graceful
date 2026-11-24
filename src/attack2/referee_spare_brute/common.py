# referee: definition check, written independently
def check(n, root, edges, lab, N):
    """relaxed growth labeling with labels 0..N-1; returns (ok, reason)"""
    if len(lab)!=n: return False,"len"
    if any((not isinstance(x,int)) or x<0 or x>=N for x in lab): return False,"range"
    if len(set(lab))!=n: return False,"inj"
    if lab[root]!=0: return False,"root"
    if len(edges)!=n-1: return False,"edges"
    adj=[[] for _ in range(n)]
    for a,b in edges: adj[a].append(b); adj[b].append(a)
    lens=[abs(lab[a]-lab[b]) for a,b in edges]
    if len(set(lens))!=n-1 or 0 in lens: return False,"lens"
    seen=[False]*n; seen[root]=True; st=[(root,10**9)]; cnt=1
    while st:
        v,up=st.pop()
        for w in adj[v]:
            if not seen[w]:
                L=abs(lab[v]-lab[w])
                if L>=up: return False,"decrease"
                seen[w]=True; cnt+=1; st.append((w,L))
    if cnt!=n: return False,"conn"
    return True,""
def unused(n,edges,lab,N):
    ul=sorted(set(range(N))-set(lab)); uk=sorted(set(range(1,N))-set(abs(lab[a]-lab[b]) for a,b in edges))
    return ul,uk
def parse_tree(line):
    t=line.split(); name=t[0]; n=int(t[1]); root=int(t[2]); v=list(map(int,t[3:]))
    return name,n,root,[(v[i],v[i+1]) for i in range(0,len(v),2)]
