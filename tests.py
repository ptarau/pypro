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
  n.query("tc cat is What ?")
  n.query("tc Who is What ?")


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

def go() :
  t1()
  t2()
  t3()
  t4()
  t5()
  t6()

if __name__=="__main__" :
  t6()