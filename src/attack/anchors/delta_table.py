# delta_table.py H : least number l of leaves at v for which v is an anchor of L(l; h1, h2), 1 <= h1 <= h2 <= H  (uses ./lch)
# Checks the Observation of PROOFS.txt section 4: for h1 even, h2 odd, h1 < h2 the value is exactly h1/2.
import subprocess,sys
def lch(l,hs): return subprocess.run(["./lch",str(l)]+[str(h) for h in hs],capture_output=True,text=True).stdout.startswith("ANCHOR")
H=int(sys.argv[1]); ok=True; cases=0
print("rows h1, columns h2 = h1..%d"%H)
for h1 in range(1,H+1):
    row=[]
    for h2 in range(h1,H+1):
        l=0
        while not lch(l,[h1,h2]): l+=1
        row.append(l)
        if h1%2==0 and h2%2==1:
            cases+=1
            if l!=h1//2: ok=False; print("EXCEPTION",h1,h2,l)
    print("%2d:"%h1," "*(2*(h1-1)),' '.join(str(x) for x in row),flush=True)
print("even h1 < odd h2 <= %d: %d cases, value == h1/2 in all: %s"%(H,cases,ok))
