// Referee side checks (all growth placements, n<=NMAX<=13):
//  (a) number of growth placements with no clean leaf ("primitive")
//  (b) the NON-order-preserving variant of C(2): p is marked if deleting some 1 or 2 labels (and the brackets at them)
//      leaves a marked growth placement, with no condition on length order.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int n; int p[20];
vector<unordered_map<u64,unsigned char>> mk(20);   // growth placement -> marked?
static u64 key(const int*q,int m){u64 k=0;for(int i=1;i<m;i++)k=k*16+q[i];return k;}
string canon_rooted(int v,int par,vector<vector<int>>&adj){ vector<string> ch; for(int w:adj[v]) if(w!=par) ch.push_back(canon_rooted(w,v,adj)); sort(ch.begin(),ch.end()); string s="("; for(auto&c:ch)s+=c; return s+")"; }
string canon(const int*q,int m){
  vector<vector<int>> adj(m+1); for(int k=1;k<m;k++){adj[q[k]].push_back(q[k]+k);adj[q[k]+k].push_back(q[k]);}
  vector<int> deg(m+1),lv; int rem=m; vector<char> gone(m+1,0);
  for(int v=1;v<=m;v++){deg[v]=adj[v].size(); if(deg[v]<=1)lv.push_back(v);}
  while(rem>2){vector<int> nl; for(int v:lv){gone[v]=1;rem--; for(int w:adj[v]) if(!gone[w]&&--deg[w]==1) nl.push_back(w);} lv=nl;}
  vector<int> c; for(int v=1;v<=m;v++) if(!gone[v]) c.push_back(v);
  if(c.size()==1) return canon_rooted(c[0],0,adj);
  string a=canon_rooted(c[0],c[1],adj), b=canon_rooted(c[1],c[0],adj); if(a>b)swap(a,b); return a+b; }
long long cntp,prim,marked; set<string> shapes,msh;
void leaf(){
  cntp++; int deg[20]={0}; for(int k=1;k<n;k++){deg[p[k]]++;deg[p[k]+k]++;}
  bool anyclean=false;
  for(int L=1;L<=n&&!anyclean;L++) if(deg[L]==1){ int j=0; for(int k=1;k<n;k++) if(p[k]==L||p[k]+k==L) j=k;
    bool ok=true; for(int k=1;k<n&&ok;k++) if(k!=j){ bool jumps=p[k]<L&&L<p[k]+k; if(jumps!=(k>j)) ok=false; } anyclean=ok; }
  if(!anyclean) prim++;
  bool m=false;
  for(int a=1;a<=n&&!m;a++) for(int b=a;b<=n&&!m;b++){ // R={a} if a==b else {a,b}
    int sz=(a==b)?1:2; if(n-sz<2) continue; unsigned mask=1u<<a|1u<<b;
    int newlab[20],c=0; for(int x=1;x<=n;x++){ if(!(mask>>x&1))c++; newlab[x]=c; }
    int mm=n-sz; int q[20]={0}; int kept=0; bool ok=true;
    for(int k=1;k<n&&ok;k++){ int u=p[k],v=u+k; if((mask>>u&1)||(mask>>v&1)) continue; kept++; int l=newlab[v]-newlab[u]; if(l<1||l>=mm||q[l]) ok=false; else q[l]=newlab[u]; }
    if(!ok||kept!=mm-1) continue;
    if(mm==2){m=true;break;}
    auto it=mk[mm].find(key(q,mm)); if(it!=mk[mm].end()&&it->second) m=true; }
  mk[n][key(p,n)]=m; string s=canon(p,n); shapes.insert(s); if(m){marked++; msh.insert(s);}
}
void rec(int k,unsigned used){ if(k==0){leaf();return;}
  for(int a=1;a<=n-k;a++){ int ua=used>>a&1, ub=used>>(a+k)&1; if(k==n-1||ua+ub==1){p[k]=a; rec(k-1,used|1u<<a|1u<<(a+k));}}}
int main(int argc,char**argv){ int NMAX=atoi(argv[1]);
  for(n=3;n<=NMAX;n++){ cntp=prim=marked=0; shapes.clear(); msh.clear(); rec(n-1,0);
    printf("n=%d growth=%lld primitive(no clean leaf)=%lld | no-order C(2): %lld placements, %zu of %zu trees",n,cntp,prim,marked,msh.size(),shapes.size());
    for(auto&s:shapes) if(!msh.count(s)) printf("  MISSING %s",s.c_str()); printf("\n"); fflush(stdout); } }
