# The original intuition

This file records the idea this repository started from, in the author's own
words, so that it stays distinguishable from everything built on top of it.
**Nothing below the quotations was part of the original idea.**

## In the author's words

From the message that opened the project (22 November 2026), unedited:

> I have toyed with the Graceful Tree Conjecture in undergrad, and came to the
> insight that the problem can be represented as a horizontal line of nodes
> listed 1 through n, with "brackets" of each edge length 1 through (n-1) that
> can be slid between each. "Starfish" graphs and other trivial configurations
> are the starting point while establishing basic sliding rules seem like the
> key to unlock this. Yet I am not able to fit the full context of the problem
> in my mind to finish see the proof through.

And on how the reasoning should be done:

> The best solutions are ones that can be shown logically to humans; thinking
> of your reasoning as a many-dimensional graph, the parts that flow through
> human cognition and intuition tend to produce the best results. Working
> through this visually has helped enormously.

Later, on the growth conjecture's leaf-by-leaf form: *"Worth trying?"* — the
question that led to section 7 of the README.

## The four pieces of the intuition

1. **The line.** Vertices are the numbers `1..n` laid out left to right.
2. **The brackets.** One bracket for each length `1..n−1`; an edge *is* a
   bracket.
3. **Sliding.** Brackets move; the right "basic sliding rules" are the key.
4. **Start from the trivial shapes.** Stars / starfish first, then slide away
   from them.

Plus a method: keep it visual, and keep to arguments a person can follow.

## What each piece became

| Original piece | What was built on it | Who |
|---|---|---|
| The line and the brackets | The exact model: placement `(p_1..p_{n−1})`, one rail per length, `(n−1)!` placements, each one a graceful labeling (README §1) | formalised by Claude; known in print as Sheppard's sequences / graceful chessboards |
| "Basic sliding rules" | The slide rule (Lemma 1); the slide graph; its islands; right slides (README §2, §4) | Claude |
| "Starfish and other trivial configurations are the starting point" | The star as the origin of every route; the right-slide conjecture (Conjecture A) | idea: author; statement and evidence: Claude |
| Sliding from trivial shapes | Staircases = caterpillars, and right slides reach all of them (Theorems 2–3). The labeling itself is Rosa's, 1967 | Claude, restating a classical result |
| "Shown logically to humans… visually" | The interactive bench in `web/`; proofs written to be watched | Claude, to the author's brief |
| Sliding from trivial shapes | Theorem 9: growth plus "all brackets jump one point" forces a staircase (grid proof) | Claude |
| — (not in the original idea) | Growth placements and the growth conjecture (Conjecture B); anchors; the gluing lemma; the interval variant; the root form (Theorem 7); clean cuts and gap splits (Lemma 8, §10); the three-run conjecture B3 (§11); the offset rule for skips (§14); fattening and the spider rules (§15, found by a multi-agent run and refereed) | Claude |

## A note on the name "starfish"

In the literature a star with its arms lengthened is a **spider**. Spiders are
not known to be graceful in general, so the author's starting shapes are an
open problem in their own right, not a trivial case.

## What turned out to be known already

A literature pass after the first rounds (README §5) found that two pieces
exist in print under other names. The author arrived at the first
independently; Claude re-derived the second without knowing of it.

* The line-and-brackets picture is the "labelling sequence" of Sheppard
  (1976) and the "graceful chessboard" of Haviar and Ivaška (2015).
* Placing edge labels longest first, each on a vertex whose parent is already
  labelled, is the backtracking order of Horton (2003) and Fang (2010).
* A later literature pass (README §19) found more: the conjecture that every
  tree can be built this way (README Conjecture B) is Horton's "edge search
  conjecture" (2003), which Horton checked for all trees on up to 29
  vertices. An earlier version of this file and of the README said it had
  not been found in print; that was wrong.

Sliding as a move between placements was not found. Of README §7–11, the
growth conjecture itself is Horton's; the other items marked proved or
conjectured there were not found (by a web search only).

## Attribution in short

* The representation (line, brackets, sliding, start at the star) and the
  insistence on visual, human-followable reasoning are the author's.
* The formalisation, the proofs, the searches, the two conjectures and the
  write-up were produced by Claude (Anthropic's AI model) in one
  extended session directed by the author.
* The classical results used belong to their authors (Rosa; Hrnčiar and
  Haviar; the α-labeling composition), as cited in the README.
