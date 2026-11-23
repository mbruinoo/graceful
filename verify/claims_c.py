"""The specific failures claimed in README sections 11-12, each checked by the Rust search and by SAT.
usage: python3 claims_c.py [nosat]"""
import sys, subprocess, time
def spider(legs):
    e = []; nxt = 1
    for L in legs:
        prev = 0
        for _ in range(L):
            e.append((prev, nxt)); prev = nxt; nxt += 1
    return nxt, e
def line(n, e): return str(n) + " " + " ".join(f"{a}-{b}" for a, b in e)
T22 = "22 0-1 1-2 2-3 3-4 4-5 4-6 4-7 4-8 4-9 4-10 0-11 11-12 12-13 13-14 13-15 13-16 13-17 13-18 13-19 12-20 20-21"
T16a = "16 1-0 1-2 0-7 2-3 3-4 4-5 4-6 7-8 7-12 8-9 9-10 9-11 12-13 13-14 13-15"
T16b = "16 1-0 1-2 0-6 0-11 2-3 2-4 2-5 6-7 7-8 7-9 7-10 11-12 12-13 12-14 12-15"
cases = [
 ("S(2,2,2,2), n=9: zero skips (one run)",      line(*spider([2,2,2,2])), "1", "inf", "NONE"),
 ("S(2,2,2,2), n=9: one skip",                  line(*spider([2,2,2,2])), "2", "1",   "OK"),
 ("S(3,3,3), n=10: zero skips",                 line(*spider([3,3,3])),   "1", "inf", "NONE"),
 ("S(3,3,3), n=10: one skip",                   line(*spider([3,3,3])),   "2", "1",   "NONE"),
 ("S(3,3,3), n=10: two skips",                  line(*spider([3,3,3])),   "3", "1",   "OK"),
 ("16-vertex tree a: two runs",                 T16a, "2", "inf", "NONE"),
 ("16-vertex tree a: three runs",               T16a, "3", "inf", "OK"),
 ("16-vertex tree b: two runs",                 T16b, "2", "inf", "NONE"),
 ("16-vertex tree b: three runs",               T16b, "3", "inf", "OK"),
 ("22-vertex tree: at most two single skips",   T22,  "3", "1",   "NONE"),
 ("22-vertex tree: three single skips",         T22,  "4", "1",   "OK"),
 ("22-vertex tree: three runs of any size",     T22,  "3", "inf", "OK"),
]
for name, t, R, B, want in (cases if __name__ == "__main__" else []):
    rs = subprocess.run(["./rs/gsearch", "solve", R, B], input=t + "\n", capture_output=True, text=True).stdout.split()[0]
    msg = f"{name:45s} README: {want:4s}  search: {rs:4s}"
    if "nosat" not in sys.argv:
        t0 = time.time()
        sat = subprocess.run([sys.executable, "sat_check.py", R, B], input=t + "\n", capture_output=True, text=True).stdout.strip()
        sat = {"SAT": "OK", "UNSAT": "NONE"}.get(sat, sat)
        msg += f"  SAT: {sat:4s} ({time.time() - t0:.0f}s)"
        rs = rs if rs == sat else "DISAGREE"
    print(msg, " agree" if rs == want else " *** DISCREPANCY ***", flush=True)
