R=/tmp/claude-0/-home-user-graceful/0371e752-f73a-552a-b40d-e3821e32333f/scratchpad
python3 gen.py P33 15 331 > $R/P33.t; $R/ref 1 3000000 0 1 40 < $R/P33.t > $R/P33.o 2> $R/P33.e; python3 chk.py $R/P33.t $R/P33.o 1 > $R/bg2.out 2>&1
