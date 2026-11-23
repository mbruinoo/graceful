// Referee: generic existence search for a growth placement of trees read from stdin ("n u v u v ..." per line).
// Tries every vertex as the root labelled 0, DFS over lengths n-1..1 (README definition / heap form),
// node limit per root, escalating.  Each certificate re-checked by the definition.  With SHOW=1 prints
// "tree | labels(1..n)" lines.  With CHECKONLY: stdin has "tree | labels" lines, only check them.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned __int128 u128;typedef unsigned long long u64;
int n;int par[130];vector<int> ch[130];int prevSame[130];int shape[130];int lab[130];
u64 nodes,limitN;map<vector<int>,int> shapeId;vector<vector<int>> adj;
int computeShape(int v){vector<int> k;for(int c:ch[v])k.push_back(computeShape(c));sort(k.begin(),k.end());
    auto it=shapeId.find(k);int id;if(it==shapeId.end()){id=shapeId.size();shapeId[k]=id;}else id=it->second;return shape[v]=id;}
int rootv;
void setup(int r){
    rootv=r;for(int i=0;i<n;i++)ch[i].clear();
    vector<int> q{r};par[r]=-1;vector<char> seen(n,0);seen[r]=1;
    for(size_t h=0;h<q.size();h++){int v=q[h];for(int u:adj[v])if(!seen[u]){seen[u]=1;par[u]=v;ch[v].push_back(u);q.push_back(u);}}
    computeShape(r);
    for(int v=0;v<n;v++){auto&c=ch[v];for(size_t i=0;i<c.size();i++){prevSame[c[i]]=-1;for(int j=(int)i-1;j>=0;j--)if(shape[c[j]]==shape[c[i]]){prevSame[c[i]]=c[j];break;}}}
}
int front[130];int nf;
bool dfs(int k,u128 used){
    if(k==0)return true;
    if(++nodes>limitN)return false;
    int M=n-1;int loc[130];int c=nf;memcpy(loc,front,sizeof(int)*nf);
    for(int i=0;i<c;i++){int u=loc[i];int pl=lab[par[u]];
        for(int s=0;s<2;s++){int x=s?pl-k:pl+k;if(x<0||x>M||((used>>x)&1))continue;
            lab[u]=x;nf=0;for(int j=0;j<c;j++)if(j!=i)front[nf++]=loc[j];
            for(int w:ch[u])if(prevSame[w]<0)front[nf++]=w;
            for(int w:ch[par[u]])if(prevSame[w]==u)front[nf++]=w;
            if(dfs(k-1,used|((u128)1<<x)))return true;
            if(nodes>limitN)return false;}}
    nf=c;memcpy(front,loc,sizeof(int)*c);return false;
}
bool check(const vector<pair<int,int>>&E){
    int M=n-1;vector<int> seenL(n,0);
    for(int v=0;v<n;v++){if(lab[v]<0||lab[v]>M||seenL[lab[v]])return false;seenL[lab[v]]=1;}
    if((int)E.size()!=n-1)return false;
    vector<int> A(n,-1),B(n,-1);
    for(auto&e:E){int L=abs(lab[e.first]-lab[e.second]);if(L<1||A[L]>=0)return false;A[L]=lab[e.first];B[L]=lab[e.second];}
    vector<int> used(n,0);
    for(int L=M;L>=1;L--){if(L==M){used[A[L]]=used[B[L]]=1;continue;}if(used[A[L]]==used[B[L]])return false;used[A[L]]=used[B[L]]=1;}
    return true;
}
int main(int argc,char**argv){
    u64 base=argc>1?atoll(argv[1]):20000;int rounds=argc>2?atoi(argv[2]):3;
    bool show=getenv("SHOW"),checkonly=getenv("CHECKONLY");
    string line;u64 tot=0,found=0,unres=0,okc=0,badc=0;
    while(getline(cin,line)){
        string tl=line,ll;size_t bar=line.find('|');
        if(bar!=string::npos){tl=line.substr(0,bar);ll=line.substr(bar+1);}
        istringstream is(tl);if(!(is>>n))continue;
        vector<pair<int,int>> E;int u,v;while(is>>u>>v)E.push_back({u,v});
        if(checkonly){
            if(bar==string::npos)continue;
            istringstream ls(ll);bool good=true;for(int i=0;i<n;i++){int x;if(!(ls>>x)){good=false;break;}lab[i]=x-1;}
            // also verify E is a tree on 0..n-1 (connected, n-1 edges)
            if(good){vector<int> p(n);iota(p.begin(),p.end(),0);function<int(int)> f=[&](int x){return p[x]==x?x:p[x]=f(p[x]);};
                int comps=n;for(auto&e:E){if(e.first<0||e.first>=n||e.second<0||e.second>=n){good=false;break;}int a=f(e.first),b=f(e.second);if(a!=b){p[a]=b;comps--;}}
                if(comps!=1||(int)E.size()!=n-1)good=false;}
            if(good&&check(E))okc++;else{badc++;printf("BAD %s\n",line.c_str());}
            continue;
        }
        tot++;adj.assign(n,{});for(auto&e:E){adj[e.first].push_back(e.second);adj[e.second].push_back(e.first);}
        vector<int> order(n);iota(order.begin(),order.end(),0);
        stable_sort(order.begin(),order.end(),[&](int a,int b){return adj[a].size()>adj[b].size();});
        bool ok=false;u64 lim=base;
        for(int r=0;r<rounds&&!ok;r++,lim*=20)
            for(int ri=0;ri<n&&!ok;ri++){int root=order[ri];setup(root);lab[root]=0;nf=0;for(int w:ch[root])if(prevSame[w]<0)front[nf++]=w;
                nodes=0;limitN=lim;if(n==1||dfs(n-1,(u128)1)){if(!check(E)){fprintf(stderr,"CHECK FAILED\n");return 2;}ok=true;}}
        if(ok){found++;if(show){printf("%s |",tl.c_str());for(int i=0;i<n;i++)printf(" %d",lab[i]+1);printf("\n");}}
        else{unres++;printf("UNRESOLVED %s\n",tl.c_str());}
    }
    if(checkonly)printf("certificates checked: ok=%llu bad=%llu\n",okc,badc);
    else printf("trees=%llu found=%llu unresolved=%llu\n",tot,found,unres);
}
