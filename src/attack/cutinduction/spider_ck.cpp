// Does a given spider have a growth placement in the class C(K) (built from the single edge by clean steps that open at most K gaps)?
// Exhaustive breadth-first closure restricted to placements whose tree is a subtree of the target spider (every member of a
// chain ending at the target is such a subtree, so the restriction loses nothing).  Self-contained (n<=26).
// Usage: spider_c2 K leg1 leg2 ...      prints per-size counts and REACHED / NOT REACHED (exhaustive unless the cap is hit)
#include <bits/stdc++.h>
using namespace std;
typedef unsigned __int128 u128; typedef unsigned long long u64;
struct Pl{ int n; int pos[32]; };
static u128 enc(const Pl&p){ u128 x=0; for(int k=1;k<p.n;k++) x|=(u128)p.pos[k]<<(5*(k-1)); return x; }
static Pl dec(u128 x,int n){ Pl p; p.n=n; for(int k=1;k<n;k++) p.pos[k]=(int)((x>>(5*(k-1)))&31); return p; }
struct H{ size_t operator()(u128 x) const { u64 a=(u64)x, b=(u64)(x>>64); a^=b*0x9e3779b97f4a7c15ULL; a^=a>>33; a*=0xff51afd7ed558ccdULL; a^=a>>33; return a; } };
static bool isGrowth(const Pl&p){ int n=p.n; unsigned used=0; for(int k=n-1;k>=1;k--){ int a=p.pos[k], b=a+k; if(a<1||b>n) return false;
  if(k==n-1){ used=(1u<<a)|(1u<<b); continue; } bool ua=used>>a&1, ub=used>>b&1; if(ua==ub) return false; used|=(1u<<a)|(1u<<b); } return true; }
vector<int> target; int TN;
static bool embeds(const Pl&p){ int n=p.n; vector<vector<int>> adj(n+1); for(int k=1;k<n;k++){ adj[p.pos[k]].push_back(p.pos[k]+k); adj[p.pos[k]+k].push_back(p.pos[k]); }
  int c=0; for(int v=1;v<=n;v++) if(adj[v].size()>=3){ if(c) return false; c=v; }
  if(!c) return n-1<=target[0]+target[1];
  vector<int> legs; for(int w:adj[c]){ int len=1, prev=c, cur=w; while(adj[cur].size()==2){ int nx=adj[cur][0]==prev?adj[cur][1]:adj[cur][0]; prev=cur; cur=nx; len++; } legs.push_back(len); }
  sort(legs.rbegin(),legs.rend()); if(legs.size()>target.size()) return false; for(size_t i=0;i<legs.size();i++) if(legs[i]>target[i]) return false; return true; }
int main(int argc,char**argv){ int K=atoi(argv[1]); for(int i=2;i<argc;i++) target.push_back(atoi(argv[i])); sort(target.rbegin(),target.rend()); TN=1; for(int x:target) TN+=x;
  size_t CAP=60000000; vector<unordered_set<u128,H>> C(TN+3); { Pl p; p.n=2; p.pos[1]=1; C[2].insert(enc(p)); } bool capped=false;
  for(int n=2;n<=TN;n++){ printf("n=%d placements=%zu\n",n,C[n].size()); fflush(stdout); if(n==TN) break;
    for(u128 x:C[n]){ Pl p=dec(x,n),q;
      for(int k=1;k<=K && n+k<=TN;k++){ int g[8]; 
        // gap multisets g[0]<=...<=g[k-1], cuts 0..n ; new labels L_i=g[i]+i+1
        function<void(int,int)> rec=[&](int i,int lo){
          if(i<k){ for(int v=lo;v<=n;v++){ g[i]=v; rec(i+1,v); } return; }
          q.n=n+k; int last=0; bool have[40]={0};
          for(int e=1;e<n;e++){ int a=p.pos[e], b=a+e; int sa=0,sb=0; for(int t=0;t<k;t++){ sa+=(a>g[t]); sb+=(b>g[t]); } a+=sa; b+=sb; int len=b-a; if(len<=last) return; last=len; have[len]=1; q.pos[len]=a; }
          int fr[8],nf=0; for(int e=1;e<=n+k-1;e++) if(!have[e]){ if(nf<k) fr[nf]=e; nf++; } if(nf!=k) return;
          int L[8]; for(int t=0;t<k;t++) L[t]=g[t]+t+1;
          function<void(int)> put=[&](int j){ if(j==k){ if(isGrowth(q)&&embeds(q)){ if(C[n+k].size()<CAP) C[n+k].insert(enc(q)); else capped=true; } return; }
            for(int t=0;t<k;t++) for(int s2=0;s2<2;s2++){ int pp=s2?L[t]:L[t]-fr[j]; if(pp<1||pp+fr[j]>n+k) continue; q.pos[fr[j]]=pp; put(j+1); } };
          put(0); };
        rec(0,0); } }
    if(n>=3) unordered_set<u128,H>().swap(C[n-1]); }
  // the target itself: placements of size TN embed in the target and have TN vertices, hence are the target
  printf("spider"); for(int x:target) printf(" %d",x); printf(" (n=%d): %s in C(%d)%s\n",TN,C[TN].empty()?"NOT REACHED":"REACHED",K,capped?"  [cap hit: not exhaustive]":"");
  if(!C[TN].empty()){ Pl p=dec(*C[TN].begin(),TN); printf("  witness (brackets longest first):"); for(int k=TN-1;k>=1;k--) printf(" %d-%d",p.pos[k],p.pos[k]+k); printf("\n"); } }
