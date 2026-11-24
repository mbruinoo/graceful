#!/bin/sh
# rules_pipe.sh RULE n -- as rules_run.sh but trees are piped straight from ../../gentrees.py (no tree file)
R=$1; n=$2
python3 ../../gentrees.py $n | FREE=1 QUIET=1 RULE=$R ./tidy 20000000 900 | awk -v R=$R -v n=$n '{c[$5" "$6]++; if($5=="ub=NONE") f=f" "$2} END{printf "RULE=%d n=%d:",R,n; for(k in c) printf "  [%s] %d",k,c[k]; if(f!="") printf "   failing trees:%s",f; printf "\n"}'
