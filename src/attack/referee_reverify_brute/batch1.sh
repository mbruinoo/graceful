#!/bin/sh
# core 1: run rules
for n in 4 5 6 7; do ./enum $n 1 -1 0; done
for n in 4 5 6 7 8 9 10 11 12 13 14 15 16; do ./enum $n 2 -1 0 d_R2_$n.txt; ./enum $n 3 -1 0 d_R3_$n.txt; done
./enum 16 1 -1 0
./enum 17 2 -1 0 d_R2_17.txt
./enum 18 2 -1 0 d_R2_18.txt
