// Generic solver.  Label set L = union of intervals.  Find a set O of vertices (half of L) and a graph on O in which
// every vertex has degree 2 (a loop counts 2, no double edges) such that the edge sums are exactly L \ O.
// For L = [1,2k] this is a zigzag deal of k legs of length 2 (edge {o,d(o)}; orient each cycle).
// Optional split threshold T>0: every edge {u,w} must satisfy [u>T]+[w>T] == [u+w>T].
// Usage: capsearch T maxprint lo1 hi1 [lo2 hi2 ...]
#include <cstdio>
#include <cstdlib>
#include <vector>
using namespace std;
int T,maxprint,found=0,N;
bool inL[4096]; int deg[4096]; bool isSum[4096];
vector<int> LB; vector<pair<int,int>> edges;
void rec(int idx){
    if(idx<0){
        found++;
        for(auto&e:edges) printf("%d+%d=%d  ",e.first,e.second,e.first+e.second); printf("\n");
        if(found>=maxprint) exit(0);
        return;
    }
    int v=LB[idx];
    if(deg[v]==2){ rec(idx-1); return; }
    if(deg[v]==1) return;
    isSum[v]=true;
    for(int u=1;2*u<=v;u++){
        int w=v-u;
        if(!inL[u]||!inL[w]||isSum[u]||isSum[w]) continue;
        if(u==w){ if(deg[u]!=0) continue; }
        else if(deg[u]>=2||deg[w]>=2) continue;
        if(T>0 && ((u>T)+(w>T)!=(v>T))) continue;
        // endpoints above v cannot happen; endpoints already passed? all labels > v are decided; u,w < v fine
        deg[u]++; deg[w]++; edges.push_back({u,w});
        rec(idx-1);
        edges.pop_back(); deg[u]--; deg[w]--;
    }
    isSum[v]=false;
}
int main(int c,char**a){
    T=atoi(a[1]); maxprint=atoi(a[2]);
    for(int i=3;i+1<c;i+=2) for(int v=atoi(a[i]);v<=atoi(a[i+1]);v++){ inL[v]=true; LB.push_back(v);}    
    rec((int)LB.size()-1);
    printf("found %d\n",found);
}
