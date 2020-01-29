from natlog.natlog import *

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

def db_test() :
  nd = natlog(file_name="natprogs/dbtc.nat",db_name="natprogs/db.nat")
  print('RULES')
  print(nd)
  print('DB FACTS')
  print(nd.db)
  nd.query("tc Who is_a animal ?")


def py_test() :
  nd = natlog(file_name="natprogs/py_call.nat")
  print('RULES')
  print(nd)
  nd.query("goal X?")


def go() :
  t1()
  t2()
  t3()
  t4()
  t5()
  t6()

  
import timeit
def time_of(f,x,times=1) :
 start_time = timeit.default_timer()
 for i in range(times) :
   res=f(x)
   if i== times-1 :print(x)
 end_time=timeit.default_timer()
 print(x,'==>','res = ',res)
 print('time = ',end_time - start_time)
 print('')
 
def bm() :
  n = natlog(text=my_text)
  n.query("goal 10 L?")
  time_of(n.count, "goal 16 L?", times=256)
  time_of(n.count, "goal 32 L?", times=64)
  time_of(n.count, "goal 64 L?", times=16)
  time_of(n.count, "goal 128 L?",times=4)
  time_of(n.count, "goal 250 L?", times=1)
  print('')
  n = natlog(file_name="natprogs/queens.nat")
  time_of(n.count,"goal Queens?",times=9)
  time_of(n.count, "goal9 Queens?")
  time_of(n.count, "goal10 Queens?")
  return # runs, but quite a bit longer
  time_of(n.count, "goal11 Queens?")
  time_of(n.count, "goal12 Queens?")

def prof() :
  import cProfile
  p=cProfile.Profile()
  def fun() :
    n=natlog(text=my_text)
    n.count('goal 200 L?')

  p.runcall(fun)
  p.print_stats(sort=1)


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
  # db_test()
  #py_test()
  #bm()
  #prof()
  dtestj()
  t2()
