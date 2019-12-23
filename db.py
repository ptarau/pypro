from collections import defaultdict

from unify import unifyToEnv, unifyToTerm, isvar,istuple
from parser import parse
from scanner import Int

def make_index() :
  return defaultdict(set)

def const_of0(t) :
  if isvar(t):
    pass
  elif istuple(t) :
    for x in t:
      yield from const_of(x)
  else :
    yield t

def const_of(t) : return set(const_of0(t))

def vars_of0(t) :
  if isvar(t):
    yield t
  elif istuple(t) :
    for x in t:
      yield from vars_of(x)
  else :
    pass

def vars_of(t) : return set(vars_of0(t))

def has_vars(t) :
  r = next(vars_of0(t),-1)
  return r>=0


def add_clause(index,css,h) :
  i=len(css)
  css.append(h)
  for c in const_of(h) :
    index[c].add(i)

class db:
  def __init__(self):
    self.index=make_index() # content --> int index
    self.css=[]  # content as ground tuples

  def digest(self,text):
    for cs in parse(text,ground=True) :
      self.add_clause(cs)

  def add_clause(self,cs):
    add_clause(self.index,self.css,cs)

  def ground_match_of(self,h):
    cs=const_of(h)
    if not cs :
      return set(range(len(self.css)))
    c=next(iter(cs))
    r=self.index[c].copy()
    for x in cs:
      r &= self.index[x]
    return r

  def match_of(self,h):
    ms=self.ground_match_of(h)
    for i in ms:
      h0=self.css[i]
      u = unifyToTerm(h,h0)
      if u : yield u

  def search(self,query):
    qss=parse(query,ground=False)
    for qs in qss:
        for rs in self.match_of(qs) :
          yield rs

  def __repr__(self):
    xs=[str(cs)+'\n' for cs in self.css]
    return "".join(xs)

c1=('a',Int(1),'car','a')
c2=('a',Int(2),'horse','aa')
c3=('b',Int(1),'horse','b')
c4=('b',Int(2),'car','bb')

g1=('a',0,1,2)
g2=(0,1,'car',2)
g3=(0,1,2,0)

def dtest1() :
  print(c1,'<-const:',list(const_of(c1)))
  print(c3,'<-vars:',list(vars_of(c3)))
  d=db()
  for cs in [c1,c2,c3,c4]:
    d.add_clause(cs)
  print('index',d.index)
  print('css',d.css)
  print('Gmatch', g1, list(d.ground_match_of(g1)))
  print('Vmatch',g1,list(d.match_of(g1)))
  print('Gmatch', g2, list(d.ground_match_of(g2)))
  print('Vmatch',g2,list(d.match_of(g2)))
  print('Gmatch', g3, list(d.ground_match_of(g3)))
  print('Vmatch', g3, list(d.match_of(g3)))


def dtest() :
  text='''
   John has (a car).
   Mary has (a bike).
   Mary is (a student).
   John is (a pilot).
   '''
  print(text)
  d = db()
  d.digest(text)
  print(d)
  print('')

  def ask(query):
    print(query)
    for r in d.search(query):
      print('-->',r)
    print('')

  query = "Who has (a What)?"
  ask(query)

  query = "Who is (a pilot)?"
  ask(query)

  query = "'Mary' is What?"
  ask(query)

  query = "'John' is (a What)?"
  ask(query)

  query = "Who is What?"
  ask(query)

if __name__=='__main__' :
  dtest()


