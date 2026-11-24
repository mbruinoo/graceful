"""Valid designs (Rule B) for the star with centre at label 0 in which every leaf owns exactly one block.
A design is a bijection  j -> v(j)  from blocks 0..d-1 to leaves 1..d with bands
beta = j-v (v<=j, needs j<2v)  or  v-j-1 (v>j)  forming a permutation of 0..d-1.
usage: python3 stardesign.py DMAX   -- prints the number of designs and the lexicographically first one."""
import sys
def designs(d, limit=None):
    out = []; own = [None] * d; usedv = [False] * (d + 1); usedb = [False] * d
    # fill bands from the largest: band b
    def rec(b):
        if limit and len(out) >= limit: return
        if b < 0: out.append(own[:]); return
        # band b: (v<=j) j = v+b < 2v  => v > b ; (v>j) j = v-b-1
        for v in range(1, d + 1):
            if usedv[v]: continue
            for j in ((v + b) if v > b else None, v - b - 1):
                if j is None or j < 0 or j > d - 1 or own[j] is not None: continue
                own[j] = v; usedv[v] = True
                rec(b - 1)
                own[j] = None; usedv[v] = False
    rec(d - 1)
    return out
if __name__ == '__main__':
    for d in range(1, int(sys.argv[1]) + 1):
        D = designs(d)
        print(d, len(D), D[:3])
