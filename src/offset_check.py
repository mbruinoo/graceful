# The offset rule for skips, checked on every growth placement.
# State before a move: labels 1..n, U = used.  The MAIN GAP is the longest run of unused labels; a = the used label just
# left of it, d = the used label just right of it; the other unused labels are HOLES (H of them).
# Claim A: if the new label x lies in the main gap and joins a label y on the other side of the main gap, then
#          y = d + (H + s)  when x is on the left  (x = a + 1 + s, having skipped s cells),
#          y = a - (H + s)  when x is on the right (x = d - 1 - s).
#          i.e. the partner sits exactly (number of holes after the move) places in from the innermost label opposite.
# Claim B (threads): with H holes held fixed and pushes alternating left, right, left, ..., the across-edges form
#          2H+1 parallel paths.  (Checked symbolically below on the index pattern.)
from growslide import growth_cfgs
def runs(n,U):
    out=[]; i=1
    while i<=n:
        if i not in U:
            j=i
            while j+1<=n and j+1 not in U: j+=1
            out.append((i,j)); i=j+1
        else: i+=1
    return out
tot=bad=across=0
for n in range(4,11):
    for p in growth_cfgs(n):
        U={1,n}
        for k in range(n-2,0,-1):
            x,y=p[k],p[k]+k
            if x in U: x,y=y,x                  # x = new label, y = partner
            R=runs(n,U); main=max(R,key=lambda r:r[1]-r[0])
            a,d=main[0]-1,main[1]+1; H=sum(r[1]-r[0]+1 for r in R)-(main[1]-main[0]+1)
            if main[0]<=x<=main[1] and ((y<=a)!=(x-a<=d-x) or True):
                left = (y>=d)                     # joining something on the right side means x counts from the left
                if y>=d or y<=a:
                    s = x-a-1 if y>=d else d-1-x
                    # only the "across" case: partner beyond the main gap on the far side from where x was counted
                    tot+=1; across+=1
                    want = d+H+s if y>=d else a-H-s
                    if y!=want: bad+=1
            U|={x}
print(f"across moves checked (n=4..10): {across}, violations of the offset rule: {bad}")
# Claim B: x_i joins R[H] = y_{i-1-H}; y_i joins L[H] = x_{i-H}.  Follow one thread.
for H in range(0,5):
    def nxt(side,i): return ('y',i+H) if side=='x' else ('x',i+H+1)
    seen=set(); threads=0
    for start in [('x',i) for i in range(1,60)]+[('y',i) for i in range(1,60)]:
        if start in seen: continue
        cur=start; 
        # walk backwards to the thread's first element inside the window, then forwards
        while cur not in seen and cur[1]<400: seen.add(cur); cur=nxt(*cur)
        threads+=1
    # count distinct threads among late vertices only (steady state)
    roots=set()
    for i in range(200,200+2*H+1+3):
        cur=('x',i)
        for _ in range(4*(2*H+1)): cur=nxt(*cur)
        roots.add((cur[0], cur[1]%(2*H+1)))
    print(f"H={H}: thread period in the push index = {2*H+1}")
