from natlog.natlog import *
from natlog.db import *
from natlog.ndb import *
from natlog.neural_natlog import *

my_text = """
    app () Ys Ys. 
    app (X Xs) Ys (X Zs) : 
        app Xs Ys Zs.

    nrev () ().
    nrev (X Xs) Zs : nrev Xs Ys, app Ys (X ()) Zs.

    goal N L :
      `genList N Xs,
      nrev Xs Ys,
      `llen Ys L. 
    """

def test_generators():
  prog="""
  good 'l'.
  good 'o'.
  goal X : ``iter hello X, good X.
  goal X : ``range 1000 1005 X.
  """
  n = natlog(text=prog)
  for answer in n.solve("goal R?") :
    print(answer[1])

def test_answer_stream():
  prog="""
  perm () ().
  perm (X Xs) Zs : perm Xs Ys, ins X Ys Zs.

  ins X Xs (X Xs).
  ins X (Y Xs) (Y Ys) : ins X Xs Ys.
  """
  n=natlog(text=prog)
  for answer in n.solve("perm (a (b (c ()))) P?"):
    print(answer[2])

def yield_test():
  prog="""
    worm : ^o, worm.
  """
  n = natlog(text=prog)
  for i,answer in enumerate(n.solve("worm ?")):
    print(answer[0],end='')
    if i > 42 : break
  print('')

# testing with string text
def t1():
  n=natlog(text=my_text)
  n.query("nrev  (a (b (c (d ())))) R ?")
  n.query("goal 10 L?")

# testing with some .nat files

def t2()  :
  n=natlog(file_name="natprogs/tc.nat")
  print(n)
  n.query("tc Who is animal ?")
  #n.query("tc Who is What ?")


def t4():
  n = natlog(file_name="natprogs/perm.nat")
  n.query("perm (1 (2 (3 ()))) Ps?")

def t3():
  n = natlog(file_name="natprogs/arith.nat")
  print(n)
  n.query("goal R ?")


# longer output: 8 queens
def t5():
  n = natlog(file_name="natprogs/queens.nat")
  print(n)
  n.query("goal Queens?")

def t6() :
  n = natlog(file_name="natprogs/family.nat")
  print(n)
  n.query("grand_parent_of 'Joe' GP ?")

def t7() :
  n = natlog(file_name="natprogs/family.nat")
  print('Enter some queries!')
  n.repl()

def loop():
  n = natlog(file_name="natprogs/loop.nat")
  print(n)
  n.query("goal X?")

def db_test() :
  nd = natlog(file_name="natprogs/dbtc.nat",db_name="natprogs/db.nat")
  print('RULES')
  print(nd)
  print('DB FACTS')
  print(nd.db)
  nd.query("tc Who is_a animal ?")

def ndb_test() :
  nd = neural_natlog(file_name="natprogs/dbtc.nat",db_name="natprogs/db.nat")
  print('RULES')
  print(nd)
  print('DB FACTS')
  print(nd.db)
  nd.query("tc Who is_a animal ?")

def db_chem() :
  nd = natlog(
    file_name="natprogs/elements.nat",
    db_name="natprogs/elements.tsv"
  )
  print('RULES')
  print(nd)
  print('DB FACTS')
  print(nd.db)
  nd.query("an_el Num Element ?")
  nd.query("gases Num Element ?")

def ndb_chem() :
  nd = neural_natlog(
    file_name="natprogs/elements.nat",
    db_name="natprogs/elements.tsv"
  )
  print('RULES')
  print(nd)
  print('DB FACTS')
  print(nd.db)
  nd.query("gases Num Element ?")


def py_test() :
  nd = natlog(file_name="natprogs/py_call.nat")
  print('RULES')
  #print(nd)
  nd.query("goal X?")

def go() :
  t1()
  t2()
  t3()
  t4()
  t5()
  t6()

  


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

# db built form text
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
  fname='natprogs/db'
  jname=fname+'.json'
  nname=fname+'.nat'
  d=db()
  d.load(nname)
  d.save(jname)
  d = db()
  d.load(jname)
  #print(d)
  print('LOADED:',jname)
  print("")
  query="Who is What?"
  d.ask(query)


if __name__=="__main__" :
  '''
  uncomment any
  '''
  #db_test()
  #py_test()
  #test_generators()
 # test_answer_stream()
  #yield_test()
  #bm()
  #prof()
  dtestj()
  t5()
  #ndb_test() # tests transitive closure with learner
  ndb_chem() # tests query about chemical elements

  pass
