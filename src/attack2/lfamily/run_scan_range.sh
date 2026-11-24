#!/bin/sh
# usage: run_scan_range.sh n parts first last  -- parts first..last of ascan n . parts 4 2e9, four at a time
n=$1; parts=$2
seq $3 $4 | xargs -P 4 -I{} sh -c "./ascan $n {} $parts 4 2000000000 > out_${n}_{}of${parts}.txt"
