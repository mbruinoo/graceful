// Referee for claim 2, written from README sec 2 (growth placement definition).
// Enumerate all growth placements on vertices 1..n (brackets n-1..1, each with
// exactly one used foot; top bracket {1,n}).  Root = vertex 1 (label 0 in the
// 0..m convention).  For each placement record, for every length k, the length
// of the bracket above it (the bracket that introduced its old foot; 0 if the
// old foot is the root) and whether the new foot is below the old foot.
// The parent-length vector is the class (T,r,w); the down/up bits are eps.
// Sort, group by class, report group sizes, sign-difference histogram, and
// check on every pair: sum_{u in D} eps_u w_u s_u == 0 and labels agree mod 2.
// Optional: for classes of size 1, collect the unrooted tree shapes (AHU
// canonical form) and count them.
// usage: sign n [shapes]
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int n,m; bool used_[40]; int intro[40];
int par[40]; int sg[40]; // per length
vector<u64> recs;
void emit(){
    u64 key=0;
    for(int k=m-1;k>=1;k--){ int idx = par[k]==0?0:par[k]-k; key = key*(u64)(m-k+1)+idx; }
    u64 s=0; for(int k=m-1;k>=1;k--) s=(s<<1)|sg[k];
    recs.push_back((key<<(m-1))|s);
}
void rec(int k){
    if(k==0){emit();return;}
    for(int pos=1;pos<=n-k;pos++){
        int a=pos,b=pos+k;
        if(used_[a]==used_[b]) continue;
        int o=used_[a]?a:b, nw=used_[a]?b:a;
        par[k]=intro[o]; sg[k]=(nw<o);
        used_[nw]=true; intro[nw]=k;
        rec(k-1);
        used_[nw]=false;
    }
}
void decode(u64 r,int*P,int*S){
    u64 s=r&((1ULL<<(m-1))-1), key=r>>(m-1);
    for(int k=1;k<=m-1;k++){ S[k]=(s>>(k-1))&1; }
    for(int k=1;k<=m-1;k++){ int base=m-k+1; int idx=key%base; key/=base; P[k]=idx==0?0:idx+k; }
    P[m]=0; S[m]=0;
}
// AHU canonical form of the unrooted tree given by parent-length vector
string canon_rooted(int v,int from,vector<vector<int>>&adj){
    vector<string> ch; for(int w:adj[v]) if(w!=from) ch.push_back(canon_rooted(w,v,adj));
    sort(ch.begin(),ch.end()); string s="("; for(auto&c:ch)s+=c; return s+")";
}
string canon_free(int*P){
    // vertices: 0 = root, k = child end of edge of length k
    vector<vector<int>> adj(m+1);
    for(int k=1;k<=m;k++){adj[k].push_back(P[k]);adj[P[k]].push_back(k);}
    // centres by leaf stripping
    vector<int> deg(m+1),layer; int left=m+1; vector<char> gone(m+1,0);
    for(int v=0;v<=m;v++){deg[v]=adj[v].size(); if(deg[v]<=1) layer.push_back(v);}
    while(left>2){ vector<int> nx; for(int v:layer){gone[v]=1;left--; for(int w:adj[v]) if(!gone[w] && --deg[w]==1) nx.push_back(w);} layer=nx; }
    vector<int> cs; for(int v=0;v<=m;v++) if(!gone[v]) cs.push_back(v);
    string best=canon_rooted(cs[0],-1,adj);
    if(cs.size()==2){ string a=canon_rooted(cs[0],cs[1],adj), b=canon_rooted(cs[1],cs[0],adj); if(a>b)swap(a,b); best="["+a+b+"]"; }
    return best;
}
int main(int argc,char**argv){
    n=atoi(argv[1]); m=n-1; bool shapes=argc>2;
    used_[1]=used_[n]=true; intro[1]=0; intro[n]=m; par[m]=0; sg[m]=0;
    rec(m-1);
    printf("n=%d growth placements=%zu\n",n,recs.size());
    sort(recs.begin(),recs.end());
    size_t N=recs.size(); long long classes=0; map<int,long long> sizeh; map<int,long long> diffh;
    long long idbad=0, parbad=0, pairs=0; unordered_set<string> shapeset, shapeall;
    int shown=0;
    for(size_t i=0;i<N;){
        size_t j=i; u64 key=recs[i]>>(m-1);
        while(j<N && (recs[j]>>(m-1))==key) j++;
        int sz=j-i; classes++; sizeh[sz]++;
        int P[40],S1[40],S2[40];
        if(shapes){ decode(recs[i],P,S1); string c=canon_free(P); shapeall.insert(c); if(sz==1) shapeset.insert(c); }
        if(sz>=2){
            for(size_t a=i;a<j;a++) for(size_t b=a+1;b<j;b++){
                pairs++;
                decode(recs[a],P,S1); decode(recs[b],P,S2);
                int d=0; for(int k=1;k<m;k++) d+=S1[k]!=S2[k];
                if(sz==2) diffh[d]++;
                // subtree sizes: process lengths ascending (children have smaller length)
                int sub[40]; for(int k=1;k<=m;k++) sub[k]=1;
                for(int k=1;k<=m;k++) if(P[k]) sub[P[k]]+=sub[k];
                long long tot=0; for(int k=1;k<m;k++) if(S1[k]!=S2[k]) tot+=(S1[k]?-1:1)*(long long)k*sub[k];
                if(tot!=0) idbad++;
                // labels (0..m): descending length so parents first
                int f1[40],f2[40]; f1[0]=f2[0]=0;
                for(int k=m;k>=1;k--){ f1[k]=f1[P[k]]+(S1[k]?-k:k); f2[k]=f2[P[k]]+(S2[k]?-k:k); }
                bool okp=true; u64 seen1=0,seen2=0;
                for(int k=0;k<=m;k++){ if((f1[k]-f2[k])&1) okp=false; if(f1[k]<0||f1[k]>m||f2[k]<0||f2[k]>m) okp=false; else {seen1|=1ULL<<f1[k];seen2|=1ULL<<f2[k];} }
                if(seen1!=(1ULL<<(m+1))-1||seen2!=seen1) okp=false;
                if(!okp) parbad++;
                if(n==10 && shown<12){ shown++;
                    printf("  pair %d:",shown);
                    for(int q=0;q<2;q++){ int*f=q?f2:f1; printf(q?"  |":""); for(int k=m;k>=1;k--) printf(" %d->%d:%d",f[P[k]],f[k],k);} printf("\n"); }
            }
        }
        i=j;
    }
    printf("n=%d classes=%lld; class sizes:",n,classes); for(auto&x:sizeh) printf(" size%d:%lld",x.first,x.second);
    printf("; sign-differences within size-2 classes:"); for(auto&x:diffh) printf(" %d:%lld",x.first,x.second);
    printf("; pairs=%lld identity failures=%lld parity/label failures=%lld",pairs,idbad,parbad);
    if(shapes) printf("; tree shapes with a growth placement=%zu, shapes having a (root,w) class with exactly one sign vector=%zu",shapeall.size(),shapeset.size());
    printf("\n");
}
