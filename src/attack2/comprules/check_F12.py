"""F1 and F2: identify two anchors / join two anchors by an edge.  Exhaustive over rooted trees with
at most NMAX vertices each; anchor tests by ./rootsolve (exhaustive search from the definition).
usage: python3 check_F12.py [NMAX=7]"""
import sys, subprocess
from functools import lru_cache
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7

@lru_cache(None)
def rooted(n):
    """All rooted trees on n vertices as canonical nested tuples (sorted tuples of subtrees)."""
    if n == 1: return [()]
    out = set()
    def parts(left, maxsize, acc):
        if left == 0:
            out.add(tuple(sorted(acc))); return
        for s in range(min(left, maxsize), 0, -1):
            for t in rooted(s):
                parts(left - s, s, acc + [t])
    parts(n - 1, n - 1, [])
    return sorted(out)

def parents(t):
    """parent array (root 0, BFS-free preorder) of a nested tuple."""
    par = []
    def walk(node, me):
        for c in node:
            par.append(me); idx = len(par); walk(c, idx)
    walk(t, 0)
    return par          # par[i-1] = parent of vertex i

def solve(queries):
    inp = '\n'.join('%d %s' % (len(q) + 1, ' '.join(map(str, q))) for q in queries) + '\n'
    out = subprocess.run(['./rootsolve'], input=inp, capture_output=True, text=True).stdout.split()
    return [x == '1' for x in out]

def show(t): return '(' + ''.join(show(c) for c in t) + ')'

allr = [t for n in range(1, NMAX + 1) for t in rooted(n)]
print('rooted trees with 1..%d vertices:' % NMAX, len(allr), [len(rooted(n)) for n in range(1, NMAX + 1)])
anch = solve([parents(t) for t in allr])
A = [t for t, a in zip(allr, anch) if a]
print('anchored (root is an anchor):', len(A), ' non-anchors:', [show(t) for t, a in zip(allr, anch) if not a])
size = lambda t: 1 + sum(size(c) for c in t)

# F1: identify the roots
A2 = [t for t in A if size(t) >= 2]
pairs = [(A2[i], A2[j]) for i in range(len(A2)) for j in range(i, len(A2))]
res = solve([parents(tuple(sorted(a + b))) for a, b in pairs])
fails = [(a, b) for (a, b), r in zip(pairs, res) if not r]
print('F1: unordered pairs:', len(pairs), ' merged vertex not an anchor:', len(fails))
fails.sort(key=lambda ab: size(ab[0]) + size(ab[1]))
for a, b in fails[:3]: print('   n=%d  %s + %s' % (size(a) + size(b) - 1, show(a), show(b)))

# F2: join the roots by an edge; test both ends
pairs = [(A[i], A[j]) for i in range(len(A)) for j in range(i, len(A))]
ra = solve([parents(tuple(sorted(a + (b,)))) for a, b in pairs])      # rooted at root of a
rb = solve([parents(tuple(sorted(b + (a,)))) for a, b in pairs])      # rooted at root of b
one = [(a, b) for (a, b), x, y in zip(pairs, ra, rb) if not (x and y)]
both = [(a, b) for (a, b), x, y in zip(pairs, ra, rb) if not x and not y]
print('F2: unordered pairs:', len(pairs), ' some end not an anchor:', len(one), ' neither end an anchor:', len(both))
one.sort(key=lambda ab: size(ab[0]) + size(ab[1])); both.sort(key=lambda ab: size(ab[0]) + size(ab[1]))
for a, b in one[:3]: print('   one end fails: n=%d  %s -- %s' % (size(a) + size(b), show(a), show(b)))
for a, b in both[:3]: print('   both ends fail: n=%d  %s -- %s' % (size(a) + size(b), show(a), show(b)))
