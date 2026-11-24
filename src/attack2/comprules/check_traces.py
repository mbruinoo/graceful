"""Check the two printed derivations (S(2,2,2), S(3,3,3)), the worked example of Rule B and the two
smallest non-caterpillar families of results/composition/REPORT.md, step by step, from the definitions."""
from gp import *
def parse(s):
    br = [tuple(map(int, x.split('-'))) for x in s.split()]
    m = len(br); P = [None] * (m + 1)
    for a, b in br: P[b - a] = a
    assert None not in P[1:], s
    return P, m
def band(j, v): return j - v if v <= j else v - j - 1
def B(s, design, t):
    P, m = parse(s); new, old, ell = info(P, m)
    bands = [band(j, v) for j, v in enumerate(design)]
    assert sorted(bands) == list(range(m)) and all(v == 0 or bands[j] < ell[v] for j, v in enumerate(design)), 'design not valid'
    Q = [None] * (m * t + 1)
    for i in range(1, m + 1): Q[t * i] = t * P[i]
    for j, v in enumerate(design):
        for d in range(1, t):
            a, b = sorted((t * v, j * t + d)); assert Q[b - a] is None; Q[b - a] = a
    assert is_growth(Q, m * t)
    return fmt(Q, m * t)
def C(s):
    P, m = parse(s); return fmt(complement(P, m), m)
def T(sf, sh, k, shift):
    f, mf = parse(sf); h, mh = parse(sh)
    assert k < mf and k < mh
    Ff = free_at(f, mf, k); Fh = free_at(h, mh, k)
    assert frozenset(x + shift for x in Fh) == Ff, 'hypothesis 1'
    new, old, ell = info(h, mh)
    for i in range(1, k + 1):
        if old[i] not in Fh: assert 0 <= old[i] + shift <= mf and old[i] + shift not in Ff, 'hypothesis 2'
    Q = f[:]
    for i in range(1, k + 1): Q[i] = h[i] + shift
    assert is_growth(Q, mf)
    return fmt(Q, mf)
def spider(legs):
    E = []; c = 0; nxt = 1
    for L in legs:
        prev = 0
        for _ in range(L): E.append((prev, nxt)); prev = nxt; nxt += 1
    return tree_canon(E)
def shape(s): P, m = parse(s); return tree_canon(edges(P, m))
ok = True
def eq(a, b, what):
    global ok
    print(('ok   ' if a == b else 'DIFF ') + what + (': ' + a if a == b else ': got %s, report prints %s' % (a, b))); ok &= (a == b)
# worked example of Rule B
eq(B('0-2 0-1', [2, 1], 3), '0-6 1-6 2-6 0-3 3-5 3-4', 'Rule B example t=3')
# S(2,2,2)
s1 = '0-2 0-1'
s2 = B(s1, [2, 1], 2); eq(s2, '0-4 1-4 0-2 2-3', '#2')
s3 = T('0-5 0-4 0-3 0-2 0-1', s2, 3, 0); eq(s3, '0-5 0-4 1-4 0-2 2-3', '#3')
s4 = C(s3); eq(s4, '0-5 1-5 1-4 3-5 2-3', '#4')
s5 = T('0-6 0-5 0-4 0-3 0-2 0-1', s4, 4, 0); eq(s5, '0-6 0-5 1-5 1-4 3-5 2-3', '#5')
eq(shape(s5), spider([2, 2, 2]), '#5 draws S(2,2,2)')
# S(3,3,3)
t1 = '0-4 0-3 0-2 0-1'
t2 = B(t1, [4, 4, 4, 3], 2); eq(t2, '0-8 1-8 0-6 3-8 0-4 5-8 0-2 6-7', '#2')
t3 = C(t2); eq(t3, '0-8 0-7 2-8 0-5 4-8 0-3 6-8 1-2', '#3')
stair = '0-9 0-8 1-8 1-7 1-6 1-5 1-4 1-3 1-2'      # a staircase beginning 0-9 0-8 1-8
P, m = parse(stair); assert is_staircase(P, m)
t4 = T(stair, t3, 6, 1); eq(t4, '0-9 0-8 1-8 3-9 1-6 5-9 1-4 7-9 2-3', '#4')
t5 = B(t1, [4, 4, 2, 2], 2); eq(t5, '0-8 1-8 0-6 3-8 0-4 4-7 0-2 4-5', '#5')
t6 = '0-3 0-2 0-1'
t7 = B(t6, [3, 0, 2], 2); eq(t7, '0-6 1-6 0-4 0-3 0-2 4-5', '#7')
t8 = C(t7); eq(t8, '0-6 0-5 2-6 3-6 4-6 1-2', '#8')
t9 = None
for s in range(-8, 9):
    try: t9 = T(t5, t8, 2, s)
    except AssertionError: continue
    print('     (#9 uses shift %d)' % s); break
eq(str(t9), '0-8 1-8 0-6 3-8 0-4 4-7 5-7 2-3', '#9')
t10 = None
for s in range(-9, 10):
    try: t10 = T(t4, t9, 4, s)
    except AssertionError: continue
    print('     (#10 uses shift %d)' % s); break
eq(str(t10), '0-9 0-8 1-8 3-9 1-6 0-4 4-7 5-7 2-3', '#10')
eq(shape(t10), spider([3, 3, 3]), '#10 draws S(3,3,3)')
# remark 4
P, m = parse('0-6 0-5 1-5 0-3 4-6 2-3'); print('remark 4 placement is growth:', is_growth(P, m), ' draws S(2,2,2):', shape('0-6 0-5 1-5 0-3 4-6 2-3') == spider([2, 2, 2]))
# the two smallest non-caterpillar families (p = 5)
for s, des in (('0-4 0-3 0-2 1-2', [4, 4, 4, 3]), ('0-4 0-3 0-2 0-1', [4, 1, 0, 2])):
    for t in (2, 3, 4):
        q = B(s, des, t); Q, mq = parse(q)
        print('family', s, des, 't=%d' % t, 'growth, caterpillar: %s' % is_caterpillar(edges(Q, mq)), ' S(2,2,2,1,1): %s' % (shape(q) == spider([2, 2, 2, 1, 1])))
print('ALL STEPS AS PRINTED' if ok else 'SOME STEP DIFFERS')
