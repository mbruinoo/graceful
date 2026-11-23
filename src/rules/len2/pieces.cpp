// Like capsearch, but bounds the number P of "translation pieces": a piece is a maximal family of edges
// {u-i, w-i} (i=0,1,..) whose sums go down in steps of 2.  (Ladders are 2 pieces + 1 closing edge; a run of loops is 1 piece.)
// Env TSPLIT=T: require split threshold T.  Env DIFF=1: allow exactly one 'difference edge' o-x (a leg that goes up twice).
// Usage: pieces P maxprint lo1 hi1 [lo2 hi2 ...]
#include <cstdio>
#include <cstdlib>
#include <vector>
using namespace std;
int P,maxprint,found=0,TS=0; // TS: optional split threshold from env TSPLIT
bool inL[4096]; int deg[4096]; bool isSum[4096]; int eu[4096],ew[4096];
bool pre[4096]; int DO=0,DX=0;
vector<int> LB; vector<pair<int,int>> edges;
void rec(int idx,int pieces){
    if(idx<0){
        found++;
        if(DO) printf("[diff %d-%d=%d]  ",DO,DX,DO-DX);
        for(auto&e:edges) printf("%d+%d=%d  ",e.first,e.second,e.first+e.second); printf("\n");
        if(found>=maxprint) exit(0);
        return;
    }
    int v=LB[idx];
    if(pre[v]){ rec(idx-1,pieces); return; }
    if(deg[v]==2){ rec(idx-1,pieces); return; }
    if(deg[v]==1) return;
    isSum[v]=true;
    int cu=-1,cw=-1;
    if(isSum[v+2]){ cu=eu[v+2]-1; cw=ew[v+2]-1; }
    for(int pass=0;pass<2;pass++){
      if(pass==0){ if(cu<1) continue; }
      else if(pieces+1>P) break;
      for(int u=(pass==0?cu:v/2);u>=1;u--){
        int w=v-u;
        if(pass==1 && u==cu) continue;
        if((TS==0||((u>TS)+(w>TS)==(v>TS))) && inL[u]&&inL[w]&&!isSum[u]&&!isSum[w] && (u==w ? deg[u]==0 : (deg[u]<2&&deg[w]<2))){
            deg[u]++; deg[w]++; edges.push_back({u,w}); eu[v]=u; ew[v]=w;
            rec(idx-1,pieces+pass);
            edges.pop_back(); deg[u]--; deg[w]--;
        }
        if(pass==0) break;
      }
    }
    isSum[v]=false;
}
int main(int c,char**a){
    P=atoi(a[1]); maxprint=atoi(a[2]); if(getenv("TSPLIT")) TS=atoi(getenv("TSPLIT"));
    for(int i=3;i+1<c;i+=2) for(int v=atoi(a[i]);v<=atoi(a[i+1]);v++){ inL[v]=true; LB.push_back(v);}    
    if(getenv("DIFF")){
        for(int o:LB) for(int x:LB){ int i=o-x; if(i<1||!inL[i]||i==x) continue;
            DO=o; DX=x; deg[o]++; deg[x]++; pre[i]=isSum[i]=true;
            rec((int)LB.size()-1,0);
            deg[o]--; deg[x]--; pre[i]=isSum[i]=false; }
    } else
    rec((int)LB.size()-1,0);
    printf("found %d\n",found);
}
