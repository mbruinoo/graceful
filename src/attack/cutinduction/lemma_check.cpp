// Brute-force checks, from the definitions, of the statements claimed as proved.
//  CLEAN SET (definition): p a growth placement on labels 1..n, R a set of labels with n-|R| >= 2, such that
//     (1) exactly |R| brackets have a foot in R ("R-brackets"), and
//     (2) every other bracket jumps over exactly as many labels of R as there are R-brackets shorter than it.
//  T1: if R is a clean set, deleting R and closing the gaps gives a growth placement (definition of growth, README section 2).
//  T1c: conversely, if (1) holds and deleting R gives a placement in which the kept brackets keep their order by length, then (2) holds.
//  T2: if R1, R2 are disjoint clean sets and n-|R1|-|R2| >= 2 then the image of R2 is a clean set after deleting R1.
//  T3: (every leaf clean) <=> staircase <=> (the leaf end of the shortest bracket is clean)       [n>=3]
// Usage: lemma_check N MAXR      (all R with |R|<=MAXR; all growth placements on n<=N)
#include "enum.h"
static bool isClean(const Pl&p,unsigned R){ int n=p.n; int r=__builtin_popcount(R); if(n-r<2) return false; int rb=0;
  for(int k=1;k<n;k++) if((R>>p.pos[k]&1)||(R>>(p.pos[k]+k)&1)) rb++; if(rb!=r) return false;
  int shorter=0; for(int k=1;k<n;k++){ int a=p.pos[k], b=a+k; if((R>>a&1)||(R>>b&1)){ shorter++; continue; }
    int jump=0; for(int v=a+1;v<b;v++) if(R>>v&1) jump++; if(jump!=shorter) return false; } return true; }
// delete R, close the gaps.  ok=false if not a placement.  mono = kept brackets keep their order by length
static bool del(const Pl&p,unsigned R,Pl&q,bool&mono){ int n=p.n; int below[20],c=0; for(int v=1;v<=n;v++){ below[v]=c; if(R>>v&1) c++; } q.n=n-c; if(q.n<2) return false;
  bool have[20]={0}; int cnt=0,last=0; mono=true;
  for(int k=1;k<n;k++){ int a=p.pos[k], b=a+k; if((R>>a&1)||(R>>b&1)) continue; int a2=a-below[a], len=(b-below[b])-a2; if(have[len]) return false; have[len]=1; q.pos[len]=a2; cnt++; if(len<=last) mono=false; last=len; }
  return cnt==q.n-1; }
static bool isStaircase(const Pl&p){ int n=p.n; if(p.pos[n-1]!=1) return false; for(int k=1;k<n-1;k++){ int d=p.pos[k]-p.pos[k+1]; if(d!=0&&d!=1) return false; } return true; }
int main(int argc,char**argv){ int N=atoi(argv[1]), MAXR=atoi(argv[2]);
  for(int n=3;n<=N;n++){ long pl=0, cleanSets=0, bad1=0, bad1c=0, pairs=0, bad2=0, bad3=0, growthNonMono=0;
    enumGrowth(n,[&](const Pl&p){ pl++; Pl q; bool mono; vector<unsigned> cs;
      for(unsigned R=2;R<(2u<<n);R+=2){ int r=__builtin_popcount(R); if(r>MAXR||n-r<2) continue;
        bool c=isClean(p,R); bool ok=del(p,R,q,mono); bool g=ok&&isGrowth(q);
        if(c){ cleanSets++; cs.push_back(R); if(!g||!mono) bad1++; }
        if(ok&&mono&&!c) bad1c++; if(g&&!mono) growthNonMono++; }
      for(unsigned R1:cs) for(unsigned R2:cs) if(!(R1&R2) && n-__builtin_popcount(R1|R2)>=2){ pairs++; del(p,R1,q,mono);
        unsigned R2n=0; int c=0; for(int v=1;v<=n;v++){ if(R1>>v&1){ c++; continue; } if(R2>>v&1) R2n|=1u<<(v-c); } if(!isClean(q,R2n)) bad2++; }
      // T3
      int deg[20]={0}; for(int k=1;k<n;k++){ deg[p.pos[k]]++; deg[p.pos[k]+k]++; }
      bool allLeaves=true; for(int L=1;L<=n;L++) if(deg[L]==1 && !isClean(p,1u<<L)) allLeaves=false;
      int a=p.pos[1]; bool shortClean=(deg[a]==1&&isClean(p,1u<<a))||(deg[a+1]==1&&isClean(p,1u<<(a+1)));
      bool st=isStaircase(p); if(allLeaves!=st||shortClean!=st) bad3++; });
    printf("n=%d growth placements=%ld  clean sets(|R|<=%d)=%ld  T1 violations=%ld  T1c violations=%ld  disjoint clean pairs=%ld T2 violations=%ld  T3 violations=%ld  [growth restrictions that are not order-preserving: %ld]\n",n,pl,MAXR,cleanSets,bad1,bad1c,pairs,bad2,bad3,growthNonMono); fflush(stdout); }
}
