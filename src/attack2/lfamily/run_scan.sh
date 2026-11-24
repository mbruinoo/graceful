#!/bin/sh
# usage: run_scan.sh n parts   -- runs ascan n p parts 4 2e9 for p=0..parts-1, four at a time
n=$1; parts=$2
seq 0 $((parts-1)) | xargs -P 4 -I{} sh -c "./ascan $n {} $parts 4 2000000000 > out_${n}_{}of${parts}.txt"
