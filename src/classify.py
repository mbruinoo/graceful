# Which trees lack an interval-growth placement?  Classify by family.
import sys, subprocess, networkx as nx
def canon(T):
    n=T.number_of_nodes(); adj={v:list(T[v]) for v in T}
    c=nx.center(T)
    def enc(v,pa): return "("+"".join(sorted(enc(u,v) for u in adj[v] if u!=pa))+")"
    if len(c)==1: return enc(c[0],None)
    return "".join(sorted([enc(c[0],c[1]),enc(c[1],c[0])]))
def is_spider(T): return sum(1 for v in T if T.degree(v)>=3)<=1
def strip(T):
    H=T.copy(); H.remove_nodes_from([v for v in T if T.degree(v)==1]); return H
def is_path(T): return T.number_of_nodes()<=1 or max(d for _,d in T.degree())<=2
def is_cat(T): return is_path(strip(T))
def is_lob(T): return is_cat(strip(T)) if strip(T).number_of_nodes()>1 else True
for n in range(8,int(sys.argv[1])+1):
    subprocess.run(["./interval",str(n),"/tmp/claude-0/-home-user-graceful/0371e752-f73a-552a-b40d-e3821e32333f/scratchpad/sh.txt"],stdout=subprocess.DEVNULL)
    have=set(open("/tmp/claude-0/-home-user-graceful/0371e752-f73a-552a-b40d-e3821e32333f/scratchpad/sh.txt").read().split())
    tot={"all":0,"spider":0,"lobster":0,"diam<=4":0,"diam<=5":0,"maxdeg<=3":0,"leaves<=4":0}; miss=dict.fromkeys(tot,0); ex=[]
    for T in nx.nonisomorphic_trees(n):
        d=nx.diameter(T); L=sum(1 for v in T if T.degree(v)==1)
        tags=["all"]+(["spider"] if is_spider(T) else [])+(["lobster"] if is_lob(T) else [])+(["diam<=4"] if d<=4 else [])+(["diam<=5"] if d<=5 else [])+(["maxdeg<=3"] if max(dict(T.degree()).values())<=3 else [])+(["leaves<=4"] if L<=4 else [])
        m=canon(T) not in have
        for t in tags:
            tot[t]+=1; miss[t]+=m
        if m and len(ex)<2: ex.append(sorted(T.edges()))
    print(n," ".join(f"{t}:{miss[t]}/{tot[t]}" for t in tot), ex if n<=10 else "")
