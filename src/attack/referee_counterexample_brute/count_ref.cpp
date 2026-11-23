// Referee: exact number of growth placements of a tree (stdin "n u v u v ..." per line), by DFS in growth order
// (labels 0..n-1; the vertex labelled 0 is the root; lengths n-1..1 each attach a new child to a placed parent).
// placements = sum over root orbits of (#labelings with that root up to rooted automorphism).
// Symmetry: same-shape siblings are placed in index order (exactly one representative per automorphism class).
// Prune (necessary condition only): a placed vertex with q unplaced children needs q distinct lengths j<=k with
// a free label at distance j.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned __int128 u128;typedef unsigned long long u64;
int n;int par[130];vector<int> ch[130];int prevSame[130];int shape[130];int lab[130];int unplacedKids[130];
u64 nodes,cntSol;map<vector<int>,int> shapeId;vector<vector<int>> adj;
int computeShape(int v){vector<int> k;for(int c:ch[v])k.push_back(computeShape(c));sort(k.begin(),k.end());
    auto it=shapeId.find(k);int id;if(it==shapeId.end()){id=shapeId.size();shapeId[k]=id;}else id=it->second;return shape[v]=id;}
int setup(int r){
    for(int i=0;i<n;i++)ch[i].clear();
    vector<int> q{r};par[r]=-1;vector<char> seen(n,0);seen[r]=1;
    for(size_t h=0;h<q.size();h++){int v=q[h];for(int u:adj[v])if(!seen[u]){seen[u]=1;par[u]=v;ch[v].push_back(u);q.push_back(u);}}
    int s=computeShape(r);
    for(int v=0;v<n;v++){auto&c=ch[v];unplacedKids[v]=c.size();for(size_t i=0;i<c.size();i++){prevSame[c[i]]=-1;for(int j=(int)i-1;j>=0;j--)if(shape[c[j]]==shape[c[i]]){prevSame[c[i]]=c[j];break;}}}
    return s;
}
int front[130];int nf;int act[130];int na; // act = placed vertices with unplaced kids
void dfs(int k,u128 used){
    if(k==0){cntSol++;return;}
    nodes++;
    int M=n-1;
    // prune
    for(int v=0;v<n;v++)if(lab[v]>=0&&unplacedKids[v]>0){
        int a=lab[v],av=0,q=unplacedKids[v];
        for(int j=1;j<=k&&av<q;j++){if((a+j<=M&&!((used>>(a+j))&1))||(a-j>=0&&!((used>>(a-j))&1)))av++;}
        if(av<q)return;
    }
    int loc[130];int c=nf;memcpy(loc,front,sizeof(int)*nf);
    for(int i=0;i<c;i++){int u=loc[i];int p=par[u];int pl=lab[p];
        for(int s=0;s<2;s++){int x=s?pl-k:pl+k;if(x<0||x>M||((used>>x)&1))continue;
            lab[u]=x;unplacedKids[p]--;nf=0;for(int j=0;j<c;j++)if(j!=i)front[nf++]=loc[j];
            for(int w:ch[u])if(prevSame[w]<0)front[nf++]=w;
            for(int w:ch[p])if(prevSame[w]==u)front[nf++]=w;
            dfs(k-1,used|((u128)1<<x));
            lab[u]=-1;unplacedKids[p]++;}}
    nf=c;memcpy(front,loc,sizeof(int)*c);
}
int main(){
    string line;
    while(getline(cin,line)){
        istringstream is(line);if(!(is>>n))continue;
        adj.assign(n,{});int u,v;while(is>>u>>v){adj[u].push_back(v);adj[v].push_back(u);}
        set<int> seenShape;u64 total=0;nodes=0;
        for(int r=0;r<n;r++){
            int s=setup(r);if(seenShape.count(s))continue;seenShape.insert(s);
            for(int i=0;i<n;i++)lab[i]=-1;lab[r]=0;nf=0;for(int w:ch[r])if(prevSame[w]<0)front[nf++]=w;
            cntSol=0;if(n==1)cntSol=1;else dfs(n-1,(u128)1);total+=cntSol;
        }
        printf("n=%d count=%llu nodes=%llu\n",n,total,nodes);fflush(stdout);
    }
}
