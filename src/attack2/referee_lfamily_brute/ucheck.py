"""Rebuild the Theorem U labelling from the claim text and check it from the definition
(graceful, root v at 0, lengths strictly decrease away from v). Usage: python3 ucheck.py SMAX QMAX"""
import sys

def build(s, q):
    m = 3 * s + q + 3; a = m
    lab = {"v": 0, "c": a, "Q": 2, "P": 3}
    par = {"c": "v", "Q": "c", "P": "c"}
    for i in range(s):                      # leaves of v at a-1, a-4, ..., a-3s+2
        lab[f"vl{i}"] = a - 1 - 3 * i; par[f"vl{i}"] = "v"
    for j in range(q):                      # Q leaves labels 5..q+4
        lab[f"ql{j}"] = 5 + j; par[f"ql{j}"] = "Q"
    pl = [4, 1] + [x for i in range(1, s) for x in (a - 3 * i, a - 3 * i + 1)]
    for j, x in enumerate(pl):
        lab[f"pl{j}"] = x; par[f"pl{j}"] = "P"
    return m, lab, par, len(pl)

def ok(m, lab, par):
    if sorted(lab.values()) != list(range(m + 1)): return "labels"
    L = {x: abs(lab[x] - lab[par[x]]) for x in par}
    if sorted(L.values()) != list(range(1, m + 1)): return "lengths"
    for x in par:
        if par[x] in par and L[x] >= L[par[x]]: return "decrease"
    return "ok"

if __name__ == "__main__":
    S, Qm = int(sys.argv[1]), int(sys.argv[2]); bad = 0; tot = 0
    for s in range(1, S + 1):
        for q in range(1, Qm + 1):
            m, lab, par, np_ = build(s, q); tot += 1
            assert np_ == 2 * s and sum(1 for x in par if par[x] == "v") == s + 1
            r = ok(m, lab, par)
            if r != "ok": bad += 1; print("FAIL", s, q, r)
    print("checked", tot, "failures", bad)
