# Referee check (proof-reading lens): verify the smallest F1/F2 examples by brute force
# from the README definition (labels 0..m, growth = each bracket, longest first, has one used foot).
import networkx as nx
from networkx.algorithms.isomorphism import GraphMatcher

def growth_placements(n):
    m = n - 1
    out = []
    def rec(k, used, edges):
        if k == 0:
            out.append(list(edges)); return
        for p in range(0, m - k + 1):
            a, b = p, p + k
            if (a in used) != (b in used):
                new = b if a in used else a
                used.add(new); edges.append((a, b))
                rec(k - 1, used, edges)
                edges.pop(); used.remove(new)
    rec(m - 1, {0, m}, [(0, m)])
    return out

def anchors(G):
    """vertices of G that can carry label 0 in a growth placement"""
    n = G.number_of_nodes(); res = set()
    for E in growth_placements(n):
        H = nx.Graph(E)
        for iso in GraphMatcher(H, G).isomorphisms_iter():
            res.add(iso[0])
    return res

def path(k, pre):
    G = nx.path_graph(k); return nx.relabel_nodes(G, {i: pre + str(i) for i in G})

# F1: P3 rooted at end 'a0', K_{1,3} rooted at a leaf
P = path(3, 'a')
S = nx.star_graph(3); S = nx.relabel_nodes(S, {i: 'b' + str(i) for i in S})  # centre b0, leaf b1
print('P3 end anchor:', 'a0' in anchors(P), ' K13 leaf anchor:', 'b1' in anchors(S))
U = nx.contracted_nodes(nx.union(P, S), 'a0', 'b1')
print('F1 union vertex anchor:', 'a0' in anchors(U))
# F2 pair 1: P3 end -- P3 centre
Q = path(3, 'c')
J = nx.union(P, Q); J.add_edge('a0', 'c1')
A = anchors(J); print('F2 pair1: c-centre anchor of P3:', 'c1' in anchors(Q), ' ends anchors:', 'a0' in A, 'c1' in A)
# F2 pair 2: K2 -- K13 at leaf
K = nx.Graph([('d0', 'd1')])
J2 = nx.union(K, S); J2.add_edge('d0', 'b1')
A = anchors(J2); print('F2 pair2 ends anchors:', 'd0' in A, 'b1' in A)
# F2 neither: P3 end -- P4 end = P7
R = path(4, 'e'); J3 = nx.union(P, R); J3.add_edge('a0', 'e0')
A = anchors(J3); print('P4 end anchor:', 'e0' in anchors(R), ' P7 joined ends anchors:', 'a0' in A, 'e0' in A)
