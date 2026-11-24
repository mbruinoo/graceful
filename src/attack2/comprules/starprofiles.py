import sys
from collections import Counter
def designs(d):
    """all valid designs for the star with centre 0, leaves 1..d (ell(v)=v). own[j] in 0..d."""
    own = [None]*d; out = []
    def rec(b):
        if b < 0: out.append(own[:]); return
        # centre owns block b
        if own[b] is None:
            own[b] = 0; rec(b-1); own[b] = None
        for v in range(1, d+1):
            for j in ((v+b) if v > b else None, v-b-1):
                if j is None or j < 0 or j > d-1 or own[j] is not None: continue
                own[j] = v; rec(b-1); own[j] = None
    rec(d-1); return out
for d in range(2, int(sys.argv[1])+1):
    D = designs(d)
    prof = Counter()
    best = None
    for own in D:
        c = Counter(own); lam0 = c.get(0, 0); hubs = tuple(sorted((c.get(v, 0) for v in range(1, d+1)), reverse=True))
        prof[(lam0, hubs)] += 1
        if max(hubs) == 1:
            if best is None or lam0 < best[0]: best = (lam0, own[:])
    eq = sorted(k for k in prof if len(set(x for x in k[1] if x)) <= 1)
    print(d, len(D), 'profiles', len(prof), 'min centre blocks with hubs all 0/1:', best)
    print('    equal nonzero hubs:', [(l0, (h[0], sum(1 for x in h if x))) for l0, h in eq if any(h)][:12])
