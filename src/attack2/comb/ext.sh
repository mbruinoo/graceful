#!/bin/sh
# ext.sh LO HI : all-up comb check for every multiset S with |S|+sum(S)+max(S)+2 = n, LO <= n <= HI.
# Pass 1: exact-cover search capped at MAXLIM nodes per attempt (4 parts in parallel).
# Pass 2: every S that pass 1 gave up on ("HARD") is given to CP-SAT (cpsat.py), w = 0,1,..,max(S).  Certificates go to certs/n<N>.gz; check with verify.py.
LO=$1; HI=$2
for n in $(seq $LO $HI); do
  for p in 0 1 2 3; do MAXLIM=${MAXLIM:-3000000} ./combx $n $n 0 $p 4 > certs/tmp_${n}_$p.txt & done
  wait
  cat certs/tmp_${n}_?.txt | grep '^S' > certs/n$n.txt
  cat certs/tmp_${n}_?.txt | grep '^HARD' | sed 's/^HARD n=[0-9]* //' > certs/hard_$n.txt
  nh=$(wc -l < certs/hard_$n.txt)
  if [ "$nh" -gt 0 ]; then
    sed 's/^S //' certs/hard_$n.txt | while read line; do python3 cpsat.py -t ${HARDTIME:-900} -j 4 $line; done > certs/hardsol_$n.txt
    grep '^S' certs/hardsol_$n.txt >> certs/n$n.txt
    grep '^#' certs/hardsol_$n.txt > certs/hardnotes_$n.txt
  fi
  echo "n=$n pass1 certificates $(grep -c '^S' certs/tmp_${n}_0.txt certs/tmp_${n}_1.txt certs/tmp_${n}_2.txt certs/tmp_${n}_3.txt | awk -F: '{s+=$2} END{print s}')  given up in pass 1: $nh  settled by CP-SAT: $( [ -f certs/hardsol_$n.txt ] && grep -c '^S' certs/hardsol_$n.txt || echo 0)  total $(wc -l < certs/n$n.txt)  $(date +%T)"
  rm -f certs/tmp_${n}_?.txt certs/hardsol_$n.txt
  gzip -f certs/n$n.txt
done
