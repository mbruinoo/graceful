# checkrule.py -- referee's own re-check of stored labelings (no code shared with folds/).
# usage: python3 checkrule.py trees.txt results.txt RULE
# For each line with "labels:", checks: labels are a permutation of 1..n; edge lengths are 1..n-1 once each;
# taking brackets longest first, bracket n-1 is {1,n} and each later bracket has exactly one used foot;
# and the build obeys RULE (bits: 2 across-only skips, 4 no B, 8 FIFO, 16 LIFO, 32 ENDS), with the
# unused cells = gap + isolated holes, steps S/B (gap end), K1 (one in from a gap end), F (hole).
import sys

def check(edges, lab, rule):
    n = len(lab)
    if sorted(lab) != list(range(1, n + 1)): return 'not a permutation'
    br = {}
    for u, v in edges:
        a, b = sorted((lab[u], lab[v])); k = b - a
        if k in br: return 'length repeated'
        br[k] = (a, b)
    if sorted(br) != list(range(1, n)): return 'lengths not 1..n-1'
    if br[n - 1] != (1, n): return 'longest bracket not {1,n}'
    used = {1, n}; lo, hi = 2, n - 1; holes = []  # holes in creation order
    for t in range(n - 2, 0, -1):
        a, b = br[t]
        if (a in used) == (b in used): return f'growth fails at t={t}'
        x, y = (a, b) if b in used else (b, a)
        if lo <= hi and x == lo:
            typ = 'S' if y > hi else 'B'; lo += 1
        elif lo <= hi and x == hi:
            typ = 'S' if y < lo else 'B'; hi -= 1
        elif lo + 1 <= hi and x == lo + 1 and (y > x or x != hi - 1):
            # (a 3-cell gap with x in the middle is read as an across skip, as tidy.cpp does: r = 1 first)
            typ = 'Ka' if y > x else 'Kb'; holes.append(lo); lo += 2
        elif lo + 1 <= hi and x == hi - 1:
            typ = 'Ka' if y < x else 'Kb'; holes.append(hi); hi -= 2
        elif x in holes:
            typ = 'F'
            if rule & 8 and x != holes[0]: return f'FIFO at t={t}'
            if rule & 16 and x != holes[-1]: return f'LIFO at t={t}'
            if rule & 32 and x not in (min(holes), max(holes)): return f'ENDS at t={t}'
            holes.remove(x)
        else:
            return f'step outside vocabulary at t={t} (x={x})'
        if typ == 'B' and rule & 4: return f'B at t={t}'
        if typ == 'Kb' and rule & 2: return f'back-skip at t={t}'
        used.add(x)
    return ''

trees = [l for l in open(sys.argv[1]) if l.strip()]
res = [l for l in open(sys.argv[2]) if l.startswith('T ')]
rule = int(sys.argv[3]) | 1
assert len(trees) == len(res), (len(trees), len(res))
ok = bad = none = 0
for t, r in zip(trees, res):
    if 'labels:' not in r: none += 1; continue
    el = list(map(int, t.split())); E = list(zip(el[0::2], el[1::2]))
    lab = list(map(int, r.split('labels:')[1].split()))
    why = check(E, lab, rule)
    if why: bad += 1; print('BAD', r.split()[1], why)
    else: ok += 1
print(f'{sys.argv[2]} rule={rule}: ok={ok} bad={bad} without labels={none}')
