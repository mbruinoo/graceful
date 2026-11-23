#!/bin/bash
# Independent re-verification of README numbers (sections 4, 7, 11, 12, 13).
# Usage: ./run_all.sh [workdir] [NBIG]      (default workdir /tmp/reverify, NBIG=18)
#   NBIG up to 22 extends the R=3 / H=2 / R=2 runs (n=22: ~5.6M trees, about 30 min).
# Nothing here uses or reads src/growsolve.cpp, src/runsolve_gen.cpp, src/holes.cpp.
# Needs: g++, python3 with networkx; python-sat for the SAT part.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
W=${1:-/tmp/reverify}; NBIG=${2:-18}
mkdir -p $W/t $W/o $W/e
cd $HERE
g++ -O2 -o $W/gp gp.cpp
g++ -O2 -o $W/enumgp enumgp.cpp
g++ -O2 -DSLOWCHECK -o $W/enumgp_slow enumgp.cpp
g++ -O2 -o $W/spiderdeal spiderdeal.cpp
short() { sed 's#.*: ##'; }
tag() { echo "$1" | tr -d ' ='; }

echo "== trees (networkx, counts asserted against A000055)"
for n in $(seq 4 $NBIG); do [ -s $W/t/t$n.txt ] || python3 gentrees_nx.py $n > $W/t/t$n.txt; done

echo "== (a)+(b) three-run growth placement for every tree, certificates checked from definitions"
for n in $(seq 4 $NBIG); do
  $W/gp R=3 < $W/t/t$n.txt > $W/o/R3_$n.txt 2>/dev/null
  echo "n=$n R=3: $(python3 check_cert.py $W/t/t$n.txt $W/o/R3_$n.txt R=3 | short)"
done

echo "== number of growth placements, shapes drawn (pure enumeration); README sec 4: 4,12,32,116,412,1764,7888,40220,214600,1275368"
$W/enumgp_slow 10 R=2; $W/enumgp_slow 11 H=2 SIDE=1; $W/enumgp_slow 11 H=2 SIDE=2
for n in $(seq 4 14); do $W/enumgp $n rooted=1 out=$W/e/all$n; done

echo "== (e) anchors: enumeration (rooted shapes) vs tree search, vertex by vertex"
for n in 6 7 8 9 10 11 12 13 14; do
  $W/gp mode=anchors < $W/t/t$n.txt > $W/o/anch$n.txt 2>/dev/null
  echo "n=$n $(python3 canon.py anchors $W/t/t$n.txt $W/e/all$n.rooted $W/o/anch$n.txt)"
done

echo "== (c) run and skip rules, tree search (NONE = exhaustive failure)"
for n in $(seq 5 18); do
  for m in "R=1" "R=2" "H=1" "H=2" "H=2 SIDE=1" "H=2 SIDE=2" "H=2 SIDE=1 TRACK=1" "H=2 SIDE=2 TRACK=1" "H=1 TRACK=1" "H=2 TRACK=1"; do
    t=$(tag "$m"); $W/gp $m < $W/t/t$n.txt > $W/o/${t}_$n.txt 2>/dev/null
    echo "n=$n $m: $(python3 check_cert.py $W/t/t$n.txt $W/o/${t}_$n.txt $m | short)"
  done
  cmp -s <(cut -c1-2 $W/o/H1_$n.txt) <(cut -c1-2 $W/o/H1TRACK1_$n.txt) || echo "n=$n: H=1 tracked/state-based DIFFER"
  cmp -s <(cut -c1-2 $W/o/H2_$n.txt) <(cut -c1-2 $W/o/H2TRACK1_$n.txt) || echo "n=$n: H=2 tracked/state-based DIFFER"
done | grep -v "NONE 0 "

echo "== (c) same rules by pure enumeration of placements (second method); 'not drawn' must equal NONE above"
for n in $(seq 8 16); do
  for m in "R=1" "R=2" "H=1" "H=2" "H=2 SIDE=1" "H=2 SIDE=2"; do
    if [ $n -eq 16 ] && [[ "$m" == *SIDE* ]]; then continue; fi
    t=$(tag "$m")
    echo "$($W/enumgp $n $m out=$W/e/${t}_$n) :: $(python3 canon.py missing $W/t/t$n.txt $W/e/${t}_$n.shapes 2>/dev/null | head -1)"
  done
done | grep -v "not drawn 0"

echo "== (c) the named trees"
paste -d'|' $W/o/R2_16.txt $W/t/t16.txt | grep ^NONE | cut -d'|' -f2 | diff - trees16_no2run.txt && echo "two 16-vertex trees without a two-run placement: same as trees16_no2run.txt"
paste -d'|' $W/o/R2_18.txt $W/t/t18.txt | grep ^NONE | cut -d'|' -f2 | diff - tree18_no2run.txt && echo "18-vertex tree without a two-run placement: same as tree18_no2run.txt"
for m in "H=1" "H=2" "H=2 TRACK=1" "H=3" "R=3" "R=2"; do
  $W/gp $m < tree22.txt > $W/o/t22.txt 2>/dev/null
  echo "22-vertex tree, $m: $(cat $W/o/t22.txt) :: $(python3 check_cert.py tree22.txt $W/o/t22.txt $m | short)"
done
python3 probe_side.py 10

echo "== (d) spiders: deals (Conjecture S) and restricted deals"
for n in $(seq 4 26); do $W/spiderdeal $n free 2>/dev/null | python3 check_deal.py $n free; done
for n in $(seq 4 21); do $W/spiderdeal $n zigzag 2>/dev/null | python3 check_deal.py $n zigzag; done
for md in level first; do for n in 8 18 20; do $W/spiderdeal $n $md 2>/dev/null | python3 check_deal.py $n $md; done; done

echo "== SAT cross-check (CaDiCaL via python-sat)"
for n in 8 9 10; do
  python3 sat_check.py $W/t/t$n.txt H=0 expect=$W/o/R1_$n.txt | short
  python3 sat_check.py $W/t/t$n.txt H=1 expect=$W/o/H1_$n.txt | short
  python3 sat_check.py $W/t/t$n.txt R=2 expect=$W/o/R2_$n.txt | short
done
python3 sat_check.py $W/t/t11.txt R=1 expect=$W/o/R1_11.txt | short
python3 sat_check.py trees16_no2run.txt R=2
python3 sat_check.py trees16_no2run.txt R=3
python3 sat_check.py tree18_no2run.txt R=2
python3 sat_check.py tree22.txt H=3
echo "(python3 sat_check.py tree22.txt H=2 is the long one; run separately)"
