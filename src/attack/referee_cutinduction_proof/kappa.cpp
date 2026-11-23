// Referee top-down step-number computation for one tree.
// Usage: kappa CAP  n  u1 v1 u2 v2 ...   (0-based edge list)   or   kappa CAP spider L1 L2 ...
// Enumerates every growth labeling of the tree, then
//   kappa(p) = min over clean sets R (|R|<=CAP, complement connected, >=2 labels left) of max(|R|, kappa(p\R)).
// Clean = conditions (1),(2) of claim 0; (1) is equivalent to "complement induces a connected subtree".
#include <bits/stdc++.h>
using namespace std;
int CAP;
unordered_map<string,int> memo;
int kappa(const string&p){ // p[k-1]=position of bracket k, n=p.size()+1
  int n=p.size()+1; if(n==2) return 0;
  auto it=memo.find(p); if(it!=memo.end()) return it->second;
  vector<vector<int>> adj(n+1);
  for(int k=1;k<n;k++){int a=p[k-1],b=a+k; adj[a].push_back(b); adj[b].push_back(a);}
  // root at 1, parent/children
  vector<int> par(n+1,0),order; order.push_back(1); par[1]=-1;
  for(size_t i=0;i<order.size();i++){int v=order[i]; for(int w:adj[v]) if(w!=par[v]){par[w]=v;order.push_back(w);}}
  int best=1000;
  // enumerate connected subsets S by top vertex t
  vector<char> inS(n+1,0);
  function<void(vector<int>&,size_t,int)> go=[&](vector<int>&cand,size_t i,int sz){
    // prune: |R| = n-sz must be able to reach <=CAP and <best: max possible final size = sz + (subtree stuff) -- skip pruning except trivial
    if(i==cand.size()){
      int r=n-sz; if(sz<2||r<1||r>CAP||r>=best) return;
      // check (2), build q
      int rb=0; string q; vector<int> nl(n+1); int c=0; for(int x=1;x<=n;x++){ if(inS[x])c++; nl[x]=c; }
      for(int k=1;k<n;k++){int a=p[k-1],b=a+k; if(!inS[a]||!inS[b]){rb++;continue;}
        int inside=(b-a-1)-(nl[b-1]-nl[a]); if(inside!=rb) return; q.push_back((char)nl[a]); }
      if(rb!=r){fprintf(stderr,"count mismatch\n");exit(1);}
      int v=max(r,kappa(q)); if(v<best) best=v; return; }
    int c=cand[i];
    go(cand,i+1,sz); // exclude c
    inS[c]=1; size_t old=cand.size(); for(int w:adj[c]) if(w!=par[c]) cand.push_back(w);
    go(cand,i+1,sz+1); cand.resize(old); inS[c]=0;
  };
  for(int t=1;t<=n;t++){ vector<int> cand; inS[t]=1; for(int w:adj[t]) if(w!=par[t]) cand.push_back(w); go(cand,0,1); inS[t]=0; }
  memo[p]=best; return best;
}
long long withCleanLeaf=0;
bool hasCleanLeaf(const string&p){ int n=p.size()+1; vector<int> deg(n+2,0); for(int k=1;k<n;k++){deg[p[k-1]]++;deg[p[k-1]+k]++;}
  for(int L=1;L<=n;L++) if(deg[L]==1){ int j=0; for(int k=1;k<n;k++) if(p[k-1]==L||p[k-1]+k==L) j=k; bool ok=true;
    for(int k=1;k<n&&ok;k++) if(k!=j){ bool jumps=p[k-1]<L&&L<p[k-1]+k; if(jumps!=(k>j)) ok=false; } if(ok) return true; } return false; }
int N; vector<vector<int>> A; vector<int> lab; vector<char> usedl; long long nlab; map<int,long long> dist; set<string> pls; string cur;
void grow(int k){
  if(k==0){ nlab++; if(pls.insert(cur).second){} dist[kappa(cur)]++; withCleanLeaf+=hasCleanLeaf(cur); return; }
  for(int u=0;u<N;u++) if(lab[u]) for(int v:A[u]) if(!lab[v]) for(int s=-1;s<=1;s+=2){
    int l=lab[u]+s*k; if(l<1||l>N||usedl[l]) continue;
    lab[v]=l; usedl[l]=1; cur[k-1]=(char)min(l,lab[u]); grow(k-1); lab[v]=0; usedl[l]=0; }
}
int main(int argc,char**argv){
  CAP=atoi(argv[1]); vector<pair<int,int>> E;
  if(string(argv[2])=="spider"){ N=1; for(int i=3;i<argc;i++){int L=atoi(argv[i]); int prev=0; for(int j=0;j<L;j++){E.push_back({prev,N}); prev=N++;}} }
  else { N=atoi(argv[2]); for(int i=3;i+1<argc;i+=2) E.push_back({atoi(argv[i]),atoi(argv[i+1])}); }
  if((int)E.size()!=N-1){fprintf(stderr,"bad edge count\n");return 1;}
  A.assign(N,{}); for(auto&e:E){A[e.first].push_back(e.second);A[e.second].push_back(e.first);}
  lab.assign(N,0); usedl.assign(N+2,0); cur.assign(N-1,0);
  for(int u=0;u<N;u++) for(int v:A[u]){ lab[u]=1; lab[v]=N; usedl[1]=usedl[N]=1; cur[N-2]=1; grow(N-2); lab[u]=lab[v]=0; usedl[1]=usedl[N]=0; }
  printf("n=%d labelings=%lld placements=%zu  kappa distribution over labelings (1000 = not reducible with |R|<=%d):",N,nlab,pls.size(),CAP);
  for(auto&d:dist) printf(" %d:%lld",d.first,d.second); printf("\n  memo size %zu; labelings with a clean leaf: %lld\n",memo.size(),withCleanLeaf);
}
