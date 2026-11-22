#include "treegen.h"
#include <cstdio>
#include <cstdlib>
int main(int c,char**v){ int n=atoi(v[1]); TreeGen g(n); long long k=0; while(g.next()) k++; printf("n=%d trees=%lld\n",n,k); }
