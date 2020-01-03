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

if __name__=="__main__" :
  # db_test()
  #py_test()
  #bm()
  #prof()
  t2()
