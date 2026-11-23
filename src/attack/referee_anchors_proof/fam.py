def L(l,h1,h2):
    e=[(0,1),(1,2),(1,3)]; nx=4
    for _ in range(h1): e.append((2,nx)); nx+=1
    for _ in range(h2): e.append((3,nx)); nx+=1
    for _ in range(l): e.append((0,nx)); nx+=1
    return nx,e
def hubs(sizes, rootleaves=0):
    e=[]; nx=1
    for s in sizes:
        h=nx; nx+=1; e.append((0,h))
        for _ in range(s): e.append((h,nx)); nx+=1
    for _ in range(rootleaves): e.append((0,nx)); nx+=1
    return nx,e
def line(n,e,root=0): return "%d %d "%(n,root)+" ".join("%d %d"%x for x in e)
