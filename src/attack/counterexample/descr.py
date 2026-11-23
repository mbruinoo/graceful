# describe trees ("n u v ...") by canonical paren string rooted at centre, compressing repeats
import sys
for l in sys.stdin:
    if ":" in l: tag,l=l.split(":",1)
    else: tag=""
    t=l.split()
    if not t or not t[0].isdigit(): print(l.strip()); continue
    n=int(t[0]); x=list(map(int,t[1:])); adj=[[] for _ in range(n)]
    for a,b in zip(x[0::2],x[1::2]): adj[a].append(b); adj[b].append(a)
    def enc(v,p):
        ch=sorted(enc(u,v) for u in adj[v] if u!=p); out=[]; i=0
        while i<len(ch):
            j=i
            while j<len(ch) and ch[j]==ch[i]: j+=1
            out.append(ch[i]+("^%d"%(j-i) if j-i>1 else "")); i=j
        return "("+"".join(out)+")"
    ecc=[]
    def far(s):
        d={s:0}; q=[s]
        for v in q:
            for u in adj[v]:
                if u not in d: d[u]=d[v]+1; q.append(u)
        return d
    e=[max(far(v).values()) for v in range(n)]; c=e.index(min(e))
    print(tag,"n=%d"%n,enc(c,-1))
