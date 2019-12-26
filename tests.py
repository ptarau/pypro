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
def t2() :
  n=natlog(file_name="natprogs/perm.nat")
  n.query("perm (1 (2 (3 ()))) Ps?")
  n=natlog(file_name="natprogs/nrev.nat")
  n.query("nrev  (a (b (c (d ())))) R ?")

  n=natlog(file_name="natprogs/tc.nat")
  n.query("tc cat is What ?")
  n.query("tc Who is What ?")


# longer output: 8 queens
def t3():
  n = natlog(file_name="natprogs/queens.nat")
  print(n)
  n.query("goal Queens?")

def t4():
  n = natlog(file_name="natprogs/arith.nat")
  print(n)
  n.query("goal R ?")

def t5() :
  n = natlog(file_name="natprogs/family.nat")
  n.query("grand_parent_of 'Joe' GP ?")
  print('Enter some queries!')
  n.repl()

if __name__=="__main__" :
  t4()
