#include "idict.h"
#include <stdlib.h>
#include <assert.h>
#include <string.h>
#include "defs.h"

struct idelt {
  struct idelt *next;
  long key;
  long value;
} *idelt_ptr;

struct iddict {
  int size;           /* size of the pointer table */
  int n;              /* number of elements stored */
  struct idelt **table;
};

#define INITIAL_SIZE (1<<4)
#define GROWTH_FACTOR (2)
#define MAX_LOAD_FACTOR (1)

long idDictCount(IdDict d) {
  return d->n;
}

long IdDictSize(IdDict d) {
  return d->size;
}

/* dictionary initialization code used in both newIdDict and grow */
static IdDict internalnewIdDict(int size) {
  IdDict d=XALLOC(1,struct iddict);
  //IdDict d = malloc(sizeof(*d));
  int i;
  
  assert(d != 0);
  
  d->size = size;
  d->n = 0;
  //d->table = malloc(sizeof(struct idelt *) * d->size);
  d->table = XALLOC((d->size),struct idelt *);
  
  assert(d->table != 0);
  
  for(i = 0; i < d->size; i++) d->table[i] = 0;
  
  return d;
}

IdDict newIdDict(void) {
  return internalnewIdDict(INITIAL_SIZE);
}

void freeIdDict(IdDict d)
{
  int i;
  struct idelt *e;
  struct idelt *next;
  
  for(i = 0; i < d->size; i++) {
    for(e = d->table[i]; e != 0; e = next) {
      next = e->next;
      XFREE(e);
    }
  }
  
  XFREE(d->table);
  XFREE(d);
}

#define MULTIPLIER (97)

inline static unsigned long hash_function(const long s)
{
  return s;
}

static void grow(IdDict d)
{
  IdDict d2;            /* new dictionary we'll create */
  struct iddict swap;   /* temporary structure for brain transplant */
  int i;
  struct idelt *e;
  
  d2 = internalnewIdDict(d->size * GROWTH_FACTOR);
  
  for(i = 0; i < d->size; i++) {
    for(e = d->table[i]; e != 0; e = e->next) {
      /* note: this recopies everything */
      /* a more efficient implementation would
       * patch out the strdups inside IdDictInsert
       * to avoid this problem */
      idDictPut(d2, e->key, e->value);
    }
  }
  
  /* the hideous part */
  /* We'll swap the guts of d and d2 */
  /* then call freeIdDict on d2 */
  swap = *d;
  *d = *d2;
  *d2 = swap;
  
  freeIdDict(d2);
}

/* insert a new key-value pair into an existing dictionary */
void idDictPut(IdDict d,  long key, const long value)
{
  //struct idelt *e=malloc(sizeof(*e));
  struct idelt *e = XALLOC(1,struct idelt);
  unsigned long h;
  
  assert(e);
  
  e->key = key;
  e->value = value;
  
  h = hash_function(key) % d->size;
  
  e->next = d->table[h];
  d->table[h] = e;
  
  d->n++;
  
  /* grow table if there is not enough room */
  if(d->n >= d->size * MAX_LOAD_FACTOR) {
    grow(d);
  }
}

/* return the most recently inserted value associated with a key */
/* or 0 if no matching key is present */
const long idDictGet(IdDict d, const long key) {
  struct idelt *e;
  
  for(e = d->table[hash_function(key) % d->size]; e != 0; e = e->next) {
    if(e->key== key) {
      /* got it */
      return e->value;
    }
  }
  return NOT_FOUND;
}

int inIdDict(IdDict d, const long key) {
  return NOT_FOUND!=idDictGet(d,key);
}

/* delete the most recently inserted record with the given key */
/* if there is no such record, has no effect */
void idDictDel(IdDict d, const long key) {
  struct idelt **prev;          /* what to change when idelt is deleted */
  struct idelt *e;              /* what to delete */
  
  for(prev = &(d->table[hash_function(key) % d->size]);
      *prev != 0;
      prev = &((*prev)->next)) {
    if((*prev)->key==key) {
      /* got it */
      e = *prev;
      *prev = e->next;
      XFREE(e);
      return;
    }
  }
}

// generic variants, by cating to/from Any

void gIdDictPut(IdDict d, long key, const Any value) {
  idDictPut(d,key,(long)value);
}

const Any gIdDictGet(IdDict d, long key) {
  return (Any)idDictGet(d,key);
}

