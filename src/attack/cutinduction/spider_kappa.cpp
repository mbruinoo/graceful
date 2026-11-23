// Exact step number kappa(T) of a spider T: the least K such that T has a growth placement in C(K), i.e. one that can be taken
// apart down to the single edge by deleting clean sets of at most K labels at a time.  Computed top-down (independent of the
// bottom-up closure in spider_ck.cpp): enumerate all growth placements of T; kappa(p) = min over clean sets R of max(|R|, kappa(p minus R)).
// Usage: spider_kappa leg1 leg2 ...
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> V;   // pos[0]=n, pos[k]=left foot of bracket k
map<V,int> memo;
static bool isGrowth(const V&p){ int n=p[0]; unsigned used=0; for(int k=n-1;k>=1;k--){ int a=p[k], b=a+k; if(a<1||b>n) return false; if(k==n-1){ used=(1u<<a)|(1u<<b); continue; } bool ua=used>>a&1, ub=used>>b&1; if(ua==ub) return false; used|=(1u<<a)|(1u<<b); } return true; }
static bool isClean(const V&p,unsigned R){ int n=p[0]; int r=__builtin_popcount(R); if(n-r<2) return false; int rb=0;
  for(int k=1;k<n;k++) if((R>>p[k]&1)||(R>>(p[k]+k)&1)) rb++; if(rb!=r) return false;
  int shorter=0; for(int k=1;k<n;k++){ int a=p[k], b=a+k; if((R>>a&1)||(R>>b&1)){ shorter++; continue; } int jump=__builtin_popcount(R & (((1u<<b)-1) & ~((1u<<(a+1))-1))); if(jump!=shorter) return false; } return true; }
static V del(const V&p,unsigned R){ int n=p[0]; int below[40],c=0; for(int v=1;v<=n;v++){ below[v]=c; if(R>>v&1) c++; } V q(n-c,0); q[0]=n-c; for(int k=1;k<n;k++){ int a=p[k], b=a+k; if((R>>a&1)||(R>>b&1)) continue; int a2=a-below[a]; q[(b-below[b])-a2]=a2; } return q; }
int kappa(const V&p){ int n=p[0]; if(n==2) return 0; auto it=memo.find(p); if(it!=memo.end()) return it->second;
  vector<V> adj(n+1); for(int k=1;k<n;k++){ adj[p[k]].push_back(p[k]+k); adj[p[k]+k].push_back(p[k]); }
  int c=0; for(int v=1;v<=n;v++) if(adj[v].size()>=3) c=v; if(!c) for(int v=1;v<=n;v++) if(adj[v].size()==1){ c=v; break; }
  vector<V> legv; for(int w:adj[c]){ V lv; int prev=c, cur=w; while(true){ lv.push_back(cur); if(adj[cur].size()!=2) break; int nx=adj[cur][0]==prev?adj[cur][1]:adj[cur][0]; prev=cur; cur=nx; } legv.push_back(lv); }
  int L=legv.size(); int best=n-2;     // deleting everything but the top bracket {1,n} is always clean
  vector<pair<int,unsigned>> cand; V t(L,0);
  while(true){ unsigned R=0; int r=0; for(int i=0;i<L;i++) for(int j=0;j<t[i];j++){ R|=1u<<legv[i][legv[i].size()-1-j]; r++; } if(r>0&&n-r>=2) cand.push_back({r,R});
    int i=0; while(i<L && t[i]==(int)legv[i].size()){ t[i]=0; i++; } if(i==L) break; t[i]++; }
  for(int i=0;i<L;i++) for(size_t a=0;a<legv[i].size();a++) for(size_t b=a+1;b<legv[i].size();b++){ unsigned R=((2u<<n)-2); int r=n; for(size_t j=a;j<=b;j++){ R&=~(1u<<legv[i][j]); r--; } cand.push_back({r,R}); }
  sort(cand.begin(),cand.end());
  for(auto&cr:cand){ if(cr.first>=best) break; if(!isClean(p,cr.second)) continue; V q=del(p,cr.second); if(!isGrowth(q)){ fprintf(stderr,"THEOREM VIOLATION\n"); exit(2);} int v=max(cr.first,kappa(q)); if(v<best) best=v; }
  return memo[p]=best; }
int n; vector<int> adjT[40]; int lab[40]; bool used[41]; long total=0; map<int,long> dist;
void dfs(int k){ if(k==0){ total++; V p(n,0); p[0]=n; for(int u=0;u<n;u++) for(int w:adjT[u]) if(u<w){ int a=min(lab[u],lab[w]), b=max(lab[u],lab[w]); p[b-a]=a; } dist[kappa(p)]++; return; }
  for(int u=0;u<n;u++) if(lab[u]) for(int s=-1;s<=1;s+=2){ int x=lab[u]+s*k; if(x<1||x>n||used[x]) continue; for(int w:adjT[u]) if(!lab[w]){ lab[w]=x; used[x]=1; dfs(k-1); lab[w]=0; used[x]=0; } } }
int main(int argc,char**argv){ vector<int> legs; for(int i=1;i<argc;i++) legs.push_back(atoi(argv[i])); n=1; int v=1; for(int l:legs){ int p=0; for(int j=0;j<l;j++){ adjT[p].push_back(v); adjT[v].push_back(p); p=v; v++; } n+=l; }
  for(int r=0;r<n;r++) for(int w:adjT[r]){ memset(lab,0,sizeof lab); memset(used,0,sizeof used); lab[r]=1; lab[w]=n; used[1]=used[n]=1; dfs(n-2); }
  printf("spider"); for(int l:legs) printf(" %d",l); printf(" n=%d: growth labelings=%ld ; step number kappa -> count:",n,total); for(auto&d:dist) printf(" %d:%ld",d.first,d.second); printf("  => kappa(T)=%d\n",dist.empty()?-1:dist.begin()->first); }
