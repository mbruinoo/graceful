#!/bin/sh
# portfolio.sh treefile slack cap out.log -- run spare with branching order 0; rerun every CAP line with order 1
# (skip-first), then with randomised parent order, seeds 2..9.  NONE is exact (that search was exhausted);
# CAP means undecided.  The final log has one line per tree.  SPARE=binary (default ./spare).
f=$1; s=$2; cap=$3; out=$4; tmp=${out}.tmp; SPARE=${SPARE:-./spare}
$SPARE $s $cap 0 < $f > $tmp.cur
: > $out
for o in 1 2 3 4 5 6 7 8 9; do
  grep -v " CAP " $tmp.cur >> $out
  grep " CAP " $tmp.cur | awk '{print $1}' > $tmp.names
  if [ ! -s $tmp.names ]; then : > $tmp.cur; break; fi
  awk 'NR==FNR{want[$1]=1; next} ($1 in want)' $tmp.names $f > $tmp.hard
  $SPARE $s $cap $o < $tmp.hard > $tmp.cur
done
cat $tmp.cur >> $out
rm -f $tmp.cur $tmp.names $tmp.hard
awk '{c[$5]++} END{for(k in c) printf "%s=%d ", k, c[k]; print ""}' $out
