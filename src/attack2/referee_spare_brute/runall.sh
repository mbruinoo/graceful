#!/bin/sh
# all rooted trees (= all (tree,vertex) pairs up to automorphism), slack 1
for n in 18 19 20 21 22 23; do
  for p in 0 1 2; do ./rs all $n 1 $p 3 100000 1000000000 > all1_${n}_$p.log 2>&1 & done
  wait
done
