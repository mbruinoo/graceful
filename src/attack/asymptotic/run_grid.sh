#!/bin/sh
# Success rate of the one-pass longest-first process as a function of eps and tree type.
# usage: sh run_grid.sh > run_grid.log     (about 2-3 minutes, one core)
g++ -O2 -o greedy greedy.cpp || exit 1
for pol in 0 1 6; do
for type in prufer recursive pa binary lobster cater cbin comb3 comb10 spider3 spider10 spider50 path; do
for n in 200 500 1000 2000; do
  sl=""; for e in 0 1 2 5 10 15 20 30 50 100; do sl="$sl $((n*e/100))"; done
  THETA=5 ./greedy $type $n 100 $pol c 2026 $sl
done; done; done
