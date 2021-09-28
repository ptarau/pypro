#ifndef defs_h
#define defs_h

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

//static char* fname="../../../out/bnf_asm.txt";
static char* fname="/Users/tarau/Desktop/sit/LogicTransformers/out/bnf_asm.txt";

typedef unsigned long term;

#define MAXHEAP (1L<<32)

//*************************

//#define GC_ON

#ifdef GC_ON /* ----------------------- WITH GC ENABLED ------------ */
#include "/usr/local/include/gc/gc.h"

#define XALLOC(NbOfEls,TypeOfEls) ((TypeOfEls *)GC_malloc((NbOfEls)*sizeof(TypeOfEls)))

#define XFREE(Ptr)


#else /**************************  NO BOEHM GC USED ************************************/

#define XALLOC(NbOfEls,TypeOfEls) ((TypeOfEls *)malloc((NbOfEls)*sizeof(TypeOfEls)))

#define XFREE(Ptr) free(Ptr)

#endif /* GC_ON*/

typedef void *Any;



#endif /* defs_h */
