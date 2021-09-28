#include "defs.h"
#include "istack.h"

static long MINSIZE = 1<<4;

static inline term *makeIArray(long size) {
  return XALLOC(size,term);
}

inline istack newStack() {
  istack s=XALLOC(1,struct istackholder);
  s->capacity=MINSIZE;
  s->array=makeIArray(s->capacity);
  s->top= -1L;
  return s;
}

inline void clearStack(stack s) {
  s->top = -1L;
}

void freeStack(stack s) {
  XFREE(s->array);
  XFREE(s);
}

inline int isEmpty(stack s) {
  return s->top<0;
}

inline long size(stack s) {
  return s->top+1;
}

static void maybe_iexpand(istack s) {
  if(s->top+1>=s->capacity) {
    
    s->capacity=s->capacity<<1; // *2
    
    term  *oldarray=s->array;
    s->array=makeIArray(s->capacity);
    { long i; // copying old stack
      for(i=0;i<=s->top;i++) {
        s->array[i]=oldarray[i];
      }
    }
    XFREE(oldarray); // avoids memory leaks
  }
}

/*
 static void maybe_ishrink(istack s) {
 if(s->top-1<s->capacity>>2 && s->capacity>>1>MINSIZE) { // div by 4
 
 s->capacity=s->capacity>>1; // div by 2
 
 term  *oldarray=s->array;
 s->array=makeIArray(s->capacity);
 { long i; // copying old stack
 for(i=0;i<=s->top;i++) {
 s->array[i]=oldarray[i];
 }
 }
 XFREE(oldarray); // avoids memory leaks
 
 }
 }
 */

inline void ipush(istack s,term  t) {
  maybe_iexpand(s);
  s->array[++s->top]=t;
}

inline term  ipop(istack s) {
  //maybe_ishrink(s);
  return s->array[s->top--];
}

inline term  ipeek(istack s) {
  return s->array[s->top];
}

inline term  iat(istack s,long i) {
  assert (i>=0 && i<=s->top);
  return s->array[i];
}

inline void  iset(istack s,long i,term v) {
  assert (i>=0 && i<=s->top);
  s->array[i]=v;
}


int find(istack s,const long k) {
  long l=size(s);
  for(long i=0;i<l;i++) {
    long x=iat(s,i);
    //printf("--------%lu =?=  %lu\n",k,x);
    if(k==x)  {
      
      return 1;
    }
  }
  return 0;
}


// generic stack via casts

inline void push(stack s,Any t) {
  ipush(s,(term )t);
}

inline Any pop(stack s) {
  return (Any)ipop(s);
}

inline Any peek(stack s) {
  return (Any)ipeek(s);
}

inline Any at(stack s,long i) {
  return (Any)iat(s,i);
}

