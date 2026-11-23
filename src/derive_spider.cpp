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
// SPIDER VERSION.  Keep only placements in which every vertex except the one labelled 1 has degree <= 2
// (a spider, or a path, whose centre carries label 1), and grow them by clean gap insertions of a leaf.
// Reports which multisets of leg lengths are reached.   Usage: derive_spider N
bool centred(int n,const Cfg&p,vector<int>&legs){ vector<int> deg(n+1,0); vector<vector<int>> adj(n+1);
  for(int k=1;k<n;k++){ int a=p[k-1],b=a+k; deg[a]++; deg[b]++; adj[a].push_back(b); adj[b].push_back(a); }
  for(int v=2;v<=n;v++) if(deg[v]>2) return false;
  legs.clear(); for(int w:adj[1]){ int L=1,prev=1,cur=w; while(true){ int nx=0; for(int u:adj[cur]) if(u!=prev) nx=u; if(!nx) break; prev=cur; cur=nx; L++; } legs.push_back(L); }
  sort(legs.rbegin(),legs.rend()); return true; }
void parts(int rem,int mx,vector<int>&cur,set<vector<int>>&out){ if(rem==0){ out.insert(cur); return; } for(int x=min(rem,mx);x>=1;x--){ cur.push_back(x); parts(rem-x,x,cur,out); cur.pop_back(); } }
int main(int argc,char**argv){ int N=atoi(argv[1]);
  set<Cfg> cur; cur.insert(Cfg{1}); vector<int> legs;
  for(int n=2;n<N;n++){ set<Cfg> nxt;
    for(const Cfg&p:cur){
      for(int L=2;L<=n+1;L++){ int c=0, minlen=n;                       // L>=2: the centre keeps label 1
        for(int k=1;k<n;k++){ int a=p[k-1],b=a+k; if(a<L&&b>=L){ c++; minlen=min(minlen,k);} }
        if(c>0 && minlen!=n-c) continue;
        int j=n-c; Cfg q(n);
        for(int k=1;k<n;k++){ int a=p[k-1],b=a+k; int na=a>=L?a+1:a; int nk=(a<L&&b>=L)?k+1:k; q[nk-1]=na; }
        for(int s=0;s<2;s++){ int a= s? L-j : L; if(a<1||a+j>n+1) continue; q[j-1]=a; if(isGrowth(n+1,q) && centred(n+1,q,legs)) nxt.insert(q); }
      } }
    cur.swap(nxt); set<vector<int>> reached; for(auto&p:cur){ centred(n+1,p,legs); reached.insert(legs); }
    set<vector<int>> all; vector<int> tmp; parts(n,n,tmp,all);
    printf("n=%d centre-anchored placements reached=%zu  leg patterns reached=%zu of %zu",n+1,cur.size(),reached.size(),all.size());
    int shown=0; for(auto&a:all) if(!reached.count(a) && shown<6){ printf(shown?"; ":"   missing: "); for(int x:a) printf("%d ",x); shown++; } printf("\n"); fflush(stdout);
  } }
