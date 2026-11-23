// Referee: independent all-up comb search for every diameter-4 tree on n vertices.
// Tree: centre with neighbours of leaf-counts s_1>=...>=s_k>=0 (>=2 positive), n = 1+k+sum s.
// Search: root = a largest hub at 0, centre at y. Lengths x = y-1..1 are assigned longest first to:
//  hub edge (new hub at y-x), leaf edge of a placed hub h (cell h+x free, <y), or root leaf at cell x.
// Prints one labeling per tree (labels 0..m) for verification by ref_verify.py.
#include <cstdio>
#include <vector>
#include <cstdlib>
using namespace std;
int n,y,k; vector<int> s; int Wmax,Wleft;
vector<int> hubpos, need; vector<char> usedc; vector<int> who; // who[x]: -2 W, -1 hubedge, i>=0 leaf of hub i
long long nodes;
bool dfs(int x){
  nodes++;
  if(x==0){ for(int i=1;i<k;i++) if(hubpos[i]<0||need[i]) return false; return true; }
  // hub edge
  int h=y-x;
  if(!usedc[h]){
    for(int i=1;i<k;i++){ if(hubpos[i]>=0) continue; if(i>1&&s[i]==s[i-1]&&hubpos[i-1]<0) continue;
      hubpos[i]=h; usedc[h]=1; who[x]=-1;
      if(dfs(x-1)) return true;
      hubpos[i]=-1; usedc[h]=0; }
  }
  for(int i=1;i<k;i++){ if(hubpos[i]<0||!need[i]) continue; int c=hubpos[i]+x; if(c>=y||usedc[c]) continue;
    usedc[c]=1; need[i]--; who[x]=i;
    if(dfs(x-1)) return true;
    usedc[c]=0; need[i]++; }
  if(Wleft>0 && !usedc[x]){ usedc[x]=1; Wleft--; who[x]=-2;
    if(dfs(x-1)) return true;
    usedc[x]=0; Wleft++; }
  return false;
}
int total=0, found=0;
void solve(){
  k=s.size(); int inner=0; for(int i=1;i<k;i++) inner+=1+s[i];
  for(int w=0;w<=s[0];w++){
    y=inner+w+1; Wmax=Wleft=w;
    hubpos.assign(k,-1); need=s; usedc.assign(y+1,0); who.assign(y+1,0);
    if(dfs(y-1)){
      found++;
      printf("T");for(int v:s)printf(" %d",v);
      printf(" | y %d | hubs",y); for(int i=1;i<k;i++) printf(" %d",hubpos[i]);
      printf(" | leaves"); for(int x=1;x<y;x++) if(who[x]>=0) printf(" %d:%d",who[x],hubpos[who[x]]+x);
      printf(" | W"); for(int x=1;x<y;x++) if(who[x]==-2) printf(" %d",x);
      printf("\n"); return; }
  }
  printf("NONE");for(int v:s)printf(" %d",v);printf("\n");
}
void gen(int rem,int mx){ // parts (s_i+1) nonincreasing, sum = n-1
  if(rem==0){ int pos=0; for(int v:s) if(v>0) pos++; if(pos>=2){ total++; solve(); } return; }
  for(int p=mx<rem?mx:rem;p>=1;p--){ s.push_back(p-1); gen(rem-p,p); s.pop_back(); }
}
int main(int c,char**v){ n=atoi(v[1]); gen(n-1,n-1);
  fprintf(stderr,"n=%d diameter-4 trees=%d comb at largest hub=%d nodes=%lld\n",n,total,found,nodes); }
