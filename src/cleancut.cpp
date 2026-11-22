// CLEAN-CUT leaves.  In a growth labeling (labels 1..n), a leaf l with label L and edge length j is "clean" if the
// other edges that jump over L (one end < L, other end > L) are exactly the edges longer than j.
// Deleting a clean leaf and closing the gap at L gives a growth labeling of T - l.
// For every tree: (Q1) is some leaf clean in some growth labeling?  (Q2) is EVERY leaf clean in some growth labeling?
// Usage: cleancut n [v] < trees
#include <bits/stdc++.h>
using namespace std;
int n; vector<int> adj[40]; int lab[40]; bool used[41]; vector<int> leaves; unsigned long long okmask, want; long long budget;
void check(){
  for(size_t i=0;i<leaves.size();i++){ if(okmask>>i&1) continue; int l=leaves[i], L=lab[l], j=abs(L-lab[adj[l][0]]); bool ok=true;
    for(int u=0;u<n&&ok;u++) for(int w:adj[u]) if(u<w && u!=l && w!=l){ int a=min(lab[u],lab[w]), b=max(lab[u],lab[w]); bool cross=a<L&&L<b; if(cross!=(b-a>j)){ ok=false; break; } }
    if(ok) okmask|=1ull<<i; }
}
void dfs(int k){
  if(okmask==want||budget<0) return;
  if(k==0){ check(); return; } budget--;
  for(int u=0;u<n;u++) if(lab[u]){
    for(int s=-1;s<=1;s+=2){ int x=lab[u]+s*k; if(x<1||x>n||used[x]) continue;
      int prevdeg=-1;
      for(int w:adj[u]) if(!lab[w]){ if((int)adj[w].size()==1){ if(prevdeg==1) continue; prevdeg=1; }   // leaves at the same vertex are interchangeable... 
        lab[w]=x; used[x]=1; dfs(k-1); lab[w]=0; used[x]=0; if(okmask==want) return; } } }
}
int main(int argc,char**argv){ n=atoi(argv[1]); bool verbose=argc>2; string line; long trees=0,q1fail=0,q2fail=0,leafT=0,leafBad=0,cut=0;
  while(getline(cin,line)){ if(line.empty()) continue; istringstream is(line); for(int i=0;i<n;i++) adj[i].clear(); int u,v; while(is>>u>>v){ adj[u].push_back(v); adj[v].push_back(u);} 
    trees++; leaves.clear(); for(int i=0;i<n;i++) if(adj[i].size()==1) leaves.push_back(i);
    // one representative leaf per parent would suffice, but keep all: sibling leaves get identical answers only up to symmetry, so test all.
    want=(1ull<<leaves.size())-1; okmask=0; budget=200000000;
    for(int r=0;r<n&&okmask!=want;r++) for(int w:adj[r]){ memset(lab,0,sizeof lab); memset(used,0,sizeof used); lab[r]=1; lab[w]=n; used[1]=used[n]=1; dfs(n-2); if(okmask==want) break; }
    if(budget<0) cut++;
    // sibling leaves: if one sibling is ok, all are (symmetry)
    for(size_t i=0;i<leaves.size();i++) if(okmask>>i&1) for(size_t j=0;j<leaves.size();j++) if(adj[leaves[i]][0]==adj[leaves[j]][0]) okmask|=1ull<<j;
    int bad=0; for(size_t i=0;i<leaves.size();i++){ leafT++; if(!(okmask>>i&1)){ bad++; leafBad++; } }
    if(okmask==0) q1fail++; if(bad) { q2fail++; if(verbose) printf("Q2FAIL %s | bad leaves:%d of %zu\n",line.c_str(),bad,leaves.size()); }
  }
  printf("n=%d trees=%ld  no-clean-leaf-at-all=%ld  some-leaf-never-clean=%ld  (leaves %ld, never-clean %ld)  budget-cut=%ld\n",n,trees,q1fail,q2fail,leafT,leafBad,cut); }
