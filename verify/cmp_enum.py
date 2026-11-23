"""Compare `gsearch enum N R B` output with networkx's trees and (if present) the Python reference.
usage: python3 cmp_enum.py N ENUMFILE [reffile]   prints shape counts, run/skip histograms, anchor table."""
import sys, json
from collections import Counter
from gen import trees, KNOWN
from common import adjacency, rooted_code, canon

def paren_to_edges(s):
    edges = []; stack = []; nxt = 0
    for ch in s:
        if ch == "(":
            nxt += 1
            if stack: edges.append((stack[-1], nxt))
            stack.append(nxt)
        else:
            stack.pop()
    return nxt, edges

n = int(sys.argv[1])
shapes = {}; anchors = set(); head = None
for line in open(sys.argv[2]):
    t = line.split()
    if t[0] == "N": head = line.strip()
    elif t[0] == "T":
        m, e = paren_to_edges(t[1]); assert m == n
        c = canon(n, e); assert c not in shapes
        shapes[c] = (int(t[2]), int(t[3]), int(t[4]))
    elif t[0] == "A":
        m, e = paren_to_edges(t[1]); anchors.add(rooted_code(adjacency(n, e), 1))
res = dict(n=n, header=head, shapes_found=len(shapes), placements=sum(v[0] for v in shapes.values()))
runs = Counter(); skips = Counter(); missing = 0
tot = non = allanch = noleaf = 0; maxdeg = 0; ntrees = 0
for e in trees(n):
    e = [(a + 1, b + 1) for a, b in e]; ntrees += 1
    c = canon(n, e)
    if c not in shapes: missing += 1; continue
    runs[shapes[c][1]] += 1; skips[shapes[c][2]] += 1
    adj = adjacency(n, e)
    bad = [v for v in adj if rooted_code(adj, v) not in anchors]
    tot += n; non += len(bad); allanch += (not bad)
    if all(v in bad for v in adj if len(adj[v]) == 1): noleaf += 1
    for v in bad: maxdeg = max(maxdeg, len(adj[v]))
assert ntrees == KNOWN[n]
res.update(trees=ntrees, trees_missing=missing, by_min_runs=dict(sorted(runs.items())), by_min_skips=dict(sorted(skips.items())),
           vertices=tot, non_anchors=non, trees_all_anchor=allanch, trees_no_anchor_leaf=noleaf, max_degree_non_anchor=maxdeg)
if len(sys.argv) > 3:
    ref = json.load(open(sys.argv[3]))
    ok = set(ref["anchors"]) == anchors and all(shapes[c][1] == r for c, r in ref["minruns"].items()) \
         and len(ref["minruns"]) == len(shapes) and all(shapes[c][2] == ref["minskip"].get(c, 255) for c in shapes)
    res["equals_python_reference"] = ok
print(json.dumps(res))
