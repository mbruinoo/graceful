#!/bin/sh
# usage: ./run_big.sh N R B     like run_trees.sh solve, but the certificate check runs as 4 parallel parts
set -e
N=$1; R=$2; B=$3
[ -s out/trees_$N.txt ] || python3 gen.py $N > out/trees_$N.txt
./rs/gsearch solve $R $B < out/trees_$N.txt > out/solve_${N}_${R}_${B}.txt
for i in 0 1 2 3; do PART=$i/4 python3 check_cert.py $N out/trees_$N.txt out/solve_${N}_${R}_${B}.txt $R $B & done; wait
