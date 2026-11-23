"""Extra spot checks of README sections 11-12 (not exhaustive families; each case is one tree).
Each line: least number of skips / least number of runs found by exhaustive Rust search, with a time limit.
usage: python3 extras.py [seconds per case]"""
import sys, subprocess
from claims_c import spider, line
from check_cert import check_labels
LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 300
def ask(mode, n, e):
    try:
        out = subprocess.run(["./rs/gsearch", mode], input=line(n, e) + "\n", capture_output=True, text=True,
                             timeout=LIMIT, env={"THREADS": "1"}).stdout.split()
    except subprocess.TimeoutExpired:
        return "timeout"
    val = int(out[1]); r, b = check_labels(n, e, list(map(int, out[2:])))
    assert (r <= val) if mode == "minruns" else (b <= 1 and r <= val + 1)
    return val
def spherical(br):
    e = []; level = [0]; nxt = 1
    for d in br:
        new = []
        for v in level:
            for _ in range(d):
                e.append((v, nxt)); new.append(nxt); nxt += 1
        level = new
    return nxt, e
def hubs(m):   # centre, three arms of length 2, each ending in a hub of m leaves
    e = []; nxt = 1
    for _ in range(3):
        e.append((0, nxt)); e.append((nxt, nxt + 1)); h = nxt + 1; nxt += 2
        for _ in range(m): e.append((h, nxt)); nxt += 1
    return nxt, e
README_SPIDER = {1: [0,0,0,0,0], 2: [0,1,1,1,1], 3: [2,2,2,2,2], 4: [0,2,1,2,2], 5: [0,1,1,2,2], 6: [1,1,1,1,2]}
print("equal-leg spiders, least skips (README 12 table)")
for L in range(1, 7):
    for j, k in enumerate([3, 4, 5, 6, 8]):
        n, e = spider([L] * k)
        got = ask("minskip", n, e) if n <= 40 else "skipped (n > 40)"
        print(f"  L={L} k={k} n={n}: README {README_SPIDER[L][j]}  mine {got}", flush=True)
print("spherically symmetric trees, least runs (README 11: (4,4),(5,5) need 3; (2,2,2),(2,2,2,2) need at most 2)")
for br in [(2,2,2), (4,4), (2,2,2,2), (5,5)]:
    n, e = spherical(br); print(f"  {br} n={n}: least runs {ask('minruns', n, e)}", flush=True)
print("three arms of length 2 ending in hubs of m leaves, least runs (README 11: 1 if m even, 3 if m odd)")
for m in range(2, 9):
    n, e = hubs(m); print(f"  m={m} n={n}: least runs {ask('minruns', n, e)}", flush=True)
