// print every tree on n vertices as "n u v u v ..."  (uses ../../treegen.h)
#include "../../treegen.h"
#include <cstdio>
#include <cstdlib>
int main(int c,char**v){ int n=atoi(v[1]); TreeGen g(n); std::vector<int> p; while(g.next()){ g.parents(p); printf("%d",n); for(int i=1;i<n;i++) printf(" %d %d",p[i],i); printf("\n"); } }
