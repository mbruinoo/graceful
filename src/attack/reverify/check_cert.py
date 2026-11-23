#!/usr/bin/env python3
"""Certificate checker, straight from README section 1/2/11 definitions.  No search.

Usage: check_cert.py treefile outfile [R=r] [H=h] [SIDE=s]
  treefile: lines "n u1 v1 ..." ; outfile: lines "OK l0 .. l(n-1)" or "NONE" (same order).
For every OK line it verifies, using only the definitions:
  * labels are a permutation of 1..n;
  * the tree's edges have lengths |l(u)-l(v)| = 1..n-1, each once (so it is a placement:
    bracket k sits at p_k = min label of the edge of length k, 1 <= p_k <= n-k);
  * growth: taking brackets k = n-1, n-2, ..., 1, each has exactly one foot on a label
    already used (the first has none used and must be {1,n});
  * if R is given: after every bracket the unused labels form at most R runs;
  * if H is given: after every bracket the unused labels have at most one run of size > 1
    and at most H+1 runs in total (one run plus at most H isolated single labels);
    SIDE=1: singles all on one side of the big run; SIDE=2: at most one on each side.
  * TRACK=1 (with H): the tracked-main-run reading described in gp.cpp; the checker follows
    every possible reading of the build (a small set of states (a,d,left skips,right skips)).
Prints counts of verified / NONE lines."""
import sys

def runs_of(unused_sorted):
    runs = []
    for x in unused_sorted:
        if runs and runs[-1][1] == x - 1:
            runs[-1][1] = x
        else:
            runs.append([x, x])
    return runs

def shape_ok(used, n, R, H, SIDE):
    runs = runs_of([x for x in range(1, n + 1) if x not in used])
    if R is not None and len(runs) > R:
        return False
    if H is not None:
        big = [r for r in runs if r[1] > r[0]]
        if len(big) > 1 or len(runs) > H + 1:
            return False
        if SIDE and len(big) == 1:
            nb = sum(1 for r in runs if r[1] < big[0][0])
            na = sum(1 for r in runs if r[0] > big[0][1])
            if SIDE == 1 and nb and na:
                return False
            if SIDE == 2 and (nb > 1 or na > 1):
                return False
    return True

def side_ok(sl, sr, H, SIDE):
    if sl + sr > H: return False
    if SIDE == 1 and sl and sr: return False
    if SIDE == 2 and (sl > 1 or sr > 1): return False
    return True

def tracked_ok(n, order, H, SIDE):
    """order = labels placed after the top bracket, in build order."""
    states = {(1, n, 0, 0)}
    for x in order:
        new = set()
        for a, d, sl, sr in states:
            if x < a: new.add((a, d, sl - 1, sr))
            elif x > d: new.add((a, d, sl, sr - 1))
            else:
                s1, s2 = x - a - 1, d - 1 - x
                if s1 <= 1 and side_ok(sl + s1, sr, H, SIDE): new.add((x, d, sl + s1, sr))
                if s2 <= 1 and side_ok(sl, sr + s2, H, SIDE): new.add((a, x, sl, sr + s2))
        states = new
        if not states: return False
    return True

def verify(n, edges, lab, R=None, H=None, SIDE=0, TRACK=0):
    if sorted(lab) != list(range(1, n + 1)):
        return "labels not a permutation"
    bylen = {}
    for u, v in edges:
        d = abs(lab[u] - lab[v])
        if d in bylen:
            return "repeated length"
        bylen[d] = (min(lab[u], lab[v]), max(lab[u], lab[v]))
    if sorted(bylen) != list(range(1, n)):
        return "lengths not 1..n-1"
    used = set(); order = []
    for k in range(n - 1, 0, -1):
        a, b = bylen[k]
        assert b - a == k and 1 <= a <= n - k
        cnt = (a in used) + (b in used)
        if k == n - 1:
            if cnt != 0 or (a, b) != (1, n):
                return "top bracket"
        elif cnt != 1:
            return f"bracket {k} has {cnt} used feet"
        if k < n - 1: order.append(b if a in used else a)
        used.add(a); used.add(b)
        if not TRACK and not shape_ok(used, n, R, H, SIDE):
            return f"shape violated after bracket {k}"
    if TRACK and not tracked_ok(n, order, H, SIDE):
        return "no tracked reading"
    return None

def main():
    tf, of = sys.argv[1], sys.argv[2]
    R = H = None; SIDE = 0; TRACK = 0
    for a in sys.argv[3:]:
        if a.startswith("R="): R = int(a[2:])
        if a.startswith("H="): H = int(a[2:])
        if a.startswith("SIDE="): SIDE = int(a[5:])
        if a.startswith("TRACK="): TRACK = int(a[6:])
    ok = none = 0
    with open(tf) as f, open(of) as g:
        tl = [l for l in f if l.strip()]
        ol = [l for l in g if l.strip()]
    assert len(tl) == len(ol), (len(tl), len(ol))
    for t, o in zip(tl, ol):
        x = list(map(int, t.split()))
        n = x[0]
        edges = [(x[1 + 2 * i], x[2 + 2 * i]) for i in range(n - 1)]
        assert len(x) == 2 * n - 1
        if o.startswith("NONE"):
            none += 1
            continue
        lab = list(map(int, o.split()[1:]))
        assert len(lab) == n
        err = verify(n, edges, lab, R, H, SIDE, TRACK)
        if err:
            print("BAD CERTIFICATE:", t.strip(), o.strip(), err)
            sys.exit(1)
        ok += 1
    print(f"{tf}: trees {len(tl)}, certificates verified {ok}, NONE {none} (R={R} H={H} SIDE={SIDE} TRACK={TRACK})")

if __name__ == "__main__":
    main()
