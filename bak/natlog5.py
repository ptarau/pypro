from natlog.parser import parse
from natlog.unify import unifyWithEnv,extractTerm, \
                  isvar,istuple, extendTo,vars_of
from natlog.natlog import *

print('ver 0.05')

# unfolds repeatedly; when done yields answer
def interp(css,goals) :

  def step(g) :
    ttop=len(trail)
    vtop=len(vs)

    def undo(vtop,ttop) :
      top = len(vs)
      for _ in range(vtop, top): vs.pop()
      top = len(trail)
      for _ in range(ttop, top):
        v = trail.pop()
        if v<vtop: vs[v] = v

    def unfold(b,gs,vtop,ttop):
      # fresh copy of term, with vars >=vtop
      def relocate(t):
        if isvar(t):
          newt=vtop+t
          if newt >= len(vs) :
            extendTo(newt,vs)
          return newt
        elif not istuple(t): return t
        else: return tuple(map(relocate,t))

      g0, gs0 = gs
      for cs0 in css:
        h0,bs0=cs0
        h=relocate(h0)
        if not unifyWithEnv(h, g0, vs, trail=trail, ocheck=False):
          undo(vtop,ttop)
          continue  # FAILURE
        else:
          newb = b
          g = g0
          bs1 = relocate(bs0)
          bs = fromList(bs1)
          bsgs = concat(bs, gs0)
          yield newb, bsgs # SUCCESS

    nonlocal goals
    if goals == () :
      yield extractTerm(g,vs)
    else :
      for newggs in unfold(g,goals,vtop,ttop) :
        newg,goals=newggs
        yield from step(newg)
        undo(vtop,ttop)

  # interp
  goal = goals[0]
  goals = (goal, ())
  vs = list(vars_of(goal))
  trail = []

  yield from step(goal)


# encapsulates reading code, guery and REPL
class natlog:
  def __init__(self,text=None,file_name=None):
    if file_name :
      text=self.consult(file_name)
    self.css=tuple(parse(text,ground=False,rule=True))

  def solve(self,quest):
    goals = tuple(parse(quest,ground=False,rule=False))
    yield from interp(self.css,goals)

  def count(self,quest):
    c=0
    for a in self.solve(quest):
      c+=1
    return c
    
  def query(self,quest):
    goals = tuple(parse(quest,ground=False,rule=False))
    print('GOAL PARSED:',goals)
    for answer in interp(self.css,goals) :
      print('ANSWER:',answer)
    print('')

  def consult(self,file_name) :
    with open(file_name,'r') as f:
      text = f.read()
      return text

  def repl(self):
    print("Type ENTER to quit.")
    while (True):
      q = input('?- ')
      if not q: return
      self.query(q)

  def __repr__(self):
    xs = [str(cs) + '\n' for cs in self.css]
    return "".join(xs)

if __name__ == '__main__':
  print('See tests for examples of code running.')
