#!/bin/sh
# scanbig.sh "small sizes" kmin kmax step : report hub trees (small..., k) whose root is NOT an anchor (uses ./d2)
for k in $(seq $2 $4 $3); do r=$(./d2 $1 $k | cut -d' ' -f1-2); case "$r" in NOT*) echo "NOT: $1 $k $r";; esac; done; echo "scanned $1 k=$2..$3 step $4"
