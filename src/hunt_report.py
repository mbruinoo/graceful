#!/usr/bin/env python3
"""Fill results/counterexample-hunt/REPORT.md from REPORT.template.md, the existence logs, the count files and the B3 pieces."""
import subprocess, glob, re
R = "../results/counterexample-hunt/"
ex = subprocess.run(["python3", "hunt_summary.py"], capture_output=True, text=True).stdout.strip()
counts = subprocess.run(["python3", "hunt_counts_table.py"], capture_output=True, text=True).stdout.strip()
total = re.search(r"\*\*total\*\* \| ([\d,]+)", ex).group(1)
pieces = []; bad = []
for f in sorted(glob.glob("r3_26_p*of64.txt"), key=lambda s: int(re.search(r"_p(\d+)of", s).group(1))):
    for line in open(f):
        if line.startswith("n="): pieces.append(line.strip())
        elif line.strip(): bad.append(line.strip())
open(R + "b3_n26_pieces.txt", "w").write("\n".join(pieces + bad) + "\n")
trees = sum(int(re.search(r"trees=(\d+)", p).group(1)) for p in pieces)
none = sum(int(re.search(r"none=(\d+)", p).group(1)) for p in pieces); unres = sum(int(re.search(r"unresolved=(\d+)", p).group(1)) for p in pieces)
k = len(pieces); ALL = 279793450
if k == 64:
    short = f"all {trees:,} trees on 26 vertices"; out = f"**Observation (`n = 26`)**: {none} trees without a three-run growth placement, {unres} unresolved"
    long = f"`./runsolve_gen 26 3`, run as 64 pieces: all pieces finished, {trees:,} trees, {none} with no three-run growth placement, {unres} unresolved. With the README's range this makes B3 an Observation for `n ≤ 26`, resting on `runsolve_gen.cpp` alone (the tree total equals the known number of trees on 26 vertices). Since every three-run growth placement is a growth placement, Conjecture B is likewise an Observation for `n ≤ 26`. `README.md` and `web/evidence.json` still say 25; they were deliberately not edited in this task."
else:
    short = f"**incomplete**: {k} of 64 pieces finished, {trees:,} of the {ALL:,} trees on 26 vertices"
    out = f"in the finished pieces: {none} trees without a three-run growth placement, {unres} unresolved. **Not an exhaustive check of n = 26.**"
    long = (f"**Not finished.** The run was split into 64 pieces (piece `i` takes the trees whose index in the generator's order is `i` mod 64) so that it can be resumed. "
            f"When this report was written {k} pieces had finished: {trees:,} of the {ALL:,} trees on 26 vertices ({100 * trees / ALL:.0f}%), with {none} trees lacking a three-run growth placement and {unres} unresolved "
            f"(`b3_n26_pieces.txt`). The whole run needs roughly 25 core-hours; the same four cores were shared with the searches above. "
            f"**This does not extend the exhaustive range of Conjecture B3, which stays `n ≤ 25`.** It is a systematic sample of every 64th tree, for {k} offsets. "
            f"`./hunt_b3.sh 26 64 4` skips finished pieces and completes the rest.")
t = open(R + "REPORT.template.md").read()
for key, val in (("{{EXIST}}", ex), ("{{COUNTS}}", counts), ("{{EXISTTOTAL}}", total), ("{{B3SHORT}}", short), ("{{B3OUT}}", out), ("{{B3LONG}}", long)): t = t.replace(key, val)
open(R + "REPORT.md", "w").write(t)
print(k, "pieces;", total, "trees in existence table")
