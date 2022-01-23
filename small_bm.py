import timeit
from natlog.natlog import *

def time_of(f, x, times=1):
  start_time = timeit.default_timer()
  for i in range(times):
    res = f(x)
    if i == times - 1: print(x)
  end_time = timeit.default_timer()
  print(x, '==>', 'res = ', res)
  print('time = ', end_time - start_time)
  print('')


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

def bm():
  n = Natlog(text=my_text)
  n.query("goal 10 L?")
  time_of(n.count, "goal 16 L?", times=256)
  time_of(n.count, "goal 32 L?", times=64)
  time_of(n.count, "goal 64 L?", times=16)
  time_of(n.count, "goal 128 L?", times=4)
  # time_of(n.count, "goal 250 L?", times=1)
  print('')
  n = Natlog(file_name="natprogs/queens.nat")
  time_of(n.count, "goal8 Queens?", times=9)
  time_of(n.count, "goal9 Queens?")
  time_of(n.count, "goal10 Queens?")
  # return # runs, but quite a bit longer
  time_of(n.count, "goal11 Queens?")
  time_of(n.count, "goal12 Queens?")


def prof():
  import cProfile
  p = cProfile.Profile()

  def fun():
    n = Natlog(text=my_text)
    n.count('goal 200 L?')

  p.runcall(fun)
  p.print_stats(sort=1)


if __name__=="__main__" :
  bm()
