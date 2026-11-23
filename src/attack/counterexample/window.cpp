// Windows: for t0=2k' and N=2k, is there a set of k-k' legs (a,o) with all labels and all lengths in (t0,N],
// labels distinct, lengths distinct, each leg: inner length a, outer length a-o, a>o?  (a zigzag deal of S(2^k)
// restricted to the window; any zigzag deal of S(2^k') on [1..t0] then extends to S(2^k).)   Exhaustive.
// usage: window kmax  -> table of (k',k) pairs with a window
#include <bits/stdc++.h>
using namespace std;
int N,t0; bool usedLab[512]; int openLegs[512], nopen; long long nodes; vector<pair<int,int>> legs;
bool dfs(int x,int toOpen){
  if(x==t0) return nopen==0 && toOpen==0;
  if(nopen>x-t0) return false; nodes++;
  int cntHigh=0; for(int y=x+1;y<=N;y++) if(!usedLab[y]) cntHigh++; if(cntHigh>nopen) return false;
  for(int i=0;i<nopen;i++){ int a=openLegs[i], o=a-x; if(o>t0 && !usedLab[o]){ usedLab[o]=1; openLegs[i]=openLegs[--nopen]; legs.push_back({a,o});
      if(dfs(x-1,toOpen)) return true; legs.pop_back(); openLegs[nopen++]=openLegs[i]; openLegs[i]=a; usedLab[o]=0; } }
  if(toOpen>0 && !usedLab[x]){ usedLab[x]=1; openLegs[nopen++]=x; if(dfs(x-1,toOpen-1)) return true; nopen--; usedLab[x]=0; }
  return false; }
int main(int c,char**v){ int kmax=atoi(v[1]); bool show=c>2;
  for(int kp=0;kp<=(getenv("ONLY0")?0:kmax);kp++){ printf("k'=%d: k =",kp); for(int k=kp+1;k<=kmax;k++){ t0=2*kp; N=2*k; long long S=0; for(int y=t0+1;y<=N;y++) S+=y; if(S%3) continue;
      memset(usedLab,0,sizeof usedLab); nopen=0; legs.clear(); nodes=0; if(dfs(N,k-kp)){ printf(" %d",k); if(show){ printf("["); for(auto&p:legs) printf("%d:%d ",p.first,p.second); printf("]"); } } fflush(stdout); } printf("\n"); } }
