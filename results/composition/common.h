// Shared helpers for results/composition.  Labels are 0..m (m = n-1).  A placement is pos[k] (left foot of the
// bracket of length k), k = 1..m, packed 4 bits per bracket into a uint64 (n <= 14).
#pragma once
#include <bits/stdc++.h>
using namespace std;
typedef uint64_t P;
static inline P packp(const int*pos,int m){ P x=0; for(int k=1;k<=m;k++) x|=(P)pos[k]<<(4*(k-1)); return x; }
static inline void unpackp(P x,int m,int*pos){ for(int k=1;k<=m;k++) pos[k]=(x>>(4*(k-1)))&15; }

// Growth placement test straight from the definition (README section 2): taking brackets longest first, the top
// bracket is {0,m} and every later bracket has exactly one foot on a label already used.
// Fills par[label] (the used foot when the label was added; par[0] = -1, par[m] = 0) and plen[label] (length of that bracket).
static inline bool growth_info(const int*pos,int m,int*par,int*plen){
  if(m==0){ par[0]=-1; plen[0]=99; return true; }
  if(pos[m]!=0) return false;
  unsigned used=1u|(1u<<m); par[0]=-1; plen[0]=99; par[m]=0; plen[m]=m;
  for(int k=m-1;k>=1;k--){ int a=pos[k],b=a+k; if(a<0||b>m) return false; bool x=used>>a&1,y=used>>b&1; if(x==y) return false;
    if(x){ par[b]=a; plen[b]=k; } else { par[a]=b; plen[a]=k; } used|=(1u<<a)|(1u<<b); }
  return true; }
static inline bool is_growth(const int*pos,int m){ int par[16],plen[16]; return growth_info(pos,m,par,plen); }

// Canonical code of an unrooted tree: balanced-parenthesis bit string of the tree rooted at its centre.
struct Code { uint32_t bits; int len; };
static inline bool codeless(const Code&a,const Code&b){ return ((uint64_t)a.bits<<(32-a.len)) > ((uint64_t)b.bits<<(32-b.len)); }
static Code rcode(int v,int pa,const vector<int>*adj){ Code ch[16]; int c=0; for(int u:adj[v]) if(u!=pa) ch[c++]=rcode(u,v,adj);
  sort(ch,ch+c,codeless); Code r{1,1}; for(int i=0;i<c;i++){ r.bits=(r.bits<<ch[i].len)|ch[i].bits; r.len+=ch[i].len; } r.bits<<=1; r.len++; return r; }
static uint32_t canon_adj(int n,const vector<int>*adj){
  int deg[16]; char gone[16]={0}; vector<int> layer; int rem=n;
  for(int i=0;i<n;i++){ deg[i]=adj[i].size(); if(deg[i]<=1) layer.push_back(i); }
  while(rem>2){ vector<int> nx; for(int v:layer){ gone[v]=1; rem--; for(int u:adj[v]) if(!gone[u] && --deg[u]==1) nx.push_back(u);} layer=nx; }
  if(layer.size()==1) return rcode(layer[0],-1,adj).bits;
  uint32_t a=rcode(layer[0],-1,adj).bits,b=rcode(layer[1],-1,adj).bits; return max(a,b); }
static uint32_t canon_pos(const int*pos,int m){ vector<int> adj[16]; for(int k=1;k<=m;k++){ adj[pos[k]].push_back(pos[k]+k); adj[pos[k]+k].push_back(pos[k]); } return canon_adj(m+1,adj); }
static uint32_t rooted_pos(const int*pos,int m,int root){ vector<int> adj[16]; for(int k=1;k<=m;k++){ adj[pos[k]].push_back(pos[k]+k); adj[pos[k]+k].push_back(pos[k]); } return rcode(root,-1,adj).bits; }
// decode a parenthesis code (2n bits) into a parent array, vertex 0 = root
static void decode(uint32_t bits,int n,int*par){ int st[32],sp=0,id=0; for(int i=2*n-1;i>=0;i--){ if(bits>>i&1){ par[id]= sp?st[sp-1]:-1; st[sp++]=id++; } else sp--; } }
static string paren(uint32_t bits,int n){ string s; for(int i=2*n-1;i>=0;i--) s+= (bits>>i&1)?'(':')'; return s; }
// all trees on n vertices (canonical codes), by adding a leaf to every tree on n-1 vertices
static vector<set<uint32_t>> all_trees(int N){ vector<set<uint32_t>> T(N+1); T[1].insert(2);
  for(int n=1;n<N;n++) for(uint32_t c:T[n]){ int par[16]; decode(c,n,par);
    for(int v=0;v<n;v++){ vector<int> adj[16]; for(int i=1;i<n;i++){ adj[i].push_back(par[i]); adj[par[i]].push_back(i); } adj[v].push_back(n); adj[n].push_back(v); T[n+1].insert(canon_adj(n+1,adj)); } }
  return T; }
static bool is_caterpillar(uint32_t c,int n){ int par[16]; decode(c,n,par); int deg[16]={0}; for(int i=1;i<n;i++){ deg[i]++; deg[par[i]]++; }
  // caterpillar iff no vertex has 3 or more non-leaf neighbours
  int nl[16]={0}; for(int i=1;i<n;i++){ if(deg[i]>1) nl[par[i]]++; if(deg[par[i]]>1) nl[i]++; } for(int i=0;i<n;i++) if(nl[i]>=3) return false; return true; }
