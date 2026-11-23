// Decide, for each tree on stdin ("n u v u v ..."), whether it has a growth placement.
// Randomised DFS with restarts (limits L, 3L, ...), then, if still unresolved, one ORDERED exhaustive
// DFS with node limit XLIM (0 = unlimited).  Same symmetry rule as gcount.cpp (isomorphic sibling
// branches, seen from the centre, receive their parent edges in index order).
// Every placement found is re-checked from the definition (README section 1-2): labels are 1..n once
// each, lengths are 1..n-1 once each, and for every k the brackets of length >= k are connected.
// env ROOT0=1: only placements with vertex 0 labelled 1 (is vertex 0 an anchor?).
// usage: gsolve [L=2000] [rounds=10] [XLIM=0]     env SHOW=1 prints labels;  QUIET=1 prints only non-FOUND
#include <bits/stdc++.h>
using namespace std;
typedef unsigned __int128 u128;
int n; vector<int> adj[128]; int par[128], prevSib[128]; int lab[128]; bool edgeDone[128]; int openCnt[128];
u128 usedm; long long nodes, limit_; mt19937 rng(2026); bool RANDOM=true, ROOT0=false;  // ROOT0: vertex 0 must carry label 1 (anchor test)
map<string,int> ids;
int enc(int v,int p){ par[v]=p; vector<pair<int,int>> ch; for(int u:adj[v]) if(u!=p) ch.push_back({enc(u,v),u}); sort(ch.begin(),ch.end());
  string s="("; for(auto&c:ch) s+=to_string(c.first)+","; s+=")"; auto it=ids.find(s); int id; if(it==ids.end()){ id=ids.size(); ids[s]=id; } else id=it->second;
  for(size_t i=0;i<ch.size();i++) prevSib[ch[i].second]=(i>0&&ch[i-1].first==ch[i].first)?ch[i-1].second:-1;
  return id; }
int dfs(int k){
  if(k==0) return 1; if(limit_ && ++nodes>limit_) return -1;
  int cu[512], cw[512], cx[512], c=0;
  for(int u=0;u<n;u++) if(lab[u] && openCnt[u]){
    for(int s=-1;s<=1;s+=2){ int x=lab[u]+s*k; if(x<1||x>n||(usedm>>x&1)) continue;
      for(int w:adj[u]) if(!lab[w]){ int ce=(par[w]==u)?w:u; if(prevSib[ce]>=0 && !edgeDone[prevSib[ce]]) continue; cu[c]=u; cw[c]=w; cx[c]=x; c++; } } }
  if(RANDOM) for(int i=c-1;i>0;i--){ int j=rng()%(i+1); swap(cu[i],cu[j]); swap(cw[i],cw[j]); swap(cx[i],cx[j]); }
  for(int i=0;i<c;i++){ int u=cu[i], w=cw[i], x=cx[i]; int ce=(par[w]==u)?w:u;
    lab[w]=x; usedm|=(u128)1<<x; edgeDone[ce]=true; openCnt[u]--; openCnt[w]=adj[w].size()-1;
    int r=dfs(k-1); if(r==1) return 1;
    lab[w]=0; usedm&=~((u128)1<<x); edgeDone[ce]=false; openCnt[u]++; openCnt[w]=0; if(r<0) return -1; }
  return 0; }
int solve(long long lim){ limit_=lim; vector<pair<int,int>> es; for(int u=0;u<n;u++) for(int w:adj[u]){ int ce=(par[w]==u)?w:u; if(prevSib[ce]<0) es.push_back({u,w}); }
  if(ROOT0){ vector<pair<int,int>> f; for(auto e:es) if(e.first==0) f.push_back(e); es=f; }
  if(RANDOM) shuffle(es.begin(),es.end(),rng); bool hit=false;
  for(auto e:es){ memset(lab,0,sizeof lab); memset(edgeDone,0,sizeof edgeDone); memset(openCnt,0,sizeof openCnt); int ce=(par[e.second]==e.first)?e.second:e.first;
    lab[e.first]=1; lab[e.second]=n; usedm=((u128)1<<1)|((u128)1<<n); edgeDone[ce]=true; openCnt[e.first]=adj[e.first].size()-1; openCnt[e.second]=adj[e.second].size()-1; nodes=0;
    int r=dfs(n-2); if(r==1) return 1; if(r<0) hit=true; }
  return hit?-1:0; }
bool verify(){ vector<int> seenL(n+1,0), len(n,0); for(int i=0;i<n;i++){ if(lab[i]<1||lab[i]>n||seenL[lab[i]]) return false; seenL[lab[i]]=1; }
  vector<pair<int,pair<int,int>>> E; for(int u=0;u<n;u++) for(int w:adj[u]) if(u<w){ int d=abs(lab[u]-lab[w]); if(d<1||d>n-1||len[d]) return false; len[d]=1; E.push_back({d,{u,w}}); }
  if((int)E.size()!=n-1) return false; sort(E.rbegin(),E.rend()); vector<char> in(n,0); in[E[0].second.first]=in[E[0].second.second]=1;
  for(int i=1;i<n-1;i++){ int a=E[i].second.first,b=E[i].second.second; if(in[a]==in[b]) return false; in[a]=in[b]=1; } return true; }
int main(int argc,char**argv){ long long L=argc>1?atoll(argv[1]):2000; int rounds=argc>2?atoi(argv[2]):10; long long XLIM=argc>3?atoll(argv[3]):0; bool SHOW=getenv("SHOW"), QUIET=getenv("QUIET"); ROOT0=getenv("ROOT0");
  string line; long long total=0,found=0,none=0,unres=0;
  while(getline(cin,line)){ if(line.empty()) continue; istringstream is(line); is>>n; for(int i=0;i<n;i++) adj[i].clear(); int u,v; while(is>>u>>v){ adj[u].push_back(v); adj[v].push_back(u); }
    vector<int> deg(n), layer; vector<char> gone(n,0); int rem=n; for(int i=0;i<n;i++){ deg[i]=adj[i].size(); if(deg[i]<=1) layer.push_back(i); }
    while(rem>2){ vector<int> nx; for(int x:layer){ gone[x]=1; rem--; for(int y:adj[x]) if(!gone[y] && --deg[y]==1) nx.push_back(y);} layer=nx; }
    ids.clear(); memset(prevSib,-1,sizeof prevSib); enc(ROOT0?0:layer[0],-1);   /* with a fixed anchor the symmetries are those fixing vertex 0 */
    total++; int r=-1; long long lim=L; RANDOM=true; for(int a=0;a<rounds&&r<0;a++){ r=solve(lim); lim*=3; }
    if(r<0){ RANDOM=false; r=solve(XLIM); }
    if(r==1){ if(!verify() || (ROOT0 && lab[0]!=1)){ printf("VERIFY-FAILED: %s\n",line.c_str()); return 1; } found++; if(!QUIET){ printf("FOUND n=%d",n); if(SHOW){ printf(" labels:"); for(int i=0;i<n;i++) printf(" %d",lab[i]); } printf("\n"); } }
    else if(r==0){ none++; printf("NONE: %s\n",line.c_str()); } else { unres++; printf("UNRESOLVED: %s\n",line.c_str()); }
    fflush(stdout); }
  printf("trees=%lld found=%lld none=%lld unresolved=%lld\n",total,found,none,unres); }
