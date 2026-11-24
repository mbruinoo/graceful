R=/tmp/claude-0/-home-user-graceful/0371e752-f73a-552a-b40d-e3821e32333f/scratchpad
for n in 13 14 15 16 17; do python3 gen.py ALL $n 1 > $R/a$n.t; $R/ref 1 200000000 0 < $R/a$n.t > $R/a$n.o1 2> $R/a$n.e1; python3 chk.py $R/a$n.t $R/a$n.o1 1; done > $R/bg1.out 2>&1
for n in 14 15 16; do python3 gen.py ALL $n > $R/b$n.t; $R/ref 0 200000000 0 < $R/b$n.t 2>&1 >/dev/null | sed "s/^/n=$n allroots slack0 /"; done >> $R/bg1.out 2>&1
