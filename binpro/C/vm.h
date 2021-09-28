
#ifndef vm_h
#define vm_h

#include <stdio.h>

#define SHIFT 3

#define NIL (0ul)

#define HNIL 0
#define  ATOM 1
#define PAIR 2
#define  VAR 3
#define  REF 4

#define MASK (7ul)

void interp(void);

#endif /* vm_h */
