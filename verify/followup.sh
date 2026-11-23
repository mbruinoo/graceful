#!/bin/sh
# usage: ./followup.sh N   trees that came back NONE under the two-skip rule (solve 3 1) are re-run with
# three runs of any size (solve 3 inf) and the certificates are checked.
N=$1
grep -n NONE out/solve_${N}_3_1.txt | cut -d: -f1 > out/none_$N.idx
awk 'NR==FNR{want[$1]=1; next} (FNR in want)' out/none_$N.idx out/trees_$N.txt > out/none_trees_$N.txt
./rs/gsearch solve 3 inf < out/none_trees_$N.txt > out/none_solve_$N.txt
python3 check_cert.py $N out/none_trees_$N.txt out/none_solve_$N.txt 3 inf
