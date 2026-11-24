R=/tmp/claude-0/-home-user-graceful/0371e752-f73a-552a-b40d-e3821e32333f/scratchpad
python3 gen.py D2 3 30 1 > $R/D2.t 2>/dev/null; $R/ref 1 2000000 0 1 30 < $R/D2.t > $R/D2.o 2> $R/D2.e; python3 chk.py $R/D2.t $R/D2.o 1 > $R/bg3.out 2>&1
python3 gen.py DH 31 > $R/DH31.t; $R/ref 0 300000000 0 < $R/DH31.t > $R/DH31.o 2>> $R/bg3.out
python3 gen.py H3 13 41 > $R/H3s.t; $R/ref 0 300000000 0 < $R/H3s.t > $R/H3s.o 2>> $R/bg3.out
python3 gen.py LLL 1 14 x > $R/Sl.t; $R/ref 0 2000000000 0 < $R/Sl.t > $R/Sl.o 2>> $R/bg3.out
