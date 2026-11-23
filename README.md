# graceful — a bracket model for the Graceful Tree Conjecture

**Status: the Graceful Tree Conjecture is open, and nothing here proves it.**
This repository makes one picture of the problem exact, proves a few small
things about it, and records two conjectures that are *stronger* than the
Graceful Tree Conjecture and survive an exhaustive computer search.

Interactive version (drag the brackets, watch the proofs): `web/index.html`.

The bracket-and-slide picture is the repository author's; see `INTUITION.md`
for the original idea in their words and a table of who contributed what.
The formalisation, proofs, searches and conjectures were produced by Claude
(Anthropic's AI model) under the author's direction.

## 1. The model

Put vertices `1, 2, …, n` on a line. For each length `k = 1, …, n−1` there is
one **bracket** of length `k`. It sits at a position `p_k ∈ {1, …, n−k}` and is
the edge `{p_k, p_k + k}`. Think of each length as having its own horizontal
rail; a bracket moves only along its rail.

* A **placement** is the tuple `(p_1, …, p_{n−1})`. There are `(n−1)!` of them.
* Every placement is a graceful labeling of the graph it draws: the vertex
  labels are `1..n` and the edge lengths are `1..n−1`, each once.
* A **tree placement** is one whose `n−1` brackets form a tree.
  Most placements are not: brackets can close a cycle and leave a vertex
  out (for `n = 4`: `{1,4}`, `{1,3}`, `{3,4}` is a triangle missing vertex 2).
  A *rail* is only the track of positions available to one bracket.
* The **Graceful Tree Conjecture (GTC)** says: every tree shape on `n`
  vertices is drawn by at least one tree placement.
* The **star** is the placement `p_k = 1` for all `k` (centre at vertex 1).
* A **slide** changes one `p_k` by `±1`. A slide is **legal** if both the
  placement before and after are trees. A **right slide** is `p_k → p_k + 1`.

Reflection `i ↦ n+1−i` maps placements to placements, and right slides to left
slides.

## 2. What is proved

**Lemma 1 (slide rule).** Let `e = {a, b}` be a bracket of a tree placement
and let `A ∋ a`, `B ∋ b` be the two pieces left when `e` is removed. Moving
`e` to `{a', b'}` gives a tree iff `a'` and `b'` lie in different pieces.

*Proof.* `n−1` edges on `n` vertices form a tree iff they are connected. The
new edge reconnects `A` and `B` iff it has one foot in each. ∎

**Theorem 2 (staircases = caterpillars; classical, Rosa 1967).** Call a
placement a *staircase* if `p_{n−1} = 1` and `p_k − p_{k+1} ∈ {0, 1}` for all
`k`: each bracket shares one foot with the next longer bracket ("keeps left"
if the difference is 0, "keeps right" if it is 1) and its other foot is one
step inward. Then every staircase is a caterpillar, and every caterpillar is
drawn by a staircase.

*Proof.* Left feet weakly increase and right feet weakly decrease as `k`
falls, so the foot that moves lands on a vertex untouched by any longer
bracket. Each bracket therefore adds exactly one new vertex: no cycle, `n`
vertices, a tree. The shared feet form a path (the spine) and every other
vertex has degree 1. A run of `m` equal choices hangs `m` vertices on one
spine vertex, a change of choice advances along the spine, so any sequence of
leaf counts along a spine is realised. ∎

**Theorem 3 (right slides reach every caterpillar).** Every staircase can be
reached from the star by right slides, passing only through staircases.

*Proof.* Write `d_k = p_k − p_{k+1} ∈ {0,1}`. A right slide of bracket `k ≥ 2`
changes `(d_k, d_{k−1})` from `(0,1)` to `(1,0)`; a right slide of bracket 1
changes `d_1` from 0 to 1. So a 1 can be created at `d_1` and moved up one
index per slide. Build the target pattern from the largest index down. ∎

**Lemma 4 (all right-slide routes have the same length).** Any route of right
slides from the star to a placement `p` has length `Σ (p_k − 1)`.

*Proof.* Each right slide raises `Σ p_k` by exactly 1, and the star has
`Σ p_k = n − 1`. ∎

**Definition (growth placement).** A placement is a *growth placement* if, for
every `k`, brackets `n−1, n−2, …, k` form a connected tree; equivalently each
bracket, taken longest first, has exactly one foot on a vertex already used.
Equivalently: in the graceful labeling, edge 1 is a pendant edge, after
deleting it edge 2 is a pendant edge, and so on. Staircases are growth
placements.

**Lemma 5.** Every growth placement is a tree placement (same argument as
Theorem 2).

**Lemma 6 (leaf extension).** If a tree `T` has a growth placement, and `v` is
either foot of its longest bracket, then `T` plus a new leaf at `v` has a
growth placement. The same holds with "has a growth placement" replaced by
"is drawn by a placement reachable from the star by legal right slides".

*Proof.* For the vertex labelled `n`: shift all labels up by one and add the
new longest bracket `{1, n+1}`. For the vertex labelled 1: keep all labels and
add `{1, n+1}`. In both cases the old brackets never touch the new vertex, so
the growth order carries over, and so does any sequence of legal slides once
the starting placement is reached. For the vertex labelled 1 the starting
placement is the star itself. For the vertex labelled `n` it is "bracket `n`
at position 1, every shorter bracket at position 2", which is reached from
the star on `n+1` vertices by sliding brackets `1, 2, …, n−1` right once each
in that order (a staircase at every step, Theorem 3). ∎

## 3. Conjectures

Each of A and B implies GTC.

**Conjecture A (right-slide conjecture).** For every `n`, every tree shape on
`n` vertices is drawn by a placement reachable from the star by legal right
slides.

**Conjecture B (growth conjecture).** Every tree has a growth placement.

**Observation C.** For `n ≥ 3`, every tree placement admits at least one legal slide
(checked `n ≤ 14`).

**Observation D.** If a bracket may jump to any position on its rail in one
move, all tree placements form one connected component (checked `n ≤ 14`).

## 4. Evidence

Exhaustive over all tree placements (`src/slide.cpp`):

| n | tree shapes | tree placements | slide components | in star's component | shapes reached by right slides only |
|---|---|---|---|---|---|
| 7 | 11 | 164 | 5 | 148 | 11 |
| 8 | 23 | 752 | 11 | 696 | 23 |
| 9 | 47 | 4,020 | 55 | 3,622 | 47 |
| 10 | 106 | 23,576 | 171 | 22,082 | 106 |
| 11 | 235 | 155,632 | 1,013 | 147,342 | 235 |
| 12 | 551 | 1,112,032 | 4,987 | 1,067,746 | 551 |
| 13 | 1,301 | 8,733,628 | 34,181 | 8,433,246 | 1,301 |
| 14 | 3,159 | 73,547,332 | 216,791 | 71,562,128 | 3,159 |

For `n ≤ 6` the slide graph is connected. From `n = 7` small components split
off, but the star's component always contains every shape.

Growth placements, exhaustive over all trees (`src/growsolve.cpp`, trees from
`networkx.nonisomorphic_trees`): **every tree on `n ≤ 23` vertices has
one**, and every tree on `n ≤ 25` vertices by the stronger three-run check of
section 11. Every spider on `n ≤ 48` vertices has one too (section 8). Spot checks: 200 uniformly random trees at each of `n = 30, 40, 50`,
the path on 40, complete binary tree on 31, complete ternary on 40, spiders
with 10 legs of length 3 and 7 legs of length 5 — all have one.

Number of growth placements for `n = 4..13`:
4, 12, 32, 116, 412, 1764, 7888, 40220, 214600, 1275368.

Negative result: slides that also preserve the growth property are too rigid.
Growth-preserving right slides from the star reach exactly `5·2^(n−4) − 1`
placements (`5 ≤ n ≤ 11`) and miss some shapes from `n = 9` on; allowing left
slides as well does not fix this (`src/growslide.py`).

## 5. Relation to known work, and caveats

A literature pass (Gallian's survey, 28th ed. 2025, sections on graceful trees
and α-labelings read in full; Fang's paper read in full; others by abstract or
partial text) found the following. Items marked † were not read directly.

**The model is known.** Choosing one position for each length is Sheppard's
"labelling sequence" (1976†), which gives the `(n−1)!` count; as a picture it
is the *graceful chessboard* of Haviar and Ivaška (2015†): one dot on each
diagonal of the adjacency matrix. The bracket-and-rail drawing is the same
object. What was not found in the literature: slides as moves, the slide
graph and its islands, and Conjecture A.

**The growth order is known as a search order.** Fang's computer verification
of GTC for `n ≤ 35` (*A computational approach to the graceful tree
conjecture*, arXiv:1003.3045, 2010; derandomising Horton's 2003 thesis†) uses
a backtracking search that puts label 0 on the root (the centre of the tree)
and assigns edge labels `n−1` down to `1`, each to an unlabelled vertex whose
parent is already labelled. Every labeling that search outputs is a growth
placement with the centre as anchor. So:

* `src/growsolve.cpp` is a re-discovery of that search (with the anchor left
  free instead of fixed at the centre).
* Fang's table is evidence for Conjecture B far beyond this repository's
  range: the search succeeded, within a backtrack cap, for 104,635,672 of
  104,636,890 trees at `n = 25` and 2,262,333,140,305 of 2,262,366,343,746 at
  `n = 35` — more than 99.998% at every size from 20 to 35. The rest were
  finished by a different (tabu) search and are not known to have or lack a
  growth placement. Some trees genuinely have none anchored at the centre
  (section 7: the middle of the path on 7 vertices is not an anchor), which
  matches Fang's remark that fixing the root at 0 "misses a lot of potential
  solutions".
* What was not found: the growth property stated as a property of labelings
  or as a conjecture; Theorem 7; clean cuts and gap splits; Theorem 9; the
  `R`-run refinement and Conjecture B3.

**Nearby notions.** Which vertex can carry label 0 ("0-rotatable",
"0-centred", "0-ubiquitously graceful": Van Bussel 2004; Anick 2016; Luiz,
Campos, Richter 2020) is the anchor question without the growth condition; Van
Bussel shows some diameter-4 trees cannot have the centre at 0. Anick's study
found that the trees with fewest graceful labelings fall in two caterpillar
families, consistent with section 8. Dumitru and Nacu (arXiv:2607.12597, 2026)
use a largest-difference-first search for spiders and state that it is not
proved to succeed.

**Classical results used.** Caterpillars: Rosa 1967 (Theorem 2 is that result
in bracket language). Transfers: Hrnčiar and Haviar 2001, all trees of
diameter ≤ 5 are graceful; here a transfer looks like a pair of brackets
reflected together (an informal remark, not worked out). The composition
behind the gluing statement of section 7: Stanton–Zarnke, Koh–Rogers–Tan†.

**State of the conjecture (2026).** Open. Verified for `n ≤ 35` (Fang).
Spiders: graceful with at most 5 legs (Huang–Kotzig–Rosa; Panpa et al.
2025†), with leg lengths differing by at most 1 (Bahls–Lake–Wertheim 2010),
and some further families; open in general. Lobsters (Bermond's conjecture):
open. Asymptotically, every large tree has a labeling using labels up to
`(1+γ)n` when the maximum degree is `O(n/log n)` (Adamaszek, Allen, Grosu,
Hladký 2020) and gracesize at least `(1−ε)n` (Letzter, Pokrovskiy, Williams,
arXiv:2511.11331). Those proofs embed randomly and do not place edge labels
in a prescribed order, so they do not obviously adapt to growth.

**Caveats.** This search was done by an AI system in a few hours and is
not a substitute for an expert's reading. Graceful labelings are abundant for
small trees, so strong statements can hold for all small cases and still be
false.

## 6. Reproducing

```sh
cd src
g++ -O2 -o slide slide.cpp        && ./slide 11 iso      # slide graph statistics
g++ -O2 -o growth growth.cpp      && ./growth 11         # count growth placements
g++ -O2 -o growsolve growsolve.cpp
pip install networkx
python3 gentrees.py 16 | ./growsolve 16                  # growth placement for every tree
python3 growslide.py                                     # growth-preserving slides
python3 export_atlas.py && python3 ../web/build.py       # rebuild the interactive page
g++ -O2 -o growsolve_big growsolve_big.cpp
python3 spiders.py 48 | ./growsolve_big 48 20000         # every spider on 48 vertices
```

## 7. Trying to prove Conjecture B by induction (what was tried, where it breaks)

**The naive step fails.** Deleting the last-placed leaf of a growth placement
leaves `n−1` vertices on `n−1` of the `n` labels with lengths `2..n−1`. That is
not a growth placement of a smaller tree, so "remove a leaf, recurse" does not
close.

**What does go through: gluing at the top (proved).** Let `O` be a tree with a
growth placement on labels `1..r+1` in which every bracket joins a label
`≤ a+1` to a label `> a+1`, and let `x` be the vertex labelled `a+1`. Let `T'`
have a growth placement on `m` vertices with `y` labelled 1 (or `m`; in that case reflect `T'` first). Then the
tree obtained by identifying `x` with `y` has a growth placement: keep `O`'s
low labels, raise its high labels by `m−1`, and drop `T'` into the gap
`a+1..a+m`. `O`'s lengths become `n−1..m`, `T'` keeps `m−1..1`, and the build
order is `O` first, then `T'`. Lemma 6 is the case `O = K_2`. This is the
classical "α-labeling ⊕ graceful labeling" composition; the point is that it
preserves growth.

So induction needs **anchors**: vertices that can carry label 1 in some growth
placement (`src/anchors.cpp`, exhaustive):

| n | vertices over all trees | non-anchors | trees with every vertex an anchor |
|---|---|---|---|
| 8 | 184 | 6 | 18 / 23 |
| 10 | 1,060 | 19 | 95 / 106 |
| 12 | 6,612 | 37 | 525 / 551 |
| 14 | 44,226 | 84 | 3,092 / 3,159 |

For all `n ≤ 14`: almost every vertex is an anchor (99.8% at `n = 14`), every
tree has one, and non-anchors have degree ≤ 3. But they exist (the smallest is
at `n = 6`; the simplest to state are the three middle vertices of the path on
7 vertices), and they follow no pattern
found so far, so "every vertex is an anchor" cannot be the induction
hypothesis. Lemma 6 alone only ever produces anchors at the two ends of the
top bracket, which regenerates exactly the caterpillars.

**A small-state variant fails.** Require the unused labels to form a single
interval `(a, b)` throughout. Then the state is just `(a, b)` and each new leaf
has four options: label `a+1` hung on `b` or on its mirror `2a+2−b`; label
`b−1` hung on `a` or on its mirror `2b−2−a`. This covers every tree on ≤ 8
vertices and 91% at 15, but misses the spider with four legs of length 2 at
`n = 9`, and should fail for most large trees if the observed growth rate
persists: such placements grow by a factor ≈ 2.5 per vertex in the data (the
provable bound is only 4), trees by ≈ 2.96 (`src/interval.cpp`,
`src/classify.py`).

**Where that leaves the induction.** The missing ingredient is a lemma that
produces anchors at *internal* vertices of a tree from growth placements of
smaller trees. The data says such anchors nearly always exist; nothing proved
here creates them.

**Leaf rule (proved).** Let `ℓ` be a leaf of `T` with neighbour `v`. Then `ℓ`
is an anchor of `T` if and only if `v` is an anchor of `T − ℓ`. (If `ℓ` has
label 1 its only bracket is the top one, `{1, n}`, and everything else is a
growth placement of `T − ℓ` on `2..n` with `v` at the top label; conversely
Lemma 6.) The counts agree: the kinds of non-anchor leaf at `n` (vertices
up to symmetry of the tree) are as many as the kinds of non-anchor at `n−1`,
for every `n ≤ 14`. So every exception traces back to a
*primitive* internal non-anchor; there are 1, 2, 2, 4, 4, 5, 14, 18, 24 kinds
of those for `n = 6..14`, almost all of degree 2, with no rule found.

**"Label 1 on a leaf" fails.** One might hope every tree has a growth
placement with label 1 on a leaf, which would make the leaf rule a complete
induction. It does not: among `n ≤ 14`, one tree on 10 vertices and one on 12
have no anchor leaf (and one more appears at `n = 15`).

**Every vertex of degree ≥ 4 is an anchor: true for `n ≤ 19`, fails at
`n = 24`.** This was recorded here as an observation for `n ≤ 14`. It holds
for every tree on `n ≤ 19` vertices and is false in general: in the 24-vertex
tree with edges `0-1, 1-2, 1-3`, leaves `4..11` on `2`, leaves `12..20` on `3`
and leaves `21, 22, 23` on `0`, the degree-4 vertex `0` is not an anchor (two
independent exhaustive searches, and two referees; section 16).

## 8. A cleaner statement of the growth property, and a counterexample hunt

**Theorem 7 (heap form; proved).** A graceful labeling of a tree is a growth
placement if and only if, rooting the tree at the vertex labelled 1, edge
lengths strictly decrease along every path away from the root. (The same
holds rooting at the vertex labelled `n`.)

*Proof.* In a growth placement the brackets of length `≥ k` form a subtree
containing the top bracket `{1, n}`, so each vertex's edge towards the root
was placed before any edge below it, i.e. is longer. Conversely, if lengths
decrease away from the root then the set of edges of length `≥ k` is closed
under moving towards the root, hence connected. ∎

**Corollary (signed-sum form).** Write labels as `0..m`, `m = n−1`. Conjecture
B says: every tree has a root, a bijection `w` from non-root vertices to
`{1..m}` with `w(child) < w(parent)`, and signs `ε`, such that the signed
sums `Σ ε(u) w(u)` along root paths take each value `0, 1, …, m` exactly once.
The sum set obeys `Σ(X) = {0} ⊔ ⊔_children (ε_i a_i + Σ(C_i))`, so the
conjecture is a statement about tiling an interval by translates of the sum
sets of subtrees. An *anchor* is exactly a vertex that can serve as the root.

**Rigid build orders fail.** Requiring the build order to be a depth-first
walk fails for 1 of 47 trees at `n = 9` and 896 of 3,159 at `n = 14`;
breadth-first fails from `n = 7` (`src/ordered.cpp`). The freedom to
interleave branches is essential.

**Where a counterexample would be.** The number of growth placements per tree
has median 56, 110, 258, 572, 1260 for `n = 10..14`, but a few trees have very
few (`src/growcount.cpp`, `src/scarce.py`). The scarcest overall are
caterpillars (safe by Theorem 2). The scarcest non-caterpillars fall in a
handful of families (`src/hardfam.py`): a centre carrying one hub of leaves
and two legs of length 2 (12–24 placements for `n = 10..14`); three equal hubs
around a centre; spiders with three equal legs. Each family was pushed to
52–56 vertices and a growth placement was found every time.

**Spiders.** Every spider on `n ≤ 48` vertices has a growth placement
(exhaustive over all leg-length partitions; 124,730 spiders at `n = 48`;
`src/spiders.py`). Solutions with the centre as root are few and show no
uniform pattern (`src/spiderview.py`), so this is evidence, not a
construction. Gracefulness of all spiders is open.

**Related recent work.** MathWorld's *Graceful Tree Conjecture* entry
describes a different leaf-by-leaf strategy (E. Pegg Jr. and E. Weisstein,
August 2026): open a gap in the label sequence and attach a new leaf to the
root with the gap's label; reported to work for every rooted tree through 22
vertices, and stated there not to be a proof. That move re-labels the tree at
each step; a growth placement is a single labeling whose edges peel off in
order of length. See section 5 for Fang's search, which already builds
labelings in growth order, and for what was and was not found on Theorem 7.

## 9. Clean cuts: an induction step that works almost always

Fix a growth labeling with labels `1..n`. A leaf `ℓ` with label `L`, hung by an
edge of length `j`, is **clean** if the other edges that jump over `L` (one
end below `L`, one above) are exactly the edges longer than `j`.

**Lemma 8 (clean-cut removal and insertion; proved).** If `ℓ` is clean, delete
it and close the gap (labels above `L` drop by one). The result is a growth
labeling of `T − ℓ`. Conversely, in a growth labeling on `n` vertices, if the
edges jumping over a cut position are exactly the `c` longest, open a gap
there: those edges lengthen by one, length `j = n − c` becomes free, and a new
leaf with the gap's label may be hung by a bracket of length `j` on a vertex
`u` at distance `j` from the gap, provided `u` is the root or `u`'s edge
towards the root is one of the `c` edges that jump the cut. Here the root is
the vertex labelled 1, or the vertex labelled `n` if the cut is at the far
left. Given a clean cut, this condition on `u` is necessary and sufficient
for the result to be a growth labeling.

*Proof.* Closing the gap shortens exactly the edges that jumped over `L`, i.e.
those longer than `j`, by one, and leaves shorter edges alone; so lengths
`1..j−1, j+1..n−1` become `1..n−2`, order of lengths is preserved, and hence
so is "lengths decrease away from the root" (Theorem 7; root at the vertex
labelled 1, or at the vertex labelled `n` when `L = 1` and the deleted leaf
was the old root). Insertion is the inverse, and by Theorem 7 the new leaf's
edge, of length `j`, must be shorter than its parent's edge towards the root,
which after opening the gap means that edge is one of the lengthened ones. ∎

Lemma 6 is the special case where the cut is at the far left or far right
(`c = 0`). The gap move is the one described on MathWorld (Pegg, Weisstein,
2026) for graceful labelings in general; the content here is that a leaf can be
added this way only at a clean cut (otherwise two lengths collide and the
labeling is not even graceful), and that it then preserves the growth
property exactly when the new leaf's parent satisfies the condition above.

**How often is a leaf clean?** (`src/cleancut.cpp`, exhaustive.)

| n | leaves over all trees | leaves clean in no growth labeling | trees with no clean leaf at all |
|---|---|---|---|
| 9 | 226 | 2 | 0 |
| 10 | 556 | 5 | 1 |
| 11 | 1,333 | 2 | 0 |
| 12 | 3,365 | 3 | 0 |
| 13 | 8,500 | 3 | 0 |
| 14 | 22,007 | 4 | 0 |

So for `n ≤ 14` every tree except one arises from a growth labeling of a
smaller tree by one clean gap insertion. The exception is the spider with
three legs of length 3 (`n = 10`): it has growth labelings, but none with a
clean leaf.

**Why this is still not a proof.** The step needs the smaller tree to have a
growth labeling *with the right clean cut next to the right vertex*, and the
labeling the step produces need not have the cuts required by the next step.
Carrying only "is a growth labeling" forward is not enough: starting from a
single edge and applying clean gap insertions repeatedly reaches 10 of 11
trees at `n = 7`, 93 of 106 at `n = 10` and 2,663 of 3,159 at `n = 14`
(`src/derive.cpp`); the first tree missed is the spider with three legs of
length 2. The open problem in this form: find a property of growth labelings,
stronger than having one clean cut, that is preserved by the insertion it
enables.

**How the reachable class compares with α-labelings.** A placement is an
*α-placement* if all brackets jump over one common point (the classical
α-labeling). For `n = 7..14` (`src/alpha.cpp`, `src/derive.cpp`):

| n | trees | with an α-placement | reached by clean gap insertions | reached but no α-placement | α-placement but not reached |
|---|---|---|---|---|---|
| 9 | 47 | 42 | 43 | 2 | 1 |
| 11 | 235 | 213 | 205 | 11 | 19 |
| 13 | 1,301 | 1,219 | 1,112 | 43 | 150 |
| 14 | 3,159 | 3,012 | 2,663 | 82 | 431 |

The two classes overlap heavily but neither contains the other, so the
gap-insertion closure is not the α-labelable trees under another name.

**Theorem 9 (α and growth together force a staircase; proved).** If a
placement is a growth placement and all its brackets jump over one common
point, then it is a staircase. Hence a tree has such a placement if and only
if it is a caterpillar.

*Proof.* Let the common point separate left feet `1..A₀` from right feet. Give
bracket `k` the cell `(a, β)` where `a` is its left foot and `β = n − (right
foot)`, so `a ≥ 1`, `β ≥ 0`. A bracket of length `k` has `a + β = n − k`: the
bracket placed at step `t = n − k` lies on anti-diagonal `t` (the top bracket
is the cell `(1, 0)` at step 1). A row or column is *used* once a cell lies in
it. The growth property says each new cell lies in exactly one used row or
column and uses one new one. Claim: after every step `t` the used rows are
`1..A` and the used columns are `0..B` for some `A + B = t`. This holds after
the last step, when every label is used. If it holds after step `t`, the cell
placed at step `t` satisfies `a ≤ A`, `β ≤ B` and `a + β = t = A + B`, so it is
`(A, B)`, and the row or column it newly used is the last one; removing it
leaves the same shape with `A` or `B` one smaller. By backward induction the
claim holds throughout, and the cell at step `t+1` is `(A+1, B)` or
`(A, B+1)`: bracket `k−1` keeps one foot of bracket `k` and moves the other
one step inward. ∎

Checked by brute force for `n ≤ 12` (`src/alphagrowth_check.py`): exactly
`2^(n−2)` growth placements are α-placements, and all are staircases. So
outside caterpillars every growth placement contains a bracket that does not
jump the common point; the classical α-labeling toolkit cannot be combined
with growth beyond caterpillars.

## 10. Vertex splitting: growth labelings of most trees can be built by local moves

A leaf can only be added through a gap by a clean-cut insertion (if any other
set of edges jumps over the gap, two lengths collide). To go further, allow
the new vertex to be more than a leaf.

**Gap split move.** In a growth placement on `n` vertices, open a gap at `L`
(labels `≥ L` move up by one; brackets jumping over the gap lengthen by one).
Put a new vertex `x` at label `L`, join it to an existing vertex `y`, and move
any chosen subset of `y`'s other edges from `y` to `x`. Keep the result if it
is a growth placement. Moving no edge is the leaf insertion of Lemma 8;
moving one edge places `x` in the middle of an edge. Read backwards the move
is: contract an edge, then close the gap. Every tree on `n+1` vertices
contracts to trees on `n`, so in principle this move can reach anything.

**What it reaches, starting from a single edge** (`src/derive2.cpp`):

| n | trees | leaf insertions only | + put `x` in the middle of an edge | any split |
|---|---|---|---|---|
| 7 | 11 | 10 | 11 | 11 |
| 8 | 23 | 21 | 23 | 23 |
| 9 | 47 | 43 | 46 | 46 |
| 10 | 106 | 93 | 105 | 105 |
| 11 | 235 | 205 | 232 | 233 |
| 12 | 551 | 474 | 539 | 544 |
| 13 | 1,301 | 1,112 | 1,274 | 1,283 |

With splits the number of reachable placements grows by a factor of about 3.5
per vertex, faster than the number of trees (about 2.96), so counting no
longer rules out reaching everything. The trees missed are few and of one
kind: the spider with four legs of length 2 (`n = 9`), the spider with three
legs of length 3 (`n = 10`), and at `n = 11, 12` trees made of three or four
long equal arms with a small decoration. They all have growth placements; the
placements just do not arise from a smaller growth placement by one split.

**One step back is almost always possible.** Drop the requirement that the
smaller placement was itself built by splits: ask only whether a tree has
*some* growth placement that comes from *some* growth placement of a smaller
tree by one gap split (`derive2 N 3 prefix full`). For `n ≤ 13` this holds
for every tree except one: the spider with three legs of length 3. About two
thirds of all growth placements on 13 vertices arise this way (851,358 of
1,275,368). So that spider is the only tree found whose growth placements
are all "primitive".

**The exceptions are not one tidy family.** Add every growth placement of
each unreached tree as a new starting point and continue
(`derive2 N 3 prefix prim`). New unreached trees keep appearing: 1, 1, 1, 2,
3, 7 of them for `n = 9..14`. They are spider-like or built from a few equal
branches, but they do not form a single recognisable family, so "prove the
generic case by splits and handle one explicit family separately" is not
available in this simple form. An earlier version of this section suggested
it was; that was too optimistic.

**Growth placements and right slides are unrelated.** Most growth placements
are *not* reachable from the star by legal right slides (31,774 of 40,220 at
`n = 11`; `src/growreach.py`), so Conjecture B does not feed Conjecture A.

**Where the difficulty sits.** An induction by gap splits must carry, for each
tree, which cuts are available next to which vertices. One step back is
almost always possible; no property found so far is both preserved by the
step and strong enough to guarantee the next one.

## 11. Blocks and holes: how little freedom a growth placement needs

Watch the set of unused labels while brackets are placed longest first
(`src/trace.cpp` prints it; the page shows it as a "tape"). Typically a block
of used labels grows in from each end and a few holes are left behind and
filled late by short brackets. Call a maximal interval of unused labels a
*run*. A growth placement is an **`R`-run growth placement** if the unused
labels never form more than `R` runs. `R = 1` is the interval variant of
section 7: used labels are a left block and a right block. `R = 2` allows one
island between them, `R = 3` two islands.

| | `R = 1` | `R = 2` | `R = 3` |
|---|---|---|---|
| first tree with no such placement | spider `S(2,2,2,2)`, `n = 9` | two trees at `n = 16` | none found |
| trees without one, `n = 15` | 724 of 7,741 | 0 | 0 |
| trees without one, `n = 16` | — | 2 of 19,320 | 0 |
| trees without one, `n = 18` | — | 1 of 123,867 | 0 |
| exhaustive range with none missing | `n ≤ 8` | `n ≤ 15` | `n ≤ 25` (104,636,890 trees at `n = 25`) |

(`src/holes.cpp` enumerates placements; `src/runsolve.cpp` and
`src/runsolve_gen.cpp` search tree by tree, the latter with a built-in tree
generator, `src/treegen.h`, validated against the known numbers of trees. The
two `R = 2` failures at `n = 16` were confirmed independently: the enumerator
finds 19,318 of 19,320 shapes.)

**Conjecture B3 (three-run growth conjecture).** Every tree has a growth
placement in which the unused labels never form more than three runs.
B3 implies B, which implies GTC.

Evidence beyond the exhaustive range: 300 uniformly random trees at each of
`n = 30, 40, 50, 60`; and the symmetric families that defeat `R = 2` (three to
eight equal branches, hubs of odd size, equal-leg spiders), followed to 53
vertices, where three runs were always enough and sometimes necessary.

**Why this matters.** The state of a three-run build is at most four blocks of
used labels, i.e. a handful of integers, and each step has a bounded number of
choices (the new label must extend a block or start an island). That is the
smallest search space found so far that still seems to contain every tree, and
the search is fast: all 2,144,505 trees on 21 vertices in about two minutes on
one core.

**Caution, from this project's own history.** The two-run version looked
universal through `n = 15` (7,741 trees) and then failed for 2 trees in 19,320
at `n = 16`. Most of its known failures are trees with three equal branches
(one of the two 16-vertex failures has only two). A three-run failure could be waiting in the same way at a size not
yet reached.

**Parity in the failures.** In the family "centre, three arms of length 2,
each ending in a hub of `m` leaves", one run suffices when `m` is even and
three are needed when `m` is odd (`m = 2..8`). Unexplained.

**Lemma 10 (balance rule; proved).** Play on a row of `n` cells with the two
end cells used and joined. A move picks an unused cell `x` and a used cell `y`
such that the number of used cells strictly between them equals the number of
unused cells outside the interval from `x` to `y`; it marks `x` used and joins
`x` to `y`. The trees obtained after `n − 2` moves, with cells as labels, are
exactly the growth placements. Bracket lengths never need to be mentioned.

*Proof.* When `k` cells are unused the next bracket in a growth placement has
length `k`, so `k − 1` cells lie strictly between its feet. Of the `k` unused
cells one is `x`; the others are between the feet or outside. Hence
(used between) `= k − 1 −` (unused between) `=` (unused outside). The converse
is the same count read backwards. ∎ (Checked for `n ≤ 9`,
`src/balance_check.py`.)

Equivalently: going right from `x`, the partner is the `(1 + j + b)`-th used
cell, where `j` unused cells lie to the left of `x` and `b` to the right of
the partner. With a single gap and no holes, an end cell of the gap attaches
across the gap to the innermost cell of the opposite block (`j = b = 0`): a
staircase step. Each outstanding hole shifts that target one cell deeper.

**The two-skip rule (fails at `n = 22`).** For a while the following looked
universal: every tree has a growth placement in which, at every moment, the
unused labels are one run together with at most two isolated single labels
(two blocks grow inward; a move may skip one cell; at most two skipped cells
wait to be filled). It holds for every tree on `n ≤ 21` vertices and fails for
exactly one of the 5,623,756 trees on 22 vertices: two vertices, each carrying
six leaves, joined by a path with one extra pendant path
(edges `0-1 1-2 2-3 3-4`, leaves `5..10` on `4`, `0-11 11-12 12-13`, leaves
`14..19` on `13`, `12-20 20-21`). That tree can be built with three single
skips, and with only two runs when a hole may have more than one cell.
Confirmed with a second solver (`src/runsolve128.cpp`) and by the independent
re-verification of section 16, which used a SAT solver for this tree.

| rule | first failure | exhaustive range with no failure |
|---|---|---|
| one run, at most one single skipped cell | 1 tree at `n = 10` (spider `S(3,3,3)`); none at 11, 12; 1 at 13 | `n ≤ 9` |
| one run, two skipped cells, both on the same side of the run | 1 tree at `n = 15` | `n ≤ 14` |
| one run, at most one skipped cell on each side of the run | 1 tree at `n = 18` | `n ≤ 17` |
| one run, at most two single skipped cells | 1 tree at `n = 22` | `n ≤ 21` |
| at most three runs of any sizes (B3) | none found | `n ≤ 25` |

(`./holes n R HS SIDE` enumerates; `./runsolve_gen n 3 part parts 1 SIDE`
searches tree by tree. The two agree at `n = 13` and `n = 15`.)

The number of single skipped cells needed therefore grows with the size of
the tree: none suffices up to 8 vertices, one up to 9, two up to 21. It is not
monotone in between: the spider `S(3,3,3)` on 10 vertices needs two, while
every tree on 11 or 12 vertices needs at most one. (An earlier version of
this table gave 13 and 18 as first failures for two of the rules; those rules
had only been run from `n = 12` up. `src/skipmin.cpp` now computes the least
number of skips for every tree and all rows were re-run from `n = 5`. A later
independent re-verification (section 16) corrected the "one on each side" row
a second time: read literally, that rule first fails for one tree on 18
vertices; the value 10 came from this repository's program treating the
leftmost single cell as the main run when every unused run is a single cell.) Every
tightening tried has failed, the looser ones at larger sizes. Conjecture B3
(three runs of any size) is the loosest of these rules and has not failed for
`n ≤ 25`, but by the same pattern it may fail at a size not yet reached; the
statement to trust least is any fixed bound on the number of holes. What
survives all of this is Conjecture B itself, with no bound on holes.

In a build with at most two skipped cells each step has at most six candidate cells (either end of the
main run, one cell in from either end, or a skipped cell) and two possible
partners for each, and the state is the main run plus at most two positions.

**Spherically symmetric trees** (every vertex at depth `i` has `d_i`
children) are the natural stress test for these rules. With a 128-bit
solver (`src/runsolve128.cpp`): three runs suffice, and are needed, for
branching `(3,3,3)` on 40 vertices, `(4,4)` on 21, `(5,5)` on 31,
`(2,2,2,2,2)` on 63 and `(3,3,3,2)` on 94; two runs suffice for `(2,2,2)` and
`(2,2,2,2)`. None needed four.

## 12. What the number of skips depends on, and spiders

**Least number of skips, tree by tree** (`src/skipmin.cpp`, exhaustive; a skip
is a single unused cell outside the main run, as in section 11):

| n | trees | need 0 | need 1 | need 2 |
|---|---|---|---|---|
| 9 | 47 | 46 | 1 | 0 |
| 10 | 106 | 104 | 1 | 1 |
| 12 | 551 | 531 | 20 | 0 |
| 14 | 3,159 | 2,926 | 232 | 1 |
| 16 | 19,320 | 17,132 | 2,177 | 11 |
| 18 | 123,867 | 103,980 | 19,837 | 50 |

No tree on `n ≤ 21` needs three; one on 22 does (section 11).

**What predicts it** (all 32,307 trees with `11 ≤ n ≤ 16`,
`src/skipfeat.py`). The best single predictor found is the largest number of
*non-leaf* neighbours of any vertex, i.e. how many real branches meet at one
point:

| branches meeting at one vertex | trees | need at least one skip |
|---|---|---|
| ≤ 2 (caterpillars) | 8,232 | 0% |
| 3 | 19,922 | 8% |
| 4 | 3,674 | 37% |
| 5 | 430 | 76% |
| 6 | 45 | 98% |
| 7 | 4 | 100% |

Leaves do not count: maximum degree by itself predicts nothing (stars and
near-stars need no skips). Number of branch vertices and diameter are weak
predictors. The trees needing *two* skips at `n ≤ 16` are almost all built
from three to five equal branches of depth at least 2 (for instance spiders
with all legs of length 3). So skips are needed to return to a vertex where
several deep branches meet; this is a tendency, not a law, and the exact
number depends on arithmetic coincidences (next table).

**Spiders.** Spiders put all branching at one vertex, so they are the natural
test. Least number of skips for the spider with `k` legs of length `L`
(`src/runsolve128.cpp`, which now treats unbuilt branches of the same shape as
interchangeable):

| `L` \ `k` | 3 | 4 | 5 | 6 | 8 |
|---|---|---|---|---|---|
| 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | 0 | 1 | 1 | 1 | 1 |
| 3 | 2 | 2 | 2 | 2 | 2 |
| 4 | 0 | 2 | 1 | 2 | 2 |
| 5 | 0 | 1 | 1 | 2 | 2 |
| 6 | 1 | 1 | 1 | 1 | 2 |

Over *all* spiders (every multiset of leg lengths, `src/spiderskips.sh`):

| n | spiders | need 0 | need 1 | need 2 | need more |
|---|---|---|---|---|---|
| 16 | 168 | 143 | 24 | 1 | 0 |
| 20 | 480 | 378 | 102 | 0 | 0 |
| 24 | 1,243 | 888 | 343 | 12 | 0 |
| 26 | 1,945 | 1,325 | 591 | 29 | 0 |
| 28 | 2,996 | 1,930 | 990 | 76 | 0 |
| 30 | 4,550 | 2,823 | 1,557 | 170 | 0 |

**Observation (even `n` from 10 to 30).** Every spider can be built with
at most two skips. Unlike general trees, there is no sign yet of the number
growing. Whether all spiders are graceful is an open problem (known for at
most 5 legs and for leg lengths differing by at most one; section 5), so a
proof of this observation would be a new theorem.

**A cleaner form of the spider question.** Put the centre at label 0 and let
every leg zigzag. Then a graceful numbering is exactly this: split the numbers
`1..m` into one strictly decreasing list per leg, of the leg's length, so that
all the alternating sums `w_1`, `w_1 − w_2`, `w_1 − w_2 + w_3`, … over all
lists are different. (They are then automatically the labels `1..m`, the
lists are the edge lengths going outward, and the result is a growth placement
anchored at the centre.) `src/spiderzig.cpp` searches for such a split.

For every spider on `n ≤ 21` vertices a split exists, except:

* three-legged spiders with a leg of length 1 and certain other two legs
  (`(3,3,1)`, `(5,5,1)`, `(6,5,1)`, …); these are caterpillars and have
  staircases;
* `S(3,3,3)`;
* `S(2,2,…,2)` with `k = 5` and `k = 8` legs (and `k = 11`, on 23 vertices,
  outside the fully checked range).

**Lemma 11 (an arithmetic obstruction; proved).** The spider with `k` legs of
length 2 has no zigzag split when `k ≡ 2 (mod 3)`.

*Proof.* Let `I` be the labels next to the centre and `O` the outer labels,
so `I ⊔ O = {1..2k}`. The inner edge lengths are the labels in `I`, so the
outer edge lengths are exactly the numbers in `O`. Each outer label is its
inner neighbour minus an outer edge length, so `ΣO = ΣI − ΣO`, i.e.
`3·ΣO = ΣI + ΣO = k(2k+1)`. If `k ≡ 2 (mod 3)` then `k(2k+1) ≡ 1 (mod 3)`. ∎

So the zigzag form is not universal, and its failures are arithmetic, in the
same way as the parity effect noted in section 11. Those spiders still have
growth placements with at most two skips; they need a leg that does not
alternate, or the centre away from label 0.

**What a proof for spiders would need.** A rule for dealing the numbers
`m, m−1, …, 1` to the legs. Dealing them in strict rotation fails (two legs
get the same second label). The builds found by search for equal legs
interleave the legs in a regular but not purely rotating order
(`src/spidershow.py` prints them). No explicit rule has been found.

## 13. The spider dealing problem

**Setting.** Put a spider's centre at label 0, labels `0..m`. A growth
placement anchored at the centre is then a *deal*: hand the numbers
`m, m−1, …, 1` to the legs, one at a time, each leg receiving as many numbers
as its length; each number moves that leg's tip up or down by that amount
(the first move of a leg is up, from 0). The deal is valid if no label is
visited twice. A *zigzag deal* is one in which every leg alternates up, down,
up, … (section 12).

**Conjecture S (centre-anchored spiders).** Every spider has a valid deal;
that is, a graceful labeling with the centre labelled 0 and edge lengths
decreasing outward along every leg.

Evidence: every spider on `4 ≤ n ≤ 37` vertices has one, with no
exception (`FREE=1 ./spiderzig n`; exhaustive over all leg-length patterns
with at least three legs). The spiders that have no zigzag deal (`S(3,3,3)`,
legs of length 2 with `k ≡ 2 mod 3`, …) all have a valid deal once a leg may
move twice in the same direction. Conjecture S implies that all spiders are
graceful, which is open.

**Reductions and partial steps (proved).**

* *Legs of length 1 can be ignored.* If a spider has a valid deal, so does
  the spider with extra legs of length 1: deal the new longest numbers to the
  new legs first (Lemma 6). So Conjecture S reduces to spiders with all legs
  of length at least 2.
* *One more leg of any length, without the anchor.* If a tree has a growth
  placement with `y` as anchor, then the tree with a pendant path of any
  length `r` attached at `y` has a growth placement. (Gluing statement of
  section 7 with `O` the path on `r` edges in zigzag form: started from its
  label-1 end if `r` is even, or reflected if `r` is odd, its other end carries
  the largest low label.) In particular: if a spider has a valid deal, the
  spider with one more leg of any length is graceful. The new placement is not
  anchored at the centre, so the step cannot be repeated.

**What does not work** (all for centre-anchored deals).

| rule tried | result |
|---|---|
| zigzag deal, numbers handed out in a repeating order of period 3, 6 or 9, three equal legs | no order works for all leg lengths (`src/dealrule.py`) |
| level by level (every leg gets its `j`-th number before any gets its `(j+1)`-th) | fails for 3 of 11 spiders at `n = 8`, 129 of 288 at `n = 18` |
| first number of every leg first, then free | fails for 3 of 11 at `n = 8`, 26 of 480 at `n = 20`; the failures have many legs of length 1 |
| leg by leg (finish one leg before starting the next) | the second leg cannot start unless the first has at least half the edges |
| growing by clean gap insertion of one leaf at a time (Lemma 8), keeping the centre at 0 | reaches 36 of 231 leg patterns at `n = 17` (`src/derive_spider.cpp`) |

**Status.** No explicit dealing rule has been found, for all spiders or for a
new family. What this section adds is the exact form of the problem
(Conjecture S), its verification range, the reduction to legs of length at
least 2, and a list of natural rules that are now known not to work.

## 14. What a skip does (worked by hand)

**Setting.** Labels `1..n`, brackets placed longest first. At any moment call
the longest run of unused labels the *main gap*; `a` is the used label just
left of it and `d` the used label just right of it. The other unused labels
are *holes* (skipped cells); let `H` be their number. A new label placed in
the main gap and joined to a label on the far side of the gap is an *across*
move.

**Lemma 12 (offset rule; proved).** Suppose the new label is `a + 1 + s`
(counting from the left, having skipped `s ≥ 0` cells) and the move is across.
Then its partner is exactly `d + H + s`: the label `H + s` places in from the
innermost label on the right. Symmetrically, the new label `d − 1 − s` joins
`a − H − s`. In words: **the partner sits as many places in from the tip of
the opposite block as there are holes after the move.**

*Proof.* The bracket placed has length equal to the number of unused labels,
`(d − a − 1) + H`. So the partner of `a + 1 + s` is
`a + 1 + s + (d − a − 1) + H = d + H + s`. The other side is the same count. ∎
(Checked on all 70,382 across moves in all growth placements with `n ≤ 10`,
`src/offset_check.py`.)

**Reading it as two stacks.** Think of the left block and the right block as
stacks whose tops are `a` and `d`. With no holes, a new label on one side
joins the *top* of the other stack. Staying on the same side adds another
child to that top; switching sides descends to the child just added. One can
only walk down a path, hanging leaves along the way: a caterpillar
(Theorem 2). Once the walk has descended past a vertex, that vertex is buried
one place down and can never be joined again by an across move.

With one hole, every across move joins the cell *one place down* instead of
the top. So a vertex becomes available as a parent one push after it is
placed, and the build can return to it after having gone past it once.

**Corollary (threads).** Hold `H` holes fixed and push alternately left,
right, left, …. The `i`-th left label joins the right label pushed `H + 1`
pushes earlier, and the `i`-th right label joins the left label pushed `H`
pushes earlier; following parents, the push index drops by `2H + 1` per round
trip. So the across edges form **`2H + 1` parallel paths**: no holes, one
path; one hole, three paths growing in rotation; two holes, five.

**The smallest example.** The spider with four legs of length 2 (9 vertices)
is the smallest tree that needs a skip (section 11). Its build, with the
centre at label 1:

| bracket | new label | joins | what happened |
|---|---|---|---|
| 8 | 9 | 1 | the only place for the longest bracket |
| 7 | 2 | 9 | left block grows; joins the right tip |
| 6 | 7 | 1 | **skips 8**; so it joins one place down on the left: the centre, not 2 |
| 5 | 6 | 1 | one hole still open: again one place down, the centre |
| 4 | 3 | 7 | left block grows; joins one place down on the right |
| 3 | 4 | 1 | a same-side bracket (see below) |
| 2 | 8 | 6 | the hole is filled by a short same-side bracket |
| 1 | 5 | 4 | |

After `1–9` and `9–2` the centre is buried under label 2. Without a hole every
further across move would join 2 or 9, and the centre could never get its
remaining legs that way. The skip is what brings the centre back into reach.

**Two more facts that complete the picture.**

* *Same-side brackets come late.* A new label `a + 1` can also join a label on
  its own side, namely `a + 1 − t` where `t` is the number of unused labels.
  That label exists only when `t ≤ a`, i.e. once a block is at least as large
  as what remains. So roughly the first half of every build consists of
  across moves only, and obeys the offset rule exactly.
* *A hole is repaid late.* A hole at `h` can only be filled by a bracket of
  length `t` joining `h − t` or `h + t`, both of which must already be used;
  for a hole inside a block this needs `t` small. So holes opened early stay
  open for most of the build: `H` goes up easily and comes down only near the
  end.

**What this says about which trees are hard.** During the across phase the
number of holes is the number of places down that parents are taken from, on
both sides at once, and it cannot be lowered. A tree whose first half can be
laid out so that this depth never has to decrease is easy. Several equal deep
branches meeting at one vertex force the build to keep returning to that
vertex while the branches advance, which is the three-or-five-threads
pattern, and that is exactly the kind of tree found to need skips
(section 12). This is an explanation of the data, not yet a theorem about
which trees need how many holes.

## 15. Composition: fattening, and explicit rules for spider families

These results came from a multi-agent run: four independent attempts, each
followed by an independent referee who re-implemented the rule from its
statement and tried to break it. The statements below are the ones that
survived; the first is re-proved here and was re-checked by the main author's
own program, including for trees that are not spiders.

**Theorem 13 (fattening; proved).** Let `S` and `T` be trees with growth
placements anchored at roots `r_S` and `r_T`, with `m` and `n` edges. Then the
tree obtained by gluing `S` and `2m + 1` copies of `T` at their roots has a
growth placement anchored at the glued root.

*Construction.* Use labels from 0, roots at 0. Put `k = 2m + 1` and, for
`x ∈ [−m, m]`, `δ(x) = −x − m` if `x ≤ 0`, `δ(x) = m + 1 − x` if `x > 0`.
Keep `S` as it is (labels `0..m`). For every non-root vertex `v` of `T`, with
label `ℓ` and depth `j ≥ 1`, and every `i ∈ [−m, m]`, make a copy with label
`kℓ + δ^{j−1}(i)`, joined to the copy of `v`'s parent with the same `i`
(copies of children of the root are joined to the root).

*Proof.* `δ` reverses `[−m, 0]` and reverses `[1, m]`, so it is a permutation
of `[−m, m]`; and `τ(x) = x − δ(x)` equals `2x + m` for `x ≤ 0` and
`2x − m − 1` for `x > 0`, so it takes each value of `[−m, m]` once.
*Labels.* For a fixed vertex of `T` with label `ℓ`, the copies carry
`kℓ + δ^{j−1}(i)`, `i ∈ [−m, m]`, which is the window `[kℓ − m, kℓ + m]`.
The labels of `T` are `1..n`, so the windows tile `[m + 1, m + kn]`; with
`S` on `[0, m]` every label is used once.
*Lengths.* Take an edge of `T` of length `c` from parent label `p` to child
label `p + sc` (`s = ±1`), and let the parent's copy carry offset `E`. The
copy edge joins `kp + E` to `k(p + sc) + δ(E)`, so its length is
`kc − sτ(E)` (for an edge at the root, `kc + i`). As `i` runs over
`[−m, m]`, so does `E` and hence `−sτ(E)`: the copies of that edge have
exactly the lengths `kc − m .. kc + m`. For `c = 1..n` these windows tile
`[m + 1, m + kn]`; with `S`'s lengths `1..m`, every length is used once.
*Downhill.* Along a path away from the root in `T` the lengths drop by at
least 1 per edge, so in a copy they drop by at least `k − 2m = 1`; all copy
lengths exceed `m`, so `S` stays downhill too. By Theorem 7 this is a growth
placement anchored at the root. ∎

Checked: all 28,056 pairs of anchored growth placements of trees with at most
7 vertices each (`src/fatten_trees.py`); for spiders, all 638,401 pairs of
valid deals with at most 9 edges each, by the referee.

*Picture.* Scale `T` by `2m + 1`. Every label and every length of `T` becomes
a window of `2m + 1` cells; the root's window is `[−m, m]` and `S` sits in its
right half; the copies thread the windows, shuffled by `δ` at each step.

**Consequences (all with no search).**

* *Stacking.* If a tree with `t` edges has an anchor `v`, then hanging
  `2t + 1` pendant paths of any common length `L` on `v` gives a tree with a
  growth placement anchored at `v`. For spiders there is a closed form: with
  `k = 2t + 1`, leg `s = 1..k` receives `t + (L−1)k + s` first and then
  `t + (L−j)k + u(s)` for `j = 2..L`, where `u(s) = 2s` for `s ≤ t` and
  `2s − k` otherwise, moving up, down, up, …
  (`src/rules/equal/rule_equal.py`, proof in `src/rules/equal/REPORT.txt`;
  refereed as complete).
* *Equal-leg spiders in towers.* `K` legs of length `L` have a valid deal
  whenever `K = 1 + (2L+1) + … + (2L+1)^j`: 6 legs of length 2, 8 of length
  3, 10 of length 4, then 31 legs of length 2, 57 of length 3, ….
* *`2j + 1` legs of length `L` plus `j` legs of length 1*, for every `L` and
  `j`.
* *Odd bunches of any anchored tree.* For any tree `T` with anchor `v` and any
  `j ≥ 0`: `2j + 1` copies of `T` glued at `v`, plus `j` leaves at `v`, has a
  growth placement. The result is anchored at `v`, so the step can be
  repeated and mixed with Lemma 6.

**Explicit rules for two more spider families** (written arguments exist in
`src/rules/…`; each was re-implemented and confirmed by a referee on the
ranges shown; the referees judged the arguments free of errors but with gaps
of exposition, so they are recorded here as *verified with a written
argument*, not as Proved in the sense of `CLAUDE.md`).

* *All legs of length 2.* A recursive rule with no search gives a valid deal
  for every number of legs `k`: a zigzag deal when `k ≡ 0, 1 (mod 3)`, and a
  deal with exactly one leg moving up twice when `k ≡ 2 (mod 3)`, where
  Lemma 11 shows a zigzag deal is impossible. Confirmed for every `k ≤ 6000`
  and spot-checked to `k = 2,000,006` (`src/rules/len2/rule.py`, argument in `REPORT.txt` there).
* *One long leg and `k` legs of length 2.* An explicit rule covers every `k`
  and every long-leg length `r` with `r + k ≡ 1 (mod 3)` above a small
  threshold, and every `r ≥ 2k` when `3 | k`. Confirmed for all `k ≤ 330`,
  `r ≤ 1500` (`src/rules/twolens/rule.py`, `PROOF.txt`).

**Steps that do not work** (from the same run, exhaustive over all valid
deals of spiders with up to 13–16 edges): lengthening one leg by one,
lengthening every leg by one or two, adding one leg of length 2, adding two
legs of length 2. Each fails for some small deal; the smallest failures are
listed in `src/rules/induct/PROOF.txt`.

**Novelty.** Theorem 13 is a product construction in the spirit of
Stanton–Zarnke and Koh–Rogers–Tan (section 5); what is checked here is that
it preserves the growth property and the anchor. Whether the spider families
above are new as graceful trees has not been checked against the literature:
equal-leg spiders are known to be graceful (Bahls–Lake–Wertheim), spiders
with legs of two very different lengths in general are not.

## 16. Results of the nine-line panel

A multi-agent run attacked the problem along nine independent lines. Every
claim was then given to two referees who had not seen the claimant's code: one
re-implemented the statement from the definitions and tried to break it, one
read the proof line by line. What follows is what survived both, in the
author's summary; the full statements, proofs, programs and verdicts are in
`src/attack/<line>/REPORT.txt`, `src/attack/<line>/` and
`src/attack/REFEREE_VERDICTS.json`. "Proved" below means: a complete written
argument in the cited file, judged complete by the proof referee and
confirmed by brute force by the other. None of this proves the Graceful Tree
Conjecture or Conjecture B.

**Slides (the original picture).**

* *Proved: Conjecture A holds for every spider with legs of length at most
  2.* An explicit placement of the spider with `a` legs of length 2 and `b`
  leaves is reached from the star by an explicit sequence of legal right
  slides. This is the first family beyond caterpillars for which a slide route
  is proved (`src/attack/slides`).
* *Proved: what freezes a bracket.* A bracket of length at least 2 with a leaf
  at one foot has no legal slide; a bracket of length 1 with a leaf foot has
  exactly one. An explicit two-element island exists for every `n ≥ 7`.
* *Fails:* "every tree shape is drawn by a placement with no legal left
  slide" is false at `n = 4, 6, 8, 12` (one shape missing each time).
* *Observation (`n ≤ 13`):* allowing two brackets to slide at once makes all
  tree placements one island.

**Explicit builds for trees of diameter 4.**

* *Proved:* closed-form growth placements, with no search, for (i) every tree
  made of a centre joined to three stars, and (ii) every tree made of a centre
  joined to `d` stars with `a` leaves each and one more star with at least
  `d − 1` leaves (`src/attack/gamestrategy`).
* *Conjecture (checked for every diameter-4 tree with `n ≤ 26`):* every
  diameter-4 tree has a growth placement of one specific shape, with a largest
  star's centre at the end label ("all-up comb").

**Induction by clean cuts.**

* *Proved:* the clean leaf of Lemma 8 generalises to a *clean set* of labels:
  deleting a clean set leaves a growth placement; disjoint clean sets stay
  clean, so deletions commute; peeling clean leaves in any order ends at the
  same placement. A placement in which every leaf is clean is a staircase.
* *Fails: no bounded step size.* Let `C(K)` be the placements that can be
  dismantled by clean sets of size at most `K`. For each `K ≤ 5` some
  three-legged spider has growth placements but none in `C(K)`; the step
  needed for three legs of length `L = 1..9` is 1, 2, 3, 2, 2, 5, 3, 6, 6. So
  the gap-insertion induction of sections 9–10 needs unboundedly large steps
  (`src/attack/cutinduction`).

**Anchors.**

* *Fails:* "every vertex of degree ≥ 4 is an anchor" (see section 7); by
  search the same family gives non-anchors of every degree from 2 to 9.
* *Proved: non-anchors are arithmetic.* For the tree "path `c₁ – v – c₂` with
  `p` leaves on `c₁` and `q` on `c₂`", `v` is an anchor exactly when a stated
  divisibility condition on `m = p + q + 2` holds; in particular, if `m` is
  prime and `p, q ≥ 1`, `v` is never an anchor. A similar exact rule holds for
  a second family. This explains why no structural pattern was found in
  section 7 (`src/attack/anchors/PROOFS.txt`).
* *Proved:* any vertex becomes an anchor once enough leaves are attached to
  it, with an explicit (large) bound.
* *Proved (path anchors):* the vertex at distance 2 from the end of a path
  with `m` edges is an anchor when `m = 3s+2`, `5s+4` or `7s+3`; with the
  pendant-path step of section 13 this gives growth placements for the
  three-legged spiders `S(a, 2, c)` for those `a` and every `c`
  (`src/attack/polynomial`). *Conjecture (checked `15 ≤ m ≤ 2500`):* these
  congruences are exactly the cases.

**Composition** (extending Theorem 13; `src/attack/composition`).

* *Proved (core fattening):* the copies in Theorem 13 need not be glued at
  the root: the branches hanging off any subtree containing the root may be
  multiplied `2m + 1` times, including gluing `2m + 1` copies of a
  growth-placed tree along its top bracket.
* *Proved (mixed bunch):* the `2m + 1` copies may be different trees, equal
  in pairs, under stated conditions.
* *Observation (all trees `S` with at most 14 vertices):* in the corona of
  `S` (one new leaf on every vertex) every vertex of `S` is an anchor.

**Where a counterexample to Conjecture B cannot be.**

* *Proved (with a finite computer check):* if a tree has a vertex `v` such
  that removing the leaves at `v` leaves at most 20 vertices, it has a growth
  placement (every rooted tree on at most 20 vertices was checked, then
  Lemma 6).
* *Observation:* about 1.15 million structured trees with `26 ≤ n ≤ 70`
  (all diameter-4 trees to `n = 42`, all diameter-5 trees to `n = 32`,
  symmetric and spider families to `n = 70`) all have growth placements. No
  counterexample was found (`src/attack/counterexample`).

**One spare label.**

* *Proved:* for every tree and every root there is a labeling with distinct
  edge lengths decreasing away from the root that uses labels up to `2n − 2`.
* *Observation (every tree with `n ≤ 18`, every vertex):* with just one spare
  label (`n + 1` labels for `n` vertices) **every** vertex can be the root.
  The anchor obstructions of section 7 disappear completely with one extra
  label (`src/attack/asymptotic`).
* The published probabilistic methods do not adapt directly: fixing the order
  in which edge lengths are used removes the randomness they rely on. A
  one-pass random longest-first process needs about 6–10% spare labels.

**Signs.** *Proved:* for a fixed rooted tree and a fixed order of lengths, two
different valid sign choices must differ in at least two places; for `n ≤ 9`
the valid sign choice is unique (`src/attack/polynomial`).

**Independent re-verification** (`src/attack/reverify`): new programs written
without reading this repository's solvers, including a SAT formulation,
reproduce every number checked in sections 4, 7, 11, 12 and 13 (growth
placements for all trees with `n ≤ 22` under the three-run rule; the skip
tables; the failing trees at 9, 10, 16 and 22 vertices; anchors; Conjecture S
to `n = 31`), with one exception, corrected above: the "one skipped cell on
each side" row.

**What changes.** Three things recorded earlier in this file were wrong or
too optimistic and are now corrected: the degree-4 anchor observation, the
"one on each side" row, and the hope that the clean-cut induction might work
with bounded steps. On the positive side there are now explicit, search-free
growth placements for several infinite families that are not caterpillars,
and the first proved slide routes beyond caterpillars. The conjecture itself
is no closer to proved; what has improved is the map of which approaches are
dead and which statements are sharp.

## 17. Checking

The statements marked proved in sections 2 and 7–9 were re-checked by an
independent pass that tested each one by brute force from the definitions in
section 1 (all placements up to `n = 8..10`, every tree and leaf up to
`n = 12` for the leaf rule). It found no false theorem; it found a wrong
exponent, an under-specified condition in Lemma 8, a false summary sentence
and several unbounded claims, all corrected in this version. The exhaustive
runs for `n ≥ 14` rest on the programs in `src/` alone and have not been
independently re-implemented.
