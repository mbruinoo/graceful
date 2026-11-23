#!/bin/sh
# Family survey for results/counterexample-hunt: exact numbers of growth placements, family by family.
# Usage: ./hunt_survey.sh STREAM   (STREAM = 1, 2 or 3; run the three in parallel)   needs ./growfam
O=../results/counterexample-hunt/counts; mkdir -p $O
B=${COUNTBUDGET:-200000000}; export COUNTBUDGET=$B; export TABLE=${TABLE:-23}; export ANCHORS=1 STOPABORT=2
run(){ out=$1; shift; python3 huntfam.py "$@" | ./growfam count > $O/$out.txt; }
case $1 in
1) for k in 3 4 5 6 8; do run spider_${k}_L spider $k 1..40 maxn=49; done; run spider_k_2 spider 3..40 2; run spider_k_3 spider 3..40 3
   run comb_p_2 comb 3..20 2; run comb_p_3 comb 3..14 3
   for k in 2 3 4; do run bin_${k}_d bin $k 1..4 maxn=64; done ;;
2) for k in 3 4 5 6; do for a in 1 2 3; do run hubspider_${k}_${a}_m hubspider $k $a 1..30 maxn=70; done; done
   for k in 2 3 4; do for j in 2 3; do run twolevel_${k}_${j}_m twolevel $k $j 1..12 maxn=64; done; done ;;
3) for k in 2 3 4 5; do for L in 2 3 4; do run hublegs_m_${k}_${L} hublegs 1..64 $k $L maxn=70; run hubleaflegs_m_${k}_${L} hubleaflegs 1..64 $k $L maxn=70; done; done
   run dbl_m_7_1_2 dbl 1..31 7 1 2 maxn=70
   for P in 3 5 7 9; do for t in 1 2 3; do run dbl_m_${P}_${t}_2 dbl 1..12 $P $t 2; done; done
   for a in 1 2 3; do for b in 2 3; do run forkhub_${a}_m_${b} forkhub $a 1..50 $b maxn=60; done; done
   for d in "2 2" "3 3" "4 4" "5 5" "6 6" "7 7" "2 2 2" "3 3 3" "2 2 2 2" "2 2 2 2 2" "3 2 2" "2 3 3" "3 3 2" "2 2 3" "4 4 2" "3 3 3 2" "4 3" "3 4" "5 2" "2 5" "4 2 2" "2 4 2" "2 2 4"; do python3 huntfam.py sph $d; done | STOPABORT=99 ./growfam count > $O/sph.txt ;;
esac
