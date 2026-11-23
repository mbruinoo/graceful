# Independent verification report

**Scope.** The Graceful Tree Conjecture is open; nothing here proves it or any
of the conjectures in the README. This report re-derives the README's
*computational* claims with programs written from the definitions in README
§1, 2, 3, 7, 8, 11, 12, 13 only. The logic of `src/growsolve.cpp`,
`src/runsolve*.cpp`, `src/holes.cpp`, `src/skipmin.cpp`, `src/spiderzig.cpp`
and `src/treegen.h` was not read. Trees come from
`networkx.nonisomorphic_trees`, not from `src/treegen.h`.

**Result in one line.** Every *number* checked agrees with the README.
**One descriptive sentence of the README is wrong** (§4.1 below): README §11
says of the two-run rule that "all its known failures are trees with three or
more equal branches"; one of the two 16-vertex failures has only two equal
branches and a longer third one. Three further remarks that are not
discrepancies are in §4.2–4.4.

Status words follow `CLAUDE.md`: everything below is an **Observation** with
the stated bound, unless it says otherwise.

## 1. How the checks are built

Four independent pieces, so that a bug in one is caught by another.

| piece | file | what it is | used for |
|---|---|---|---|
| reference | `ref_small.py`, `common.py` | Python, straight from the definitions: all `(n−1)!` placements for `n ≤ 8`; all tree placements for `n ≤ 12`; all growth placements for `n ≤ 13` | §4 tables, Theorem 9, Lemma 10, anchors, runs, skips; ground truth for the pieces below |
| enumerator | `rs/gsearch.rs enum` | Rust; walks over *all* growth placements on `n` labels (position by position, longest bracket first) and records per tree shape the least number of runs, the least number of skips, and which rooted shapes occur with the root at label 1 | anchors `n ≤ 16`, run and skip tables `n ≤ 16`, "exactly two trees at `n = 16`" |
| searcher | `rs/gsearch.rs solve / minskip / minruns / anchors / spider` | Rust; tree by tree. Cell-driven: at the step for bracket `k` it walks over the unused *cells* `x`, looks at cells `x±k`, and hangs an unlabelled neighbour of the vertex found there. Isomorphic hanging branches are tried once. Search budgets are doubled until the answer is certain, so a "none" is exhaustive | every per-tree claim; negative claims |
| certificate checker | `check_cert.py`, `check_spider.py` | Python; reads the tree from networkx's output and the labeling from the searcher, and checks the definition directly | every "each tree has …" claim |
| SAT | `sat_check.py` | PySAT/CaDiCaL; labels, lengths, "used after step `s`" and run-start variables with cardinality constraints | the specific failures in (c); validated against the reference on all trees with `n = 9, 10` |

What a positive claim rests on: the networkx generator (count compared with
OEIS A000055 and, for `n ≤ 23`, all canonical codes pairwise different) and
the Python certificate checker. The searcher's correctness is irrelevant for
positive claims, because every answer it gives is re-checked.

What a negative claim ("this tree has no such placement") rests on: an
exhaustive search. Each one below is confirmed by at least two of
{enumerator, searcher, SAT, Python reference}.

Self-tests (`python3 ref_small.py selftest`): for `n ≤ 8` the two forms of the
growth definition (connected for every `k`; one used foot per bracket) give
the same set of placements among all `(n−1)!`, the fast tree-placement
enumeration equals the plain filter, and the README's `n = 4` triangle is
rejected. The enumerator equals the Python reference shape by shape for
`n = 8..13` (`equals_python_reference: true` in `results/log_enum.txt`). The
fast certificate check used for `n ≥ 23` agrees with the definitional one on
3,757 certificates and 11,271 deliberately corrupted ones.

## 2. Results

`=` means my value equals the README's.

### (a) A growth placement for every tree

| n | trees (networkx) | known count | trees with a verified growth placement | README | agree? |
|---|---|---|---|---|---|
| 5–18 | 3 … 123,867 | = | all (`results/log_twoskip_5_18.txt`, `log1.txt`) | all | yes |
| 19 | 317,955 | = | 317,955 | all | yes |
| 20 | 823,065 | = | 823,065 | all | yes |
| 21 | 2,144,505 | = | 2,144,505 | all | yes |
| 22 | 5,623,756 | = | 5,623,756 | all | yes |
| 23 | 14,828,074 | = | N23_OK | all (`growsolve`, `n ≤ 23`) | N23_AGREE |
| 24 | 39,299,897 | = | N24_OK | all (via three runs, `n ≤ 25`) | N24_AGREE |
| 25 | 104,636,890 | = | N25_OK | all (via three runs, `n ≤ 25`) | N25_AGREE |

Number of growth placements for `n = 4..13` (README §4): mine
4, 12, 32, 116, 412, 1764, 7888, 40220, 214600, 1275368 — all `=`. Further:
7,926,160 (`n = 14`), 53,623,768 (`n = 15`), 380,045,060 (`n = 16`); the README
gives no value for these.

### (b) Three runs (README §11)

The certificates in (a) were searched under the *two-skip* rule (at most three
runs, at most one of them longer than one cell), which is stronger than three
runs, and re-checked as such. Separately, for `n = 15..18` under plain three
runs.

| claim | README | mine | agree? |
|---|---|---|---|
| every tree has a three-run growth placement, `n ≤ 16` | yes | yes, `n ≤ 21` by certificates; `n ≤ 16` also by full enumeration | yes |
| same, `n = 22..25` | yes (`n ≤ 25`) | N22_25_R3 | N22_25_R3_AGREE |
| `R = 1`: first tree without one | `S(2,2,2,2)`, `n = 9` | `S(2,2,2,2)`, `n = 9`; none for `n ≤ 8` | yes |
| `R = 1`: trees without one, `n = 15` | 724 of 7,741 | 724 of 7,741 (enumerator and searcher) | yes |
| `R = 2`: trees without one, `n ≤ 15` | 0 | 0 | yes |
| `R = 2`: trees without one, `n = 16` | 2 of 19,320 | 2 of 19,320 (enumerator, searcher, SAT) | yes |
| `R = 2`: trees without one, `n = 18` | 1 of 123,867 | 1 of 123,867 (searcher only) | yes |

The two 16-vertex trees (networkx vertex numbers):
`1-0 1-2 0-7 2-3 3-4 4-5 4-6 7-8 7-12 8-9 9-10 9-11 12-13 13-14 13-15` and
`1-0 1-2 0-6 0-11 2-3 2-4 2-5 6-7 7-8 7-9 7-10 11-12 12-13 12-14 12-15`
(see §4.1 for their shapes). The 18-vertex tree (three hubs of three leaves on one vertex, plus a fourth branch):
`1-0 1-2 1-6 1-10 0-14 2-3 2-4 2-5 6-7 6-8 6-9 10-11 10-12 10-13 14-15 15-16 15-17`.

### (c) The specific failures

`results/log_claims_c.txt`; "none" = exhaustive search found nothing.

| claim | README | searcher | SAT | enumerator / reference | agree? |
|---|---|---|---|---|---|
| `S(2,2,2,2)` (`n = 9`): build with zero skips | none | none | UNSAT | none | yes |
| `S(2,2,2,2)`: build with one skip | exists | found | SAT | found | yes |
| `S(3,3,3)` (`n = 10`): zero skips | none | none | UNSAT | none | yes |
| `S(3,3,3)`: one skip | none | none | UNSAT | none | yes |
| `S(3,3,3)`: two skips | exists | found | SAT | found | yes |
| exactly two 16-vertex trees have no two-run placement | 2 | 2 | UNSAT for both; SAT with three runs | 19,318 of 19,320 shapes reach two runs (380,045,060 placements enumerated) | yes |
| 22-vertex tree of §11: at most two single skips | none | none | UNSAT (16 s) | — | yes |
| 22-vertex tree: three single skips | exists | found, checked | SAT | — | yes |
| 22-vertex tree: three runs of any size | exists | found, checked | SAT | — | yes |
| two-skip rule holds for every tree, `n ≤ 21` | yes | yes (certificates, all trees `n = 5..21`) | — | `n ≤ 16` | yes |
| two-skip rule fails for exactly one tree at `n = 22` | 1 of 5,623,756 | 1 of 5,623,756, and it is the README's tree (same edge list); the other 5,623,755 have checked certificates | UNSAT for that tree | — | yes |

Least number of skips, tree by tree (README §12 table):

| n | need 0 | need 1 | need 2 | README | agree? |
|---|---|---|---|---|---|
| 9 | 46 | 1 | 0 | = | yes (reference, enumerator, searcher) |
| 10 | 104 | 1 | 1 | = | yes (same three) |
| 12 | 531 | 20 | 0 | = | yes (same three) |
| 14 | 2,926 | 232 | 1 | = | yes (enumerator, searcher) |
| 16 | 17,132 | 2,177 | 11 | = | yes (enumerator, searcher) |
| 18 | 103,980 | 19,837 | 50 | = | yes (searcher only) |

Also `=`: the first row of the §11 rule table ("one run, at most one single
skipped cell": 1 tree at `n = 10`, none at 11 and 12, 1 at 13).

### (d) Spiders (README §12–13)

All spiders with at least three legs; the list of leg patterns is generated
independently in Python and compared (`results/log_spiders.txt`).

| claim | README | mine | agree? |
|---|---|---|---|
| Conjecture S: every spider has a valid deal, `4 ≤ n ≤ 22` | yes (`n ≤ 32`) | yes for every `n = 4..22` (781 spiders at `n = 22`); every deal re-checked in Python | yes |
| Conjecture S, `n = 23..26` | yes | SPIDER_FREE_23_26 | SPIDER_FREE_AGREE |
| spiders with no zigzag deal, `n ≤ 21` | three-legged with a leg of length 1; `S(3,3,3)`; `S(2,…,2)` with 5 and 8 legs | exactly the list below | yes |
| Lemma 11: `S(2^k)` has no zigzag deal for `k ≡ 2 (mod 3)` | proved | `k = 5, 8`: none; `k = 3, 4, 6, 7, 9, 10`: a zigzag deal exists | consistent |

My complete list of spiders on `n ≤ 22` vertices without a zigzag deal
(exhaustive search; for `n ≤ 13` also confirmed by a second, plain Python
search):

| n | spiders without a zigzag deal |
|---|---|
| 6 | `S(2,2,1)` |
| 8 | `S(3,3,1)` |
| 10 | `S(3,3,3)` |
| 11 | `S(2,2,2,2,2)` |
| 12 | `S(5,5,1)` |
| 13 | `S(6,5,1)` |
| 14 | `S(7,5,1)`, `S(6,6,1)` |
| 16 | `S(8,6,1)`, `S(7,7,1)` |
| 17 | `S(8,7,1)`, `S(2,2,2,2,2,2,2,2)` |
| 18 | `S(13,3,1)`, `S(11,5,1)`, `S(9,7,1)` |
| 21 | `S(17,2,1)`, `S(16,3,1)`, `S(11,8,1)` |
| 22 | `S(17,3,1)`, `S(10,10,1)` |
| 4, 5, 7, 9, 15, 19, 20 | none |

Every entry is either three-legged with a leg of length 1, or `S(3,3,3)`, or
`S(2^5)`, `S(2^8)`, as the README says.

Least skips over all spiders (README §12): `n = 16`: 143 / 24 / 1;
`n = 20`: 378 / 102 / 0; `n = 24`: 888 / 343 / 12 — all `=`. The table for
equal-leg spiders (`k` legs of length `L`) agrees in all 28 entries with
`n ≤ 40` (`results/log_extras.txt`); the two entries with `n = 41, 49` were not
run.

### (e) Anchors (README §7) and the slide graph (README §4)

Anchors, by two methods (full enumeration of growth placements; per-vertex
exhaustive search):

| n | vertices | non-anchors | trees with every vertex an anchor | README | agree? |
|---|---|---|---|---|---|
| 8 | 184 | 6 | 18 / 23 | = | yes |
| 10 | 1,060 | 19 | 95 / 106 | = | yes |
| 12 | 6,612 | 37 | 525 / 551 | = | yes |
| 14 | 44,226 | 84 | 3,092 / 3,159 | = | yes |

Also `=`: every tree on `n ≤ 14` has an anchor; non-anchors have degree ≤ 3 for
`n ≤ 14` (and ≤ 2 at `n = 15, 16`); exactly one tree at each of
`n = 10, 12, 15` has no anchor leaf, none at the other `n ≤ 16`. Beyond the
README: 117 non-anchors among 116,115 vertices at `n = 15`, 154 among 309,120
at `n = 16`.

Slide graph (Python, all tree placements; `results/log_slide.txt`):

| n | tree shapes | tree placements | slide components | in star's component | shapes reached by right slides | agree? |
|---|---|---|---|---|---|---|
| 7 | 11 | 164 | 5 | 148 | 11 | yes |
| 8 | 23 | 752 | 11 | 696 | 23 | yes |
| 9 | 47 | 4,020 | 55 | 3,622 | 47 | yes |
| 10 | 106 | 23,576 | 171 | 22,082 | 106 | yes |
| 11 | 235 | 155,632 | 1,013 | 147,342 | 235 | yes |
| 12 | 551 | 1,112,032 | 4,987 | 1,067,746 | 551 | yes |

Also `=`: the slide graph is connected for `n ≤ 6`; every tree placement has
a legal slide for `3 ≤ n ≤ 12` (Observation C, README bound `n ≤ 14`).

### (f) Theorem 9 and Lemma 10

| claim | README | mine | agree? |
|---|---|---|---|
| Theorem 9: growth placements whose brackets all jump one common point are staircases, and there are `2^(n−2)` of them | proved; checked `n ≤ 12` | true for every `n = 3..13` (2, 4, …, 2048 placements, all staircases, equal to the set of staircases) | yes |
| Lemma 10: the balance game produces exactly the growth placements | proved; checked `n ≤ 9` | set equality for every `n = 3..10` (7,888 placements at `n = 10`) | yes |

### Extras from §11 (single trees, exhaustive search, `results/log_extras.txt`)

Least number of runs: spherically symmetric `(2,2,2)`: 2; `(4,4)`: 3;
`(2,2,2,2)`: 2; `(5,5)`: 3 — as in the README. "Centre, three arms of length 2
ending in hubs of `m` leaves": 1 run for `m = 2, 4, 6, 8`, 3 runs for
`m = 3, 5, 7` — as in the README.

## 3. Not checked

* README §9, §10 tables (clean cuts, gap splits, α-placements) — outside the
  assigned sections.
* The two "side" rows of the §11 rule table (skipped cells on the same side /
  one per side). They depend on which run is called the main run; I did not
  implement them.
* §13 "what does not work" table; spherically symmetric trees on 40, 63, 94
  vertices; equal-leg spiders on 41 and 49 vertices; spiders beyond the sizes
  listed above.
* Observations C and D beyond `n = 12`; slide table for `n = 13, 14`.
* Random-tree spot checks at `n = 30..60`.

## 4. Discrepancy and remarks

### 4.1 Discrepancy: "three or more equal branches" (README §11, *Caution*)

README: "The two-run version looked universal through `n = 15` (7,741 trees)
and then failed for 2 trees in 19,320 at `n = 16`. **All its known failures are
trees with three or more equal branches.**"

The two 16-vertex trees without a two-run growth placement are (by three
methods: full enumeration of all 380,045,060 growth placements on 16 labels,
tree-by-tree search, SAT; the enumerator and the searcher single out the same
two shapes):

* tree **b**, `1-0 1-2 0-6 0-11 2-3 2-4 2-5 6-7 7-8 7-9 7-10 11-12 12-13 12-14 12-15`:
  a centre with three equal branches (arm of length 2 ending in a hub of three
  leaves). This fits the sentence.
* tree **a**, `1-0 1-2 0-7 2-3 3-4 4-5 4-6 7-8 7-12 8-9 9-10 9-11 12-13 13-14 13-15`:
  its only vertex with three non-leaf branches is vertex 7, and the branches
  there are: arm of length 2 ending in a two-leaf fork, the same again, and an
  arm of length **5** ending in a two-leaf fork. Two equal branches, not three.
  (Branch codes at vertex 7: `((()()))`, `((()()))`, `(((((()())))))`.)

So the sentence does not hold for tree **a** as written. The count (2 of
19,320) is right; only the description of the failures is too narrow. A
statement that does hold for both, and for the single failure at `n = 18`:
"each has a vertex with three or more branches that end in the same hub or
fork". I checked only these three trees against it, so that is an
**Observation** on three trees, nothing more. I could not test whether the
author's program singles out the same two trees, since the README does not
list them; the count and three independent methods leave no room for a
different pair.

### 4.2 What "at most `s` single skips" was taken to mean

The README describes the rule twice (unused labels are "one run together with
at most two isolated single labels"; "a move may skip one cell"). I used: *at
every moment the unused labels form at most `s + 1` runs, and at most one run
has more than one cell*. With this reading every number in the §11 and §12
tables that I checked is reproduced exactly, so it is evidently the same rule;
it would be worth stating it this way in the README.

### 4.3 The 22-vertex tree needs only two runs

The README says that tree "can be built with three single skips, and with
three runs when one hole has two cells." The searcher finds, and the Python
checker confirms, a growth placement of it in which the unused labels never
form more than **two** runs (labels for the README's vertices `0..21`:
`18 3 17 4 16 5 6 11 12 14 15 2 19 1 22 21 20 9 8 7 10 13`). So the tree
defeats the two-skip rule but not the two-run rule; the README's sentence is
true but weaker than it could be.

### 4.4 Smallest spider without a zigzag deal

The README's examples of three-legged failures start at `S(3,3,1)`; the
smallest is `S(2,2,1)` on 6 vertices (also a caterpillar, so it has a
staircase). The README's description ("three-legged spiders with a leg of
length 1 and certain other two legs") covers it.

## 5. Reproducing

```sh
cd verify
pip install networkx python-sat
rustc -O -C target-cpu=native -o rs/gsearch rs/gsearch.rs

python3 ref_small.py selftest
for n in 3 4 5 6 7 8 9 10 11 12; do python3 ref_small.py slide $n; done      # (e) slide table; n=12 takes ~4 min
for n in 3 4 5 6 7 8 9 10 11 12 13; do python3 ref_small.py growth $n; done  # (f), counts, runs, skips
for n in 8 10 12; do python3 anchors_ref.py $n; done                         # (e) anchors from the reference

for n in 8 9 10 11 12 13 14 15 16; do                                        # enumerator; n=16 takes ~4 min on 3 cores
  ./rs/gsearch enum $n inf inf > out/enum_$n.txt
  python3 cmp_enum.py $n out/enum_$n.txt $( [ $n -le 13 ] && echo out/ref_growth_$n.json )
done

for n in $(seq 5 18); do CHECK=1 ./run_trees.sh $n solve 3 1; done           # (a), (b): two-skip certificates
for n in 15 16 17 18; do ./run_trees.sh $n solve 3 inf; done                 # (b): three runs
./run_trees.sh 15 solve 1 inf; ./run_trees.sh 16 solve 2 inf; ./run_trees.sh 18 solve 2 inf
for n in 9 10 12 14 16 18; do ./run_trees.sh $n minskip; done                # section 12 table
for n in 8 10 12 14; do ./rs/gsearch anchors < out/trees_$n.txt | tr -cd '-' | wc -c; done

for n in 19 20 21 22; do python3 gen.py $n check > out/trees_$n.txt; ./run_big.sh $n 3 1; done
for n in 23 24 25; do python3 gen.py $n > out/trees_$n.txt; FAST=1 ./run_big.sh $n 3 1; done   # hours; ~25 GB in out/

python3 claims_c.py                                                          # (c): searcher and SAT
for rb in "1 inf" "2 1"; do python3 sat_check.py $rb < out/trees_10.txt | sort | uniq -c; done

for n in $(seq 4 22); do for kind in free zig; do                            # (d)
  ./rs/gsearch spider $n $kind > out/spider_${n}_$kind.txt
  python3 check_spider.py $n $kind out/spider_${n}_$kind.txt
done; done
for n in 16 20 24; do python3 spider_trees.py $n > out/sp_$n.txt; ./rs/gsearch minskip < out/sp_$n.txt > out/sp_minskip_$n.txt
  python3 check_cert.py $n out/sp_$n.txt out/sp_minskip_$n.txt; done
python3 extras.py 300
```

`THREADS=k` sets the number of threads of `gsearch` (default 4). The summary
lines of every run reported here are in `results/`; raw outputs (`out/`) are
not committed.
