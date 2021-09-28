#include <limits.h>
#include "defs.h"

#define NOT_FOUND (LONG_MIN)

typedef struct dict *Dict;

/* create a new empty dictionary */
Dict newDict(void);

long dictCount(Dict d);

long dictSize(Dict d);

/* destroy a dictionary */
void freeDict(Dict);

/* insert a new key-value pair into an existing dictionary */
void dictPut(Dict, const char *key, const long value);

/* return the most recently inserted value associated with a key */
/* or 0 if no matching key is present */
const long dictGet(Dict, const char *key);

int inDict(Dict, const char *key);

/* delete the most recently inserted record with the given key */
/* if there is no such record, has no effect */
void dictDel(Dict, const char *key);

// generic casted variants

void gDictPut(Dict, const char *key, const Any value);

const Any gDictGet(Dict, const char *key);

int dict_test(void);
