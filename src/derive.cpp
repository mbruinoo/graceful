// GAP-INSERTION CLOSURE.  Start from the single edge on labels {1,2}.  Move: in a growth placement on n vertices pick a
// cut position L (new label L; old labels >= L move up by one).  The cut is CLEAN if the edges jumping over it are exactly
// the c longest ones; then lengths n-c..n-1 grow by one, length j=n-c becomes free, and a new leaf with label L is hung by a
// bracket of length j on L-j or L+j, provided the result is again a growth placement.
// D_n = all placements reachable.  Reports |D_n| and how many tree shapes D_n draws.   Usage: derive N [v]
#include <bits/stdc++.h>
using namespace std;
typedef vector<signed char> Cfg;   // p[k] for k=1..n-1 (index k-1)
string canon(int n,const Cfg&p){
  vector<vector<int>> adj(n+1);
  for(int k=1;k<n;k++){ adj[p[k-1]].push_back(p[k-1]+k); adj[p[k-1]+k].push_back(p[k-1]); }
  vector<int> deg(n+1), layer; int rem=n;
  for(int i=1;i<=n;i++){ deg[i]=adj[i].size(); if(deg[i]<=1) layer.push_back(i); }
  vector<char> gone(n+1,0);
  while(rem>2){ vector<int> nx; for(int v:layer){ gone[v]=1; rem--; for(int u:adj[v]) if(!gone[u] && --deg[u]==1) nx.push_back(u);} layer=nx; }
  function<string(int,int)> enc=[&](int v,int pa){ vector<string> ch; for(int u:adj[v]) if(u!=pa) ch.push_back(enc(u,v)); sort(ch.begin(),ch.end()); string s="("; for(auto&c:ch) s+=c; return s+")"; };
  if(layer.size()==1) return enc(layer[0],0);
  string a=enc(layer[0],layer[1]), b=enc(layer[1],layer[0]); if(a>b) swap(a,b); return a+"|"+b;
}
bool isGrowth(int n,const Cfg&p){ unsigned S=1u<<1|1u<<n; if(p[n-2]!=1) return false;
  for(int k=n-2;k>=1;k--){ int a=p[k-1],b=a+k; bool x=S>>a&1,y=S>>b&1; if(x==y) return false; S|=1u<<a|1u<<b; } return true; }
int main(int argc,char**argv){ int N=atoi(argv[1]); bool verbose=argc>2;
  set<Cfg> cur; cur.insert(Cfg{1});   // n=2
  for(int n=2;n<N;n++){ set<Cfg> nxt;
    for(const Cfg&p:cur){
      for(int L=1;L<=n+1;L++){ int c=0, minlen=n; 
        for(int k=1;k<n;k++){ int a=p[k-1],b=a+k; if(a<L&&b>=L){ c++; minlen=min(minlen,k);} }
        if(c>0 && minlen!=n-c) continue;          // crossing edges must be exactly the c longest
        int j=n-c; Cfg q(n);
        for(int k=1;k<n;k++){ int a=p[k-1],b=a+k; int na=a>=L?a+1:a; int nk=(a<L&&b>=L)?k+1:k; q[nk-1]=na; }
        for(int s=0;s<2;s++){ int a= s? L-j : L; if(a<1||a+j>n+1) continue; q[j-1]=a; if(isGrowth(n+1,q)) nxt.insert(q); }
      } }
    cur.swap(nxt); set<string> sh; for(auto&p:cur) sh.insert(canon(n+1,p));
    printf("n=%d derivable placements=%zu shapes=%zu\n",n+1,cur.size(),sh.size()); fflush(stdout);
    if(verbose){ FILE*f=fopen(("/tmp/claude-0/-home-user-graceful/0371e752-f73a-552a-b40d-e3821e32333f/scratchpad/derived"+to_string(n+1)+".txt").c_str(),"w"); for(auto&s:sh) fprintf(f,"%s\n",s.c_str()); fclose(f); }
  } }
