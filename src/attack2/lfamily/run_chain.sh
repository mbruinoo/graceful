#!/bin/bash
# run_chain.sh -- the three "no leaf neighbour" scans behind the complete n = 24 list (REPORT.txt section B5),
# DFS node cap 2,000,000 (vertices not decided within the cap are printed as CAP and settled by satanchor.py);
# four processes at a time; each process is one part (well under 40 minutes).  Outputs s<n>_<part>of<parts>.txt.
{
for p in $(seq 0 15); do echo "./ascan2 24 $p 16 4 99 1 2000000 > s24_${p}of16.txt"; done
for p in $(seq 0 7);  do echo "./ascan2 23 $p 8 3 3 1 2000000 > s23_${p}of8.txt"; done
for n in 15 16 17 18 19; do echo "./ascan_v $n 0 1 4 2000000000 > out_${n}_0of1.txt"; done
for p in $(seq 0 31); do echo "./ascan2 22 $p 32 2 2 1 2000000 > s22_${p}of32.txt"; done
} | xargs -P 4 -I{} bash -c "{}"
