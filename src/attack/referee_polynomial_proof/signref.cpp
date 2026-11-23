// Referee: enumerate all growth placements on labels 0..m (README s2: brackets m..1, each exactly one used foot).
// Root = label 0. For each, exact code = (parent-length record in mixed radix) * 2^m + sign mask.
// Group by record; report class sizes and sign-difference sizes. Also path statistics (position of label 0).
#include <bits/stdc++.h>
using namespace std;
int m; int inlen[40]; bool used[40]; int par[40]; int sg[40]; int deg[40];
vector<uint64_t> codes; long long total; map<int,long long> pathpos; int nbr[40][3];
void emit(){
    total++;
    uint64_t rec=0;
    for(int k=m-1;k>=1;k--){ // parent of k: 0 or k+1..m -> index 0..m-k
        int p=par[k]; int idx = p==0?0:p-k; rec = rec*(uint64_t)(m-k+1)+idx;
    }
    uint64_t mask=0; for(int k=1;k<=m;k++) if(sg[k]>0) mask|=1ull<<(k-1);
    codes.push_back((rec<<m)|mask);
    bool path=true; for(int v=0;v<=m;v++) if(deg[v]>2) {path=false;break;}
    if(path){ // distance from 0 to nearest end
        int d=0;
        if(deg[0]==2){ int best=1000; for(int j=0;j<2;j++){int p=0,q=nbr[0][j],l=1; while(deg[q]==2){int z=nbr[q][0]==p?nbr[q][1]:nbr[q][0];p=q;q=z;l++;} best=min(best,l);} d=best;}
        pathpos[d]++;
    }
}
void rec(int k){
    if(k==0){emit();return;}
    for(int p=0;p+k<=m;p++){
        int a=p,b=p+k; if(used[a]==used[b]) continue;
        int u=used[a]?a:b, v=used[a]?b:a;
        used[v]=1; inlen[v]=k; par[k]=inlen[u]; sg[k]= v>u?1:-1;
        nbr[u][deg[u]<3?deg[u]:2]=v; deg[u]++; nbr[v][0]=u; deg[v]=1;
        rec(k-1);
        deg[u]--; deg[v]=0; used[v]=0;
    }
}
int main(int c,char**v){
    m=atoi(v[1])-1; 
    memset(used,0,sizeof used); memset(deg,0,sizeof deg);
    used[0]=1; inlen[0]=0; 
    rec(m);  // first bracket m: only {0,m}, root 0 used -> v=m, sign +
    sort(codes.begin(),codes.end());
    long long classes=0; map<int,long long> sizes; map<int,long long> diff; map<int,long long> zval;
    uint64_t M=(1ull<<m)-1;
    for(size_t i=0;i<codes.size();){
        size_t j=i; while(j<codes.size() && (codes[j]>>m)==(codes[i]>>m)) j++;
        classes++; sizes[j-i]++;
        int Z=0; for(size_t a=i;a<j;a++){ Z += (__builtin_popcountll((~codes[a])&M)&1)?-1:1; }
        zval[Z]++;
        for(size_t a=i;a<j;a++)for(size_t b=a+1;b<j;b++) diff[__builtin_popcountll(codes[a]^codes[b])]++;
        if(j-i==2 && m==9 && c>2){ // print n=10 pairs
            for(size_t a=i;a<j;a++){ printf("code %llx mask ",(unsigned long long)(codes[a]>>m)); for(int k=m;k>=1;k--) putchar((codes[a]>>(k-1))&1?'+':'-'); puts("");}
        }
        i=j;
    }
    printf("n=%d placements=%lld classes=%lld\n",m+1,total,classes);
    printf(" class sizes:"); for(auto&x:sizes) printf(" %d:%lld",x.first,x.second); puts("");
    printf(" sign diffs:"); for(auto&x:diff) printf(" %d:%lld",x.first,x.second); puts("");
    printf(" Z values:"); for(auto&x:zval) printf(" %d:%lld",x.first,x.second); puts("");
    printf(" paths by dist(label0,end):"); long long s=0; for(auto&x:pathpos){ printf(" %d:%lld",x.first,x.second); s+=x.second;} printf(" total %lld\n",s);
}
