from natlog import *

# testing with string text
def t1():
  text = """
      app () Ys Ys. 
      app (X Xs) Ys (X Zs) : 
          app Xs Ys Zs.

      nrev () ().
      nrev (X Xs) Zs : nrev Xs Ys, app Ys (X ()) Zs.
      """
  n=natlog(text=text)
  n.query("nrev  (a (b (c (d ())))) R ?")

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
def time_of(f,x) :
 start_time = timeit.default_timer()
 res=f(x)
 print(x)
 end_time=timeit.default_timer()
 print(x,'==>','res = ',res)
 print('time = ',end_time - start_time)
 print('')
 
def bm() :
  n = natlog(file_name="natprogs/queens.nat")
  print(n)
  time_of(n.count,"goal Queens?")
  time_of(n.count, "goal9 Queens?")
  time_of(n.count, "goal10 Queens?")
  time_of(n.count, "goal11 Queens?")
  time_of(n.count, "goal12 Queens?")
 
if __name__=="__main__" :
  # db_test()
  py_test()
