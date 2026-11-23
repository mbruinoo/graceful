// k-step peeling.  A RESTRICTION of a placement p on n labels to a label set S: keep the brackets with both feet in S,
// relabel S order-preservingly to 1..|S|.  If the result is a growth placement on |S| vertices (checked by definition) it is a
// growth restriction.  |S|=n-1 is exactly clean-leaf removal (README Lemma 8).
// Class K(k): generated from the single edge by extension steps that add at most k labels at a time.
// Usage: restrict N KMAX [MODE]  (MODE=1: order-preserving restrictions only = clean sets)     prints, for each n<=N and k<=KMAX, #placements in K(k) and #tree shapes reached.
#include "enum.h"
static int MODE=0;   // 1: only order-preserving ("clean set") restrictions
static bool restrictPl(const Pl&p,unsigned R,Pl&q){ int n=p.n; int below[20]; int c=0; for(int v=1;v<=n;v++){ below[v]=c; if(R>>v&1) c++; }
  q.n=n-c; if(q.n<2) return false; bool have[20]={0}; int cnt=0;
  for(int k=1;k<n;k++){ int a=p.pos[k], b=a+k; if((R>>a&1)||(R>>b&1)) continue; int a2=a-below[a], b2=b-below[b]; int len=b2-a2; if(have[len]) return false; have[len]=1; q.pos[len]=a2; cnt++; }
  if(cnt!=q.n-1) return false;
  if(MODE==1){ int last=0; for(int k=1;k<n;k++){ int a=p.pos[k], b=a+k; if((R>>a&1)||(R>>b&1)) continue; int len=(b-below[b])-(a-below[a]); if(len<=last) return false; last=len; } }
  return isGrowth(q); }
int main(int argc,char**argv){ int N=atoi(argv[1]), KMAX=atoi(argv[2]); if(argc>3) MODE=atoi(argv[3]);
  vector<unordered_map<u64,unsigned char>> cls(N+1);
  for(int n=2;n<=N;n++){ vector<set<string>> reachT(KMAX+1); set<string> allT; vector<long> cnt(KMAX+1,0); long total=0; long prim=0;
    vector<long> minstep(n+1,0);
    auto&M=cls[n]; 
    enumGrowth(n,[&](const Pl&p){ total++; unsigned char fl=0; int ms=0;
      if(n==2) fl=(1<<KMAX)-1; else {
        Pl q; 
        // all removal sets of size 1..KMAX
        for(int s=1;s<=KMAX && s<=n-2;s++){ unsigned char got=0;
          // enumerate subsets of size s of labels 1..n
          vector<int> idx(s); for(int i=0;i<s;i++) idx[i]=i+1;
          while(true){ unsigned R=0; for(int i=0;i<s;i++) R|=1u<<idx[i];
            if(restrictPl(p,R,q)){ if(!ms) ms=s; got|=cls[n-s][enc(q)]; }
            int i=s-1; while(i>=0 && idx[i]==n-s+1+i) i--; if(i<0) break; idx[i]++; for(int j=i+1;j<s;j++) idx[j]=idx[j-1]+1; }
          // class K(k) for k>=s may use a step of size s landing in K(k)
          for(int k=s;k<=KMAX;k++) if(got>>(k-1)&1) fl|=1<<(k-1); }
        if(ms!=1) prim++; minstep[ms]++; }
      M[enc(p)]=fl; string c; bool need=false; for(int k=1;k<=KMAX;k++) if(fl>>(k-1)&1){ cnt[k]++; need=true; }
      c=canon(p); allT.insert(c); for(int k=1;k<=KMAX;k++) if(fl>>(k-1)&1) reachT[k].insert(c); });
    printf("n=%d growth=%ld trees=%zu |",n,total,allT.size()); for(int k=1;k<=KMAX;k++) printf(" K%d: %ld pl, %zu trees |",k,cnt[k],reachT[k].size());
    printf(" smallest growth-restriction step:"); for(int s=1;s<=KMAX;s++) printf(" %d:%ld",s,minstep[s]); printf(" none<=%d:%ld\n",KMAX,minstep[0]);
    for(int k=2;k<=KMAX;k++) if(reachT[k].size()<allT.size() && allT.size()-reachT[k].size()<=6) for(auto&c:allT) if(!reachT[k].count(c)) printf("   K%d misses %s\n",k,c.c_str());
    fflush(stdout); }
}
