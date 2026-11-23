"""Check that a tree file has no two isomorphic trees, without holding all canonical codes in memory:
64-bit hashes of the canonical codes are collected (in parallel parts) and compared.
usage: PART=i/k python3 distinct.py N FILE   -> writes out/hash_N_i.bin
       python3 distinct.py N merge k        -> counts distinct hashes
Equal hashes of different codes are possible in principle (probability about m^2 / 2^65 for m trees:
4e-5 at n = 24, 3e-4 at n = 25); such a collision could only make this check fail, never pass wrongly."""
import sys, os, hashlib, array
from common import canon
n = int(sys.argv[1])
if sys.argv[2] == "merge":
    k = int(sys.argv[3]); a = array.array("Q")
    for i in range(k):
        with open(f"out/hash_{n}_{i}.bin", "rb") as f: a.frombytes(f.read())
    total = len(a)
    try:
        import numpy as np
        distinct = int(np.unique(np.frombuffer(a, dtype=np.uint64)).size)
    except ImportError:
        distinct = len(set(a))
    print(f"n={n}: {total} trees, {distinct} distinct canonical codes (by 64-bit hash): {'OK' if total == distinct else 'DUPLICATES'}")
else:
    part, parts = map(int, os.environ.get("PART", "0/1").split("/"))
    a = array.array("Q")
    with open(sys.argv[2]) as f:
        for i, line in enumerate(f):
            if i % parts != part: continue
            e = [(int(x) + 1, int(y) + 1) for x, y in (t.split("-") for t in line.split()[1:])]
            a.append(int.from_bytes(hashlib.blake2b(canon(n, e).encode(), digest_size=8).digest(), "little"))
    with open(f"out/hash_{n}_{part}.bin", "wb") as f: a.tofile(f)
