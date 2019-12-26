from parser import parse
from unify import unifyWithEnv, extractTerm, \
   isvar,istuple,vars_of,const_of, has_vars,makeEnv,extendTo
from conslist import *

def relocate(l,t) :
  vs=set()
  def ref(t) :
    if isvar(t) :
      newt=l+t
      vs.add(newt)
      return newt
    elif not istuple(t) : return t
    else : return tuple(map(ref,t))
  t=ref(t)
  return l+len(vs),t

def unfold(l,goal,gs,css) :
  assert isLList(gs)
  g0,gs0=gs
  for cs0 in css:
    newl,cs = relocate(l,cs0) # term, sorted list
    h,bs0=cs
    vs=[]
    ok = unifyWithEnv(h, g0, vs, trail=None, ocheck=True)
    if not ok: # FAILURE
      continue
    else:      # SUCCESS
      newgoal=extractTerm(goal,vs)
      g=extractTerm(g0,vs)
      bs=fromList(bs0)
      bsgs=concat(bs,gs0)
      newgs=extractTerm(bsgs,vs)
      r=newl,(newgoal,newgs)
      yield r

def interp(css,goals) :
  l,goal=relocate(0,goals[0])
  k=100
  print('GOAL STARTS', goal)
  def step(k,l,g,gs) :
    if k==0 : return
    if gs == () :
      yield g
    else :
      for newl,newggs in unfold(l,g,gs,css) :
        newg,newgs=newggs
        yield from step(k-1,newl,newg,newgs)
  yield from step(k,l,goal,(goal,()))

class natlog:
  def __init__(self,text=None,file_name=None):
    if file_name :
      text=self.consult(file_name)
    self.css=tuple(parse(text,ground=False,rule=True))

  def query(self,quest):
    goals = tuple(parse(quest,ground=False,rule=False))
    print('GOAL PARSED',goals)
    for a in interp(self.css,goals) :
      print('ANSWER',a)

  def consult(self,file_name) :
    with open(file_name,'r') as f:
      text = f.read()
      return text

  def __repr__(self):
    xs = [str(cs) + '\n' for cs in self.css]
    return "".join(xs)


def go() :
  n=natlog(file_name="natprogs/perm.nat")
  n.query("perm (1 (2 (3 ()))) Ps?")
  n=natlog(file_name="natprogs/nrev.nat")
  n.query("nrev  (a (b (c (d ())))) R ?")

# tests

def natex() :
  text = """
      app () Ys Ys. 
      app (X Xs) Ys (X Zs) : 
          app Xs Ys Zs.

      nrev () ().
      nrev (X Xs) Zs : nrev Xs Ys, app Ys (X ()) Zs.
      
perm () ().
perm (X Xs) Zs : perm Xs Ys, ins X Ys Zs.

ins X Xs (X Xs).
ins X (Y Xs) (Y Ys) : ins X Xs Ys.

      """
  return natlog(text=text)

def ntest() :
  n=natex()
  print('DB')
  print(n)
  #n.query("app Xs Ys (a (b (c ())))?")
  #n.query("app (a (b ())) (c (d ())) R ?")
  #n.query("nrev  (a (b (c (d ())))) R ?")
  #n.query("ins x (1 (2 (3 ()))) Ps?")
  n.query("perm (1 (2 (3 ()))) Ps?")

def ppp(*args) :print(*args)

if __name__ == '__main__':
  ntest()
