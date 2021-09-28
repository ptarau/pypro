#include <stdio.h>
#include <assert.h>

#include "tests.h"
#include "dict.h"
#include "io.h"
#include "istack.h"

void t3a() {
  stack wss=file2wss(fname);
  term l=size(wss);
  for(term i=0;i<l;i++) {
    istack ws=at(wss,i);
    term r=size(ws);
    for(term j=0;j<r;j++) {
      printf("%s ",at(ws,j));
    }
    printf("\n");
  }
}

void tests() {
  t3a();
}
