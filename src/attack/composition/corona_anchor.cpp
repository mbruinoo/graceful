// For s given: enumerate ALL growth placements on 2s labels 0..2s-1 (root = label 0), keep those whose tree is a
// corona S (.) K_1 (every non-leaf vertex has exactly one leaf neighbour, s leaves) with label 0 on a core vertex,
// and print the set of rooted canonical strings (AHU) of the core S rooted at label 0.
// So the output is exactly the set of rooted trees (S,v), |S| = s, such that v is an anchor of the corona of S.
#include <bits/stdc++.h>
using namespace std;
int N; int par_[40]; bool used_[40]; set<string> out; long long cnt=0, cor=0;
vector<int> ch[40];
string canon(int u){ vector<string> v; for(int c:ch[u]) v.push_back(canon(c)); sort(v.begin(),v.end()); string s="("; for(auto&x:v) s+=x; return s+")"; }
void leaf(){
  cnt++; int n=N+1; int deg[40]={0};
  for(int v=1;v<n;v++){deg[v]++;deg[par_[v]]++;}
  if(deg[0]==1) return;
  int leafn[40]={0}; int L=0;
  for(int v=1;v<n;v++) if(deg[v]==1){L++; leafn[par_[v]]++;}
  if(2*L!=n) return;
  for(int v=0;v<n;v++) if(deg[v]>1 && leafn[v]!=1) return;
  cor++;
  for(int v=0;v<n;v++) ch[v].clear();
  for(int v=1;v<n;v++) if(deg[v]>1) ch[par_[v]].push_back(v);
  out.insert(canon(0));
}
void rec(int k){
  if(k==0){leaf();return;}
  for(int a=0;a+k<=N;a++){ int b=a+k; if(used_[a]!=used_[b]){ int nw=used_[a]?b:a, ol=used_[a]?a:b;
      par_[nw]=ol; used_[nw]=true; rec(k-1); used_[nw]=false; } }
}
int main(int argc,char**argv){ int s=atoi(argv[1]); N=2*s-1; used_[0]=used_[N]=true; par_[N]=0; rec(N-1);
  fprintf(stderr,"s=%d: %lld growth placements on %d labels, %lld are coronas, %zu rooted cores\n",s,cnt,N+1,cor,out.size());
  for(auto&x:out) printf("%s\n",x.c_str()); }
