
#include <ctype.h>
#include <string.h>
#include <assert.h>
#include "defs.h"
#include "vm.h"
#include "istack.h"
#include "dict.h"
#include "idict.h"
#include "io.h"


static term *heap;
static term htop;

static Dict syms;
static stack sids;

typedef struct cls {
  term c;
  term begin;
  term neck;
  term end;
} *cls;

term sym(char *s,Dict syms,stack sids) {
  if(inDict(syms,s)) {
    return dictGet(syms,s);
  }
  term i=size(sids);
  dictPut(syms,s,i);
  push(sids,s);
  return i;
}

inline static term tag(term x,int t) {
  return (x<<SHIFT) | t;
}

inline static int tag_of(term x) {
  return (int)(x & MASK);
}

inline static term val(term x) {
  return x>>SHIFT;
}

inline static term atom(char *s) {
  return tag(sym(s,syms,sids),ATOM);
}

inline static term pair(term x,term y) {
  term h=htop;
  heap[htop++]=x;
  heap[htop++]=y;
  return tag(h,PAIR);
}

inline static term left(term p) {
  return heap[p];
}

inline static term right(term p) {
  return heap[p+1];
}

inline static term deref(term o) {
  while(1) {
    term x=val(o);
    int t=tag_of(o);
    if(VAR==t) {
      term y=heap[x];
      term v=val(y);
      int tv=tag_of(y);
      if(v==x) {
        assert(VAR==tv);
        return o;
      }
      if(VAR==tv && v>x) {
        assert(v<x);
      }
      o=y;
    }
    else {
      return o;
    }
  }
}

void px(term v0) {
  term v=deref(v0);
  //printf("deref %lu -> %lu\n",v0,v);
  term x=val(v);
  int  t=tag_of(v);
  if(v>0) assert(t>0);
  
  printf("v=%lu x=%lu t=%d\n",v,val(v),tag_of(v));
  
  if(ATOM==t) {
    printf("ATOM %s",at(sids,x));
  }
  else if (VAR==t) {
    printf("_%lu",x);
  }
  else if (PAIR==t) {
    printf("pair at: %lu",x);
  }
  else {
    printf("OTHER %lu <?> %lu,%d",v,x,t);
  }
}



void p0(term  v0,int k) {
  if(k<=0) {printf("...");return;}
  term v=deref(v0);
  term x=val(v);
  int  t=tag_of(v);

  switch(t) {
  case HNIL:
    printf("NIL");
    break;
  case VAR:
    printf("_%lu",x);
    break;
  case PAIR:
    printf("(");
    p0(left(x),k-1);
    printf("=>");
    p0(right(x),k-1);
    printf(")");
    break;
  case ATOM: {
    printf("%s",at(sids,x));
    //printf("%s%lu:","#",x);
  }
    break;
  default:
    printf("OTHER %lu:%d\n",x,t);
    assert(0);
  }
}

void p(term x) {
  p0(x,20);
}

void n() {
  printf("\n");
}

void pp(term x) {
  p(x);
  n();
}

void ph(stack code) {
  printf("HEAP:\n");
  for(term i=0;i<size(code);i++) {
    cls clause=at(code,i);
    printf("\n------CLAUSE: %lu to %lu\n\n",clause->begin,clause->neck);
    for(term j=clause->begin;j<clause->neck;j++) {
      printf("%lu: ",j);pp(heap[j]);
    }
    printf("\n----------NECK = %lu\n\n",clause->neck);
    for(term j=clause->neck;j<clause->end;j++) {
      printf("%lu: ",j);pp(heap[j]);
    }
    printf("-------------\n");
  }
  n();
}

void phb(term c) {
  term hb=val(c);
  int tg=tag_of(c);
  assert(PAIR==tg);
  term h=left(hb);
  term b=right(hb);
  p(h);printf(":-");p(b);n();
}

void pc(stack code) {
  printf("CLAUSES:\n");
  term l=size(code);
  for(term i=0;i<l;i++) {
    cls c=(cls)at(code,i);
    printf("begin=%lu, end=%lu\n",c->begin,c->end);
    phb(c->c);
  }
  printf("----------\n");
}


int eq(const char *s,const char*t) {
  return 0==strcmp(s,t);
}

term tovar(char *w,Dict vars,istack vnames) {
  assert(w!=NULL);
  char c=w[0];
  if(isupper(c)) {
    return tag(sym(w,vars,vnames),VAR);
  }
  else {
    return tag(sym(w,syms,sids),ATOM);
  }
}

term stack2tree(stack postfix,Dict vars,stack vnames,term *neck) {
  istack ts=newStack();
  term l=size(postfix);
  for(term i=0;i<l; i++) {
    char *w=at(postfix,i);
    if(eq("$",w)) {
      term t2=ipop(ts);
      term t1=ipop(ts);
      term t=pair(t1,t2); // <===============
      ipush(ts,t);
    }
    else if(eq(":-",w)) *neck=htop;
    else {
      term t=tovar(w,vars,vnames);
      ipush(ts,t);
    }
  }
  term tree=ipop(ts);
  return tree;
}


stack tload(void) {
  stack wss=file2wss(fname);
  term l=size(wss);
  stack cs=newStack();
  for(term i=0;i<l;i++) {
    stack ws=at(wss,i);
    Dict vars=newDict();
    IdDict vids=newIdDict();
    istack vnames=newStack();
    
    term begin=htop;
    term neck;
    term t=stack2tree(ws,vars,vnames,&neck);
    assert(PAIR==tag_of(t));
    term end=htop;
    
    cls clause=XALLOC(1,struct cls);
    clause->c=t;
    clause->begin=begin;
    clause->neck=neck;
    clause->end=end;
    //printf("TLOAD NECK:%lu <<%lu>> %lu\n",begin,neck,end);
    assert(begin<neck);
    assert(neck<end);
    push(cs,clause);
    
    for(term h=begin;h<end;h++) {
      term vc=heap[h];
      term x=val(vc);
      int tg=tag_of(vc);
      if(VAR==tg) {
        if(inIdDict(vids,x)) {
          term y=(term)idDictGet(vids,x);
          heap[h]=tag(y,tg);
        }
        else {
          heap[h]=tag(h,tg);
          idDictPut(vids,x,h);
        }
      }
    }
  }
  return cs;
}

inline static void vset(term x,term v) {
  heap[x]=v;
}



static int unify(term x,term y,istack trail,term umax,istack ustack) {
  clearStack(ustack);
  ipush(ustack,y);
  ipush(ustack,x);
  
  while (!isEmpty(ustack)) {
    const term x1=deref(ipop(ustack));
    const term x2=deref(ipop(ustack));
    const term i1=val(x1);
    const term i2=val(x2);
    const int t1=tag_of(x1);
    const int t2=tag_of(x2);
    
    //printf("UNIFY: //%lu\t",size(ustack));p(x1);printf("====");pp(x2);
    if(x1==x2) continue;
    if(VAR==t1 && VAR==t2) {
      if(i1>i2) {
        vset(i1,x2);
        if(i1<umax)
          ipush(trail,i1);
      }
      else {
        vset(i2,x1);
        if(i2<umax)
          ipush(trail,i2);
      }
    }
    else if(VAR==t1) {
      vset(i1,x2);
      if(i1<umax)
        ipush(trail,i1);
    }
    else if(VAR==t2) {
      vset(i2,x1);
      if(i2<umax)
        ipush(trail,i2);
    }
    else if(t1!=t2) {
      return 0;
    }
    else if(ATOM==t1) {
      if(i1!=i2) return 0;
    }
    else {
      assert(t1 == PAIR);
      assert(t2 == PAIR);
      term a1=left(i1);
      term b1=right(i1);
      term a2=left(i2);
      term b2=right(i2);
      ipush(ustack,b2);
      ipush(ustack,b1);
      ipush(ustack,a2);
      ipush(ustack,a1);
    }
  }
  //printf("SUCCESS! htop=%lu,ttop=%lu\n",htop,size(trail));
  return 1;
}

inline static void unwind(istack trail,long ttop) {
  long i=size(trail)-ttop;
  while(i>0) {
    term v=ipop(trail);
    vset(v,tag(v,VAR));
    i-=1;
  }
}

inline static void trim_heap(term h) {
  htop=h;
}

inline static void copy_cell(term j,term h,term where) {
  term v=heap[j];
  term x=val(v);
  int t=tag_of(v);
  if(ATOM==t) {
    heap[where]=v;
  }
  else {
    heap[where]=tag(x+h,t);
  }
}

inline static term activate(cls clause,term umax) {
  term c=clause->c;
  term begin=clause->begin;
  term hb=val(c);
  int ctag=tag_of(c);
  term h=umax-begin;
  for(term j=begin;j<clause->end;j++) {
    copy_cell(j,h,htop++);
  }
  return tag(h+hb,ctag);
}

static term get_goal() {
  term goal=atom("goal");
  term cont=tag(htop,VAR);
  term p=pair(cont,goal);
  term answer=tag(htop,VAR);
  return pair(answer,p);
}

int FAIL=0;int DO=1;int DONE=2;int UNDO=3;

typedef struct task {
  int op;
  term NewG;
  term OldG;
  term ttop;
  term htop;
  term i;
} *task;

task newTask(int op, term NewG,term OldG,term ttop,term htop,term i) {
  task a = XALLOC(1,struct task);
  a->op=op;
  a->NewG=NewG;
  a->OldG=OldG;
  a->ttop=ttop;
  a->htop=htop;
  a->i=i;
  return a;
}

task nothing;

void freeTask(task t) {
  if(t==nothing) return;
  XFREE(t);
}

void init() {
  syms=newDict();
  sids=newStack();
  heap=XALLOC(MAXHEAP,term);
  htop=0L;
  nothing=newTask(FAIL,NIL,NIL,NIL,NIL,NIL);
}

void ensure_undo(term OldG, stack todo, term ttop, term htop, term i, term l) {
  if(!isEmpty(todo)) {
    task t=peek(todo);
    if(t->op==UNDO && t->i==i && OldG==t->OldG && ttop==t->ttop) {
      return;
    }
  }
  push(todo,newTask(UNDO,NIL,OldG,ttop,htop,i));
}

static task step(term G,stack code,istack ustack,istack trail,term answer,term i) {
  //printf("step %lu\n",i);
  term ttop=size(trail);
  term umax=htop;
  long l=size(code);
  //G=deref(G);
  assert(val(G)<htop);
  while(i<l) {
    unwind(trail,ttop);
    trim_heap(umax);
    assert(htop==umax);
    cls clause=at(code,i++);
    term c=activate(clause,umax);
    term hb=val(c);
    term thb=tag_of(c);
    assert(PAIR==thb);
    term H=left(hb);
    
    if(!unify(G,H,trail,umax,ustack)) continue;
    
    term B=right(hb);
    term NewG=deref(B);
    int tb=tag_of(NewG);
    if(VAR==tb) {
      printf("ANSWER: ");pp(answer);
      return newTask(DONE, NIL,G, ttop, htop, i);
    }
    else {
      assert(PAIR==tb);
      return newTask(DO, NewG,G,ttop, htop, i);
    }
  }
  return nothing;
}

void interp() {
  init();
  term goal=get_goal();
  term answer=left(val(goal));
  stack code=tload();
  term l=size(code);
  //pp(goal);
  //ph(code);
  
  istack trail=newStack();
  istack ustack=newStack();
  istack todo=newStack();
  task t0=newTask(DO,goal,NIL,0,htop,size(code));
  push(todo,t0);
  while(!isEmpty(todo)) {
    task pt=pop(todo);
    int op=pt->op;
    term NewG0=pt->NewG;
    term OldG0=pt->OldG;
    term ttop0=pt->ttop;;
    term htop0=pt->htop;
    term i0=pt->i;
    freeTask(pt);
    //printf("op=%d\n",op);
    if(DO==op) {
      if(i0<l)
        ensure_undo(OldG0,todo,ttop0,htop0,i0,l);
      task newt=step(NewG0,code, ustack, trail, answer, 0);
      push(todo,newt);
    }
    else if (DONE==op) {
      if(i0<l)
        ensure_undo(OldG0,todo,ttop0,htop0,i0,l);
    }
    else if (UNDO==op) {
      unwind(trail,ttop0);
      trim_heap(htop0);
      if(i0 < l) push(todo,step(OldG0,code, ustack, trail, answer, i0));
    }
    else {
      // pass
    }
  }
  printf("DONE\n");
}
