// Referee's independent enumerator of growth placements (README sec 1-2 definitions).
// usage: ref_enum n RULE [anchors] [tree "a-b a-b ..."]
// RULE: ALL R1 R2 R3 H1 H2 SAME EACH EACHLEFT
// Enumerates placements longest bracket first, each bracket with exactly one used foot,
// filtering on the set of unused labels after every bracket. Counts placements and shapes.
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int n; string rule;
int pos[40];
u64 nplace=0;
unordered_set<u64> shapes, rooted;
unordered_map<u64, vector<pair<int,int>>> rep;
bool wantAnch=false;
vector<int> adj[40];
struct E{u64 v;int len;};
static E enc(int v,int p){
    E ch[40]; int c=0;
    for(int w:adj[v]) if(w!=p) ch[c++]=enc(w,v);
    sort(ch,ch+c,[](const E&a,const E&b){return a.len!=b.len? a.len<b.len : a.v<b.v;});
    E r; r.v=1; r.len=1;
    for(int i=0;i<c;i++){ r.v=(r.v<<ch[i].len)|ch[i].v; r.len+=ch[i].len; }
    r.v<<=1; r.len++;
    return r;
}
static u64 canonUnrooted(int N){
    // centres by stripping leaves
    int deg[40]; bool gone[40]; int rem=N; vector<int> cur;
    for(int i=1;i<=N;i++){deg[i]=adj[i].size(); gone[i]=false; if(deg[i]<=1) cur.push_back(i);}
    while(rem>2){ vector<int> nx; for(int v:cur){gone[v]=true; rem--; for(int w:adj[v]) if(!gone[w]){ if(--deg[w]==1) nx.push_back(w);} } cur=nx; }
    u64 best=~0ULL;
    for(int v:cur) best=min(best,enc(v,0).v);
    return best;
}
static bool okState(u64 used){
    if(rule=="ALL") return true;
    int len[40],c=0; int i=1;
    while(i<=n){ if(!(used>>i&1)){ int j=i; while(j<=n && !(used>>j&1)) j++; len[c++]=j-i; i=j;} else i++; }
    if(rule[0]=='R') return c<=rule[1]-'0';
    int big=0,bigidx=-1; for(int k=0;k<c;k++) if(len[k]>1){big++; bigidx=k;}
    if(big>1) return false;
    if(rule[0]=='H') return c<=(rule[1]-'0')+1;
    if(c>3) return false;
    if(c<=2) return true;
    if(rule=="SAME") return bigidx!=1;            // all singles: pick an end one as the run
    if(rule=="EACH") return bigidx==-1 || bigidx==1; // all singles: pick the middle one as the run
    if(rule=="EACHLEFT"){ int m=0; for(int k=1;k<c;k++) if(len[k]>len[m]) m=k; return m==1; }
    fprintf(stderr,"bad rule\n"); exit(1);
}
static void leaf(){
    nplace++;
    for(int i=1;i<=n;i++) adj[i].clear();
    for(int k=1;k<n;k++){ adj[pos[k]].push_back(pos[k]+k); adj[pos[k]+k].push_back(pos[k]); }
    u64 c=canonUnrooted(n);
    if(shapes.insert(c).second && wantAnch){ vector<pair<int,int>> e; for(int k=1;k<n;k++) e.push_back({pos[k],pos[k]+k}); rep[c]=e; }
    if(wantAnch) rooted.insert(enc(1,0).v);
}
static void dfs(int k,u64 used){
    if(k==0){ leaf(); return; }
    for(int p=1;p+k<=n;p++){
        bool a=used>>p&1, b=used>>(p+k)&1;
        if(a==b) continue;
        u64 u2=used|(1ULL<<p)|(1ULL<<(p+k));
        if(!okState(u2)) continue;
        pos[k]=p; dfs(k-1,u2);
    }
}
int main(int argc,char**argv){
    n=atoi(argv[1]); rule=argv[2];
    string treestr;
    for(int i=3;i<argc;i++){ if(string(argv[i])=="anchors") wantAnch=true; else if(string(argv[i])=="tree"){treestr=argv[++i];} }
    pos[n-1]=1; u64 used=(1ULL<<1)|(1ULL<<n);
    if(okState(used)) dfs(n-2,used);
    printf("n=%d rule=%s placements=%llu shapes=%zu\n",n,rule.c_str(),nplace,shapes.size());
    if(!treestr.empty()){
        for(int i=1;i<=n;i++) adj[i].clear();
        stringstream ss(treestr); string t; int m=0;
        while(ss>>t){ int a,b; sscanf(t.c_str(),"%d-%d",&a,&b); adj[a+1].push_back(b+1); adj[b+1].push_back(a+1); m++; }
        if(m!=n-1){printf("tree has %d edges?\n",m);return 1;}
        printf("given tree drawn: %s\n", shapes.count(canonUnrooted(n))?"YES":"NO");
    }
    if(wantAnch){
        long verts=0,non=0,allanch=0,noanch=0,noleaf=0; int maxdeg=0;
        for(auto&kv:rep){
            for(int i=1;i<=n;i++) adj[i].clear();
            for(auto&e:kv.second){adj[e.first].push_back(e.second);adj[e.second].push_back(e.first);}
            int bad=0,anyleaf=0; string badinfo;
            for(int v=1;v<=n;v++){ verts++; bool an=rooted.count(enc(v,0).v);
                if(!an){bad++; maxdeg=max(maxdeg,(int)adj[v].size()); badinfo+=" v"+to_string(v)+"(deg"+to_string(adj[v].size())+")";}
                else if(adj[v].size()==1) anyleaf=1; }
            non+=bad; if(!bad) allanch++; if(bad==n) noanch++;
            if(!anyleaf){ noleaf++; printf("  no anchor leaf: degrees"); vector<int>d; for(int v=1;v<=n;v++) d.push_back(adj[v].size()); sort(d.rbegin(),d.rend()); for(int x:d)printf(" %d",x); printf("  edges"); for(auto&e:kv.second)printf(" %d-%d",e.first,e.second); printf("\n"); }
            if(bad && n<=7){ printf("  non-anchors%s in tree",badinfo.c_str()); for(auto&e:kv.second)printf(" %d-%d",e.first,e.second); printf("\n"); }
        }
        printf("anchors n=%d: trees %zu vertices %ld non-anchors %ld all-anchor trees %ld no-anchor trees %ld maxdeg-nonanchor %d no-anchor-leaf trees %ld rooted shapes %zu\n",n,rep.size(),verts,non,allanch,noanch,maxdeg,noleaf,rooted.size());
    }
}
