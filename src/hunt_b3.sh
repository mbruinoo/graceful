#!/bin/sh
# Conjecture B3 (three runs) for every tree on n vertices, split into PARTS resumable pieces run on JOBS cores.
# Usage: ./hunt_b3.sh n [PARTS [JOBS]]     each piece writes r3_<n>_p<i>of<PARTS>.txt (one summary line when done)
n=$1; P=${2:-64}; J=${3:-4}
seq 0 $((P-1)) | xargs -P $J -I{} sh -c "f=r3_${n}_p{}of$P.txt; grep -q '^n=' \$f 2>/dev/null || nice -n 19 ./runsolve_gen $n 3 {} $P > \$f"
cat r3_${n}_p*of$P.txt | awk '/^n=/{split($0,a,"trees=");split(a[2],b," ");t+=b[1];split($0,c,"none=");split(c[2],d," ");no+=d[1];split($0,e,"unresolved=");u+=e[1];k++} !/^n=/{print} END{print "pieces done:",k,"trees:",t,"none:",no,"unresolved:",u}'
