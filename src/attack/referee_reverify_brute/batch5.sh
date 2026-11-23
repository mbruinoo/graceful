#!/bin/sh
# core A: anchors / counts / small-n rule rows / n=18 skip table
for n in 4 5 6 7 8 9 10 11 12 13 14; do ./enum $n 0 -1 0 - 1; done
for n in 8 9 10 11 12 13 14 15 18; do ./enum $n 1 -1 0 d_R1_$n.txt; done
for n in 9 10 11 12 13 14 18; do ./enum $n 0 1 0 d_H1_$n.txt; done
for n in 9 10 11 12 13 14 15; do ./enum $n 0 2 1 d_H2S1_$n.txt; done
for n in 9 10 11; do ./enum $n 0 2 0; ./enum $n 0 2 2 d_H2S2_$n.txt; ./enum $n 0 2 3 d_H2S3_$n.txt; done
