from collections import defaultdict

from .unify import unifyToTerm, unifyWithEnv, \
  vars_of,const_of
from .parser import parse
from .scanner import Int

def make_index() :
  return defaultdict(set)

def add_clause(index,css,h) :
  i=len(css)
  css.append(h)
  for c in const_of(h) :
    index[c].add(i)

def tuplify(t) :
  if isinstance(t,list) :
    return tuple(map(tuplify,t))
  else:
    return t

class db:
  def __init__(self):
    self.index=make_index() # content --> int index
    self.css=[]  # content as ground tuples

  # parses text to list of ground tuples
  def digest(self, text):
    for cs in parse(text, ground=True):
      self.add_clause(cs)

  # loads from json list of lists
  def load_json(self, fname):
    import json
    with open(fname,'r') as f:
      ts=json.load(f)
    for t in ts :
      self.add_clause(tuplify(t))

  # loads ground facts .nat or .json files
  def load(self,fname):
    if len(fname) > 4 and fname[-4:]=='.nat' :
      with open(fname,'r') as f:
        self.digest(f.read())
    else :
      self.load_json(fname)

  # adds a clause and indexes it for all constants
  # recurevely occurring in it, in any subtuple
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

  # uses unification to match ground fact
  # with bindining applied to vs and colelcted on trail
  def unify_with_fact(self, h, vs, trail):
    ms = self.ground_match_of(h)
    for i in ms:
      h0 = self.css[i]
      u=unifyWithEnv(h, h0, vs, trail=trail, ocheck=False)
      yield u

  # uses unification to match and return ground fact
  def match_of(self,h):
    ms=self.ground_match_of(h)
    for i in ms:
      h0=self.css[i]
      u = unifyToTerm(h,h0)
      if u : yield u

  # searches for a matching tuple
  def search(self,query):
    qss=parse(query,ground=False)
    for qs in qss:
        for rs in self.match_of(qs) :
          yield rs

  # simple search based on content
  def about(self, query):
    qss = parse(query, ground=True)
    for qs in qss:
      qs=tuple(qs)
      for i in self.ground_match_of(qs):
        yield self.css[i]

  def ask_about(self, query):
    print('QUERY:',query)
    for r in self.about(query):
      print('-->', r)
    print('')


  # queries the db directly with a text query
  def ask(self, query):
    print('QUERY:',query)
    for r in self.search(query):
      print('-->', r)
    print('')

  # builds possibly very large string representation
  # of the facts contained in the db
  def __repr__(self):
    xs=[str(cs)+'\n' for cs in enumerate(self.css)]
    return "".join(xs)

# tests

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

# bb built form text
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
  query = "Who has (a What)?"
  d.ask(query)

  query = "Who is (a pilot)?"
  d.ask(query)

  query = "'Mary' is What?"
  d.ask(query)

  query = "'John' is (a What)?"
  d.ask(query)

  query = "Who is What?"
  d.ask(query)

# db from a .nat file
def dtestf():
  fname='natprogs/db.nat'
  d = db()
  d.load(fname)
  print(d)
  print('LOADED:',fname)
  d.ask("Who is mammal?")

# db from a json file
def dtestj():
  fname='natprogs/db.json'
  d = db()
  d.load(fname)
  #print(d)
  print('LOADED:',fname)
  print("")
  d.ask("S (X Y Z U)?")
  query="reusable launch vehicle?"
  d.ask_about(query)


if __name__=='__main__' :
  dtestj()


