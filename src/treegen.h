// Free-tree generator (Wright, Richmond, Odlyzko, McKay), ported from networkx's nonisomorphic_trees.
// Usage: TreeGen g(n); while(g.next()) { g.layout is the level sequence; g.edges(parent) fills parent[i] (parent[0]=-1). }
#include <vector>
#include <algorithm>
struct TreeGen {
  int n; std::vector<int> layout; bool started=false, done=false;
  TreeGen(int n_):n(n_){ for(int i=0;i<=n/2;i++) layout.push_back(i); for(int i=1;i<(n+1)/2;i++) layout.push_back(i); }
  static bool nextRooted(std::vector<int>&L,int p){            // returns false if no successor
    if(p<0){ p=L.size()-1; while(L[p]==1) p--; }
    if(p==0) return false;
    int q=p-1; while(L[q]!=L[p]-1) q--;
    for(size_t i=p;i<L.size();i++) L[i]=L[i-p+q];
    return true; }
  static void split(const std::vector<int>&L,std::vector<int>&left,std::vector<int>&rest){
    int m=-1; bool one=false; for(size_t i=0;i<L.size();i++) if(L[i]==1){ if(one){ m=i; break; } one=true; }
    if(m<0) m=L.size();
    left.clear(); rest.clear(); for(int i=1;i<m;i++) left.push_back(L[i]-1); rest.push_back(0); for(size_t i=m;i<L.size();i++) rest.push_back(L[i]); }
  bool nextTree(){                                             // make layout a valid free tree (or advance); false if exhausted
    std::vector<int> left,rest; split(layout,left,rest);
    int lh=*std::max_element(left.begin(),left.end()), rh=*std::max_element(rest.begin(),rest.end());
    bool valid = rh>=lh;
    if(valid && rh==lh){ if(left.size()>rest.size()) valid=false; else if(left.size()==rest.size() && left>rest) valid=false; }
    if(valid) return true;
    int p=left.size(); int cp=layout[p];
    if(!nextRooted(layout,p)) return false;
    if(cp>2){ std::vector<int> nl,nr; split(layout,nl,nr); int h=*std::max_element(nl.begin(),nl.end()); int len=h+1; for(int i=0;i<len;i++) layout[layout.size()-len+i]=i+1; }
    return true; }
  bool next(){ if(done) return false; if(started){ if(!nextRooted(layout,-1)){ done=true; return false; } } started=true; if(!nextTree()){ done=true; return false; } return true; }
  void parents(std::vector<int>&par) const { par.assign(n,-1); std::vector<int> st; for(int i=0;i<n;i++){ while(!st.empty() && layout[st.back()]>=layout[i]) st.pop_back(); if(!st.empty()) par[i]=st.back(); st.push_back(i); } }
};
