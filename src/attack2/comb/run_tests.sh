#!/bin/sh
# Re-runs every formula check quoted in REPORT.txt; output in logs/tests.log
{
python3 rules.py paired-all 60 24
python3 rules.py two 200
python3 rules.py random 200 5000
python3 rules.py twos 200
python3 rules.py ones 200
python3 rounds.py two 200
python3 rounds.py test 200 30
python3 caravan.py test 200
python3 covercheck.py 24 logs/exact_5_30.txt.gz 60
python3 ../../attack/gamestrategy/comb_rules.py 200
} > logs/tests.log 2>&1
