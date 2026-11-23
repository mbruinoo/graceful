"""Check `gsearch spider N free|zig` output (README sections 12-13).
usage: python3 check_spider.py N free|zig FILE
Each 'OK' line is a certificate: centre at label 0, one list of labels per leg going outward.  Checked:
all labels distinct and equal to 0..m; edge lengths all distinct (hence 1..m); lengths strictly decrease
outward along each leg (growth placement anchored at the centre = valid deal); for zig, moves alternate
up, down, up, ...   The set of leg patterns is compared with an independent partition generator."""
import sys, json
def parts(m, mx):
    if m == 0: yield (); return
    for p in range(min(m, mx), 0, -1):
        for r in parts(m - p, p): yield (p,) + r
def py_search(legs, zig):
    """slow independent exhaustive search, used for small cases only"""
    m = sum(legs); k = len(legs)
    tip = [0] * k; done = [0] * k; last = [0] * k; used = {0}
    def rec(w):
        if w == 0: return True
        seen = set()
        for i in range(k):
            if done[i] == legs[i]: continue
            key = (legs[i], done[i], tip[i], last[i])
            if key in seen: continue
            seen.add(key)
            for d in (1, -1):
                if zig and done[i] and d == last[i]: continue
                t = tip[i] + d * w
                if t < 1 or t > m or t in used: continue
                o = (tip[i], last[i]); tip[i] = t; last[i] = d; done[i] += 1; used.add(t)
                if rec(w - 1): return True
                used.discard(t); done[i] -= 1; tip[i], last[i] = o
        return False
    return rec(m)
if __name__ == "__main__":
    n = int(sys.argv[1]); zig = sys.argv[2] == "zig"; m = n - 1
    want = sorted(p for p in parts(m, m) if len(p) >= 3)
    got = []; none = []
    for line in open(sys.argv[3]):
        head, body = line.split("|")
        legs = tuple(map(int, head.split())); got.append(legs)
        if body.split()[0] == "NONE": none.append(legs); continue
        paths = [list(map(int, p.split(","))) for p in body.split("OK")[1].split(";")]
        assert tuple(map(len, paths)) == legs
        labels = [0] + [x for p in paths for x in p]
        assert sorted(labels) == list(range(m + 1))
        lens = []
        for p in paths:
            seq = [0] + p; d = [seq[i + 1] - seq[i] for i in range(len(p))]
            assert all(abs(d[i]) > abs(d[i + 1]) for i in range(len(d) - 1))
            if zig: assert all((d[i] > 0) == (i % 2 == 0) for i in range(len(d)))
            lens += [abs(x) for x in d]
        assert sorted(lens) == list(range(1, m + 1))
    assert sorted(got) == want
    res = dict(n=n, kind=sys.argv[2], spiders=len(got), with_deal=len(got) - len(none), none=["S" + str(l).replace(" ", "") for l in none])
    if len(sys.argv) > 4:   # cross-check every answer with the slow Python search
        res["python_search_agrees"] = all(py_search(l, zig) == (l not in none) for l in got)
    print(json.dumps(res))
