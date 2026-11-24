"""Query rsolve on L(l;h1,h2) trees.  Usage: python3 lgrid.py P_LIST QMAX NMAX [allparity] | ./rsolve d"""
import sys

def L(l, p, q):
    E = [(0, 1), (1, 2), (1, 3)]
    x = 4
    for _ in range(p): E.append((2, x)); x += 1
    for _ in range(q): E.append((3, x)); x += 1
    for _ in range(l): E.append((0, x)); x += 1
    return x, E

if __name__ == "__main__":
    ps = [int(t) for t in sys.argv[1].split(",")]
    qmax, nmax = int(sys.argv[2]), int(sys.argv[3])
    allpar = len(sys.argv) > 4
    for p in ps:
        for q in range(1, qmax + 1):
            if not allpar and (q % 2 == 0 or q <= p): continue
            for l in range(0, p // 2 + 3):
                n, E = L(l, p, q)
                if n > nmax: continue
                sys.stderr.write(f"{l} {p} {q}\n")
                print(n, 0, " ".join(f"{u} {v}" for u, v in E))
