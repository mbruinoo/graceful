#!/bin/sh
# usage: ./run_trees.sh N MODE [R B]     MODE = solve | minskip | minruns
# networkx trees -> Rust search -> Python certificate check.  Prints one JSON line.
set -e
N=$1; MODE=$2; R=${3:-inf}; B=${4:-inf}
mkdir -p out
[ -s out/trees_$N.txt ] || python3 gen.py $N ${CHECK:+check} > out/trees_$N.txt
if [ "$MODE" = solve ]; then
  ./rs/gsearch solve $R $B < out/trees_$N.txt > out/solve_${N}_${R}_${B}.txt
  python3 check_cert.py $N out/trees_$N.txt out/solve_${N}_${R}_${B}.txt $R $B
else
  ./rs/gsearch $MODE < out/trees_$N.txt > out/${MODE}_$N.txt
  python3 check_cert.py $N out/trees_$N.txt out/${MODE}_$N.txt
fi
