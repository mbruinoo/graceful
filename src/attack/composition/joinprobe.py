# Probe of the two simplest compositions on all pairs of anchored rooted trees with at most NMAX vertices each:
#   (I) identify the anchors v = v'      -> is the glued vertex an anchor?  does the tree have any growth placement?
#   (J) join the anchors by a new edge   -> is v (or v') an anchor?         does the tree have any growth placement?
# Uses ./rootsolve (exhaustive anchored search).  Anchored rooted trees are found by ./rootsolve as well.
import sys, subprocess, itertools
from rooted_gen import rooted_trees, to_parents
from common import canon_rooted, adj_from_edges
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
def solve(lines):
    r = subprocess.run(["./rootsolve"], input="\n".join(lines) + "\n", capture_output=True, text=True)
    return set(l[3:] for l in r.stdout.splitlines() if l.startswith("NO "))
def line(par): return " ".join(map(str, [len(par) + 1] + par))
def reroot(par, r):
    n = len(par) + 1; adj = {i: [] for i in range(n)}
    for i, p in enumerate(par, 1): adj[i].append(p); adj[p].append(i)
    order = [r]; newid = {r: 0}; out = []
    for u in order:
        for v in adj[u]:
            if v not in newid: newid[v] = len(order); order.append(v); out.append(newid[u])
    return out
anch = []
for s in range(1, NMAX + 1):
    ps = [to_parents(t) for t in rooted_trees(s)]
    bad = solve([line(p) for p in ps]) if s > 1 else set()
    anch += [p for p in ps if line(p) not in bad]
print(f"anchored rooted trees with at most {NMAX} vertices: {len(anch)}")
for mode in ("I", "J"):
    jobs = []
    for A, B in itertools.combinations_with_replacement(anch, 2):
        a = len(A) + 1
        if mode == "I": par = A + [0 if p == 0 else p + a - 1 for p in B]
        else:           par = A + [0] + [p + a for p in B]
        jobs.append((A, B, par))
    badroot = solve([line(j[2]) for j in jobs])
    fr = [j for j in jobs if line(j[2]) in badroot]
    extra = ""
    if mode == "J":   # also try the other anchor v' as root
        other = {line(j[2]): line(reroot(j[2], len(j[0]) + 1)) for j in fr}
        bad2 = solve(list(other.values()))
        both = [j for j in fr if other[line(j[2])] in bad2]
        extra = f"; neither v nor v' an anchor: {len(both)}"
        if both:
            j = min(both, key=lambda j: len(j[2])); extra += f" (smallest: {len(j[2])+1} vertices, parents {j[2]})"
    # any growth placement at all?
    none = []
    for j in fr:
        n = len(j[2]) + 1
        if len(solve([line(reroot(j[2], r)) for r in range(n)])) == n: none.append(j)
    sm = min(fr, key=lambda j: len(j[2])) if fr else None
    print(f"({mode}) pairs: {len(jobs)}; v not an anchor of the composite: {len(fr)}"
          + (f" (smallest: {len(sm[2])+1} vertices, parents {sm[2]})" if sm else "") + extra
          + f"; composites with no growth placement at all: {len(none)}")
