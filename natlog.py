from parser import parse
from unify import unifyWithEnv, extractTerm, \
   isvar,istuple,vars_of,const_of, has_vars,makeEnv,extendTo

def refresh(l,t,vs) :
  def ref(t) :
    if isvar(t) :
      newt=l+t
      extendTo(newt,vs)
      return newt
    elif not istuple(t) : return t
    else : return tuple(map(ref,t))
  return ref(t)

def show(gs,vs) :
  print('vvvvvvvvvvvvvvvvvvvvvv')
  for g in gs:
    print(extractTerm(g,vs))
  print('^^^^^^^^^^^^^^^^^^^^')
  print('')

def unfold(g,css,vs,trail) :
  for choice in range(len(css)):
    (h0, bs0) = css[choice]
    l = len(vs)
    tl = len(trail)
    h = refresh(l, h0, vs)
    ok = unifyWithEnv(h, g, vs, trail, ocheck=True)
    if not ok: # FAILURE
      for v in trail[tl:]:
        if v < l:
          vs[v] = v
        else :
          assert not isvar(vs[v])
      trail = trail[0:tl]
      vs = vs[0:l]
      continue
    else: # SUCCESS
      bs=[]
      for b0 in bs0:
        b = refresh(l, b0, vs)
        bs.append(extractTerm(b,vs))
        #bs.append(b)
      yield bs

def interp(css,goals) :
  goal=goals[0]
  trail=[]
  gvars=vars_of(goal)
  l0=len(gvars)
  vs=makeEnv(size=l0)
  def step(g) :
      print('EVAL:',g)
      for bs in unfold(g,css,vs,trail) :
        #print("BS",bs)
        newbs=[]
        for b in bs :
          print('ENTER',b)
          r = step(b)
          print("EXIT_", b)
          newbs.append(b)
        return newbs
  return list(step(goal))



class natlog:
  def __init__(self,text):
    self.css=tuple(parse(text,ground=False,rule=True))
    #print(self.css)

  def query(self,quest):
    goals = tuple(parse(quest,ground=False,rule=False))
    print('GOAL PARSED',goals)
    r=interp(self.css,goals)
    print('ANSWER',goals)

  def __repr__(self):
    xs = [str(cs) + '\n' for cs in self.css]
    return "".join(xs)

def natex() :
  text = """
      app () Ys Ys. 
      app (X Xs) Ys (X Zs) : 
          app Xs Ys Zs.

      nrev () ().
      nrev (X Xs) Zs : nrev Xs Ys, app Ys (X ()) Zs.
      """
  return natlog(text)

def ntest() :
  n=natex()
  print('DB')
  print(n)
  #n.query("app Xs Ys (a (b (c ())))?")
  #n.query("app (a (b ())) (c (d ())) R ?")
  n.query("nrev  (a (b (c (d ())))) R ?")

def ppp(*args) :print(*args)

if __name__ == '__main__':
  ntest()
