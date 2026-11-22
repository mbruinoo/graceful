// GAP-INSERTION CLOSURE with two moves.  From a growth placement on n vertices, open a gap at L (labels >= L move up one;
// brackets jumping over the gap lengthen by one) and put a new vertex x at label L, either
//   (leaf)      joined to one existing vertex, or
//   (subdivide) placed in the middle of an existing edge {a,b}: that edge is replaced by {a,x} and {x,b}.
// Keep the result if it is again a growth placement (lengths 1..n all different, longest-first connected).
// mode 1 = leaf moves only, mode 2 = leaf + subdivide, mode 3 = any vertex split (reverse of contracting an edge).     Usage: derive2 N mode [dumpprefix]
#include <bits/stdc++.h>
using namespace std;
typedef vector<signed char> Cfg;
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
// edges (new labels) -> placement if lengths are 1..m all distinct
bool toCfg(int n,const vector<pair<int,int>>&E,Cfg&q){ q.assign(n-1,0); for(auto e:E){ int a=min(e.first,e.second), k=abs(e.first-e.second); if(k<1||k>n-1||q[k-1]) return false; q[k-1]=a; } return true; }
int main(int argc,char**argv){ int N=atoi(argv[1]), mode=atoi(argv[2]);
  set<Cfg> cur; cur.insert(Cfg{1});
  for(int n=2;n<N;n++){ set<Cfg> nxt; Cfg q;
    for(const Cfg&p:cur){
      for(int L=1;L<=n+1;L++){ vector<pair<int,int>> E;
        for(int k=1;k<n;k++){ int a=p[k-1],b=a+k; E.push_back({a>=L?a+1:a, b>=L?b+1:b}); }
        for(int u=1;u<=n+1;u++) if(u!=L){ E.push_back({L,u}); if(toCfg(n+1,E,q)&&isGrowth(n+1,q)) nxt.insert(q); E.pop_back(); }
        if(mode>=3){   // split vertex y: new x at L joined to y, and any subset of y's other edges moved from y to x
          for(int y=1;y<=n+1;y++) if(y!=L){ vector<int> inc; for(int i=0;i<n-1;i++) if(E[i].first==y||E[i].second==y) inc.push_back(i);
            int d=inc.size(); vector<pair<int,int>> F=E; F.push_back({L,y});
            for(int m=1;m<(1<<d);m++){ if(__builtin_popcount(m)<2) continue;   // sizes 0 and 1 are the leaf and subdivide moves
              for(int t=0;t<d;t++){ int i=inc[t]; auto e=E[i]; int z= e.first==y? e.second:e.first; F[i]= (m>>t&1)? make_pair(z,L): e; }
              if(toCfg(n+1,F,q)&&isGrowth(n+1,q)) nxt.insert(q); } } }
        if(mode>=2) for(int i=0;i<n-1;i++){ auto e=E[i]; E[i]={e.first,L}; E.push_back({L,e.second}); if(toCfg(n+1,E,q)&&isGrowth(n+1,q)) nxt.insert(q); E.pop_back(); E[i]=e; }
      } }
    cur.swap(nxt); set<string> sh; for(auto&p:cur) sh.insert(canon(n+1,p));
    printf("n=%d mode=%d reachable placements=%zu shapes=%zu\n",n+1,mode,cur.size(),sh.size()); fflush(stdout);
    if(argc>3){ FILE*f=fopen((string(argv[3])+to_string(n+1)+".txt").c_str(),"w"); for(auto&s:sh) fprintf(f,"%s\n",s.c_str()); fclose(f); }
  } }
