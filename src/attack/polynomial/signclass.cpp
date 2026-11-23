// For every growth placement on n vertices (README s.2: brackets n-1..1, each with exactly one
// foot already used; root = vertex labelled 1 = label 0 here) record
//   key  = the heap-ordered rooted tree: for each length k, the length of the bracket above it
//          (0 if the bracket hangs on the root).  Lengths are distinct, so this determines the
//          rooted tree together with its heap order, and nothing else.
//   mask = the signs: bit k set if bracket k goes down (child label < parent label).
// Then group by key: how many sign vectors does one heap-ordered rooted tree admit, and in how
// many signs do two of them differ?
// Usage: ./signclass n [PARTS]   (n <= 16; the classes are processed in PARTS passes to bound
//        memory: n = 15 needs about 1 GB with PARTS = 1; use PARTS = 8 for n = 16)
#include <bits/stdc++.h>
using namespace std;
typedef unsigned long long u64;
int n; bool used_[40]; int pw[40];           // pw[label] = length of the bracket from label to its parent
vector<pair<u64,unsigned>> rec; u64 key; unsigned mask; int PARTS=1, PART=0; long long total=0;
void go(int k){
  if(k==0){ total++; if((int)((key*0x9E3779B97F4A7C15ULL)>>40)%PARTS==PART) rec.push_back({key,mask}); return; }
  for(int a=0;a+k<n;a++){ int b=a+k;
    if(used_[a]==used_[b]) continue;
    int child = used_[a]? b : a, parent = used_[a]? a : b;
    u64 ok=key; unsigned om=mask;
    key |= (u64)pw[parent] << (4*(k-1)); if(child<parent) mask |= 1u<<k;
    used_[child]=true; pw[child]=k; go(k-1); used_[child]=false;
    key=ok; mask=om; }
}
int main(int argc,char**argv){ n=atoi(argv[1]); if(argc>2) PARTS=atoi(argv[2]);
  map<int,long long> hist, diff; long long classes=0, zero=0, tot=0;
  for(PART=0;PART<PARTS;PART++){ rec.clear(); total=0;
  used_[0]=used_[n-1]=true; pw[0]=0; pw[n-1]=n-1; key=0; mask=0; go(n-2); tot=total;
  sort(rec.begin(),rec.end());
  for(size_t i=0;i<rec.size();){ size_t j=i; int sg=0;
    while(j<rec.size() && rec[j].first==rec[i].first){ sg += (__builtin_popcount(rec[j].second)&1)? -1:1; j++; }
    classes++; hist[j-i]++; if(sg==0) zero++;
    for(size_t x=i;x<j;x++) for(size_t y=x+1;y<j;y++) diff[__builtin_popcount(rec[x].second^rec[y].second)]++;
    i=j; } }
  printf("n=%d growth placements %lld classes %lld\n sign vectors per class:",n,tot,classes);
  for(auto&h:hist) printf(" %d:%lld",h.first,h.second);
  printf("\n classes with signed count 0: %lld\n pairs of sign vectors in one class, by number of differing signs:",zero);
  for(auto&d:diff) printf(" %d:%lld",d.first,d.second); puts("");
}
