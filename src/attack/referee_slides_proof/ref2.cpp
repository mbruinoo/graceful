// Referee check for claim 2, written from README section 1 only.
// Dense mixed-radix table of all placements; flood fill (not union-find, not sorted lookup).
// usage: ref2 n
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int n; u64 W[20]; vector<unsigned char> st; // 0 non-tree, 1 tree, 2 visited
u64 total;
bool istree(const int*p){ int q[20]; for(int i=1;i<=n;i++)q[i]=i;
  for(int k=1;k<n;k++){int a=p[k],b=p[k]+k; while(q[a]!=a)a=q[a]; while(q[b]!=b)b=q[b]; if(a==b)return false; q[a]=b;} return true; }
void dec(u64 x,int*p){ for(int k=1;k<n;k++){ p[k]=x%(n-k)+1; x/=(n-k);} }
// canonical form via centre + sorted child strings
string enc(vector<int>*adj,int v,int pa){ vector<string> ch; for(int u:adj[v]) if(u!=pa) ch.push_back(enc(adj,u,v)); sort(ch.begin(),ch.end()); string s="("; for(auto&c:ch)s+=c; return s+")"; }
string canon(const int*p){ vector<int> adj[20]; for(int k=1;k<n;k++){adj[p[k]].push_back(p[k]+k);adj[p[k]+k].push_back(p[k]);}
  string best; for(int v=1;v<=n;v++){ string s=enc(adj,v,0); if(best.empty()||s<best) best=s; } return best; }
int mode;
template<class F> void nbrs(u64 x,const int*p,F f){
  // unit slides always
  for(int k=1;k<n;k++){ if(p[k]>1) f(x-W[k]); if(p[k]<n-k) f(x+W[k]); }
  if(mode==1) for(int k=1;k<n;k++){ if(p[k]>2) f(x-2*W[k]); if(p[k]+2<=n-k) f(x+2*W[k]); }
  if(mode==2) for(int k=1;k<n;k++){ if(p[k]-k>=1) f(x-(u64)k*W[k]); if(p[k]+k<=n-k) f(x+(u64)k*W[k]); }
  if(mode>=3) for(int k=1;k<n;k++) for(int l=k+1;l<n;l++){ if(mode==5 && l!=k+1) continue;
     for(int s=-1;s<=1;s+=2) for(int t=-1;t<=1;t+=2){ if(mode==4 && s!=t) continue;
       int a=p[k]+s,b=p[l]+t; if(a<1||a>n-k||b<1||b>n-l) continue;
       f(x + (s>0?W[k]:-W[k]) + (t>0?W[l]:-W[l])); } }
}
int main(int argc,char**argv){ n=atoi(argv[1]);
  u64 w=1; for(int k=1;k<n;k++){W[k]=w; w*=(n-k);} total=w; st.assign(total,0);
  // enumerate ALL placements by odometer, test each from the definition
  int p[20]; for(int k=1;k<n;k++)p[k]=1; u64 ntree=0;
  for(u64 x=0;x<total;x++){ if(istree(p)){st[x]=1;ntree++;}
    for(int k=1;k<n;k++){ if(p[k]<n-k){p[k]++;break;} p[k]=1; } }
  printf("n=%d tree placements=%llu\n",n,ntree);
  // local minima and shapes
  map<string,pair<long,long>> sh; u64 nmin=0; map<string,u64> ex;
  bool doshape = (argc<3);
  for(u64 x=0;x<total;x++) if(st[x]){ dec(x,p); bool L=false; for(int k=1;k<n;k++) if(p[k]>1 && st[x-W[k]]){L=true;break;}
    if(!L) nmin++;
    if(doshape){ string c=canon(p); auto&e=sh[c]; e.first++; if(!L)e.second++; if(!ex.count(c))ex[c]=x; } }
  printf("local minima=%llu",nmin);
  if(doshape){ int miss=0; for(auto&kv:sh) if(!kv.second.second) miss++;
    printf(" shapes=%zu shapes with no local minimum=%d\n",sh.size(),miss);
    for(auto&kv:sh) if(!kv.second.second){ dec(ex[kv.first],p); printf("  missing shape (%ld placements) e.g.",kv.second.first); for(int k=n-1;k>=1;k--)printf(" {%d,%d}",p[k],p[k]+k); 
      // degree sequence
      int deg[20]={0}; for(int k=1;k<n;k++){deg[p[k]]++;deg[p[k]+k]++;} vector<int> d(deg+1,deg+n+1); sort(d.rbegin(),d.rend()); printf("  degs:"); for(int v:d)printf(" %d",v); printf("\n"); } }
  else printf("\n");
  const char*nm[6]={"unit only","unit + slide-by-2","unit + reflect through foot","unit + two-at-once","unit + two-at-once same direction","unit + two-at-once consecutive lengths"};
  vector<u64> stack;
  for(mode=0;mode<6;mode++){
    for(u64 x=0;x<total;x++) if(st[x]==2) st[x]=1;
    u64 comps=0;
    for(u64 x0=0;x0<total;x0++) if(st[x0]==1){ comps++; st[x0]=2; stack.push_back(x0);
      while(!stack.empty()){ u64 x=stack.back(); stack.pop_back(); int q[20]; dec(x,q);
        nbrs(x,q,[&](u64 y){ if(st[y]==1){st[y]=2; stack.push_back(y);} }); } }
    printf("%s: components=%llu\n",nm[mode],comps); fflush(stdout);
  }
}
