#ifndef idict_h
#define idict_h

#include <limits.h>
#include "defs.h"

#define NOT_FOUND (LONG_MIN)

typedef struct iddict *IdDict;

/* create a new empty dictionary */
IdDict newIdDict(void);

long idDictCount(IdDict d);

long idDictSize(IdDict d);

/* destroy a dictionary */
void freeIdDict(IdDict);

/* insert a new key-value pair into an existing dictionary */
void idDictPut(IdDict, long key, const long value);

/* return the most recently inserted value associated with a key */
/* or 0 if no matching key is present */
const long idDictGet(IdDict, long key);

int inIdDict(IdDict, const long);

/* delete the most recently inserted record with the given key */
/* if there is no such record, has no effect */
void idDictDel(IdDict, long key);

void gIdDictPut(IdDict d, long key, const Any value);

const Any gIdDictGet(IdDict d, long key);

#endif /* idict_h */
