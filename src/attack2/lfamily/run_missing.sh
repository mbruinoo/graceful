#!/bin/sh
# usage: run_missing.sh n parts maxjobs  -- (re)runs up to maxjobs parts of "ascan n p parts 4 2e9" whose output
# file has no SUMMARY line yet (not started, or killed), four at a time.
n=$1; parts=$2; max=$3
for p in $(seq 0 $((parts-1))); do grep -q SUMMARY out_${n}_${p}of${parts}.txt 2>/dev/null || echo $p; done | head -n $max |
  xargs -P 4 -I{} sh -c "./ascan_v $n {} $parts 4 2000000000 > out_${n}_{}of${parts}.txt"
