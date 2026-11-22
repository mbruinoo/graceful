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
growth placement. The same holds for "reachable from the star by right slides".

*Proof.* For the vertex labelled `n`: shift all labels up by one and add the
new longest bracket `{1, n+1}`. For the vertex labelled 1: keep all labels and
add `{1, n+1}`. In both cases the old brackets never touch the new vertex, so
the growth order, and any sequence of legal slides, carries over. ∎

## 3. Conjectures

Each of A and B implies GTC.

**Conjecture A (right-slide conjecture).** For every `n`, every tree shape on
`n` vertices is drawn by a placement reachable from the star by legal right
slides.

**Conjecture B (growth conjecture).** Every tree has a growth placement.

**Observation C.** Every tree placement admits at least one legal slide
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
one.** Every spider on `n ≤ 48` vertices has one too (section 8). Spot checks: 200 uniformly random trees at each of `n = 30, 40, 50`,
the path on 40, complete binary tree on 31, complete ternary on 40, spiders
with 10 legs of length 3 and 7 legs of length 5 — all have one.

Number of growth placements for `n = 4..13`:
4, 12, 32, 116, 412, 1764, 7888, 40220, 214600, 1275368.

Negative result: slides that also preserve the growth property are too rigid.
From the star they reach exactly `5·2^(n−5) − 1` placements (`5 ≤ n ≤ 11`) and
miss some shapes from `n = 9` on (`src/growslide.py`).

## 5. Relation to known work, and caveats

* Caterpillars being graceful is Rosa's original result; Theorem 2 is that
  result in bracket language.
* The *transfer* technique of Hrnčiar and Haviar (all trees of diameter ≤ 5
  are graceful) moves leaves between vertices of a labelled star. In this
  model a transfer is a pair of brackets reflected together, i.e. a compound
  slide.
* A brief literature search did not find the slide graph of graceful
  labelings, Conjecture A, or the growth property / Conjecture B. That search
  was not exhaustive. Treat novelty as unverified until checked against
  Gallian's *Dynamic Survey of Graph Labeling* by someone who knows the area.
* Graceful labelings are abundant for small trees, so strong statements can
  hold for all small cases and still be false. GTC itself is verified to 35
  vertices (Fang, 2010) and remains open.

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
```

## 7. Trying to prove Conjecture B by induction (what was tried, where it breaks)

**The naive step fails.** Deleting the last-placed leaf of a growth placement
leaves `n−1` vertices on `n−1` of the `n` labels with lengths `2..n−1`. That is
not a growth placement of a smaller tree, so "remove a leaf, recurse" does not
close.

**What does go through: gluing at the top (proved).** Let `O` be a tree with a
growth placement on labels `1..r+1` in which every bracket joins a label
`≤ a+1` to a label `> a+1`, and let `x` be the vertex labelled `a+1`. Let `T'`
have a growth placement on `m` vertices with `y` labelled 1 (or `m`). Then the
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

Almost every vertex is an anchor (99.8% at `n = 14`), every tree has one, and
non-anchors have degree ≤ 3. But they exist (the three middle vertices of the
path on 7 vertices are the smallest clean example), and they follow no pattern
found so far, so "every vertex is an anchor" cannot be the induction
hypothesis. Lemma 6 alone only ever produces anchors at the two ends of the
top bracket, which regenerates exactly the caterpillars.

**A small-state variant fails.** Require the unused labels to form a single
interval `(a, b)` throughout. Then the state is just `(a, b)` and each new leaf
has four options: label `a+1` hung on `b` or on its mirror `2a+2−b`; label
`b−1` hung on `a` or on its mirror `2b−2−a`. This covers every tree on ≤ 8
vertices and 91% at 15, but misses the spider with four legs of length 2 at
`n = 9`, and must fail for most large trees by counting: such placements grow
by a factor ≈ 2.5 per vertex, trees by ≈ 2.96 (`src/interval.cpp`,
`src/classify.py`).

**Where that leaves the induction.** The missing ingredient is a lemma that
produces anchors at *internal* vertices of a tree from growth placements of
smaller trees. The data says such anchors nearly always exist; nothing proved
here creates them.

**Leaf rule (proved).** Let `ℓ` be a leaf of `T` with neighbour `v`. Then `ℓ`
is an anchor of `T` if and only if `v` is an anchor of `T − ℓ`. (If `ℓ` has
label 1 its only bracket is the top one, `{1, n}`, and everything else is a
growth placement of `T − ℓ` on `2..n` with `v` at the top label; conversely
Lemma 6.) The counts confirm it: non-anchor leaves at `n` equal all
non-anchors at `n−1` for every `n ≤ 14`. So every exception traces back to a
*primitive* internal non-anchor; there are 1, 2, 2, 4, 4, 5, 14, 18, 24 kinds
of those for `n = 6..14`, almost all of degree 2, with no rule found.

**"Label 1 on a leaf" fails.** One might hope every tree has a growth
placement with label 1 on a leaf, which would make the leaf rule a complete
induction. It does not: one tree on 10 vertices and one on 12 have no anchor
leaf.

**Observation.** Every vertex of degree ≥ 4 is an anchor (`n ≤ 14`).

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
order of length. Gnang and Wass, *Growing Graceful and Harmonious Trees*
(arXiv:1808.05551), despite the title, concerns determinantal enumeration of
gracefully labelled functional digraphs. Neither source states the growth
property or Theorem 7. A targeted search for "edge labels decreasing away
from a root" found nothing, which is still not proof of novelty.

## 9. Clean cuts: an induction step that works almost always

Fix a growth labeling with labels `1..n`. A leaf `ℓ` with label `L`, hung by an
edge of length `j`, is **clean** if the other edges that jump over `L` (one
end below `L`, one above) are exactly the edges longer than `j`.

**Lemma 8 (clean-cut removal and insertion; proved).** If `ℓ` is clean, delete
it and close the gap (labels above `L` drop by one). The result is a growth
labeling of `T − ℓ`. Conversely, in a growth labeling on `n` vertices, if the
edges jumping over a cut position are exactly the `c` longest, open a gap
there: those edges lengthen by one, length `j = n − c` becomes free, and a new
leaf with the gap's label may be hung by a bracket of length `j` on any vertex
at distance `j` whose own edge towards the root is longer than `j` (or which
is the root).

*Proof.* Closing the gap shortens exactly the edges that jumped over `L`, i.e.
those longer than `j`, by one, and leaves shorter edges alone; so lengths
`1..j−1, j+1..n−1` become `1..n−2`, order of lengths is preserved, and hence
so is "lengths decrease away from the root" (Theorem 7). Insertion is the
inverse. ∎

Lemma 6 is the special case where the cut is at the far left or far right
(`c = 0`). The gap move is the one described on MathWorld (Pegg, Weisstein,
2026) for graceful labelings in general; the content here is that it preserves
the growth property exactly when the cut is clean.

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
