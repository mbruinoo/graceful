// d2.cpp -- exact anchor decision for the ROOT of a depth-2 tree ("hubs"): root v, children c_1..c_r, c_i has k_i leaf children.
// By README Theorem 7 (root form): v is an anchor iff there are labels 0..m (v=0, m = number of edges) with
//   label(c_i)=b_i (= length of edge v-c_i), every leaf of c_i at b_i+w or b_i-w with length w<b_i,
//   all labels distinct covering 0..m and all lengths distinct covering 1..m.   (Leaves impose no further order.)
// So: choose distinct b_i (one of them = m); then a bijection from W=[1,m]\B to Y=[1,m]\B, w -> b_i +- w (w<b_i), hub i used k_i times.
// Exact search with fewest-options-first branching.  Usage: d2 k_1 ... k_r    prints ANCHOR + witness or NOT.
#include <bits/stdc++.h>
using namespace std;
int r,m; vector<int> K; int b[16]; bool isB[400];
int wOf[400];      // label -> weight using it (0 = none)
int lOf[400], hOf[400];  // weight -> label, hub
int capLeft[16]; long long nodes=0;
static inline bool freeW(int w){ return w>=1&&w<=m&&!isB[w]&&!lOf[w]; }
static inline bool freeL(int L){ return L>=1&&L<=m&&!isB[L]&&!wOf[L]; }
bool solve(int left){
  if(left==0) return true; nodes++;
  // find most constrained weight or label
  int best=1e9, bw=-1, bl=-1;
  for(int w=1;w<=m;w++) if(freeW(w)){ int c=0; for(int i=0;i<r;i++) if(capLeft[i]&&b[i]>w){ if(freeL(b[i]-w)) c++; if(freeL(b[i]+w)) c++; } if(c<best){best=c;bw=w;bl=-1;} if(c==0) return false; }
  for(int L=1;L<=m;L++) if(freeL(L)){ int c=0; for(int i=0;i<r;i++) if(capLeft[i]){ int w=abs(L-b[i]); if(w<b[i]&&freeW(w)) c++; } if(c<best){best=c;bl=L;bw=-1;} if(c==0) return false; }
  if(bw>=0){ int w=bw; for(int i=0;i<r;i++) if(capLeft[i]&&b[i]>w) for(int s=-1;s<=1;s+=2){ int L=b[i]+s*w; if(!freeL(L)) continue;
      lOf[w]=L; hOf[w]=i; wOf[L]=w; capLeft[i]--; if(solve(left-1)) return true; capLeft[i]++; lOf[w]=0; wOf[L]=0; } }
  else { int L=bl; for(int i=0;i<r;i++) if(capLeft[i]){ int w=abs(L-b[i]); if(!(w<b[i]&&freeW(w))) continue;
      lOf[w]=L; hOf[w]=i; wOf[L]=w; capLeft[i]--; if(solve(left-1)) return true; capLeft[i]++; lOf[w]=0; wOf[L]=0; } }
  return false; }
bool chooseB(int i){ // assign b[i..]; hubs sorted by k; equal-k hubs get decreasing labels
  if(i==r){ bool hasM=false; for(int j=0;j<r;j++) if(b[j]==m) hasM=true; if(!hasM) return false;
    for(int j=0;j<r;j++) capLeft[j]=K[j]; memset(wOf,0,sizeof wOf); memset(lOf,0,sizeof lOf); return solve(m-r); }
  int hi = (i>0&&K[i]==K[i-1])? b[i-1]-1 : m;
  for(int x=hi;x>=K[i]+1;x--){ if(isB[x]) continue; b[i]=x; isB[x]=1; if(chooseB(i+1)) return true; isB[x]=0; }
  return false; }
int main(int argc,char**argv){ for(int i=1;i<argc;i++) K.push_back(atoi(argv[i])); sort(K.begin(),K.end()); r=K.size(); m=r; for(int k:K) m+=k;
  bool ok=chooseB(0);
  if(ok){ printf("ANCHOR m=%d nodes=%lld b:",m,nodes); for(int i=0;i<r;i++) printf(" %d(k=%d)",b[i],K[i]); printf(" leaves(w@hub->label):"); for(int w=1;w<=m;w++) if(lOf[w]) printf(" %d@%d->%d",w,b[hOf[w]],lOf[w]); printf("\n"); }
  else printf("NOT m=%d nodes=%lld\n",m,nodes); }
