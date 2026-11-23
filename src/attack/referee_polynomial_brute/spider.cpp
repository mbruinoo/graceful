// Referee: for given n, enumerate growth placements (README sec 2: brackets
// n-1..1, each with exactly one used foot) pruned only by: every degree <= 3
// and at most one vertex of degree 3 (necessary for a 3-leg spider).
// Prints which 3-leg spiders with a leg of length 2 are drawn; with target
// args (a c) stops at the first growth placement of S(a,2,c) and prints it.
#include <bits/stdc++.h>
using namespace std;
int n; int p[40]; bool used_[40]; int deg[40]; int c3=0;
set<array<int,3>> found; int ta=-1,tc=-1; bool done=false;
void evaluate(){
    vector<int> adj[40]; int centre=0;
    for(int k=1;k<=n-1;k++){int a=p[k],b=p[k]+k;adj[a].push_back(b);adj[b].push_back(a);}
    for(int v=1;v<=n;v++) if(adj[v].size()==3) centre=v;
    if(!centre) return;
    array<int,3> L;
    for(int s=0;s<3;s++){int prev=centre,cur=adj[centre][s],d=1;
        while(adj[cur].size()==2){int nx=adj[cur][0]==prev?adj[cur][1]:adj[cur][0];prev=cur;cur=nx;d++;} L[s]=d;}
    sort(L.begin(),L.end());
    if(ta>=0){ array<int,3> T={ta,2,tc}; sort(T.begin(),T.end()); if(L==T){done=true; printf("S(%d,2,%d) n=%d: positions p_k (k=n-1..1):",ta,tc,n); for(int k=n-1;k>=1;k--)printf(" %d",p[k]); printf("\n");} }
    else found.insert(L);
}
void rec(int k){
    if(done) return;
    if(k==0){evaluate();return;}
    for(int pos=1;pos<=n-k;pos++){
        int a=pos,b=pos+k;
        if(k<n-1 && used_[a]==used_[b]) continue;
        int o = used_[a]?a:b; // old vertex gains degree (for k<n-1)
        if(k<n-1){ if(deg[o]>=3) continue; if(deg[o]==2 && c3>=1) continue; }
        bool ua=used_[a],ub=used_[b];
        used_[a]=used_[b]=true; deg[a]++;deg[b]++; if(k<n-1&&deg[o]==3)c3++;
        p[k]=pos; rec(k-1);
        if(k<n-1&&deg[o]==3)c3--; deg[a]--;deg[b]--; used_[a]=ua;used_[b]=ub;
    }
}
int main(int argc,char**argv){
    if(argc>=3){ta=atoi(argv[1]);tc=atoi(argv[2]);n=ta+tc+3; rec(n-1); if(!done) printf("S(%d,2,%d) n=%d: NO growth placement\n",ta,tc,n); return 0;}
    n=atoi(argv[1]); rec(n-1);
    // list all 3-leg spiders on n vertices containing a leg 2, and whether found
    for(int a=1;a<=n;a++){int c=n-3-a; if(c<a) break; array<int,3> T={a,2,c}; sort(T.begin(),T.end()); printf("n=%d S(%d,2,%d): %s\n",n,a,c,found.count(T)?"yes":"NO");}
}
