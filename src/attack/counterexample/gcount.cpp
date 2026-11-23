// Exact number of growth placements of one tree (README sections 1-2), by exhaustive search with
// symmetry pruning.  A growth placement is a set of brackets, i.e. a labeling up to tree automorphism.
// Input: one tree per line: "n  u v  u v ..." (vertices 0..n-1).  Output: count, search nodes.
// Options (env): LIMIT=<nodes> give up after that many nodes (prints ">=count UNFINISHED");
//                FIRST=1 stop at the first placement and print it (exhaustive decision).
// Symmetry: root the tree at its centre.  Among children of one vertex with isomorphic subtrees, the
// edges to the parent must be placed in index order (longest first).  Exactly one labeling in each
// orbit of the centre-fixing automorphism group satisfies this.  If the tree is bicentral with two
// isomorphic halves the remaining swap acts freely, so the count is halved.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned __int128 u128;
int n; vector<int> adj[128]; int par[128], prevSib[128]; int lab[128]; bool edgeDone[128]; // edgeDone[v]: edge v-par[v] placed
u128 usedm; long long cnt, nodes, LIMIT=0; bool FIRST=false, stopped=false; int openCnt[128];
map<string,int> ids; int shape[128];
int enc(int v,int p){ par[v]=p; vector<pair<int,int>> ch; for(int u:adj[v]) if(u!=p) ch.push_back({enc(u,v),u}); sort(ch.begin(),ch.end());
  string s="("; for(auto&c:ch) s+=to_string(c.first)+","; s+=")"; auto it=ids.find(s); int id; if(it==ids.end()){ id=ids.size(); ids[s]=id; } else id=it->second; shape[v]=id;
  for(size_t i=0;i<ch.size();i++) prevSib[ch[i].second]=(i>0&&ch[i-1].first==ch[i].first)?ch[i-1].second:-1;
  return id; }
int best[128];
void dfs(int k){
  if(stopped) return;
  if(k==0){ cnt++; if(FIRST){ stopped=true; memcpy(best,lab,sizeof lab);} return; }
  nodes++; if(LIMIT && nodes>LIMIT){ stopped=true; return; }
  for(int u=0;u<n;u++) if(lab[u] && openCnt[u]){
    for(int s=-1;s<=1;s+=2){ int x=lab[u]+s*k; if(x<1||x>n||(usedm>>x&1)) continue;
      for(int w:adj[u]) if(!lab[w]){
        int c = (par[w]==u)? w : u;            // child end of this edge
        if(prevSib[c]>=0 && !edgeDone[prevSib[c]]) continue;
        lab[w]=x; usedm|=(u128)1<<x; edgeDone[c]=true; openCnt[u]--; openCnt[w]=adj[w].size()-1;
        dfs(k-1);
        lab[w]=0; usedm&=~((u128)1<<x); edgeDone[c]=false; openCnt[u]++; openCnt[w]=0;
        if(stopped) return; } } }
}
int main(){ if(getenv("LIMIT")) LIMIT=atoll(getenv("LIMIT")); if(getenv("FIRST")) FIRST=true; string line;
  while(getline(cin,line)){ if(line.empty()) continue; istringstream is(line); is>>n; for(int i=0;i<n;i++) adj[i].clear(); int u,v; int m=0; while(is>>u>>v){ adj[u].push_back(v); adj[v].push_back(u); m++; }
    if(m!=n-1){ printf("bad tree\n"); continue; }
    // centre
    vector<int> deg(n), layer; vector<char> gone(n,0); int rem=n; for(int i=0;i<n;i++){ deg[i]=adj[i].size(); if(deg[i]<=1) layer.push_back(i); }
    while(rem>2){ vector<int> nx; for(int x:layer){ gone[x]=1; rem--; for(int y:adj[x]) if(!gone[y] && --deg[y]==1) nx.push_back(y);} layer=nx; }
    int div=1; ids.clear(); memset(prevSib,-1,sizeof prevSib);
    if(layer.size()==2 && n>2){ int a=layer[0], b=layer[1]; int ia=enc(a,b); ids.clear(); /* compare halves */
      // compute shapes of the two halves with a shared id table
      ids.clear(); int sa=enc(a,b); int sb=enc(b,a); if(sa==sb) div=2;
      ids.clear(); memset(prevSib,-1,sizeof prevSib); enc(a,-1); (void)ia; }
    else enc(layer[0],-1);
    cnt=0; nodes=0; stopped=false;
    for(int r=0;r<n&&!stopped;r++) for(int w:adj[r]){ int c=(par[w]==r)?w:r; if(prevSib[c]>=0) continue;
      memset(lab,0,sizeof lab); memset(edgeDone,0,sizeof edgeDone); memset(openCnt,0,sizeof openCnt);
      lab[r]=1; lab[w]=n; usedm=((u128)1<<1)|((u128)1<<n); edgeDone[c]=true; openCnt[r]=adj[r].size()-1; openCnt[w]=adj[w].size()-1; dfs(n-2); if(stopped) break; }
    if(FIRST){ if(cnt){ printf("n=%d FOUND nodes=%lld labels:",n,nodes); for(int i=0;i<n;i++) printf(" %d",best[i]); printf("\n"); } else printf("n=%d %s nodes=%lld\n",n,(LIMIT&&nodes>LIMIT)?"UNFINISHED":"NONE",nodes); }
    else if(stopped) printf("n=%d count>=%lld UNFINISHED nodes=%lld\n",n,cnt/div,nodes);
    else { if(cnt%div) printf("ERROR odd\n"); printf("n=%d count=%lld nodes=%lld\n",n,cnt/div,nodes); }
    fflush(stdout); } }
