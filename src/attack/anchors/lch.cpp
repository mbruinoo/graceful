// lch.cpp -- exact anchor decision for the root v of the tree  L(l; h_1..h_r):
//   v has l leaf neighbours and one more neighbour c;  c has r further neighbours g_1..g_r;  g_i has h_i leaf children.
// Independent of anch.cpp/anchq.cpp: uses the root form (README Theorem 7) as an exact-cover problem.
//   labels 0..m, v=0.  A root leaf has label = its length.  label(c)=a (length a).  label(g_i)=a+-x_i, length x_i<a.
//   A leaf of g_i has label g_i+-w with length w<x_i.  All labels distinct (cover 0..m), all lengths distinct (cover 1..m).
//   After choosing a, g_i: bijection  free lengths -> free labels,  w -> w (root leaf), or g_i+-w (leaf of g_i, w<x_i), with class counts l, h_i.
// Usage: lch l h_1 ... h_r   -> ANCHOR + witness, or NOT.   Fewest-options-first exact search (complete).
#include <bits/stdc++.h>
using namespace std;
int l,r,m,a; vector<int> H; int g[16],x[16]; bool fixedL[600], fixedW[600]; int wOf[600], lOf[600], cOf[600]; int capLeft[17]; long long nodes=0;
static inline bool freeW(int w){ return w>=1&&w<=m&&!fixedW[w]&&!lOf[w]; }
static inline bool freeL(int L){ return L>=1&&L<=m&&!fixedL[L]&&!wOf[L]; }
bool solve(int left){ if(left==0) return true; nodes++;
  int best=1e9,bw=-1,bl=-1;
  for(int w=1;w<=m;w++) if(freeW(w)){ int c=0; if(capLeft[r]&&freeL(w)) c++; for(int i=0;i<r;i++) if(capLeft[i]&&x[i]>w){ if(freeL(g[i]-w)) c++; if(freeL(g[i]+w)) c++; } if(c==0) return false; if(c<best){best=c;bw=w;bl=-1;} }
  for(int L=1;L<=m;L++) if(freeL(L)){ int c=0; if(capLeft[r]&&freeW(L)) c++; for(int i=0;i<r;i++) if(capLeft[i]){ int w=abs(L-g[i]); if(w<x[i]&&freeW(w)) c++; } if(c==0) return false; if(c<best){best=c;bl=L;bw=-1;} }
  if(bw>=0){ int w=bw;
    if(capLeft[r]&&freeL(w)){ lOf[w]=w; cOf[w]=r; wOf[w]=w; capLeft[r]--; if(solve(left-1)) return true; capLeft[r]++; lOf[w]=0; wOf[w]=0; }
    for(int i=0;i<r;i++) if(capLeft[i]&&x[i]>w) for(int s=-1;s<=1;s+=2){ int L=g[i]+s*w; if(!freeL(L)) continue;
      lOf[w]=L; cOf[w]=i; wOf[L]=w; capLeft[i]--; if(solve(left-1)) return true; capLeft[i]++; lOf[w]=0; wOf[L]=0; } }
  else { int L=bl;
    if(capLeft[r]&&freeW(L)){ lOf[L]=L; cOf[L]=r; wOf[L]=L; capLeft[r]--; if(solve(left-1)) return true; capLeft[r]++; lOf[L]=0; wOf[L]=0; }
    for(int i=0;i<r;i++) if(capLeft[i]){ int w=abs(L-g[i]); if(!(w<x[i]&&freeW(w))) continue;
      lOf[w]=L; cOf[w]=i; wOf[L]=w; capLeft[i]--; if(solve(left-1)) return true; capLeft[i]++; lOf[w]=0; wOf[L]=0; } }
  return false; }
bool chooseG(int i){
  if(i==r){ for(int j=0;j<r;j++) capLeft[j]=H[j]; capLeft[r]=l; memset(wOf,0,sizeof wOf); memset(lOf,0,sizeof lOf); return solve(m-1-r); }
  for(int L=1;L<=m;L++){ if(fixedL[L]) continue; int w=abs(L-a); if(w<1||w>=a||fixedW[w]||w<=H[i]) continue;   // need H[i] lengths below x_i
    if(i>0&&H[i]==H[i-1]&&L<g[i-1]) continue;    // equal hubs: ordered labels
    g[i]=L; x[i]=w; fixedL[L]=1; fixedW[w]=1; if(chooseG(i+1)) return true; fixedL[L]=0; fixedW[w]=0; }
  return false; }
int main(int argc,char**argv){ l=atoi(argv[1]); for(int i=2;i<argc;i++) H.push_back(atoi(argv[i])); sort(H.begin(),H.end()); r=H.size(); m=l+1+r; for(int h:H) m+=h;
  bool ok=false;
  for(a=m;a>=1&&!ok;a--){ if(a<m&&l==0) break; if(a<m-l) break;   // length m is on a root edge: either c (a=m) or a root leaf; at most l lengths can exceed a
    memset(fixedL,0,sizeof fixedL); memset(fixedW,0,sizeof fixedW); fixedL[a]=fixedW[a]=1; ok=chooseG(0); if(ok) break; }
  if(ok){ printf("ANCHOR m=%d nodes=%lld c=%d",m,nodes,a); for(int i=0;i<r;i++) printf(" g%d=%d(h=%d)",i+1,g[i],H[i]); printf(" | length@class->label:"); for(int w=1;w<=m;w++) if(lOf[w]){ if(cOf[w]==r) printf(" %d@root->%d",w,lOf[w]); else printf(" %d@g%d->%d",w,cOf[w]+1,lOf[w]); } printf("\n"); }
  else printf("NOT m=%d nodes=%lld\n",m,nodes); }
