// Referee re-implementation of C(K), K=1,2,3, over ALL growth placements, n<=NMAX (<=14).
// From the definitions only: clean set = conditions (1),(2) of claim 0.
// level(p) = min over clean R, |R|<=3, of max(|R|, level(p\R)); level(single edge)=0.
// p in C(K) iff level(p)<=K.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int n; int p[20];
vector<unordered_map<u64,unsigned char>> lev(20);
static u64 key(const int*q,int m){u64 k=0;for(int i=1;i<m;i++)k=k*16+q[i];return k;}
// AHU canonical form of the tree drawn by p
string canon_rooted(int v,int par,vector<vector<int>>&adj){
  vector<string> ch; for(int w:adj[v]) if(w!=par) ch.push_back(canon_rooted(w,v,adj));
  sort(ch.begin(),ch.end()); string s="("; for(auto&c:ch)s+=c; return s+")";
}
string canon(const int*q,int m){
  vector<vector<int>> adj(m+1); for(int k=1;k<m;k++){adj[q[k]].push_back(q[k]+k);adj[q[k]+k].push_back(q[k]);}
  vector<int> deg(m+1),lv; int rem=m; vector<char> gone(m+1,0);
  for(int v=1;v<=m;v++){deg[v]=adj[v].size(); if(deg[v]<=1)lv.push_back(v);}
  while(rem>2){vector<int> nl; for(int v:lv){gone[v]=1;rem--; for(int w:adj[v]) if(!gone[w]&&--deg[w]==1) nl.push_back(w);} lv=nl;}
  vector<int> c; for(int v=1;v<=m;v++) if(!gone[v]) c.push_back(v);
  if(c.size()==1) return canon_rooted(c[0],0,adj);
  string a=canon_rooted(c[0],c[1],adj), b=canon_rooted(c[1],c[0],adj); if(a>b)swap(a,b); return a+b;
}
int level_of(){
  int best=9;
  // enumerate R of size 1..3
  int R[3];
  for(int sz=1; sz<=3 && n-sz>=2; sz++){
    if(sz>=best) break;
    // iterate combinations
    int idx[3]; for(int i=0;i<sz;i++) idx[i]=i+1;
    while(true){
      unsigned mask=0; for(int i=0;i<sz;i++) mask|=1u<<idx[i];
      // condition (1),(2)
      int rb=0; bool ok=true; int q[20]; int newlab[20]; int c=0;
      for(int x=1;x<=n;x++){ if(!(mask>>x&1)) c++; newlab[x]=c; }
      int cnt=0; // R-brackets total
      for(int k=1;k<n;k++) if((mask>>p[k]&1)||(mask>>(p[k]+k)&1)) cnt++;
      if(cnt==sz){
        int kept=0;
        for(int k=1;k<n&&ok;k++){
          int a=p[k],b=a+k;
          if((mask>>a&1)||(mask>>b&1)){rb++;continue;}
          int inside=0; for(int x=a+1;x<b;x++) inside+=mask>>x&1;
          if(inside!=rb) ok=false; else { kept++; q[kept]=newlab[a]; if(newlab[b]-newlab[a]!=kept) {fprintf(stderr,"T1 violated!\n");exit(1);} }
        }
        if(ok){
          int m=n-sz; int l;
          if(m==2) l=0; else { auto it=lev[m].find(key(q,m)); if(it==lev[m].end()){fprintf(stderr,"T1 violated: restriction not growth\n");exit(1);} l=it->second; }
          int v=max(sz,l); if(v<best) best=v;
        }
      }
      int i=sz-1; while(i>=0 && idx[i]==n-(sz-1-i)) i--; if(i<0)break; idx[i]++; for(int j=i+1;j<sz;j++) idx[j]=idx[j-1]+1;
    }
  }
  return best;
}
long long cntp, inC[4]; set<string> shapes, shC[4];
void rec(int k,unsigned used){
  if(k==0){ int l=level_of(); lev[n][key(p,n)]=l; cntp++; string s=canon(p,n); shapes.insert(s);
    for(int K=1;K<=3;K++) if(l<=K){inC[K]++; shC[K].insert(s);} return; }
  for(int a=1;a<=n-k;a++){ int ua=used>>a&1, ub=used>>(a+k)&1; if(k==n-1||ua+ub==1){p[k]=a; rec(k-1,used|1u<<a|1u<<(a+k));}}
}
int main(int argc,char**argv){ int NMAX=atoi(argv[1]);
  for(n=3;n<=NMAX;n++){ cntp=0; for(int K=0;K<4;K++){inC[K]=0;shC[K].clear();} shapes.clear();
    rec(n-1,0);
    printf("n=%d growth=%lld shapes=%zu | C1: %lld pl %zu trees | C2: %lld pl %zu trees | C3: %lld pl %zu trees\n",n,cntp,shapes.size(),inC[1],shC[1].size(),inC[2],shC[2].size(),inC[3],shC[3].size());
    for(int K=2;K<=3;K++) for(auto&s:shapes) if(!shC[K].count(s)&&shapes.size()-shC[K].size()<=3) printf("   missing from C%d: %s\n",K,s.c_str());
    fflush(stdout);
    if(n>=3) lev[n-4>0?n-4:0].clear();
  }
}
