# Referee check of Lemma C (block corona) and its coverage counts. Usage: lemmaC.py SMAX
import sys
from base import *
SMAX = int(sys.argv[1])
def phi(d): return d if d >= 0 else -d - 1
for s in range(2, SMAX + 1):
    anchored = set(); covered = set(); tested = 0; fails = 0
    for T in growth_labelings(s - 1):
        cf = canon(T, 0); anchored.add(cf)
        par, dep = rooted(T, 0)
        e = {i: abs(i - par[i]) for i in range(1, s)}
        sols = []
        pi = [None] * s
        def rec(i, usedp, usedphi):
            if i == s: sols.append(list(pi)); return
            for p in range(s):
                if p in usedp: continue
                f = phi(p - i)
                if f in usedphi: continue
                if i != 0 and f > e[i] - 1: continue
                pi[i] = p; usedp.add(p); usedphi.add(f)
                rec(i + 1, usedp, usedphi)
                usedp.discard(p); usedphi.discard(f)
        rec(0, set(), set())
        for q in sols:
            tested += 1
            E = [(2 * a, 2 * b) for a, b in T] + [(2 * i, 2 * q[i] + 1) for i in range(s)]
            cor = [(('c', a), ('c', b)) for a, b in T] + [(('c', i), ('l', i)) for i in range(s)]
            if not (is_growth(E, 2 * s - 1) and canon(E, 0) == canon(cor, ('c', 0))): fails += 1
        if sols: covered.add(cf)
    unc = sorted(anchored - covered, key=len)
    print('s', s, 'anchored rooted trees', len(anchored), 'covered by Lemma C', len(covered),
          '(labeling,pi) tested', tested, 'fails', fails, 'an uncovered:', unc[0] if unc else None, flush=True)
