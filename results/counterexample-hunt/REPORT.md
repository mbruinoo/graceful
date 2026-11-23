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
| existence, complete deterministic search | 92,409 structured trees with `26 ≤ n ≤ 70` in 8 classes (section 6) | a growth placement was found and verified for every one; none unresolved |
| Conjecture B3 at `n = 26` | all 279,793,450 trees on 26 vertices | **Observation (`n = 26`)**: 0 trees without a three-run growth placement, 0 unresolved |

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

| file | members counted | n | first counts | last count | least count at n >= 26 | drops (count smaller than the previous member) | most non-anchor vertices |
|---|---|---|---|---|---|---|---|
| bin_2_d | 2 | 7..15 | 6, 370 | 370 | - | 0 | 0 of 7 |
| bin_3_d | 2 | 10..22 | 20, 1062292 | 1,062,292 | - | 0 | 0 of 10 |
| bin_4_d | 1 | 13..13 | 120 | 120 | - | 0 | 0 of 13 |
| comb_p_2 | 4 | 9..18 | 32, 400, 7686, 232882 | 232,882 | - | 0 | 1 of 9 |
| comb_p_3 | 3 | 12..20 | 98, 4324, 413330 | 413,330 | - | 0 | 0 of 12 |
| dbl_m_3_1_2 | 12 | 8..30 | 22, 42, 88, 116, 246, 424 | 21,038 | 5430 (n=26) | 0 | 0 of 8 |
| dbl_m_3_2_2 | 12 | 8..30 | 22, 42, 88, 116, 246, 424 | 21,038 | 5430 (n=26) | 0 | 0 of 8 |
| dbl_m_3_3_2 | 12 | 8..30 | 22, 56, 122, 214, 504, 944 | 80,900 | 18668 (n=26) | 0 | 1 of 8 |
| dbl_m_5_1_2 | 12 | 10..32 | 16, 100, 188, 260, 450, 850 | 39,106 | 5660 (n=26) | 0 | 0 of 10 |
| dbl_m_5_2_2 | 12 | 10..32 | 72, 130, 172, 244, 488, 824 | 40,002 | 6128 (n=26) | 0 | 1 of 10 |
| dbl_m_5_3_2 | 12 | 10..32 | 72, 130, 172, 244, 488, 824 | 40,002 | 6128 (n=26) | 0 | 1 of 10 |
| dbl_m_7_1_2 | 13 | 12..36 | 44, 96, 204, 280, 512, 926 | 76,428 | 3166 (n=26) | 0 | 0 of 12 |
| dbl_m_7_2_2 | 12 | 12..34 | 118, 154, 268, 334, 624, 1064 | 50,154 | 3686 (n=26) | 0 | 1 of 14 |
| dbl_m_7_3_2 | 12 | 12..34 | 126, 188, 304, 430, 654, 1296 | 64,446 | 4746 (n=26) | 0 | 1 of 12 |
| dbl_m_9_1_2 | 12 | 14..36 | 62, 174, 220, 388, 598, 1126 | 47,452 | 2058 (n=26) | 0 | 0 of 14 |
| dbl_m_9_2_2 | 12 | 14..36 | 142, 260, 278, 498, 726, 1346 | 59,658 | 2370 (n=26) | 0 | 0 of 14 |
| dbl_m_9_3_2 | 12 | 14..36 | 172, 248, 352, 466, 884, 1248 | 54,210 | 2856 (n=26) | 0 | 1 of 14 |
| forkhub_1_m_2 | 50 | 7..56 | 6, 10, 16, 12, 14, 16 | 184 | 52 (n=26) | 9 | 5 of 14 |
| forkhub_1_m_3 | 50 | 9..58 | 32, 40, 52, 62, 76, 96 | 8,002 | 740 (n=26) | 0 | 1 of 9 |
| forkhub_2_m_2 | 50 | 8..57 | 22, 18, 20, 16, 26, 28 | 928 | 166 (n=26) | 2 | 0 of 8 |
| forkhub_2_m_3 | 50 | 10..59 | 8, 44, 54, 36, 46, 28 | 2,138 | 138 (n=26) | 3 | 6 of 10 |
| forkhub_3_m_2 | 50 | 9..58 | 16, 32, 44, 56, 76, 96 | 17,114 | 1114 (n=26) | 0 | 4 of 9 |
| forkhub_3_m_3 | 50 | 11..60 | 54, 74, 78, 82, 100, 104 | 2,254 | 348 (n=26) | 0 | 1 of 11 |
| hubleaflegs_m_2_2 | 64 | 6..69 | 6, 14, 18, 28, 32, 48 | 2,628 | 326 (n=26) | 0 | 0 of 6 |
| hubleaflegs_m_2_3 | 63 | 8..70 | 12, 28, 42, 70, 80, 112 | 6,748 | 702 (n=26) | 0 | 1 of 8 |
| hubleaflegs_m_2_4 | 47 | 10..56 | 26, 64, 132, 220, 356, 524 | 273,064 | 8766 (n=26) | 0 | 0 of 10 |
| hubleaflegs_m_3_2 | 52 | 8..59 | 24, 54, 106, 172, 258, 388 | 95,558 | 5954 (n=26) | 0 | 0 of 8 |
| hubleaflegs_m_3_3 | 24 | 11..34 | 80, 250, 592, 1058, 1872, 2836 | 122,878 | 39212 (n=26) | 0 | 0 of 11 |
| hubleaflegs_m_3_4 | 12 | 14..25 | 276, 1082, 3002, 6586, 13036, 23140 | 269,302 | - | 0 | 0 of 14 |
| hubleaflegs_m_4_2 | 22 | 10..31 | 68, 208, 446, 950, 1626, 2816 | 191,586 | 75812 (n=26) | 0 | 0 of 10 |
| hubleaflegs_m_4_3 | 10 | 14..23 | 890, 3536, 10068, 23830, 48932, 93128 | 612,596 | - | 0 | 0 of 14 |
| hubleaflegs_m_4_4 | 4 | 18..21 | 11346, 51064, 171122, 468952 | 468,952 | - | 0 | 0 of 18 |
| hubleaflegs_m_5_2 | 13 | 12..24 | 178, 782, 1944, 4948, 9738, 19308 | 377,882 | - | 0 | 0 of 12 |
| hubleaflegs_m_5_3 | 4 | 17..20 | 13678, 64720, 228404, 628008 | 628,008 | - | 0 | 0 of 17 |
| hublegs_m_2_2 | 64 | 7..70 | 6, 10, 16, 12, 14, 16 | 270 | 52 (n=26) | 11 | 5 of 14 |
| hublegs_m_2_3 | 62 | 9..70 | 32, 40, 52, 62, 76, 96 | 13,894 | 740 (n=26) | 0 | 1 of 9 |
| hublegs_m_2_4 | 60 | 11..70 | 58, 78, 100, 120, 138, 172 | 61,252 | 1032 (n=26) | 0 | 2 of 11 |
| hublegs_m_3_2 | 62 | 9..70 | 14, 70, 96, 168, 178, 230 | 57,608 | 2224 (n=26) | 0 | 3 of 16 |
| hublegs_m_3_3 | 32 | 12..43 | 272, 482, 714, 1022, 1372, 1796 | 103,720 | 11698 (n=26) | 0 | 0 of 12 |
| hublegs_m_3_4 | 14 | 15..28 | 986, 2458, 4128, 6472, 9586, 12936 | 73,054 | 51622 (n=26) | 0 | 0 of 15 |
| hublegs_m_4_2 | 41 | 11..51 | 32, 256, 404, 630, 766, 1008 | 53,940 | 5634 (n=26) | 0 | 0 of 11 |
| hublegs_m_4_3 | 11 | 15..25 | 3186, 7604, 13266, 20806, 30684, 41346 | 144,848 | - | 0 | 0 of 15 |
| hublegs_m_4_4 | 3 | 19..21 | 52820, 150266, 326672 | 326,672 | - | 0 | 0 of 19 |
| hublegs_m_5_2 | 22 | 13..34 | 136, 1014, 1976, 3162, 3932, 4874 | 81,304 | 27036 (n=26) | 0 | 0 of 13 |
| hublegs_m_5_3 | 3 | 18..20 | 59738, 167388, 341664 | 341,664 | - | 0 | 0 of 18 |
| hubspider_3_1_m | 22 | 7..70 | 6, 20, 18, 168, 60, 842 | 1,655,497,912 | 2284 (n=31) | 8 | 0 of 7 |
| hubspider_3_2_m | 18 | 10..61 | 8, 22, 108, 154, 644, 1470 | 7,029,921,862 | 4110 (n=28) | 0 | 6 of 10 |
| hubspider_3_3_m | 10 | 13..40 | 30, 140, 420, 1298, 2894, 9156 | 792,532 | 9156 (n=28) | 0 | 0 of 13 |
| hubspider_4_1_m | 9 | 9..41 | 14, 120, 840, 9844, 32418, 407604 | 140,287,756 | 407604 (n=29) | 0 | 0 of 9 |
| hubspider_4_2_m | 5 | 13..29 | 138, 960, 8342, 58030, 508120 | 508,120 | 508120 (n=29) | 0 | 0 of 13 |
| hubspider_4_3_m | 3 | 17..25 | 1434, 12918, 116530 | 116,530 | - | 0 | 0 of 17 |
| hubspider_5_1_m | 4 | 11..26 | 32, 1940, 38942, 2246322 | 2,246,322 | 2246322 (n=26) | 0 | 0 of 11 |
| hubspider_5_2_m | 2 | 16..21 | 1622, 68194 | 68,194 | - | 0 | 0 of 16 |
| hubspider_5_3_m | 1 | 21..21 | 78780 | 78,780 | - | 0 | 0 of 21 |
| hubspider_6_1_m | 2 | 13..19 | 136, 24710 | 24,710 | - | 0 | 0 of 13 |
| hubspider_6_2_m | 1 | 19..19 | 30416 | 30,416 | - | 0 | 0 of 19 |
| sph | 11 | 7..23 | 6, 18, 9844, 370, 1062292, 2822 | 20,400 | - | 5 | 0 of 7 |
| spider_3_L | 14 | 4..43 | 2, 6, 8, 30, 134, 424 | 2,180,632 | 11202 (n=28) | 0 | 6 of 10 |
| spider_4_L | 7 | 5..29 | 2, 14, 138, 1434, 14454, 157488 | 1,684,080 | 1684080 (n=29) | 0 | 0 of 5 |
| spider_5_L | 5 | 6..26 | 2, 32, 1622, 78780, 3988962 | 3,988,962 | 3988962 (n=26) | 0 | 0 of 6 |
| spider_6_L | 3 | 7..19 | 2, 136, 30416 | 30,416 | - | 0 | 0 of 7 |
| spider_8_L | 2 | 9..17 | 2, 1734 | 1,734 | - | 0 | 0 of 9 |
| spider_k_2 | 9 | 7..23 | 6, 14, 32, 136, 520, 1734 | 316,602 | - | 0 | 0 of 7 |
| spider_k_3 | 5 | 10..22 | 8, 138, 1622, 30416, 786850 | 786,850 | - | 0 | 6 of 10 |
| twolevel_2_2_m | 6 | 11..31 | 24, 370, 2822, 20400, 171304, 1292716 | 1,292,716 | 171304 (n=27) | 0 | 0 of 11 |
| twolevel_2_3_m | 2 | 15..21 | 1038, 171144 | 171,144 | - | 0 | 0 of 15 |
| twolevel_3_2_m | 2 | 16..22 | 2458, 1062292 | 1,062,292 | - | 0 | 0 of 16 |
| twolevel_4_2_m | 1 | 21..21 | 745010 | 745,010 | - | 0 | 0 of 21 |

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

| class | trees | n | growth placement found and verified | none (complete search) | unresolved | found within <=1 / 2 / 3 / 4 runs / unrestricted attempt | most nodes (tree) |
|---|---|---|---|---|---|---|---|
| corona | 689 | 27..70 | 689 | 0 | 0 | 62 / 549 / 53 / 16 / 9 | 10,761,390 (corona(9,#31,6)) |
| dbl | 3,035 | 26..70 | 3,035 | 0 | 0 | 2,586 / 449 / 0 / 0 / 0 | 79,853 (dbl(28,8,7,2)) |
| kbranch+ | 8,241 | 26..70 | 8,241 | 0 | 0 | 74 / 4,841 / 3,091 / 151 / 84 | 165,977,511 (kbranch+(33,2,#0,2)) |
| kbranch | 2,610 | 26..70 | 2,610 | 0 | 0 | 22 / 1,443 / 1,085 / 44 / 16 | 165,975,097 (kbranch(34,2,#0)) |
| leafhubs | 900 | 26..70 | 900 | 0 | 0 | 195 / 330 / 372 / 3 / 0 | 2,883,417 (leafhubs(9,#43,8)) |
| sph | 65,693 | 26..70 | 65,693 | 0 | 0 | 5,946 / 17,619 / 41,458 / 598 / 72 | 124,757,946 (sph(1,1,3,3,6)) |
| spider1 | 108 | 26..70 | 108 | 0 | 0 | 0 / 39 / 63 / 5 / 1 | 165,979,250 (spider(34x2)) |
| spider2 | 11,133 | 26..70 | 11,133 | 0 | 0 | 2,541 / 5,106 / 3,420 / 52 / 14 | 6,855,962 (spider(18x2,11x3)) |
| **total** | 92,409 | | 92,409 | 0 | 0 | | |

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

`./runsolve_gen 26 3`, run as 64 pieces: all pieces finished, 279,793,450 trees, 0 with no three-run growth placement, 0 unresolved. With the README's range this makes B3 an Observation for `n ≤ 26`, resting on `runsolve_gen.cpp` alone (the tree total equals the known number of trees on 26 vertices). Since every three-run growth placement is a growth placement, Conjecture B is likewise an Observation for `n ≤ 26`. `README.md` and `web/evidence.json` still say 25; they were deliberately not edited in this task.

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
