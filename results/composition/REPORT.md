# Composition rules for growth placements

**Status: the Graceful Tree Conjecture is open and nothing here proves it.**
This note looks for rules that build a growth placement out of smaller growth
placements. Five rules are **Proved** below (the proofs are short and
complete). What they reach is an **Observation** with a stated range. Three
natural rules **Fail** and are recorded with their smallest failing pair.
No claim of novelty is made: none of this was checked against the literature
beyond what `README.md` section 5 already cites.

Vocabulary and notation are those of `README.md`. Labels are `0..m`
(`m = n − 1`); the bracket of length `k` is the edge `{p_k, p_k + k}`.

## 0. Summary

| | result | status |
|---|---|---|
| Rule C | complement `i ↦ m − i` | Classical / README Theorem 7 |
| Rule T | **completion transplant**: the last `k` brackets of one growth placement can be moved under the first brackets of another whenever the patterns of used cells fit | Proved |
| Rule P | **run filling**: if the unused labels form one run, any growth placement fits there (contains README Lemma 6 and the gluing statement of README §7) | Proved (corollary of T's argument) |
| Rule N | **nesting at a clean cut**: a whole truncated growth placement, not just one leaf, can be inserted in the gap (contains README Lemma 8) | Proved |
| Rule B | **block designs**: multiply all lengths by `t` and fill the freed residues with leaves, by a finite recipe that does not depend on `t` | Proved |
| Rule D | **mirror windows**: the growth version of the Stanton–Zarnke / Koh–Rogers–Tan Δ-construction with a star; an explicit special case of B | Proved |
| closure | C + T + B, started from staircases, reaches **every tree on `n ≤ 16` vertices**; C + T + (README Lemma 8) reaches every tree on `n ≤ 14` | Observation |
| | C + P + T alone never leave the caterpillars | Proved |
| F1 | "identify an anchor of `T` with an anchor of `T'`: the merged vertex is an anchor" | Fails, `n = 6` |
| F2 | "join an anchor of `T` to an anchor of `T'` by an edge: both (or one) of the two ends is an anchor" | Fails, `n = 6` (`n = 7`) |
| F3 | "the classical Δ-labelling of `T` by `T'` is a growth placement" | Fails unless `T'` is a star centred at the joining vertex (Proved); smallest `K_2`, `P_3` |

The honest reading of the closure result: rules T and P are bookkeeping (they
recombine pieces that already exist), so "everything is reached" does not
tell us *how* to label a given tree. What it does say is that for `n ≤ 16`
no tree needs a growth placement that is unrelated to the others: every tree
has one that is assembled from staircases by scaling (B) and by cutting and
pasting at moments when the patterns of used cells agree (T).

## 1. The picture: the tape

Place brackets longest first and watch only which labels are used (the
"tape" of the page, README §11). For a growth placement `f` on `n` vertices
and `0 ≤ k ≤ m` write

* **time `k`**: the moment when exactly the brackets longer than `k` are placed;
* `Free_k(f)`: the `k` labels still unused at time `k`;
* the **prefix** of `f` at time `k`: its brackets longer than `k`;
  the **completion**: its brackets of length `≤ k`.

Everything below rests on one remark, which is README Lemma 10 read from the
other side: *whether a bracket may be placed depends only on which cells are
used, not on how they were joined.*

## 2. The rules

### Rule C (complement). Classical.

`p_k ↦ m − k − p_k` maps growth placements to growth placements (the
definition is symmetric under `i ↦ m − i`; README Theorem 7).

### Rule T (completion transplant). Proved.

**Statement.** Let `f` and `h` be growth placements (on any numbers of
vertices) and let `k` be smaller than both numbers of edges. Call a label of
`h` *touched* if it is used at time `k` and is a foot of a bracket of `h` of
length `≤ k`. Suppose there is a shift `s` with

1. `Free_k(f) = Free_k(h) + s`, and
2. for every touched label `a` of `h`, `a + s` is a label of `f` that is used at time `k`.

Then the prefix of `f` at time `k`, followed by the completion of `h` shifted
by `s`, is a growth placement. It draws the tree obtained from the tree of the
prefix of `f` by attaching the forest drawn by the completion of `h`, each
touched label `a` being identified with the vertex of `f` labelled `a + s`.

```
f :  ■ ■ □ □ □ □ ■ ■ ■      prefix of f kept
h :    ■ □ □ □ □ ■ ■ ■ ■    completion of h moved (shift −1); it touches the
                            cells just left and right of the run
```

**Proof.** The new placement has one bracket of each length. Its brackets
longer than `k` are those of `f`, so at time `k` its used set is that of `f`.
Claim: for `i = k, k−1, …, 0`, at time `i` a label `x ∈ Free_k(f)` is used in
the new placement iff `x − s` is used in `h` at time `i`. This holds at
`i = k`. Take the bracket of length `i ≤ k` of `h`, with feet `a` (used at
time `i` in `h`) and `b` (unused). Then `b ∈ Free_k(h)`, so `b + s` is in
`Free_k(f)` and is unused by the claim. If `a ∈ Free_k(h)` then `a + s` is
used by the claim; otherwise `a` is touched and `a + s` is used by
hypothesis 2. So the shifted bracket has exactly one used foot, and the claim
holds at time `i − 1`. ∎

Hypothesis 2 is needed: if a touched label lands on an unused or missing
cell, that bracket has no used foot.

**Check.** `verify_rules.py`: all pairs `(f, h)` of growth placements of all
trees on `≤ 7` vertices and all `k`: 86,420 applications satisfying 1 and 2,
all growth placements; 9,888 satisfying 1 but not 2, none a growth placement.

**Families.** None by itself: T needs two placements to start from. Applied
to staircases only it gives staircases (Proposition 1 below).

### Rule P (run filling). Proved.

**Statement.** Let `f` be a growth placement on `n` vertices and
`1 ≤ k ≤ m − 1` such that `Free_k(f)` is one run `[x, x + k − 1]`. Let `g` be
any growth placement on `k + 1` vertices. Then the prefix of `f` at time `k`
followed by `g` placed on `[x − 1, x + k − 1]`, or on `[x, x + k]`, is a growth
placement. Its tree is the prefix tree `R` of `f` with the tree of `g`
attached: the vertex of `R` labelled `x − 1` is identified with the vertex of
`g` labelled `0` (respectively `x + k` with the vertex of `g` labelled `k`).

**Proof.** `x − 1` and `x + k` are labels of `f` (labels `0` and `m` are used
from the start) and are used at time `k`. The top bracket of `g` lands on
`{x − 1, x + k − 1}`: one foot used, one not. From then on, inside
`[x − 1, x + k − 1]` the used cells are exactly those of `g`'s own build, and
`g`'s brackets do not leave that interval. ∎

In tree language: call `(R, v)` a **one-run prefix of size `k`** if `R` is drawn
by the prefix at time `k` of some growth placement whose free set at that
time is a run next to the label of `v`. Then `R` with **any** anchored tree on
`k + 1` vertices glued at `v` by its anchor has a growth placement.

* `k = m − 1`: the prefix is the top bracket. This is README Lemma 6.
* `f` a staircase: this is the gluing statement of README §7 (α-labelled
  caterpillar ⊕ growth placement).
* P is new only when the prefix is not a staircase prefix; e.g. after Rule B
  the last block is always a run (§2, Rule B, remark 2).

**Check.** 12,860 applications (`f` on `≤ 7` vertices, every run, every `g`,
both positions), all growth placements.

**Families.** For every one-run prefix `(R, v)` of size `k`: the family
`{R ∪_v T' : T' anchored, k + 1 vertices}`. By Conjecture B's evidence that
is every tree on `k + 1` vertices with almost every choice of vertex
(README §7), but only anchors that have been *derived* are used in §4.

### Rule N (nesting at a clean cut). Proved.

README Lemma 8 inserts one leaf at a clean cut. The same gap takes a larger
piece.

**Statement.** Let `f` be a growth placement of `T` on `n` vertices and
`1 ≤ L ≤ m` a cut (between labels `L − 1` and `L`) such that the brackets
jumping over it are exactly the `c` longest. Put `j = n − c`, so the brackets
that do not jump are those of lengths `1..j − 1`. Let `u = L − j ≥ 0` be a
label that is `0` or was added by a jumping bracket. Let `h` be a growth
placement of `T'` on `g + j` vertices, `g ≥ 1`, in which the labels
`1..j − 1` are the last `j − 1` to be added (no condition if `j = 1`), and let
`U'` be the tree drawn by its brackets of length `≥ j`: its root has label
`0`, its other `g` vertices have labels `j..j + g − 1`. Then the following is
a growth placement on `n + g` vertices of `T` with `U'` glued by its root at
the vertex labelled `u`:

* labels of `f` that are `≥ L` move up by `g` (a gap `[L, L + g − 1]` opens);
* the `g` brackets of `U'` are placed with label `0 ↦ u` and `y ↦ u + y`.

The mirror statement (piece hung on the high side) follows by Rule C.

**Proof.** Lengths: the jumping brackets grow by `g` and become
`j + g..m + g`; `U'` uses `j..j + g − 1`; the others keep `1..j − 1`. Labels:
`U'` occupies `u` and `u + [j, j + g − 1] = [L, L + g − 1]`, the gap. Order:
first the `c` jumping brackets, in the order and with the used/unused pattern
they have in `f`. Now `u` is used. Next the brackets of `U'`: its top bracket
is `{u, L + g − 1}` (one used foot), and inside `{u} ∪` gap the build is that
of `h`. Finally the non-jumping brackets of `f`, exactly as in `f`. ∎

The condition on `u` is necessary: otherwise the top bracket of `U'` has no
used foot.

* `g = 1`: `U'` is an edge. This is README Lemma 8.
* `U'` a star: `g` leaves on the vertex labelled `u`.
* `j = 1`: all brackets jump, `f` is a staircase (README Theorem 9) and
  this is Rule P.
* Every cut of a staircase is clean (left feet increase as lengths fall), so N
  leaves the caterpillars at once.

**Check.** 27,871 applications (`T`, `T'` on `≤ 7` vertices, every clean cut,
every admissible `h`), all growth placements; 1,234 with the condition on `u`
violated, none a growth placement.

**Families.** For every growth placement with a clean cut and admissible `u`:
`T` with `g` leaves on `u` for every `g ≥ 1`, and `T ∪_u U'` for every
truncated placement `U'` with that `j`.

**What it adds.** *Observation (`n ≤ 14`):* started from staircases, C + N
derives exactly the same placements as C + Lemma 8 (96,768 placements,
2,663 trees at `n = 14`, the numbers of README §9). Inserting a piece is never
more than inserting its leaves one at a time, in the range checked. Together
with B it adds a few placements and no tree.

### Rule B (block designs: multiply by `t`, fill the residues with leaves). Proved.

**Setting.** Let `f` be a growth placement of `T` on `p` vertices and
`t ≥ 2`. Multiply every label by `t`. The labels `0..(p − 1)t` that are not
multiples of `t` fall into **blocks** `j = 0..p − 2`, block `j` being
`jt + 1, …, jt + t − 1`, between the vertices labelled `j` and `j + 1`. The
lengths that are not multiples of `t` fall into **bands** `β = 0..p − 2`,
band `β` being `βt + 1, …, βt + t − 1`.

A **design** for `f` gives each block `j` an owner `v(j) ∈ {0..p − 1}`. Its band
is `β(j) = j − v(j)` if `v(j) ≤ j` and `v(j) − j − 1` if `v(j) > j`: the number
of labels of `T` strictly between the owner and the block. The design is
**valid** if

1. `β` is a bijection onto `{0..p − 2}`, and
2. for every block, `β(j) < ℓ(v(j))`, where `ℓ(v)` is the length of the bracket
   of `f` that added label `v` (no condition for `v = 0`).

**Statement.** If the design is valid then, for every `t ≥ 2`, the tree `T`
with `(t − 1)·#{blocks owned by v}` new leaves on each vertex `v` has a growth
placement on `(p − 1)t + 1` vertices: the vertex labelled `i` gets label
`ti`, and the leaves of the owner of block `j` get the labels of block `j`.

```
t = 3,  T = star 0-2 0-1,  block 0 owned by label 2, block 1 owned by label 1

label   0   1   2   3   4   5   6
        ■   ·   ·   ■   ·   ·   ■       ■ = T times 3: brackets 0-6 and 0-3
           block 0     block 1
            1-6 2-6     3-5 3-4         block 0 hangs on 6: lengths 5, 4 (band 1)
                                        block 1 hangs on 3: lengths 2, 1 (band 0)
placement, longest first:  0-6 1-6 2-6 0-3 3-5 3-4
```

**Proof.** A leaf at `jt + d` on the owner `tv` has length `(j − v)t + d =
βt + d` if `v ≤ j` and `(v − j)t − d = βt + (t − d)` if `v > j`; as `d` runs
over `1..t − 1` these are the `t − 1` lengths of band `β`. By condition 1 the
leaf lengths are all non-multiples of `t` below `(p − 1)t`, once each, and
the brackets of `T` are the multiples. Order: the multiples of `t` see only
multiples of `t`, so they behave as in `f`. A leaf bracket of band `β` needs
its owner already used: the owner `v ≠ 0` was added by the bracket of length
`tℓ(v)`, which is longer than every length of band `β` iff `ℓ(v) ≥ β + 1`.
The leaf label itself is new. ∎

**Remarks.**

1. Validity does not involve `t`. For `t = 2` a valid design is the same
   thing as a growth placement of `T` plus one leaf per block in which the
   vertices of `T` carry the even labels. So: **if `T` plus `λ(v)` leaves on
   `v` has a growth placement with `T` on the even labels, then `T` plus
   `(t − 1)λ(v)` leaves on `v` has one for every `t ≥ 2`.**
2. The band `0` leaves are placed last and fill one block, a run with a
   vertex of `T` on each side. By Rule P that hub of `t − 1` leaves can be
   replaced by any anchored tree on `t` vertices, glued by its anchor at either
   of the two vertices of `T` next to that block.
3. Leaves at the root can always be added afterwards (Lemma 6), so the
   number of vertices is not tied to `(p − 1)t + 1`.
4. Designs that hand a block out offset by offset, or hang a residue on
   another residue, also exist: `S(2,2,2)` has the growth placement
   `0-6 0-5 1-5 0-3 4-6 2-3`, which is the star `0-2 0-1` times 3 with the
   path `0-5-1` running through two blocks. No general rule of that kind
   was found.

**Check.** 143,752 applications (`T` on `≤ 7` vertices, all valid designs,
`t = 2..5`), all growth placements, all new vertices leaves. For `t = 2` and
`T` on `≤ 6` vertices every assignment satisfying 1 was tried: it gives a
growth placement exactly when it also satisfies 2 (2,936 invalid ones).

**Families** (`families.py`). Each pair (tree `T`, distribution of blocks)
that admits a valid design is one infinite family, indexed by `t`:

| `p` | trees `T` | families | of which not caterpillars | from mirror windows (Rule D) | not caterpillars |
|---|---|---|---|---|---|
| 3 | 1 | 4 | 0 | 4 | 0 |
| 4 | 2 | 15 | 0 | 10 | 0 |
| 5 | 3 | 75 | 8 | 30 | 4 |
| 6 | 6 | 427 | 109 | 73 | 18 |
| 7 | 11 | 2,897 | 1,324 | 242 | 105 |

Smallest non-caterpillar examples (`p = 5`, written on `T`'s labels):

* `T = 0-4 0-3 0-2 1-2`, blocks owned by `4, 4, 4, 3`: a centre with a
  pendant path of length 2, a hub of `3(t − 1)` leaves and a hub of `t − 1`
  leaves.
* `T =` star `0-4 0-3 0-2 0-1`, blocks owned by `4, 1, 0, 2`: a centre
  carrying `t − 1` leaves and one more leaf, and three hubs of `t − 1`
  leaves (for `t = 2`: the spider `S(2,2,2,1,1)`).

### Rule D (mirror windows; the growth Δ-construction). Proved (special case of B).

**Statement.** Let `f` be a growth placement of `T` on `p` vertices and
`1 ≤ w ≤ p`. Suppose that for every label `1 ≤ i ≤ w − 1`

* `ℓ(i) ≥ w − 2i` if `2i ≤ w − 1`, and `ℓ(i) ≥ 2i − w + 1` if `2i ≥ w`

(the bracket that added `i` reaches at least as far as the mirror image
`w − 1 − i` of `i` in the window `[0, w − 1]`; one step further on the low
side). Then for every `t ≥ 2` the tree `T` with `t − 1` leaves on each vertex
labelled `1..w − 1` and `(p − w)(t − 1)` leaves on the root has a growth
placement: the leaves of the vertex labelled `i` take block `w − 1 − i`, the
root takes the blocks `≥ w − 1`.

**Proof.** This is the design `v(j) = w − 1 − j` for `j < w − 1`, `v(j) = 0`
for `j ≥ w − 1`. The root's bands are `j ≥ w − 1`. For `1 ≤ i ≤ w − 1` the
band is `w − 1 − 2i` (if `2i ≤ w − 1`) or `2i − w` (if `2i ≥ w`): the numbers
below `w − 1` of the parity of `w − 1`, respectively of `w`, each once. So
condition 1 holds and condition 2 is the hypothesis. ∎

For `w = p`, plus `t − 1` leaves on the root by Lemma 6, this is exactly the
labelling of `T Δ K_{1,t−1}` of Stanton–Zarnke and Koh–Rogers–Tan (every
vertex of `T` replaced by a star, the leaves of the vertex labelled `i`
sitting in the mirror block). So the classical construction preserves growth
when the copy is a star and `f` satisfies the mirror condition, and (F3
below) in no other case.

## 3. Rules that fail

All from exhaustive enumeration of growth placements (`anchortest.cpp`,
`verify_rules.py`). Rooted trees are written as nested parentheses.

**F1. Identifying two anchors. Fails.** If `v` is an anchor of `T` and `v'` an
anchor of `T'`, the merged vertex need not be an anchor of the union.
Smallest failure, `n = 6`: `T = K_{1,3}` rooted at a leaf, `T'` the path on 3
vertices rooted at an end. The union is the path `e-d-v-a-b` with one more
leaf `c` on `a`, and `v` is not an anchor of it. Among the 3,240 unordered
pairs of anchored trees with 2 to 7 vertices each, 21 fail.
(The path on 7 vertices is the union of two paths on 4 vertices at their
ends: README's non-anchor.)

**F2. Joining two anchors by an edge. Fails.** Among 3,321 unordered pairs
(1 to 7 vertices each) there are 48 in which one end of the new edge is not
an anchor of the result; smallest, `n = 6`: path on 3 vertices rooted at an
end `v`, joined to the centre of another path on 3 vertices (the same tree
and the same vertex `v` as in F1). In 8 pairs *neither* end is an anchor;
smallest, `n = 7`: the paths on 4 and on 3 vertices joined end to end.

So no rule of the form "anchor + anchor ⟹ anchor at the joint" holds; what
does hold is Rule P, where one side must be a one-run prefix.

**F3. The classical Δ-labelling with a copy that is not a star. Fails.**
Take growth placements `f` of `T` (on `p` vertices) and `g` of `T'` (on `q`),
`v'` the vertex of `T'` labelled `0`; put the vertices of copy `i` at even
distance from `v'` in block `i` and the others in block `p − 1 − i`, and join
copies at `v'` along `T`. The result is always graceful (Classical), checked
for all 361 pairs of placements with `p, q ≤ 5`. It is a growth placement in
28 of them, and in each of those `T'` is a star centred at `v'` (Rule D).
Smallest failure: `T = K_2`, `T'` the path on 3 vertices rooted at an end;
the labelling is `0-5 1-5 0-3 2-4 2-3` and the bracket `2-4` has no used foot.
**Proposition 2 (Proved).** For `p ≥ 2` this labelling is a growth placement
only if `T'` is a star centred at `v'`. *Proof.* For an edge `e` of `T'` let
`s(e)` be the label of its end at odd distance from `v'` minus the label of
its other end. In copy `0` the edge `e` has length `(p − 1)q + s(e)`, in copy
`p − 1` it has length `(p − 1)q − s(e)`. Both copies hang from their vertex
`v'`, so lengths must decrease away from `v'` in both (README Theorem 7). For
two edges `e_1, e_2` in a row on a path leaving `v'` that needs
`s(e_1) > s(e_2)` and `s(e_1) < s(e_2)`. So no vertex of `T'` is at distance
2 from `v'`. ∎

## 4. Closure

`closure.cpp` starts from all staircases (caterpillars, README Theorem 2) and
applies the rules switched on until nothing new appears, size by size. It
works with placements, not trees, because the hypotheses of the rules are
properties of placements. Every placement it produces is re-tested against
the definition. Rule T is used with `h` of the same or smaller size.
`verify_rules.py` recomputes the closures for `n ≤ 9` with separate code and
gets the same numbers of placements.

**Proposition 1 (Proved).** Staircases are closed under C, P and T. Hence
these three rules alone derive only caterpillars.

*Proof.* C: `p_k − p_{k+1}` becomes `1 − (p_k − p_{k+1})`. T and P: at time `k`
a staircase has used cells `[0, a] ∪ [b, m]` and its bracket `k + 1` is
`{a, b}`; the completion of a staircase starts with `{a, b − 1}` or
`{a + 1, b}` and continues as a staircase inside the run, and a shift that
matches the runs matches `a` and `b`. ∎

**Trees reached** (number of trees whose shape is drawn by a derived placement):

| n | trees | caterpillars | C P T | C P D | C P B | C + Lemma 8 | C P + Lemma 8 | C T D | **C T B** | **C T + Lemma 8** |
|---|---|---|---|---|---|---|---|---|---|---|
| 7 | 11 | 10 | 10 | 11 | 11 | 10 | 11 | 11 | 11 | 11 |
| 8 | 23 | 20 | 20 | 23 | 23 | 21 | 23 | 23 | 23 | 23 |
| 9 | 47 | 36 | 36 | 45 | 45 | 43 | 47 | 47 | 47 | 47 |
| 10 | 106 | 72 | 72 | 94 | 95 | 93 | 105 | 106 | 106 | 106 |
| 11 | 235 | 136 | 136 | 195 | 212 | 205 | 235 | 235 | 235 | 235 |
| 12 | 551 | 272 | 272 | 419 | 450 | 474 | 546 | 551 | 551 | 551 |
| 13 | 1,301 | 528 | 528 | 879 | 1,059 | 1,112 | 1,288 | 1,298 | 1,301 | 1,301 |
| 14 | 3,159 | 1,056 | 1,056 | 1,851 | 2,276 | 2,663 | 3,128 | 3,141 | 3,159 | 3,159 |
| 15 | 7,741 | 2,080 | | | | | | | 7,741 | |
| 16 | 19,320 | 4,160 | | | | | | | 19,320 | |

As fractions: C P D 100, 100, 95.7, 88.7, 83.0, 76.0, 67.6, 58.6 % for
`n = 7..14`; C P B 100, 100, 95.7, 89.6, 90.2, 81.7, 81.4, 72.0 %;
C P + Lemma 8: 100 % up to 9, then 99.1, 100, 99.1, 99.0, 99.0 %;
C T D: 100 % up to 12, then 99.8, 99.4 %; the two bold columns 100 %.
(Using Rule N in place of Lemma 8, or adding P to a set containing T, changes
no entry. The column "C + Lemma 8" is README §9's closure.)

**Smallest trees not reached.**

| rules | smallest trees not reached |
|---|---|
| C, P, T | `n = 7`: spider `S(2,2,2)` (every non-caterpillar is missed) |
| C, P, D and C, P, B | `n = 9`: spiders `S(2,2,2,2)` and `S(3,3,2)` |
| C + Lemma 8 (README) | `n = 7`: `S(2,2,2)` |
| C, P + Lemma 8 (also with B) | `n = 10`: `S(3,3,3)`, the only one below `n = 12` |
| C, T, D | `n = 13`, three trees: `S(2,2,2,2,2,2)`; a centre with four neighbours, each carrying two leaves; the path on 5 vertices with two pendant paths of length 2 on each end vertex |
| C, T, B | none for `n ≤ 16` |
| C, T + Lemma 8 | none for `n ≤ 14` |

**Observation (`n ≤ 16`).** Every tree on at most 16 vertices has a growth
placement derived from staircases by Rules C, T and B.
**Observation (`n ≤ 14`).** The same with README Lemma 8 in place of B.

**How much of everything is derived.** With C, T, Lemma 8 and B together the
derived placements are all growth placements for `n ≤ 10` and almost all
beyond:

| n | growth placements | derived | 
|---|---|---|
| 9 | 1,764 | 1,764 |
| 10 | 7,888 | 7,888 |
| 11 | 40,220 | 40,092 |
| 12 | 214,600 | 211,880 |
| 13 | 1,275,368 | 1,254,320 |
| 14 | 7,926,160 | 7,820,452 |

With C, T, B alone far fewer placements are derived (983,056 at `n = 14`,
4,227,136 at `n = 15`, 14,256,216 at `n = 16`) and still every tree is reached.

**Two derivations** (`TRACE=… ./closure`), to show what a derived placement
looks like. Brackets are listed longest first.

`S(2,2,2)`, the first tree outside the caterpillars:

```
#1  n=3   0-2 0-1                    star
#2  n=5   0-4 1-4 0-2 2-3            B: #1 times 2, blocks owned by labels 2, 1   (the path 1-4-0-2-3)
#3  n=6   0-5 0-4 1-4 0-2 2-3        T: top two brackets of the star on 6, last three of #2
#4  n=6   0-5 1-5 1-4 3-5 2-3        C: complement of #3
#5  n=7   0-6 0-5 1-5 1-4 3-5 2-3    T: top two brackets of the star on 7, last four of #4
```

`S(3,3,3)`, the tree README §9–10 singles out (no clean leaf, not reached by
one gap split from any smaller growth placement):

```
#1  n=5   0-4 0-3 0-2 0-1                          star
#2  n=9   0-8 1-8 0-6 3-8 0-4 5-8 0-2 6-7          B: #1 times 2, blocks owned by 4, 4, 4, 3
#3  n=9   0-8 0-7 2-8 0-5 4-8 0-3 6-8 1-2          C: complement of #2
#4  n=10  0-9 0-8 1-8 3-9 1-6 5-9 1-4 7-9 2-3      T: top three brackets of the staircase 0-9 0-8 1-8 …, last six of #3 shifted by 1
#5  n=9   0-8 1-8 0-6 3-8 0-4 4-7 0-2 4-5          B: #1 times 2, blocks owned by 4, 4, 2, 2
#6  n=4   0-3 0-2 0-1                              star
#7  n=7   0-6 1-6 0-4 0-3 0-2 4-5                  B: #6 times 2, blocks owned by 3, 0, 2
#8  n=7   0-6 0-5 2-6 3-6 4-6 1-2                  C: complement of #7
#9  n=9   0-8 1-8 0-6 3-8 0-4 4-7 5-7 2-3          T: brackets longer than 2 of #5, last two of #8
#10 n=10  0-9 0-8 1-8 3-9 1-6 0-4 4-7 5-7 2-3      T: brackets longer than 4 of #4, last four of #9
```

## 5. What this does and does not give

* **Does.** Four proved, checkable ways to combine growth placements, three of
  which (T, N, B) are not in `README.md`; explicit infinite families from B
  and D; the fact that the Δ-construction survives growth exactly for stars;
  and the observation that cut-and-paste plus scaling regenerate a growth
  placement of every tree as far as could be computed.
* **Does not.** Give a rule that says which pieces to use for a given tree.
  T does not create anything: it needs a second placement whose pattern of
  used cells matches. The closure being everything for `n ≤ 16` could fail
  later, as the two-run and two-skip rules of README §11 did.
* **Dead ends.** Anchor-level statements (F1, F2). Δ with a copy that is not
  a star (F3). Nesting whole pieces at a clean cut: correct, but it produced
  nothing that single-leaf insertion does not (Observation, `n ≤ 14`).
  Designs that thread a path through several blocks (Rule B, remark 4): they
  exist, no rule found.
* **A possible next step.** Rule T says that an induction on growth
  placements may forget the tree built so far and remember only the tape.
  A usable induction hypothesis would be a statement about which tapes
  (patterns of used cells) can be completed by which forests. For one run
  that statement is Rule P together with Conjecture B; for the next cases
  (one run plus a few cells, README §11) nothing has been formulated, let
  alone proved.

## 6. Reproducing

```sh
cd results/composition
g++ -O2 -o closure closure.cpp
#  closure N  P NEST BLK T [dumpdir]     P: run filling   NEST: 1 = Lemma 8, 2 = Rule N
#                                         BLK: 1 = Rule D, 2 = Rule B     T: transplant
./closure 14 1 0 0 0        # C P            caterpillars only
./closure 14 1 0 1 0        # C P D
./closure 14 1 0 2 0        # C P B
./closure 14 0 1 0 0        # C + Lemma 8    (README section 9 numbers)
./closure 14 0 2 0 0        # C N            (same numbers)
./closure 14 1 1 0 0        # C P + Lemma 8
./closure 14 0 0 1 1        # C T D
./closure 16 0 0 2 1        # C T B          (n = 15 after about 2 minutes; n = 16 within 15 minutes on a 16 GB machine)
./closure 14 0 1 0 1        # C T + Lemma 8  (about 2 minutes)
./closure 14 0 1 2 1        # everything     (about 3 minutes)
TRACE='((())(())(()))' ./closure 7 0 0 2 1            # a derivation of S(2,2,2)
TRACE='(((()))((()))((())))' ./closure 10 0 0 2 1     # a derivation of S(3,3,3)
mkdir -p out && ./closure 14 0 0 1 1 out && python3 show.py < out/missed13.txt   # trees not reached

python3 verify_rules.py 7 9     # every rule on all trees with <= 7 vertices, from the definitions; closures to n = 9
python3 families.py 7 5         # census of Rule B families
g++ -O2 -o anchortest anchortest.cpp && ./anchortest 14 7    # F1, F2 (about 1 minute)
```

Files: `common.h` (packing, the growth test, canonical forms, all trees by
leaf extension), `closure.cpp`, `anchortest.cpp`, `verify_rules.py`
(independent of the C++), `families.py`, `show.py` (names the trees in a
`missed*.txt` file). Binaries and `out/` are not committed.

## 7. Who contributed what

The bracket picture and the direction to look for compositions are the
repository author's and the coordinator's brief. The classical ingredients
are credited where used: Rosa (caterpillars), Stanton–Zarnke and
Koh–Rogers–Tan (Δ-construction), README Lemmas 6, 8, 10 and Theorems 7, 9.
Rules T, P, N, B, D as stated here, their proofs, the programs and the
closure computations were produced by Claude in this session; they have not
been checked against the literature and have not been refereed.
