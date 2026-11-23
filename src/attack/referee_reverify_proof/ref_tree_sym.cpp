// Referee's independent tree-by-tree search for a growth placement obeying a rule on the unused labels.
// usage: ref_tree RULE < trees   (each line: n a b a b ...  edges, vertices 0..n-1)
// RULE: ALL R1 R2 R3 H1 H2 H3 SAME EACH. Prints OK <labels of vertices 0..n-1> or NONE per tree.
// Symmetry reduction: unlabelled branches at the same vertex with the same shape are interchangeable (first one only).
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int n; string rule; vector<int> adj[40]; int lab[40], vert[40]; map<pair<int,int>,int> bid; map<string,int> ids;
static string enc(int w,int p){ vector<string> c; for(int x:adj[w]) if(x!=p) c.push_back(enc(x,w)); sort(c.begin(),c.end()); string s="("; for(auto&t:c) s+=t; return s+")"; }
static bool okState(u64 used){
    if(rule=="ALL") return true;
    int len[40],c=0; int i=1;
    while(i<=n){ if(!(used>>i&1)){ int j=i; while(j<=n && !(used>>j&1)) j++; len[c++]=j-i; i=j;} else i++; }
    if(rule[0]=='R') return c<=rule[1]-'0';
    int big=0,bigidx=-1; for(int k=0;k<c;k++) if(len[k]>1){big++; bigidx=k;}
    if(big>1) return false;
    if(rule[0]=='H') return c<=(rule[1]-'0')+1;
    if(c>3) return false; if(c<=2) return true;
    if(rule=="SAME") return bigidx!=1;
    if(rule=="EACH") return bigidx==-1 || bigidx==1;
    exit(1);
}
static bool dfs(int k,u64 used){
    if(k==0) return true;
    for(int a=1;a<=n;a++){ if(!(used>>a&1)) continue; int u=vert[a];
        for(int s=-1;s<=1;s+=2){ int b=a+s*k; if(b<1||b>n||(used>>b&1)) continue;
            u64 u2=used|(1ULL<<b); 
            bool checked=false, okk=false; int seen[40],ns=0;
            for(int w:adj[u]){ if(lab[w]) continue;
                { int id=bid[{u,w}]; bool dup=false; for(int q=0;q<ns;q++) if(seen[q]==id) dup=true; if(dup) continue; seen[ns++]=id; }
                if(!checked){checked=true; okk=okState(u2);} if(!okk) break;
                lab[w]=b; vert[b]=w;
                if(dfs(k-1,u2)) return true;
                lab[w]=0;
            } } }
    return false;
}
int main(int argc,char**argv){
    rule=argv[1]; string line; long tot=0,none=0;
    while(getline(cin,line)){ stringstream ss(line); if(!(ss>>n)) continue; for(int i=0;i<n;i++){adj[i].clear();lab[i]=0;}
        vector<pair<int,int>> ed; int a,b; while(ss>>a>>b){adj[a].push_back(b);adj[b].push_back(a);ed.push_back({a,b});}
        bid.clear(); ids.clear(); for(int i=0;i<n;i++){ sort(adj[i].begin(),adj[i].end()); for(int w:adj[i]){ string e=enc(w,i); if(!ids.count(e)){int z=ids.size()+1; ids[e]=z;} bid[{i,w}]=ids[e]; } }
        bool found=false; u64 used=(1ULL<<1)|(1ULL<<n);
        if(okState(used)) for(auto&e:ed){ for(int o=0;o<2&&!found;o++){ int x=o?e.second:e.first, y=o?e.first:e.second;
            for(int i=0;i<n;i++)lab[i]=0; lab[x]=1;vert[1]=x;lab[y]=n;vert[n]=y;
            if(dfs(n-2,used)) found=true; } if(found)break; }
        tot++; if(found){printf("OK");for(int i=0;i<n;i++)printf(" %d",lab[i]);printf("\n");} else {none++;printf("NONE | %s\n",line.c_str());}
        fflush(stdout);
    }
    fprintf(stderr,"rule %s: trees %ld NONE %ld\n",rule.c_str(),tot,none);
}
