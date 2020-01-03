from natlog.parser import parse
from natlog.unify import unifyWithEnv,extractTerm, \
                  isvar,istuple
from natlog.natlog import *

print('ver 0.02')

# frech copy of term, with vars >=l
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

# unfolds repeatedly; when done yields answer
def interp(css,goals) :
  l,goal=relocate(0,goals[0])

  goals=(goal,())

  def step(l,g) :
    nonlocal goals
    def unfold(l,b,gs):
      g0, gs0 = gs
      for cs0 in css:
        newl, cs = relocate(l, cs0)  # term, sorted list
        h, bs0 = cs
        vs = []
        if not unifyWithEnv(h, g0, vs, trail=None, ocheck=True):
          continue  # FAILURE
        else:
          newb = extractTerm(b, vs)
          g = extractTerm(g0, vs)
          bs = fromList(bs0)
          bsgs = concat(bs, gs0)
          newgs = extractTerm(bsgs, vs)
          r = newl, (newb, newgs)
          yield r  # SUCCESS

    if goals == () : yield g
    else :
      for newl,newggs in unfold(l,g,goals) :
        newg,goals=newggs
        yield from step(newl,newg)
  yield from step(l,goal)

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
