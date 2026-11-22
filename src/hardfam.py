# Families of non-caterpillar trees with few growth placements.  Usage: hardfam.py family param  -> paren string
import sys
f,m=sys.argv[1],int(sys.argv[2])
hub=lambda k:"("+"()"*k+")"
path=lambda k:"("*k+")"*k            # path with k vertices hanging down
if f=="A": s="("+hub(m)+"(())(()))"                 # centre with: a hub of m leaves, two legs of length 2      n=m+6
elif f=="B": s="("+hub(m)+")|((())(()))"            # hub - a - b, b has two legs of length 2                    n=m+7
elif f=="C": s="("+hub(m)*3+")"                     # centre with three hubs of m leaves                          n=3m+4
elif f=="D": s="("+("("+hub(m)+")")*3+")"           # centre, three paths of length 2 ending in hubs             n=3m+7
elif f=="S": s="("+path(m)*3+")"                    # spider with three legs of length m                          n=3m+1
elif f=="S4": s="("+path(m)*4+")"
elif f[0]=="D" and f[1:].isdigit(): s="("+("("+hub(m)+")")*int(f[1:])+")"      # Dk: centre, k paths of length 2 ending in hubs of m leaves
elif f[0]=="S" and f[1:].isdigit(): s="("+path(m)*int(f[1:])+")"              # Sk: spider with k legs of length m
print(s)
