# graceful — a bracket model for the Graceful Tree Conjecture

**Status: the Graceful Tree Conjecture is open, and nothing here proves it.**
This repository makes one picture of the problem exact, proves a few small
things about it, and records two conjectures that are *stronger* than the
Graceful Tree Conjecture and survive an exhaustive computer search.

Interactive version (drag the brackets, watch the proofs): `web/index.html`.

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
(checked `n ≤ 13`).

**Observation D.** If a bracket may jump to any position on its rail in one
move, all tree placements form one connected component (checked `n ≤ 13`).

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

For `n ≤ 6` the slide graph is connected. From `n = 7` small components split
off, but the star's component always contains every shape.

Growth placements, exhaustive over all trees (`src/growsolve.cpp`, trees from
`networkx.nonisomorphic_trees`): **every tree on `n ≤ 20` vertices has
one.** Spot checks: 200 uniformly random trees at each of `n = 30, 40, 50`,
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
