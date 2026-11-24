import sys
sys.path.insert(0,'.')
exec(open('ref.py').read().split('# ---- Rule T')[0])
import networkx as nx
from networkx.algorithms.isomorphism import tree_isomorphism
def edges(p,m): return [(p[k],p[k]+k) for k in range(1,m+1)]
def tree(p,m):
    T=nx.Graph(); T.add_nodes_from(range(m+1)); T.add_edges_from(edges(p,m)); return T
def rcanon(T,r,par=None):
    return '('+''.join(sorted(rcanon(T,c,r) for c in T[r] if c!=par))+')'
def canon(T):
    return min(rcanon(T,c) for c in nx.center(T))
# anchors
anch=set()
for m in range(0,7):
    for p in (G[m] if m else [(0,)]):
        anch.add(rcanon(tree(p,m),0))
def anchored(T,r): return rcanon(T,r) in anch
# F1 example: a-b-v-c-{x,y}
T=nx.Graph([(0,1),(1,2),(2,3),(3,4),(3,5)])
P3=nx.path_graph(3); K13=nx.star_graph(3)
print("F1: P3 end anchored",anchored(P3,0),"K13 leaf anchored",anchored(K13,1),"union at v anchored",anchored(T,2))
# F2 ex1: P3 end(2) -- P3 centre: same T, ends 2 and 3
print("F2 ex: ends anchored", anchored(T,2), anchored(T,3), "P3 centre", anchored(P3,1), "K2", anchored(nx.path_graph(2),0))
P7=nx.path_graph(7); print("F2 P7 ends 2,3:",anchored(P7,2),anchored(P7,3),"P4 end",anchored(nx.path_graph(4),0))
# smallest F1: check all pairs with total n<=5 for failure
rooted={}
for n in range(1,8):
    for T0 in nx.nonisomorphic_trees(n) if n>1 else [nx.empty_graph(1)]:
        for r in T0: rooted.setdefault(rcanon(T0,r),(T0,r))
def glue(A,ra,B,rb,edge):
    H=nx.disjoint_union(A,B); off=len(A)
    if edge: H.add_edge(ra,rb+off); return H,ra,rb+off
    H=nx.contracted_nodes(H,ra,rb+off,self_loops=False); return nx.convert_node_labels_to_integers(H,label_attribute='o'),None,None
keys=sorted(rooted,key=len)
f1=[];f2=[];f2b=[]
ks=list(rooted)
for i,a in enumerate(ks):
  for b in ks[i:]:
    A,ra=rooted[a];B,rb=rooted[b]
    if not(anchored(A,ra) and anchored(B,rb)): continue
    n=len(A)+len(B)
    if len(A)>=2 and len(B)>=2 and n-1<=7:
        H=nx.disjoint_union(A,B); H=nx.relabel_nodes(H,{rb+len(A):ra}); 
        if not anchored(H,ra): f1.append(n-1)
    if n<=7:
        H=nx.disjoint_union(A,B); H.add_edge(ra,rb+len(A))
        x,y=anchored(H,ra),anchored(H,rb+len(A))
        if not(x and y): f2.append(n)
        if not x and not y: f2b.append(n)
print("F1 failures (n<=7 union)",len(f1),min(f1) if f1 else None)
print("F2 failures n<=7:",len(f2),sorted(f2)[:4]," neither:",len(f2b),sorted(f2b)[:3])
