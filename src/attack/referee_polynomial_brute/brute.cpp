// Referee brute force, written from README section 1-2 only.
// Mode "full": enumerate ALL (n-1)! placements, test growth property afterwards.
// Mode "grow": enumerate only growth placements (prune as soon as a bracket fails).
// For every growth placement: total count; if it draws a path, histogram of
// the distance of vertex 1 (lowest label) from the nearer end; if it draws a
// spider with 3 legs, record the leg multiset.
#include <bits/stdc++.h>
using namespace std;
int n; bool fullmode;
int p[32];
long long total=0, pathtotal=0;
long long hist[32];
set<array<int,3>> spiders;

void evaluate(){
    // growth test from the definition: longest first, exactly one used foot
    bool used[32]={0};
    used[1]=used[n]=true; // top bracket is {1,n} necessarily (position 1)
    for(int k=n-2;k>=1;k--){
        int a=p[k], b=p[k]+k;
        if(used[a]==used[b]) return;
        used[a]=used[b]=true;
    }
    total++;
    int deg[32]={0}; vector<int> adj[32];
    for(int k=1;k<=n-1;k++){int a=p[k],b=p[k]+k;deg[a]++;deg[b]++;adj[a].push_back(b);adj[b].push_back(a);}
    int mx=0,c3=0,centre=0; for(int v=1;v<=n;v++){mx=max(mx,deg[v]); if(deg[v]>=3){c3++;centre=v;}}
    if(mx<=2){
        pathtotal++;
        // distance of vertex 1 from each end
        // walk from vertex 1 in each direction
        int best=1000;
        if(deg[1]==1) best=0;
        else for(int s=0;s<2;s++){
            int prev=1,cur=adj[1][s],d=1;
            while(deg[cur]==2){int nx=adj[cur][0]==prev?adj[cur][1]:adj[cur][0];prev=cur;cur=nx;d++;}
            best=min(best,d);
        }
        hist[best]++;
    } else if(mx==3 && c3==1){
        array<int,3> L;
        for(int s=0;s<3;s++){
            int prev=centre,cur=adj[centre][s],d=1;
            while(deg[cur]==2){int nx=adj[cur][0]==prev?adj[cur][1]:adj[cur][0];prev=cur;cur=nx;d++;}
            L[s]=d;
        }
        sort(L.begin(),L.end());
        spiders.insert(L);
    }
}
bool usedg[32];
void rec(int k){
    if(k==0){evaluate();return;}
    for(int pos=1;pos<=n-k;pos++){
        if(!fullmode && k<n-1){
            int a=pos,b=pos+k;
            if(usedg[a]==usedg[b]) continue;
            bool ua=usedg[a],ub=usedg[b];
            usedg[a]=usedg[b]=true; p[k]=pos; rec(k-1); usedg[a]=ua;usedg[b]=ub;
        } else {
            p[k]=pos;
            if(!fullmode){usedg[pos]=usedg[pos+k]=true;}
            rec(k-1);
        }
    }
}
int main(int argc,char**argv){
    n=atoi(argv[1]); fullmode = string(argv[2])=="full";
    rec(n-1);
    printf("n=%d m=%d mode=%s growth=%lld pathgrowth=%lld hist(b:count):",n,n-1,argv[2],total,pathtotal);
    for(int b=0;b<=n/2;b++) printf(" %d:%lld",b,hist[b]);
    printf("\n");
    if(argc>3){ printf(" spiders with a growth placement (3 legs):"); for(auto&L:spiders) printf(" (%d,%d,%d)",L[0],L[1],L[2]); printf("\n");}
}
