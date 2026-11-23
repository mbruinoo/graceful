#!/usr/bin/env python3
"""Independent referee check of the 'top-block rule' for spiders (r, 2^k [, 1^j]).
Written from the rule STATEMENT only.  Usage: referee.py KMAX RMAX [kstep]"""
import sys

def valid_deal(legs_numbers, lengths, m):
    """Definition check. legs_numbers[i] = numbers of leg i in the order received, with signs
    decided by caller? No: here each leg is a list of (number, sign) moves; first must be up from 0."""
    # every number m..1 handed out exactly once
    allnum = sorted(w for leg in legs_numbers for (w, s) in leg)
    if allnum != list(range(1, m + 1)): return False, "numbers not a partition of 1..m"
    if sorted(len(l) for l in legs_numbers) != sorted(lengths): return False, "leg lengths wrong"
    seen = bytearray(m + 1); seen[0] = 1
    for leg in legs_numbers:
        tip = 0; prev = m + 1
        for idx, (w, s) in enumerate(leg):
            if w >= prev: return False, "leg not decreasing"
            prev = w
            if idx == 0 and s != 1: return False, "first move not up"
            tip += s * w
            if tip < 1 or tip > m: return False, "label out of range %d" % tip
            if seen[tip]: return False, "label %d visited twice" % tip
            seen[tip] = 1
    return True, ""

def odd_design(k):
    assert k % 2 == 1
    c = (3 * k - 1) // 2
    d = {}
    for i in range(1, k + 1):
        d[i] = k - 2 * i if i <= (k - 1) // 2 else 2 * k - 2 * i
    return c, d

def even_design(k):
    h = k // 2; assert k == 2 * h and h >= 1
    c = 3 * h + 1; d = {}
    for s in range(h): d[2 * h - 1 - 2 * s] = h + 2 + s
    for j in range(1, h + 1): d[2 * j] = h - j
    return c, d

def tower_design(k, t):
    assert k % 3 == 0
    q = k
    while q % 2 == 0: q //= 2
    while q % 3 == 0: q //= 3
    Q = 3 * q; T = k // Q; assert Q * T == k
    c0, d0 = odd_design(q)
    D = [(0, q, 2 * q), (0, q, 4 * q), (0, 3 * q, 4 * q)][t]
    al = [(1, 2, 0), (2, 0, 1), (1, 2, 0)][t]
    mid = {}
    for j in range(3):
        for i2 in range(1, q + 1):
            mid[j * q + i2] = D[al[j]] + d0[i2]
    cmid = (3 + t) * q + (3 * q - 1) // 2
    d = {}
    for J in range(T):
        for i in range(1, Q + 1):
            d[J * Q + i] = 3 * Q * (T - 1 - J) + mid[i]
    return 3 * Q * (T - 1) + cmid, d

def designs(k):
    out = [("odd", ) + odd_design(k)] if k % 2 else [("even", ) + even_design(k)]
    if k % 3 == 0:
        for t in range(3): out.append(("tower%d" % t, ) + tower_design(k, t))
    return out

def build(r, k, c, d, extra=0):
    """deal from the statement; returns (legs, lengths, m) or None if l<0 / not integral"""
    B = r + k
    if (B - c) % 3 or B < c: return None
    l = (B - c) // 3; v = B - 2 * l
    m = r + 2 * k + extra
    legs = [[(m - j, 1)] for j in range(extra)]           # extra length-1 legs get the largest numbers
    short2 = set()
    for i in range(1, k + 1):
        legs.append([(B + i, 1), (v - d[i], -1)]); short2.add(v - d[i])
    long = []; s = 1
    for w in range(B, 0, -1):
        if w in short2: continue
        long.append((w, s)); s = -s
    legs.append(long)
    return legs, [1] * extra + [2] * k + [r], m

def design_ok(k, c, d):
    """the proof's design conditions, checked directly"""
    if sorted(d) != list(range(1, k + 1)): return "delta not defined on 1..k"
    vals = sorted(d.values())
    if len(set(vals)) != k or vals[0] < 0: return "offsets not distinct >=0"
    rank = {x: n for n, x in enumerate(vals)}
    if any((x - rank[x]) % 2 for x in vals): return "parity fails"
    Pi = sorted((x + rank[x]) // 2 for x in vals)
    if sorted(c - i - d[i] for i in d) != Pi: return "(*) not a bijection"
    if c - vals[-1] < 1: return "c <= max Delta"
    return ""

def main():
    KMAX = int(sys.argv[1]); RMAX = int(sys.argv[2]); kstep = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    EXTRA = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    nchecked = 0; bad = []; miss = []; desbad = []; extra_valid_outside = 0; firstr_bad = []
    for k in range(1, KMAX + 1, kstep):
        ds = designs(k)
        for name, c, d in ds:
            e = design_ok(k, c, d)
            if e: desbad.append((k, name, e))
            if name.startswith("tower"):
                t = int(name[-1]); q = k
                while q % 2 == 0: q //= 2
                while q % 3 == 0: q //= 3
                if c % 3 != (1 + t * q) % 3: desbad.append((k, name, "residue"))
                if c - k > 2 * k: desbad.append((k, name, "c-k>2k"))
            else:
                if c % 3 != 1: desbad.append((k, name, "residue"))
        for r in range(1, RMAX + 1):
            B = r + k
            inA = (B % 3 == 1) and (r >= (k - 1) / 2 if k % 2 else r >= k // 2 + 1)
            inB = (k % 3 == 0) and r >= 2 * k
            got = False
            for name, c, d in ds:
                if c % 3 != B % 3: continue
                for ex in range(EXTRA + 1):
                    dl = build(r, k, c, d, ex)
                    if dl is None: break
                    ok, why = valid_deal(*dl); nchecked += 1
                    if not ok: bad.append((k, r, name, ex, why))
                    elif ex == 0: got = True
            if (inA or inB) and not got: miss.append((k, r))
            if got and not (inA or inB): extra_valid_outside += 1
    print("k<=%d step %d, r<=%d, extra legs 0..%d: deals checked %d, invalid %d, family members with no valid deal %d, design failures %d, valid outside claimed family %d"
          % (KMAX, kstep, RMAX, EXTRA, nchecked, len(bad), len(miss), len(desbad), extra_valid_outside))
    for x in bad[:10]: print(" INVALID", x)
    for x in miss[:10]: print(" MISS", x)
    for x in desbad[:10]: print(" DESIGN", x)

if __name__ == "__main__":
    if sys.argv[1] == "example":
        c, d = odd_design(3); legs, L, m = build(10, 3, c, d)
        for leg in legs:
            tip = 0; lab = []
            for w, s in leg: tip += s * w; lab.append(tip)
            print([w for w, s in leg], lab)
        print(valid_deal(legs, L, m))
    else: main()
