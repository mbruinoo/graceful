#!/bin/sh
# core B: named trees, spiders, R=2 for n=19..21
T=../reverify
for f in $T/trees16_no2run.txt $T/tree18_no2run.txt; do ./solve file $f 2 -1 0; ./solve file $f 3 -1 0; done
./solve file $T/tree22.txt 0 2 0; ./solve file $T/tree22.txt 0 3 0; ./solve file $T/tree22.txt 2 -1 0; ./solve file $T/tree22.txt 3 -1 0
for n in 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21; do ./spider $n zigzag; done
./spider 8 level; ./spider 18 level; ./spider 8 first; ./spider 20 first
for n in 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31; do ./spider $n free; done
for n in 19 20 21; do ./solve $n 2 -1 0; done
