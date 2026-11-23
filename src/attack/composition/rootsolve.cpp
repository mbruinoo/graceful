// Reads rooted trees, one per line: "n p_1 ... p_{n-1}" (parent of vertex i, vertices 0..n-1, root 0, p_i < i).
// For each, searches for a growth placement with the root at label 0 (README Theorem 7: lengths n-1, n-2, ..., 1
// are given in turn to an unlabelled vertex whose parent is labelled).  Prints the trees with NO such placement
// (exhaustive backtracking, so "none" is a proof by search for that tree) and a summary on stderr.
// The answer found is re-verified from the definition before it is counted.
#include <bits/stdc++.h>
using namespace std;
int n, par_[64], lab[64]; bool usedlab[64], done_[64]; vector<int> ch[64]; long long nodes;
bool rec(int k, vector<int>& fr){
  if(k==0) return true;
  nodes++;
  for(size_t t=0;t<fr.size();t++){ int u=fr[t]; int p=par_[u];
    // identical leaf siblings: only try the first unlabelled leaf child of p
    bool skip=false; if(ch[u].empty()) for(size_t q=0;q<t;q++) if(par_[fr[q]]==p && ch[fr[q]].empty()){skip=true;break;}
    if(skip) continue;
    for(int sg=-1;sg<=1;sg+=2){ int L=lab[p]+sg*k; if(L<0||L>=n||usedlab[L]) continue;
      lab[u]=L; usedlab[L]=true; vector<int> f2; f2.reserve(fr.size()+ch[u].size());
      for(size_t q=0;q<fr.size();q++) if(q!=t) f2.push_back(fr[q]); for(int c:ch[u]) f2.push_back(c);
      if(rec(k-1,f2)) return true; usedlab[L]=false; } }
  return false;
}
bool verify(){ // from the definition: labels 0..n-1, lengths 1..n-1 once, brackets >= k connected for every k
  vector<pair<int,pair<int,int>>> e; set<int> L; for(int v=0;v<n;v++) L.insert(lab[v]); if((int)L.size()!=n||*L.begin()!=0||*L.rbegin()!=n-1) return false;
  for(int v=1;v<n;v++) e.push_back({abs(lab[v]-lab[par_[v]]),{lab[v],lab[par_[v]]}});
  sort(e.rbegin(),e.rend()); vector<bool> u(n,false);
  for(int i=0;i<n-1;i++){ if(e[i].first!=n-1-i) return false; int a=e[i].second.first,b=e[i].second.second;
    if(i==0){u[a]=u[b]=true;continue;} if(u[a]==u[b]) return false; u[a]=u[b]=true; }
  return lab[0]==0;
}
int main(){ long long tot=0,fail=0; string line;
  while(getline(cin,line)){ istringstream is(line); if(!(is>>n)) continue; for(int i=0;i<n;i++){ch[i].clear();usedlab[i]=false;}
    for(int i=1;i<n;i++){is>>par_[i]; ch[par_[i]].push_back(i);} lab[0]=0; usedlab[0]=true; vector<int> fr(ch[0].begin(),ch[0].end());
    tot++; bool ok=rec(n-1,fr); if(ok && !verify()){fprintf(stderr,"VERIFY ERROR\n");return 1;}
    if(!ok){fail++; printf("NO %s\n",line.c_str());} }
  fprintf(stderr,"rooted trees read: %lld, with no growth placement anchored at the root: %lld\n",tot,fail); }
