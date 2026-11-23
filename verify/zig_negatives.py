"""Second method for the spiders reported without a zigzag deal: the plain Python search of check_spider.py
(different code, different symmetry handling) on each of them.  usage: python3 zig_negatives.py [seconds]"""
import sys, glob, multiprocessing as mp
from check_spider import py_search
def work(legs):
    return legs, py_search(legs, True)
if __name__ == "__main__":
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 3600
    todo = []
    for f in sorted(glob.glob("out/spider_*_zig.txt")):
        for line in open(f):
            head, body = line.split("|")
            if body.split()[0] == "NONE": todo.append(tuple(map(int, head.split())))
    todo.sort(key=lambda l: (sum(l), l))
    with mp.Pool(2) as pool:
        res = [(l, pool.apply_async(work, (l,))) for l in todo]
        for l, r in res:
            try:
                _, found = r.get(timeout=limit)
                print(f"n={sum(l)+1} S{l}: Python search finds {'A ZIGZAG DEAL  *** DISAGREES ***' if found else 'none (agrees)'}", flush=True)
            except mp.TimeoutError:
                print(f"n={sum(l)+1} S{l}: Python search not finished in {limit}s", flush=True)
