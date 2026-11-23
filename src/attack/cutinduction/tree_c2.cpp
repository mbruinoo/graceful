// Is a given tree in C(2)?  Top-down, independent of fwd.cpp/fwd2.cpp: enumerate ALL growth placements of the tree and test
// whether one can be taken apart to the single edge by deleting clean sets of size 1 or 2 (clean set: see lemma_check.cpp).
// Usage: tree_c2 n u1 v1 u2 v2 ...   (0-based edge list)
#include <bits/stdc++.h>
using namespace std;
typedef vector<int> V; unordered_map<string,bool> memo;
static bool isGrowth(const V&p){ int n=p[0]; unsigned used=0; for(int k=n-1;k>=1;k--){ int a=p[k], b=a+k; if(a<1||b>n) return false; if(k==n-1){ used=(1u<<a)|(1u<<b); continue; } bool ua=used>>a&1, ub=used>>b&1; if(ua==ub) return false; used|=(1u<<a)|(1u<<b); } return true; }
static bool isClean(const V&p,unsigned R){ int n=p[0]; int r=__builtin_popcount(R); if(n-r<2) return false; int rb=0;
  for(int k=1;k<n;k++) if((R>>p[k]&1)||(R>>(p[k]+k)&1)) rb++; if(rb!=r) return false;
  int shorter=0; for(int k=1;k<n;k++){ int a=p[k], b=a+k; if((R>>a&1)||(R>>b&1)){ shorter++; continue; } int jump=__builtin_popcount(R & (((1u<<b)-1) & ~((1u<<(a+1))-1))); if(jump!=shorter) return false; } return true; }
static V del(const V&p,unsigned R){ int n=p[0]; int below[40],c=0; for(int v=1;v<=n;v++){ below[v]=c; if(R>>v&1) c++; } V q(n-c,0); q[0]=n-c; for(int k=1;k<n;k++){ int a=p[k], b=a+k; if((R>>a&1)||(R>>b&1)) continue; int a2=a-below[a]; q[(b-below[b])-a2]=a2; } return q; }
bool in2(const V&p){ int n=p[0]; if(n==2) return true; string key(p.begin(),p.end()); auto it=memo.find(key); if(it!=memo.end()) return it->second; bool res=false;
  for(int x=1;x<=n&&!res;x++){ if(isClean(p,1u<<x)){ V q=del(p,1u<<x); if(!isGrowth(q)){ fprintf(stderr,"THEOREM VIOLATION\n"); exit(2);} if(in2(q)) res=true; } }
  for(int x=1;x<=n&&!res;x++) for(int y=x+1;y<=n&&!res;y++){ unsigned R=(1u<<x)|(1u<<y); if(isClean(p,R)){ V q=del(p,R); if(!isGrowth(q)){ fprintf(stderr,"THEOREM VIOLATION\n"); exit(2);} if(in2(q)) res=true; } }
  return memo[key]=res; }
int n; vector<int> adjT[40]; int lab[40]; bool used[41]; long total=0, good=0;
void dfs(int k){ if(k==0){ total++; V p(n,0); p[0]=n; for(int u=0;u<n;u++) for(int w:adjT[u]) if(u<w){ int a=min(lab[u],lab[w]), b=max(lab[u],lab[w]); p[b-a]=a; } if(in2(p)) good++; return; }
  for(int u=0;u<n;u++) if(lab[u]) for(int s=-1;s<=1;s+=2){ int x=lab[u]+s*k; if(x<1||x>n||used[x]) continue; for(int w:adjT[u]) if(!lab[w]){ lab[w]=x; used[x]=1; dfs(k-1); lab[w]=0; used[x]=0; } } }
int main(int argc,char**argv){ n=atoi(argv[1]); for(int i=2;i+1<argc;i+=2){ int u=atoi(argv[i]), v=atoi(argv[i+1]); adjT[u].push_back(v); adjT[v].push_back(u); }
  for(int r=0;r<n;r++) for(int w:adjT[r]){ memset(lab,0,sizeof lab); memset(used,0,sizeof used); lab[r]=1; lab[w]=n; used[1]=used[n]=1; dfs(n-2); }
  printf("n=%d growth labelings=%ld of which in C(2): %ld  => %s\n",n,total,good,good?"IN C(2)":"NOT IN C(2)"); }
