#!/bin/sh
# rules_run.sh treedir "rules" "sizes" -- existence of a growth placement obeying each RULE bitmask (tidy.cpp, FREE=1),
# every tree on n vertices; prints the counts and the indices (line numbers, 0-based, in gentrees.py order) of failures
S=$1
for R in $2; do for n in $3; do FREE=1 QUIET=1 RULE=$R ./tidy 20000000 900 < $S/t$n.txt | awk -v R=$R -v n=$n '{c[$5" "$6]++; if($5=="ub=NONE") f=f" "$2} END{printf "RULE=%d n=%d:",R,n; for(k in c) printf "  [%s] %d",k,c[k]; if(f!="") printf "   failing trees:%s",f; printf "\n"}'; done; done
