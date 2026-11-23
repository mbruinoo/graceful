"""All spiders (>= 3 legs) on N vertices as tree lines, or one spider: python3 spider_trees.py N | python3 spider_trees.py legs 3 3 3"""
import sys
from check_spider import parts
from claims_c import spider, line
if sys.argv[1] == "legs":
    print(line(*spider(list(map(int, sys.argv[2:])))))
else:
    m = int(sys.argv[1]) - 1
    for p in parts(m, m):
        if len(p) >= 3: print(line(*spider(list(p))))
