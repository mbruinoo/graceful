#!/bin/sh
# core 2: skip rules
for n in 4 5 6 7 8 9 12; do ./enum $n 0 2 1; done
for n in 4 5 6 7 8 15 16; do ./enum $n 0 1 0; done
for n in 4 5 6 7 8 9 12 13 14 15 16; do ./enum $n 0 2 2 d_H2S2_$n.txt; ./enum $n 0 2 3; done
for n in 12 14 16; do ./enum $n 0 2 0; done
./enum 17 0 2 2 d_H2S2_17.txt
./enum 18 0 2 2 d_H2S2_18.txt
