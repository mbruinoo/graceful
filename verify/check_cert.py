"""Certificate checker.  Trust base for every 'each tree has ...' claim.

usage: python3 gen.py N | tee >(./rs/gsearch MODE ...  > answers) | ...   (see run_trees.sh)
       python3 check_cert.py N TREEFILE ANSWERFILE [R B]

For each tree (TREEFILE, from networkx) and the answer on the same line number, checks from the
definitions: labels are a bijection onto 1..N; the tree's edges have lengths 1..N-1 once each; for every
k the edges of length >= k form a connected tree (README section 2); and, watching the unused labels
after each bracket longest first, the number of runs never exceeds R and the number of runs of size >= 2
never exceeds B.  For minskip/minruns answers the claimed value is checked as an upper bound.
Prints a histogram.  'NONE' answers are counted and listed (they rest on exhaustive search alone)."""
import sys, json
from collections import Counter
from common import is_growth_by_definition, run_profile, canon

def check_labels(n, tree_edges, labels):
    assert sorted(labels) == list(range(1, n + 1)), "labels not a bijection"
    edges = [(labels[a], labels[b]) for a, b in tree_edges]
    assert is_growth_by_definition(n, edges), "not a growth placement"
    prof = run_profile(n, edges)
    return max(r for r, _ in prof), max(b for _, b in prof)

def check_labels_fast(n, tree_edges, labels):
    """Same verdict as check_labels, using the one-foot form of the definition (README section 2:
    'each bracket, taken longest first, has exactly one foot on a vertex already used') and a bit mask for
    the unused labels.  Used when FAST=1 (large n); every 100th line is then also put through check_labels."""
    assert sorted(labels) == list(range(1, n + 1)), "labels not a bijection"
    edges = sorted(((abs(labels[a] - labels[b]), labels[a], labels[b]) for a, b in tree_edges), reverse=True)
    assert [e[0] for e in edges] == list(range(n - 1, 0, -1)), "lengths are not n-1..1 once each"
    used = 0; unused = ((1 << n) - 1) << 1; mr = mb = 0
    for i, (k, a, b) in enumerate(edges):
        ua = (used >> a) & 1; ub = (used >> b) & 1
        assert (ua + ub == 1) if i else (ua + ub == 0), "bracket does not have exactly one used foot"
        used |= (1 << a) | (1 << b); unused &= ~used
        starts = unused & ~(unused << 1)
        mr = max(mr, starts.bit_count()); mb = max(mb, (starts & (unused >> 1)).bit_count())
    return mr, mb

import os
FAST = os.environ.get("FAST") == "1"
PART, PARTS = map(int, os.environ.get("PART", "0/1").split("/"))   # PART=i/k: only lines with index = i mod k

def main():
    n = int(sys.argv[1]); tf = sys.argv[2]; af = sys.argv[3]
    R = float("inf") if len(sys.argv) < 5 or sys.argv[4] == "inf" else int(sys.argv[4])
    B = float("inf") if len(sys.argv) < 6 or sys.argv[5] == "inf" else int(sys.argv[5])
    hist = Counter(); none = []; ntrees = 0
    with open(tf) as f1, open(af) as f2:
        for i, (tl, al) in enumerate(zip(f1, f2)):
            if i % PARTS != PART: continue
            tt = tl.split(); assert int(tt[0]) == n
            te = [tuple(map(int, x.split("-"))) for x in tt[1:]]
            assert len(te) == n - 1
            a = al.split(); ntrees += 1
            if a[0] == "NONE":
                hist["NONE"] += 1; none.append(tl.strip()); continue
            if a[0] == "OK":
                labs = list(map(int, a[1:]))
                if FAST:
                    r, b = check_labels_fast(n, te, labs)
                    if i % 100 == 0: assert (r, b) == check_labels(n, te, labs)
                else:
                    r, b = check_labels(n, te, labs)
                assert r <= R and b <= B, f"line {i}: runs {r} big {b} exceed ({R},{B})"
                hist["OK"] += 1
            elif a[0] == "S":
                s = int(a[1]); r, b = check_labels(n, te, list(map(int, a[2:])))
                assert b <= 1 and r <= s + 1, f"line {i}: claimed {s} skips, got runs {r} big {b}"
                hist[f"skips={s}"] += 1
            elif a[0] == "R":
                rr = int(a[1]); r, b = check_labels(n, te, list(map(int, a[2:])))
                assert r <= rr
                hist[f"runs={rr}"] += 1
            else:
                raise SystemExit(f"line {i}: unreadable answer {al!r}")
        assert f1.readline() == "" and f2.readline() == "", "files differ in length"
    print(json.dumps(dict(n=n, fast=FAST, part=f"{PART}/{PARTS}", trees=ntrees, R=str(R), B=str(B), result=dict(sorted(hist.items())), none=none[:20])))

if __name__ == "__main__":
    main()
