#!/bin/sh
# Exhaustive (deterministic, complete) existence search over a whole class of structured trees.
# Usage: ./hunt_exist.sh CLASS [nmin nmax [bmax [part parts]]]     log: hunt_exist_CLASS[.part].log (not committed)
c=$1; nmin=${2:-26}; nmax=${3:-70}; bmax=${4:-9}; part=${5:-0}; parts=${6:-1}
python3 huntsets.py $c $nmin $nmax $bmax | awk -v p=$part -v q=$parts 'NR%q==p' | QUIET=1 ./growfam exist > hunt_exist_$c.$part.log
