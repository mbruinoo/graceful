#!/bin/sh
# For every spider on n vertices: least number of skips (0..3) admitting a build.  Usage: spiderskips.sh n
n=$1; T=${TMPDIR:-/tmp}/spiderskips; mkdir -p $T; python3 spiders.py $n > $T/sp$n.txt
total=$(wc -l < $T/sp$n.txt); in=$T/sp$n.txt; line="n=$n spiders=$total"
for sk in 0 1 2 3; do
  ./runsolve128 $n $((sk+1)) 5000 1 < $in > $T/spout$n.txt
  grep "^NONE: " $T/spout$n.txt | sed 's/^NONE: //' > $T/spnext$n.txt
  unres=$(grep -c "^UNRESOLVED" $T/spout$n.txt)
  left=$(wc -l < $T/spnext$n.txt)
  line="$line | need>$sk: $left (unresolved $unres)"
  [ "$left" = "0" ] && break
  cp $T/spnext$n.txt $T/spcur$n.txt; in=$T/spcur$n.txt
done
echo "$line"
