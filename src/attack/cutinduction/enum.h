// Shared helpers.  Everything is computed from the definitions of README section 1:
// a placement on n vertices is pos[k] (k=1..n-1), bracket k is the edge {pos[k], pos[k]+k}, labels 1..n.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
struct Pl { int n; int pos[20]; };                 // pos[1..n-1]
static inline u64 enc(const Pl&p){ u64 x=0; for(int k=1;k<p.n;k++) x|=(u64)p.pos[k]<<(4*(k-1)); return x; }   // n<=16
static inline Pl dec(u64 x,int n){ Pl p; p.n=n; for(int k=1;k<n;k++) p.pos[k]=(x>>(4*(k-1)))&15; return p; }
// growth placement, by definition: brackets n-1,...,k form a connected tree for every k
// <=> taken longest first each bracket has exactly one foot on a label already used.
static inline bool isGrowth(const Pl&p){ int n=p.n; if(n<2) return false; unsigned used=0;
  for(int k=n-1;k>=1;k--){ int a=p.pos[k], b=a+k; if(a<1||b>n) return false;
    if(k==n-1){ used=(1u<<a)|(1u<<b); continue; }
    bool ua=used>>a&1, ub=used>>b&1; if(ua==ub) return false; used|=(1u<<a)|(1u<<b); }
  return true; }
// canonical form of the tree drawn by a tree placement (AHU, rooted at centre(s))
static string ahu(int v,int par,const vector<vector<int>>&adj){ vector<string> c; for(int w:adj[v]) if(w!=par) c.push_back(ahu(w,v,adj)); sort(c.begin(),c.end()); string s="("; for(auto&x:c) s+=x; return s+")"; }
static string canonAdj(const vector<vector<int>>&adj,int n){   // vertices 1..n
  vector<int> deg(n+1),lay; vector<char> rem(n+1,0); int left=n; for(int v=1;v<=n;v++){ deg[v]=adj[v].size(); if(deg[v]<=1) lay.push_back(v); }
  while(left>2){ vector<int> nx; for(int v:lay){ rem[v]=1; left--; for(int w:adj[v]) if(!rem[w]&&--deg[w]==1) nx.push_back(w); } lay=nx; }
  vector<int> cen; for(int v=1;v<=n;v++) if(!rem[v]) cen.push_back(v);
  if(cen.size()==1) return ahu(cen[0],0,adj);
  string a=ahu(cen[0],cen[1],adj), b=ahu(cen[1],cen[0],adj); if(a>b) swap(a,b); return "["+a+b+"]"; }
static inline vector<vector<int>> adjOf(const Pl&p){ vector<vector<int>> adj(p.n+1); for(int k=1;k<p.n;k++){ int a=p.pos[k], b=a+k; adj[a].push_back(b); adj[b].push_back(a);} return adj; }
static inline string canon(const Pl&p){ return canonAdj(adjOf(p),p.n); }
// cut i (0<=i<=n) lies between labels i and i+1.  crossing = brackets with pos<=i<pos+k.
// returns c>=0 if the crossing brackets are exactly the c longest, else -1.
static inline int cutHeight(const Pl&p,int i){ int n=p.n,c=0; bool seenNon=false;
  for(int k=n-1;k>=1;k--){ bool cr=p.pos[k]<=i && i<p.pos[k]+k; if(cr){ if(seenNon) return -1; c++; } else seenNon=true; }
  return c; }
// open a gap at cut i (new label L=i+1), hang the new leaf at L by a bracket to L+dir*j, where j is the unique free length.
// returns false unless the result is a placement (all lengths distinct) AND a growth placement (checked by definition).
static inline bool insertLeaf(const Pl&p,int i,int dir,Pl&q){ int n=p.n; q.n=n+1; bool have[20]={0};
  for(int k=1;k<n;k++){ int a=p.pos[k], b=a+k; if(a>i) a++; if(b>i) b++; int len=b-a; if(have[len]) return false; have[len]=1; q.pos[len]=a; }
  int j=0; for(int k=1;k<=n;k++) if(!have[k]){ if(j) return false; j=k; }
  int L=i+1, u=L+dir*j; if(u<1||u>n+1) return false; q.pos[j]=min(L,u);
  return isGrowth(q); }
// enumerate all growth placements on n vertices
template<class F> static void enumGrowth(int n,F f){ Pl p; p.n=n; p.pos[n-1]=1; unsigned used=(1u<<1)|(1u<<n);
  function<void(int,unsigned)> rec=[&](int k,unsigned used){ if(k==0){ f(p); return; }
    for(int a=1;a+k<=n;a++){ bool ua=used>>a&1, ub=used>>(a+k)&1; if(ua!=ub){ p.pos[k]=a; rec(k-1,used|(1u<<a)|(1u<<(a+k))); } } };
  if(n==2){ f(p); return; } rec(n-2,used); }
