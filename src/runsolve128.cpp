// For each tree on stdin: is there a growth placement in which the unused labels never form more than R runs?
// Randomised DFS with restarts, then exhaustive.   Usage: runsolve128 n R [nodeLimit [HS]] < trees   (128-bit version, n <= 120)
#include <bits/stdc++.h>
using namespace std;
typedef unsigned __int128 u64;   // labels up to 120
int n,R; vector<int> adj[128]; int lab[128]; u64 usedm; long long nodes, limit_; mt19937 rng(12345);
inline int pc(u64 x){ return __builtin_popcountll((unsigned long long)x)+__builtin_popcountll((unsigned long long)(x>>64)); }
bool ORDERED=false, SHOW=false; int HS=0;   /* HS>0: every run of unused labels except the longest has at most HS cells */
inline bool holesOK(u64 S){ if(!HS) return true; int cur=0,big=0,second=0; for(int i=1;i<=n+1;i++){ if(i<=n && !((S>>i)&1)) cur++; else if(cur){ if(cur>big){ second=max(second,big); big=cur; } else second=max(second,cur); cur=0; } } return second<=HS; }
inline int runs(u64 S){ u64 all=((((u64)1)<<n)-1)<<1; u64 un=~S & all; return pc(un & ~(un<<1)); }
map<int,int> subId[128];   /* subId[u][w]: shape id of the branch hanging from w, seen from u */
map<string,int> shapeIds;
string encSub(int v,int pa){ vector<string> ch; for(int u:adj[v]) if(u!=pa) ch.push_back(encSub(u,v)); sort(ch.begin(),ch.end()); string r="("; for(auto&c:ch) r+=c; return r+")"; }
void prepIds(){ shapeIds.clear(); for(int u=0;u<n;u++){ subId[u].clear(); for(int w:adj[u]){ string e=encSub(w,u); auto it=shapeIds.find(e); int id; if(it==shapeIds.end()){ id=shapeIds.size(); shapeIds[e]=id; } else id=it->second; subId[u][w]=id; } } }
int dfs(int k){
  if(k==0) return 1; if(++nodes>limit_) return -1;
  int cu[1024], cw[1024], cl[1024], c=0;
  for(int u=0;u<n;u++) if(lab[u]){ bool hasUn=false; int firstLeaf=-1; for(int w:adj[u]) if(!lab[w]){hasUn=true;break;} if(!hasUn) continue;
    for(int s=-1;s<=1;s+=2){ int x=lab[u]+s*k; if(x<1||x>n||(usedm>>x&1)) continue; if(runs(usedm|((u64)1)<<x)>R || !holesOK(usedm|((u64)1)<<x)) continue;
      int seen[130], ns=0; for(int w:adj[u]) if(!lab[w]){ int id=subId[u][w]; bool dup=false; for(int i=0;i<ns;i++) if(seen[i]==id){dup=true;break;} if(dup) continue; seen[ns++]=id;   /* unbuilt branches of the same shape at u are interchangeable */
        cu[c]=u; cw[c]=w; cl[c]=x; c++; } } }
  if(!ORDERED) for(int i=c-1;i>0;i--){ int j=rng()%(i+1); swap(cu[i],cu[j]); swap(cw[i],cw[j]); swap(cl[i],cl[j]); }
  for(int i=0;i<c;i++){ lab[cw[i]]=cl[i]; usedm|=((u64)1)<<cl[i]; int r=dfs(k-1); if(r==1) return 1; lab[cw[i]]=0; usedm&=~(((u64)1)<<cl[i]); if(r<0) return -1; }
  return 0;
}
int solve(long long lim){ limit_=lim; vector<pair<int,int>> es; for(int u=0;u<n;u++) for(int w:adj[u]) es.push_back({u,w}); if(!ORDERED) shuffle(es.begin(),es.end(),rng); bool hit=false;
  for(auto e:es){ memset(lab,0,sizeof lab); lab[e.first]=1; lab[e.second]=n; usedm=(((u64)1)<<1)|(((u64)1)<<n); nodes=0; int r=dfs(n-2); if(r==1) return 1; if(r<0) hit=true; }
  return hit?-1:0; }
int main(int argc,char**argv){ n=atoi(argv[1]); R=atoi(argv[2]); long long lim= argc>3? atoll(argv[3]) : 5000; HS=argc>4?atoi(argv[4]):0; if(getenv("ORDERED")) ORDERED=true; if(getenv("SHOW")) SHOW=true; string line; long long total=0, fail=0, none=0;
  while(getline(cin,line)){ if(line.empty()) continue; istringstream is(line); for(int i=0;i<n;i++) adj[i].clear(); int u,v; while(is>>u>>v){ adj[u].push_back(v); adj[v].push_back(u);} 
    prepIds(); total++; int r=-1; long long L=lim; for(int a=0;a<14&&r<0;a++){ r=solve(L); L*=3; }
    if(r==1 && SHOW){ printf("labels by vertex:"); for(int i=0;i<n;i++) printf(" %d",lab[i]); printf("\n"); }
    if(r==0){ none++; printf("NONE: %s\n",line.c_str()); } else if(r<0){ fail++; printf("UNRESOLVED: %s\n",line.c_str()); } }
  printf("n=%d runs<=%d trees=%lld  none=%lld unresolved=%lld\n",n,R,total,none,fail); }
