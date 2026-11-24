"""Main Theorem test.  Reduced problem R(p,q,d) solutions = anchored labellings of L(d;p,q)
with c at the top label m (then all d leaves of v lie below c, i.e. are gaps).
Enumerate them with ./rsolve a for all 1<=p<q, 0<=d, 2d<p, N=p+q+2+d<=NMAX, and test:
q-hub at label 1, or (P,Q)=(1,3).  Also reports counts and runs a few cases outside 2d<p.
Usage: python3 maincheck.py NMAX"""
import sys, subprocess
from lgrid import L

NMAX = int(sys.argv[1])
tot = q1 = p1q3 = viol = 0
allsol = 0
for p in range(1, NMAX):
    for q in range(p + 1, NMAX):
        for d in range(0, NMAX):
            N = p + q + 2 + d
            if N > NMAX: break
            n, E = L(d, p, q)
            inp = f"{n} 0 " + " ".join(f"{u} {v}" for u, v in E) + "\n"
            out = subprocess.run(["./rsolve", "a"], input=inp, capture_output=True, text=True).stdout.split("\n")
            for line in out:
                if not line or line.startswith("END"):
                    if line.startswith("END") and "CAP" in line: print("CAP", p, q, d)
                    continue
                lab = list(map(int, line.split()))
                m = n - 1
                if lab[1] != m: continue
                allsol += 1
                if 2 * d >= p: continue
                tot += 1
                P, Q = lab[2], lab[3]
                if Q == 1: q1 += 1
                elif (P, Q) == (1, 3): p1q3 += 1
                else:
                    viol += 1; print("VIOLATION", p, q, d, lab)
print(f"NMAX={NMAX} reduced solutions with p<q (any d)={allsol}; with 2d<p: {tot}, Q=1: {q1}, (P,Q)=(1,3): {p1q3}, violations: {viol}")
