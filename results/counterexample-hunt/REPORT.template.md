# Counterexample hunt for Conjecture B (growth placements), 26 ≤ n ≤ 70

**Result: nothing was found.** No tree examined lacks a growth placement, and no family
examined has a number of growth placements that decreases or stays bounded as the family
grows. Conjecture B is still a conjecture; everything below is computer evidence, not
proof, except the one remark in section 5 that follows from Lemma 6 of the README.

Status words are those of `CLAUDE.md`. "Growth placement", "anchor", "run" are as in the
README. All programs are in `src/`; all numbers below come from the commands in section 8.

## 1. What was done, in one table

| step | scope | outcome |
|---|---|---|
| exact count of growth placements, every tree | all trees on `n ≤ 16` (19,320 trees at 16) | **Observation (`n ≤ 16`)**: every tree has one; the least number among non-caterpillars is 6, 10, 14, 8, 14, 16, 18, 18, 24, 28 for `n = 7..16` |
| exact count along one-parameter families | 67 families (two of them generated twice under different names) and a list of spherically symmetric trees; members counted up to `n = 70` where the counter could reach (section 3) | every family grows; the slowest grows linearly (270 placements at `n = 70`) |
| one giant hub on every small core | all 270 cores on 6..10 vertices, hub of 20 and of 40 leaves | of the 155 cores counted at both sizes, none has fewer placements with the larger hub (section 4) |
| existence, complete deterministic search | {{EXISTTOTAL}} structured trees with `26 ≤ n ≤ 70` in 8 classes (section 6) | a growth placement was found and verified for every one; none unresolved |
| Conjecture B3 at `n = 26` | {{B3SHORT}} | {{B3OUT}} |

## 2. Programs and how far they can be trusted

* `src/growfam.cpp` — exact number of growth placements of a given tree, and existence
  search. Longest bracket first; unbuilt branches of the same shape on the same vertex are
  tried once (the `subId` idea of `runsolve128.cpp`), which makes the search count
  placements (labelings up to automorphism) exactly; completed states are remembered in a
  table keyed by a 128-bit hash of (used labels, open vertices with their labels and
  unbuilt branch shapes). A hash collision would give a wrong count; none is expected
  below about 2^32 states, but this is a probabilistic statement.
* `src/growcheck.cpp` — a second counter written independently, on a different principle
  (README Theorem 7: label the vertices in breadth-first order of the tree, require edge
  lengths to decrease away from the vertex labelled 1; no table, no symmetry pruning,
  divide by `|Aut T|` at the end).
* Checks made:
  * `growfam all n` reproduces the README totals 116, 412, 1764, 7888, 40220, 214600,
    1275368 for `n = 7..13`, the least non-caterpillar count printed by `src/scarce.py` at
    `n = 12`, and the README anchor table (non-anchors 6, 19, 37, 84 at
    `n = 8, 10, 12, 14`; trees with no anchor leaf at `n = 10, 12, 15`).
  * `growfam` and `growcheck` give the same count for each of 992 trees: every tree on
    7..12 vertices and 19 family members up to 19 vertices.
  * Every placement reported by the existence search is re-checked from the definition
    (labels `1..n` once each; taking lengths `n−1, …, 1`, each edge has exactly one foot
    already used) before it is counted as found.
* Not independently re-implemented: counts for `n > 19`, and the tree generators
  (`treegen.h` is the repository's; `hubscan_lib.py` is new and was checked only through
  the tree totals 11, 23, 47, 106, 235, 551 for `n = 7..12`).

## 3. How many growth placements: families

The scarcest non-caterpillar on `n` vertices, from the exhaustive counts:

| n | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|
| least count | 6 | 10 | 14 | 8 | 14 | 16 | 18 | 18 | 24 | 28 |
| tree | `S(2,2,2)` | H(2) | `S(2,2,2,2)` | `S(3,3,3)` | H(5) | H(6) | three hubs of 3 leaves round a centre | H(8) | H(9) | H(10) |

H(m) = `hublegs(m,2,2)`: a centre carrying two legs of length 2 and one neighbour that
carries `m` leaves. From `n = 11` on it is the scarcest non-caterpillar at every size
checked except 13 (where H(7) has 24).

**Observation (`7 ≤ n ≤ 70`, exact counts).** H(m) has 6, 10, 16, 12, 14, 16, 24, 18,
24, 28, 28, 28, 38, 34, … placements for `m = 1, 2, …`; 52 at `n = 26`, 270 at
`n = 70`. The count is not monotone (it drops 11 times in 64 steps, with period 6 in
`m`) but grows by about 4 per vertex. By the remark in section 5, every H(m) has a
growth placement: that is **Proved** (it follows from Lemma 6), not just checked.

All families counted (`src/hunt_survey.sh`; "members counted" stops where one tree
needed more than the node budget, twice in a row; "drops" counts members with fewer
placements than the previous member):

{{COUNTS}}

Reading of the table:

* **No family has a bounded or decreasing count.** The slowest growth is linear
  (`hublegs_m_2_2` = `forkhub_1_m_2`, the same trees generated two ways, with the same
  numbers). Families with one giant hub grow polynomially in the hub size; families
  with several equal deep branches grow exponentially (three legs: about ×3 per unit of
  leg length; `k` legs of length 2: ×6 to ×7 per leg).
* **Dips are local.** `forkhub_2_m_3` (a path of 2 edges with two legs of length 3 at
  one end and `m` leaves at the other) runs 8, 44, 54, 36, 46, 28, 40, 40, 34, 50, 58,
  68, … and then grows; its first member is `S(3,3,3)` and its third is the 12-vertex
  tree with no anchor leaf. `hubspider_3_1_m` (three hubs of `m` leaves round a centre)
  has a parity effect, 20, 18, 168, 60, 842, 370, 4300, 2284, …, the odd members being
  scarcer until `m = 17`; it still grows by a factor of about 6 per two steps.
* **The 22-vertex tree of README section 11** is `dbl(6,7,1,2)` and has 926 growth
  placements. Its family in `m` (hub size) runs 44, 96, 204, 280, 512, 926, 1648, 3166,
  … (`dbl_m_7_1_2`), and the eleven neighbouring families counted behave the same way.
* **Spherically symmetric trees** (`sph.txt`): counted only up to 23 vertices —
  `(2,2)`: 6, `(3,3)`: 18, `(4,4)`: 9844, `(2,2,2)`: 370, `(3,2,2)`: 1,062,292,
  `(2,2,3)`: 2822, `(2,2,4)`: 20400, `(4,3)`: 840, `(3,4)`: 168, `(5,2)`: 1940,
  `(2,5)`: 6. Larger ones exceeded the budget of the counter; they are covered by the
  existence search of section 6 only.

## 4. One giant hub on every small core

For every rooted tree `A` on `a = 6..10` vertices whose root has no leaf child (270 trees
that are not caterpillars), hang `m` leaves on the root (`src/hunt_hubcores.sh`). With
`m = 20` and `m = 40`:

* 155 cores were counted at both sizes (the rest exceeded 30,000,000 nodes at one of
  them, i.e. have very many placements). For all 155 the count at `m = 40` is larger.
* The least counts are 52 → 132 (`a = 6`, the tree H(m)), 178 → 606 (`a = 7`),
  468 → 1806 (`a = 8`): a larger core means more placements, not fewer.

Two giant hubs on a small core (`python3 hubscan.py two s m m | ./growfam count`, cores
on `s = 5..8` vertices, `m = 9, 10`; and two cores followed to `m = 31`): the least
counts found were 142 and 170 (`s = 5`, `n = 23, 25`), 200 and 204 (`s = 7`); followed
in `m` these two families run 30, 48, 64, 76, 92, 106, 124, …, 974 (`n = 67`) and
62, 68, 102, 124, 138, 158, …, 1390 (`n = 69`), growing roughly quadratically. These
scans were run by hand and their output was not kept as files.

## 5. Why hubs cannot produce a counterexample, and what to look at instead

**Remark (follows from README Lemma 6; Proved).** Write `A_v(T)` for the number of growth
placements of `T` with `v` at label 1. If `T'` is `T` plus a new leaf at `v`, then
`A_v(T') ≥ A_v(T)`.

*Proof.* Lemma 6 keeps all labels and adds the bracket `{1, n+1}`; `v` keeps label 1, and
different placements of `T` give different placements of `T'`. ∎

So once a vertex is an anchor, hanging more leaves on it can never remove the last
growth placement, and the count with that vertex at label 1 never decreases. This is
what the tables of sections 3 and 4 show for every hub family, and it settles H(m)
for all `m` (the hub is an anchor already at `m = 1`, where the tree is `S(2,2,2)`).

A counterexample is a tree with **no anchor at all**. The useful near-miss statistic is
therefore not the number of placements but the number of non-anchors
(`growfam all n`, and `ANCHORS=1 growfam count`):

| n | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|
| vertices over all trees | 77 | 184 | 423 | 1,060 | 2,585 | 6,612 | 16,913 | 44,226 | 116,115 | 309,120 |
| non-anchors | 4 | 6 | 11 | 19 | 21 | 37 | 54 | 84 | 117 | 154 |
| trees with a non-anchor | 2 | 5 | 7 | 11 | 17 | 26 | 43 | 67 | 93 | 125 |
| trees with no anchor leaf | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| trees with at least half the vertices non-anchors | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

(The rows for `n = 8, 10, 12, 14` agree with README section 7; 9, 11, 13, 15, 16 are
new.) **Observation (`n ≤ 16`)**: the fraction of non-anchors falls from 5% to 0.05%,
and the only tree in which half the vertices are non-anchors is `S(3,3,3)` (6 of 10).
The three trees with no anchor leaf are `S(3,3,3)`, `forkhub(2,3,3)` on 12 vertices and
a 15-vertex tree (edges `0-1 1-2 2-3 3-4 4-5 3-6 6-7 0-8 8-9 9-10 10-11 11-12 10-13
13-14`); none of them is close to having no anchor (6, 5 and 4 non-anchors).

In the families of section 3 the largest proportions of non-anchors are 6 of 10
(`S(3,3,3)`), 5 of 14 (H(8)) and 3 of 19 and more (the leaves of `S(L,L,L)` for
`L = 6..10, 12, 13`); in every family the proportion falls as the family grows. No
family was found in which anchors become rare.

## 6. Existence for whole classes, 26 ≤ n ≤ 70

`growfam exist` is deterministic. Each attempt is a depth-first search that is complete
unless it reaches its node budget: first with at most 1, 2, 3 runs of unused labels,
then rounds with at most 3 runs, at most 4 runs, and unrestricted, in fixed-seed
shuffled orders with doubling budgets, and finally unrestricted in natural order with no
budget. "None" would only ever be reported by a complete unrestricted search. Classes
(`src/huntsets.py`; caterpillars skipped):

* `spider1` — `k ≥ 3` equal legs; `spider2` — legs of two lengths.
* `kbranch` — a centre joined to `k ≥ 3` copies of **every** rooted tree on 2..9
  vertices; `kbranch+` — the same plus a pendant path of 1, 2 or 3 edges at the centre.
* `sph` — every spherically symmetric tree (all branching sequences).
* `corona` — every tree on 3..9 vertices with `m` leaves, or a pendant path of 2..4
  edges, on every vertex; `leafhubs` — `m` further leaves on every leaf.
* `dbl` — the relatives of the 22-vertex tree: two hubs of `m ≥ 2` leaves joined by a
  path of 2..10 edges, with a pendant path of 1..4 edges anywhere on it.

{{EXIST}}

The classes overlap (for example `kbranch` with 2-vertex branches is `spider1` with legs
of length 2, and some `kbranch` trees are spherically symmetric), so the total counts
some trees more than once. "Found within" is the first attempt that succeeded, not the least number of runs
needed, except that the columns for 1, 2 and 3 runs are preceded by complete searches
with fewer runs whenever those stayed within budget. The hardest trees for this search
were the spiders with about 30 legs of length 2 and their relatives (up to 166 million
nodes); they are not scarce — the spider with 12 legs of length 2 already has 2,357,832
growth placements — the search order is just poor for them. A complete search restricted
to three runs also finds placements for 25, 28, 29 and 30 legs of length 2
(`n = 51..61`).

**No tree without a growth placement was found, and no tree was left unresolved**, so no
second-program confirmation of a non-existence claim was needed.

## 7. Conjecture B3 at n = 26

{{B3LONG}}

## 8. Reproducing

```sh
cd src
g++ -O2 -o growfam growfam.cpp && g++ -O2 -o growcheck growcheck.cpp
g++ -O2 -o runsolve_gen runsolve_gen.cpp

# validation
for n in 7 8 9 10 11 12 13; do ./growfam all $n 6; done           # totals, least counts, anchors
for n in 7 8 9 10 11 12; do python3 alltrees.py $n; done > /tmp/t.txt
./growcheck < /tmp/t.txt | awk '{print $1,$2,$3}' > /tmp/a; ./growfam count < /tmp/t.txt | awk '{print $1,$2,$3}' > /tmp/b; diff /tmp/a /tmp/b

# every tree, n = 14, 15, 16   (about 1, 5 and 40 core-minutes)
./growfam all 14 6;  ./growfam all 15 6;  ./growfam all 16 6 0 2 & ./growfam all 16 6 1 2

# families (results/counterexample-hunt/counts/); budget: see the comment in the script
for s in 1 2 3; do ./hunt_survey.sh $s & done; wait
python3 hunt_counts_table.py
python3 huntfam.py hublegs 1..64 2 2 | ANCHORS=1 ./growfam count   # one family by hand

# one hub on every core (results/counterexample-hunt/hubcores/)
for a in 6 7 8 9 10; do COUNTBUDGET=30000000 ./hunt_hubcores.sh $a 20 40; done
python3 hubscan.py two 7 10 10 | ./growfam count

# existence for whole classes (logs hunt_exist_*.log are not committed), then the table
for c in spider1 dbl corona leafhubs kbranch spider2 kbranch+; do ./hunt_exist.sh $c; done
./hunt_exist.sh sph 26 70 9 0 2 & ./hunt_exist.sh sph 26 70 9 1 2
python3 hunt_summary.py
python3 huntfam.py spider 28..30 2 | QUIET=1 ./growfam exist 3     # three runs, complete search

# Conjecture B3 at n = 26, in 64 resumable pieces on 4 cores
./hunt_b3.sh 26 64 4
```

Files: `counts/` one file per family (name, n, count, search nodes, anchors per vertex
orbit); `alltrees/` the exhaustive scans; `REPORT.md` is built by `python3 hunt_report.py`
from `REPORT.template.md`; `hubcores/` core index, count at `m = 20`,
count at `m = 40`; `b3_n26_pieces.txt` the finished pieces of the B3 run.

## 9. Dead ends and limits

* The exact counter stops being practical when a tree has more than roughly 10^8 search
  states: about `n = 43` for three-legged spiders, `n = 29` for four legs, `n = 23` for
  combs and complete binary trees. Beyond that only existence was tested.
* The first existence schedule (natural order, a few large budgets, then unlimited) got
  stuck for over ten minutes on the spider with 28 legs of length 2; it was replaced by
  the restart schedule of section 6. Nothing from the first schedule is reported.
* The independent counter `growcheck` has no symmetry pruning and is hopeless on trees
  with large hubs (it enumerates `m!` copies of every placement); the cross-check is
  therefore strong for small trees and absent for large hub trees.
* The classes of section 6 were chosen because they are symmetric or resemble known
  hard cases. They are a vanishing fraction of all trees with 26..70 vertices; this
  hunt says nothing about unstructured trees of that size beyond the README's random
  samples.
