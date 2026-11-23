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

def main():
    n = int(sys.argv[1]); tf = sys.argv[2]; af = sys.argv[3]
    R = float("inf") if len(sys.argv) < 5 or sys.argv[4] == "inf" else int(sys.argv[4])
    B = float("inf") if len(sys.argv) < 6 or sys.argv[5] == "inf" else int(sys.argv[5])
    hist = Counter(); none = []; ntrees = 0
    with open(tf) as f1, open(af) as f2:
        for i, (tl, al) in enumerate(zip(f1, f2)):
            tt = tl.split(); assert int(tt[0]) == n
            te = [tuple(map(int, x.split("-"))) for x in tt[1:]]
            assert len(te) == n - 1
            a = al.split(); ntrees += 1
            if a[0] == "NONE":
                hist["NONE"] += 1; none.append(tl.strip()); continue
            if a[0] == "OK":
                r, b = check_labels(n, te, list(map(int, a[1:])))
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
    print(json.dumps(dict(n=n, trees=ntrees, R=str(R), B=str(B), result=dict(sorted(hist.items())), none=none[:20])))

if __name__ == "__main__":
    main()
