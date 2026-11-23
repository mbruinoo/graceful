"""README section 7 anchor table from the full enumeration of growth placements (ref_small.py growth N).
A vertex is an anchor iff the tree rooted at it has the same AHU code as some growth placement rooted at label 1."""
import sys, json
from gen import trees
from common import adjacency, rooted_code
n = int(sys.argv[1])
anch = set(json.load(open(f"out/ref_growth_{n}.json"))["anchors"])
tot = non = allanch = ntrees = noanchor = noleaf = maxdeg_non = 0
for e in trees(n):
    e = [(a + 1, b + 1) for a, b in e]
    adj = adjacency(n, e)
    ntrees += 1
    bad = [v for v in adj if rooted_code(adj, v) not in anch]
    tot += n; non += len(bad)
    allanch += (not bad)
    noanchor += (len(bad) == n)
    if all(v in bad for v in adj if len(adj[v]) == 1): noleaf += 1
    for v in bad: maxdeg_non = max(maxdeg_non, len(adj[v]))
print(json.dumps(dict(n=n, trees=ntrees, vertices=tot, non_anchors=non, trees_all_anchor=allanch,
                      trees_with_no_anchor=noanchor, trees_with_no_anchor_leaf=noleaf, max_degree_of_non_anchor=maxdeg_non)))
