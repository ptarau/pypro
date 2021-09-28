#include <string.h>
#include "defs.h"
#include "io.h"

stack file2wss(char *fname) {
  istack wss=newStack();
  istack ws=newStack();
  FILE *fp=fopen(fname,"r");
  char c;
  char tok[1<<10];
  int j=0;
  while(1) {
    c=fgetc(fp);
    if(feof(fp)) break;
    else if(' '==c || '\n'==c) {
      tok[j++]='\0';
      char *word=XALLOC(j+1,char);
      strcpy(word,tok);
      push(ws,word);
      j=0;
      if('\n'==c) {
        push(wss,ws);
        ws=newStack();
      }
    }
    else {
      tok[j++]=c;
    }
  }
  return wss;
}
