#ifndef istack_h
#define istack_h

#include "defs.h"
//#include "vm.h"

typedef struct istackholder {
  long capacity;
  long top;
  term *array;
}
*istack;

typedef istack stack;

istack newStack(void);

void freeStack(istack s);

void clearStack(istack s);

int isEmpty(istack s);

void ipush(istack s,term i);

term ipop(istack s);

term ipeek(istack s);

term iat(istack s,long i);

void  iset(istack s,long i,term v);

int find(istack s,const long k);


long size(stack s);


void push(stack s,Any i);

Any pop(stack s);

Any peek(stack s);

Any at(stack s,long i);

#endif /* istack_h */
