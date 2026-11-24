// ascan2.cpp -- as ascan.cpp (same search, same certificate check), but with a degree window and a
// "no leaf neighbour" filter, and without the maximum-degree pass.  Second mode: explicit queries from stdin.
// Usage: ascan2 n part parts dmin dmax noleaf capmax   tests every vertex v with dmin <= deg(v) <= dmax and
//          (if noleaf=1) no leaf neighbour, one per automorphism orbit.  Lines NOT/CAP as ascan, and SUMMARY.
//        ascan2 q capmax < queries     query lines "n v u1 w1 u2 w2 ..." (as anchq); prints ANCHOR/NOT/CAP + the line.
// (original header of ascan.cpp follows)
// ascan.cpp -- anchor scan over all free trees on n vertices (trees from ../../treegen.h).
// A vertex v is an ANCHOR if there is a growth placement with v at the smallest label (README sections 1,2,7):
// labels 0..n-1 bijective, v=0, and for k=n-1..1 the bracket of length k joins an already labelled vertex u
// to a not yet labelled neighbour w with label lab[u]+-k.  Search: longest first, complete unless the node cap is hit.
// Reductions (both exact): (i) vertices in the same Aut(T)-orbit are tested once (exact canonical ids, no hashing);
// (ii) among unlabelled children of u with isomorphic subtrees only the first is tried.
// Pruning (necessary conditions only): every remaining length j<=k needs a free label at distance j from a label
// that is open (labelled vertex with unlabelled children) or free; every free label needs such a partner.
// Usage: ascan n part parts mindeg capmax
//   tests every vertex of degree >= mindeg.  Lines:  NOT/CAP n deg | edges | v=..   and a SUMMARY line.
//   Also for every tree: is some vertex of maximum degree an anchor?  (max-degree vertices are tested even if
//   below mindeg, stopping at the first anchor.)  Line NOMAXDEG / MAXDEGCAP if not established.
#include <bits/stdc++.h>
#include "../../treegen.h"
using namespace std;
typedef unsigned int u32;
int n; vector<int> adj[32];
// canonical ids (exact): signature = sorted child ids
struct Sig { int c; int a[30]; };
vector<Sig> table_;
int intern(Sig&s){ sort(s.a,s.a+s.c); for(size_t i=0;i<table_.size();i++){ if(table_[i].c==s.c && !memcmp(table_[i].a,s.a,sizeof(int)*s.c)) return i; } table_.push_back(s); return table_.size()-1; }
int cls[32], par_[32]; int chs[32][32], nch[32];   // children sorted by class
int ordv[32];
int rootAt(int v){ // BFS order, then bottom-up ids
  int h=0,t=0; ordv[t++]=v; par_[v]=-1;
  while(h<t){ int u=ordv[h++]; nch[u]=0; for(int w:adj[u]) if(w!=par_[u]){ par_[w]=u; chs[u][nch[u]++]=w; ordv[t++]=w; } }
  for(int i=n-1;i>=0;i--){ int u=ordv[i]; Sig s; s.c=nch[u]; for(int j=0;j<nch[u];j++) s.a[j]=cls[chs[u][j]]; cls[u]=intern(s);
    sort(chs[u],chs[u]+nch[u],[](int a,int b){return cls[a]<cls[b];}); }
  return cls[v]; }
int lab[32]; u32 U,O,FULL; int vat[32]; // vertex at label
int done_[32]; // number of labelled children
long long nodes, cap_; bool capped; int order_=0;
// Independent certificate check, run on every labelling the search accepts: labels a bijection onto 0..n-1,
// root at 0, edge lengths (child to parent) exactly 1..n-1, strictly decreasing away from the root (Theorem 7).
int rootv_; long long verified_=0;
bool verify(){ u32 Ls=0, Ws=0; if(lab[rootv_]!=0) return false;
  for(int v=0;v<n;v++){ if(lab[v]<0||lab[v]>=n) return false; Ls|=1u<<lab[v];
    if(v!=rootv_){ int w=abs(lab[v]-lab[par_[v]]); if(w<1||w>n-1) return false; Ws|=1u<<w;
      int p=par_[v]; if(p!=rootv_ && w>=abs(lab[p]-lab[par_[p]])) return false; } }
  return Ls==FULL && Ws==(FULL&~1u); }
bool dfs(int k){
  if(k==0){ if(!verify()){ printf("VERIFYFAIL\n"); fflush(stdout); abort(); } verified_++; return true; }
  if(++nodes>cap_){ capped=true; return false; }
  u32 F=FULL&~U, A=O|F, cover=0;
  { u32 c=((O<<k)|(O>>k))&F; if(!c) return false; }
  for(int j=1;j<k;j++){ u32 c=((A<<j)|(A>>j))&F; if(!c) return false; cover|=c; }
  cover|=((O<<k)|(O>>k))&F;
  if(cover!=F) return false;
  u32 Oc=O;
  while(Oc){ int a; if(order_&1){ a=31-__builtin_clz(Oc); } else a=__builtin_ctz(Oc); Oc&=~(1u<<a); int u=vat[a];
    for(int si=0;si<2;si++){ int s=((si^(order_>>1))&1)?1:-1; int x=a+s*k; if(x<0||x>=n||((U>>x)&1)) continue; int prev=-1;
      for(int i=0;i<nch[u];i++){ int w=chs[u][i]; if(lab[w]>=0) continue; if(cls[w]==prev) continue; prev=cls[w];
        lab[w]=x; vat[x]=w; U|=1u<<x; if(nch[w]) O|=1u<<x; done_[u]++; bool closed=(done_[u]==nch[u]); if(closed) O&=~(1u<<a);
        bool ok=dfs(k-1);
        if(closed) O|=1u<<a; done_[u]--; O&=~(1u<<x); U&=~(1u<<x); lab[w]=-1;
        if(ok) return true; if(capped) return false; } } }
  return false; }
long long rounds_[8]; 
int anchor1(int v){ for(int i=0;i<n;i++){ lab[i]=-1; done_[i]=0; } lab[v]=0; vat[0]=v; rootv_=v; U=1; O=1; FULL=(1u<<n)-1; capped=false;
  long long save=nodes; nodes=0; bool ok=dfs(n-1); nodes+=save; if(ok) return 1; return capped?-1:0; }
// escalation: caps 20k, 200k, 2M, ... up to the command-line cap, each with the four branching orders.
// Any single run that ends without hitting its cap is a complete search, so NOT is exact.
long long CAPMAX;
int anchor(int v){ int lvl=0; for(long long c=20000;;c*=10,lvl++){ if(c>CAPMAX) c=CAPMAX; for(int o=0;o<4;o++){ order_=o; cap_=c; int r=anchor1(v); if(r>=0){ rounds_[min(lvl,7)]++; return r; } } if(c>=CAPMAX) return -1; } }
int main(int argc,char**argv){
  if(argv[1][0]=='q'){ CAPMAX=atoll(argv[2]); string line; long na=0,nn=0,nc=0;
    while(getline(cin,line)){ if(line.empty()) continue; istringstream is(line); int v; is>>n>>v; for(int i=0;i<n;i++) adj[i].clear(); int a,b; while(is>>a>>b){ adj[a].push_back(b); adj[b].push_back(a);} 
      table_.clear(); rootAt(v); long long before=nodes; int r=anchor(v); (r==1?na:r==0?nn:nc)++;
      printf("%s deg%d nodes=%lld | %s\n",r==1?"ANCHOR":r==0?"NOT":"CAP",(int)adj[v].size(),nodes-before,line.c_str()); fflush(stdout); }
    printf("QSUMMARY anchors=%ld NOT=%ld CAP=%ld witnesses verified: %lld\n",na,nn,nc,verified_); return 0; }
  n=atoi(argv[1]); int part=atoi(argv[2]), parts=atoi(argv[3]), dmin=atoi(argv[4]), dmax=atoi(argv[5]), noleaf=atoi(argv[6]); CAPMAX=atoll(argv[7]);
  TreeGen g(n); vector<int> par; long idx=0,trees=0,tests=0,nA=0,nNot=0,nCap=0; map<int,long> notDeg;
  while(g.next()){ if((idx++)%parts!=part) continue; g.parents(par); for(int i=0;i<n;i++) adj[i].clear(); for(int i=1;i<n;i++){ adj[i].push_back(par[i]); adj[par[i]].push_back(i);} trees++;
    table_.clear(); int seenId[32], ns=0;
    for(int v=0;v<n;v++){ int d=adj[v].size(); if(d<dmin||d>dmax) continue;
      if(noleaf){ bool hasleaf=false; for(int w:adj[v]) if(adj[w].size()==1) hasleaf=true; if(hasleaf) continue; }
      int id=rootAt(v); bool seen=false; for(int i=0;i<ns;i++) if(seenId[i]==id){ seen=true; break; }
      if(seen) continue; seenId[ns++]=id; int r=anchor(v); tests++;
      if(r==1) nA++; else { if(r==0){ nNot++; notDeg[d]++; } else nCap++;
        printf("%s %d deg%d |",r==0?"NOT":"CAP",n,d); for(int i=1;i<n;i++) printf(" %d-%d",par[i],i); printf(" | v=%d\n",v); fflush(stdout); } } }
  printf("SUMMARY2 n=%d part=%d/%d dmin=%d dmax=%d noleaf=%d capmax=%lld trees=%ld orbitsTested=%ld anchors=%ld NOT=%ld CAP=%ld nodes=%lld | NOT kinds by degree:",n,part,parts,dmin,dmax,noleaf,CAPMAX,trees,tests,nA,nNot,nCap,nodes);
  for(auto&p:notDeg) printf(" d%d:%ld",p.first,p.second); printf(" | resolved at escalation level:"); for(int i=0;i<8;i++) printf(" %lld",rounds_[i]); printf(" | witnesses verified: %lld\n",verified_); }
