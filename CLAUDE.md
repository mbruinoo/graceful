# Working in this repository

A research notebook on the Graceful Tree Conjecture built around one picture:
vertices `1..n` on a line, one sliding bracket per edge length. Read
`README.md` for the mathematics and `INTUITION.md` for where it came from.

## How the author wants the work done

These come from the author's opening brief; treat them as standing.

* **Reason where a person can follow.** Prefer arguments that can be shown
  step by step and drawn. If a result can only be stated as "the computer
  checked it", say so and keep looking for the picture.
* **Work visually.** The bracket-and-rail picture is the home notation. New
  ideas should be expressible on the bench in `web/` before they get symbols.
* **Take the wheel.** Explore without asking permission for each step.
  Compute is not the constraint; clarity is. Report what was found, including
  dead ends.
* **Never overclaim.** The conjecture is open. Do not write "proof" for
  anything unproved, do not round "checked to n" up to "true", and do not
  claim novelty that has not been checked against the literature.

## Status words (use exactly these)

| Word | Meaning |
|---|---|
| **Proved** | A complete argument is written in the README. |
| **Classical** | Proved by someone else; cite them. |
| **Conjecture** | Believed, unproved, with stated evidence. |
| **Observation** | True in every case checked; give the bound (`n ≤ …`). |
| **Fails** | A counterexample is recorded; give the smallest one. |

Negative results are kept, not deleted (README §7).

## Keeping provenance straight

* `INTUITION.md` is the author's. Quote it, never paraphrase it into
  something stronger, and do not edit the quotations.
* When adding a result, add a row to the table in `INTUITION.md` if it grows
  out of one of the four original pieces, and say who contributed what.
* Credit classical results to their authors in the README.

## Vocabulary

*placement* (positions of all brackets) · *tree placement* · *slide* /
*right slide* (one step along a rail, tree before and after) · *star* (all
brackets at position 1) · *staircase* · *growth placement* (longest-first,
one fresh vertex per bracket) · *anchor* (a vertex that can carry label 1 in
a growth placement) · *island* (connected component of the slide graph; in §11 also a block of used labels between the two end blocks) · *run* (maximal interval of unused labels) · *clean cut*, *gap split* (§9–10).
Use "spider" in mathematical text; "starfish" is the author's name for it.

## Layout

```
README.md       definitions, proofs, conjectures, evidence, failed attempts
INTUITION.md    the author's original idea and the attribution table
src/            searches (C++ for enumeration, Python for glue)
web/            interactive page: page.template.html + atlas.json + evidence.json -> index.html
```

## Commands

```sh
cd src
g++ -O2 -o slide slide.cpp       && ./slide 11 iso            # slide graph, islands, right-slide reach
g++ -O2 -o growsolve growsolve.cpp
python3 gentrees.py 16 | ./growsolve 16                       # growth placement for every tree (needs networkx)
g++ -O2 -o anchors anchors.cpp   && python3 gentrees.py 12 | ./anchors 12
g++ -O2 -o interval interval.cpp && ./interval 12
g++ -O2 -o runsolve_gen runsolve_gen.cpp && ./runsolve_gen 18 3   # three-run growth placement for every tree (built-in generator)
python3 export_atlas.py && python3 ../web/build.py            # rebuild web/index.html
```

Rough costs: `slide 13` ≈ 90 s, `slide 14` ≈ 13 min and ~2 GB; `growsolve`
≈ 2 min at n=20, ≈ 50 min at n=23.

## Conventions

* Every number in the README or on the page must come from a command in
  this repo. When a bound is extended, update `README.md`,
  `web/evidence.json` and rebuild the page in the same commit.
* Exhaustive checks say "all trees on n ≤ N"; sampled checks say how many
  trees and which families.
* Compiled binaries and raw run logs are not committed (`.gitignore`).
* Edit `web/page.template.html`, never `web/index.html` directly.
