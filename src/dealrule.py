# Search for PERIODIC dealing rules for spiders with k equal legs.
# A rule is a word over legs 0..k-1 of length P in which every leg occurs P/k times.  To deal: hand the numbers
# m, m-1, ..., 1 to the legs following the word cyclically.  Leg labels are the alternating sums of its numbers.
# The rule "works for L" if the spider with k legs of length L (m = kL, P | m) gets all labels different.
# Usage: dealrule.py k P Lmax
import sys, itertools
k,P,Lmax=int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3])
def works(word,L):
    m=k*L; cur=[0]*k; cnt=[0]*k; seen=set()
    for t in range(m):
        i=word[t%P]; w=m-t
        cur[i]+= w if cnt[i]%2==0 else -w; cnt[i]+=1
        x=cur[i]
        if x<1 or x>m or x in seen: return False
        seen.add(x)
    return True
per=P//k; Ls=[L for L in range(per,Lmax+1) if (k*L)%P==0]
base=[i for i in range(k) for _ in range(per)]
seen=set(); good=[]
for w in set(itertools.permutations(base)):
    if w[0]!=0: continue                      # leg 0 takes the largest number (legs are interchangeable)
    ok=[L for L in Ls if works(w,L)]
    if len(ok)==len(Ls): good.append(w)
    elif len(ok)>=max(3,len(Ls)-2): seen.add((len(ok),w,tuple(L for L in Ls if L not in ok)))
print(f"k={k} period={P} leg lengths tested={Ls}")
print(f"rules that work for every tested length: {len(good)}")
for w in sorted(good)[:20]: print("   ","".join(str(i+1) for i in w))
if not good:
    for c,w,bad in sorted(seen,reverse=True)[:8]: print(f"   near miss {''.join(str(i+1) for i in w)} fails at L={bad}")
