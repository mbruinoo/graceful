#!/bin/sh
# all rooted trees (= all (tree,vertex) pairs up to automorphism), slack 1, fast first pass (rs2 allf)
for n in 21 22 23; do
  for p in 0 1 2 3; do ./rs2 allf $n 1 $p 4 100000 1000000000 > allf1_${n}_$p.log 2>&1 & done
  wait
done
