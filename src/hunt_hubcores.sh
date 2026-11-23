#!/bin/sh
# One giant hub plus every small core: how does the number of growth placements change when the hub grows?
# For every rooted tree A on a vertices (root without leaf children) hang m leaves on the root, m = M1 and M2.
# Usage: ./hunt_hubcores.sh a M1 M2      prints: count(M1) count(M2) name edges-of-the-core
a=$1; M1=$2; M2=$3; export COUNTBUDGET=${COUNTBUDGET:-200000000}
python3 hubscan.py one $a $M1 | ./growfam count | awk '{print $1, $3}' | sed 's/count=//; s/one([0-9]*,[0-9]*,//; s/)//' | sort > ${TMPDIR:-/tmp}/hc_$a.$M1
python3 hubscan.py one $a $M2 | ./growfam count | awk '{print $1, $3}' | sed 's/count=//; s/one([0-9]*,[0-9]*,//; s/)//' | sort > ${TMPDIR:-/tmp}/hc_$a.$M2
join ${TMPDIR:-/tmp}/hc_$a.$M1 ${TMPDIR:-/tmp}/hc_$a.$M2 | sort -k3 -n
