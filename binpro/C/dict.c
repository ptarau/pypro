#include <stdlib.h>
#include <assert.h>
#include <string.h>

#include "dict.h"
#include "defs.h"

struct elt {
  struct elt *next;
  const char *key;
  long value;
} *elt_ptr;

struct dict {
  int size;           /* size of the pointer table */
  int n;              /* number of elements stored */
  struct elt **table;
};

#define INITIAL_SIZE (1024)
#define GROWTH_FACTOR (2)
#define MAX_LOAD_FACTOR (1)

long dictCount(Dict d) {
  return d->n;
}

long dictSize(Dict d) {
  return d->size;
}

/* dictionary initialization code used in both newDict and grow */
static Dict internalnewDict(int size) {
  Dict d=XALLOC(1,struct dict);
  //Dict d = malloc(sizeof(*d));
  int i;
  
  assert(d != 0);
  
  d->size = size;
  d->n = 0;
  //d->table = malloc(sizeof(struct elt *) * d->size);
  d->table = XALLOC((d->size),struct elt *);
  
  assert(d->table != 0);
  
  for(i = 0; i < d->size; i++) d->table[i] = 0;
  
  return d;
}

Dict newDict(void) {
  return internalnewDict(INITIAL_SIZE);
}

void freeDict(Dict d)
{
  int i;
  struct elt *e;
  struct elt *next;
  
  for(i = 0; i < d->size; i++) {
    for(e = d->table[i]; e != 0; e = next) {
      next = e->next;
      
      //XFREE(e->key);
      //XFREE(e->value);
      XFREE(e);
    }
  }
  
  XFREE(d->table);
  XFREE(d);
}

#define MULTIPLIER (97)

static unsigned long hash_function(const char *s)
{
  unsigned const char *us;
  unsigned long h;
  
  h = 0;
  
  for(us = (unsigned const char *) s; *us; us++) {
    h = h * MULTIPLIER + *us;
  }
  
  return h;
}

static void grow(Dict d)
{
  Dict d2;            /* new dictionary we'll create */
  struct dict swap;   /* temporary structure for brain transplant */
  int i;
  struct elt *e;
  
  d2 = internalnewDict(d->size * GROWTH_FACTOR);
  
  for(i = 0; i < d->size; i++) {
    for(e = d->table[i]; e != 0; e = e->next) {
      /* note: this recopies everything */
      /* a more efficient implementation would
       * patch out the strdups inside DictInsert
       * to avoid this problem */
      dictPut(d2, e->key, e->value);
    }
  }
  
  /* the hideous part */
  /* We'll swap the guts of d and d2 */
  /* then call freeDict on d2 */
  swap = *d;
  *d = *d2;
  *d2 = swap;
  
  freeDict(d2);
}

/* insert a new key-value pair into an existing dictionary */
void dictPut(Dict d, const char *key, const long value)
{
  //struct elt *e=malloc(sizeof(*e));
  struct elt *e = XALLOC(1,struct elt);
  unsigned long h;
  
  assert(key);
  //assert(value);
  
  
  
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
const long dictGet(Dict d, const char *key) {
  struct elt *e;
  
  for(e = d->table[hash_function(key) % d->size]; e != 0; e = e->next) {
    if(!strcmp(e->key, key)) {
      /* got it */
      return e->value;
    }
  }
  return NOT_FOUND;
}

int inDict(Dict d, const char *key) {
  return NOT_FOUND!=dictGet(d,key);
}

/* delete the most recently inserted record with the given key */
/* if there is no such record, has no effect */
void dictDel(Dict d, const char *key) {
  struct elt **prev;          /* what to change when elt is deleted */
  struct elt *e;              /* what to delete */
  
  for(prev = &(d->table[hash_function(key) % d->size]);
      *prev != 0;
      prev = &((*prev)->next)) {
    if(!strcmp((*prev)->key, key)) {
      /* got it */
      e = *prev;
      *prev = e->next;
      XFREE(e);
      return;
    }
  }
}

// generic variants, by cating to/from Any

void gDictPut(Dict d, const char *key, const Any value) {
  dictPut(d,key,(long)value);
}

const Any gDictGet(Dict d, const char *key) {
  return (Any)dictGet(d,key);
}


