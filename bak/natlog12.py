from natlog.parser import parse
from natlog.unify import unifyWithEnv, extractTerm, \
  isvar, istuple, extendTo, vars_of
from natlog.natlog import db

print('version 0.1.0')

# unfolds repeatedly; when done yields answer
def interp(css, goals ,db=None):

  # reduces goals and yields answer when no more goals
  def step(goals):

    # undoes bindings of variables contained in the trail
    def undo():
      l = len(vs) - vtop
      while (l):
        vs.pop()
        l -= 1
      while trail:
        v = trail.pop()
        if v < vtop: vs[v] = v

    # fresh copy of term, with vars >=vtop
    def relocate(t):
          if isvar(t):
            newt = vtop + t
            if newt >= len(vs):
              extendTo(newt, vs)
            return newt
          elif not istuple(t):
            return t
          else:
            return tuple(map(relocate, t))

    # unfolds a goal using matching clauses
    def unfold(g, gs):
      for cs in css:
        h, bs = cs
        if not unifyWithEnv(relocate(h), g, vs, trail=trail, ocheck=False):
          undo()
          continue  # FAILURE
        else:
          bs1 = relocate(bs)
          bsgs = gs
          for b1 in reversed(bs1) :
            bsgs=(b1,bsgs)
          yield bsgs  # SUCCESS

    # special operators
    def db_call(g,goals) :
      for ok in db.unify_with_fact(g, vs, trail):
        if not ok:  # FAILURE
          undo()
          continue
        yield from step(goals)  # SUCCESS
        undo()
    def python_call(g,goals):
      f=eval(g[0])
      f(g[1:])



    # step
    if goals == ():
      yield extractTerm(goal, vs)
    else:
      trail = []
      vtop = len(vs)
      g, goals = goals
      op=g[0]
      if op in ["~","`","``","^"] :
         g = extractTerm(g[1:], vs)
         if op=='~': # matches against database of facts
           yield from db_call(g,goals)
         elif op=='`' :
          python_call(g,goals)
          yield from step(goals)
          undo()
         elif op=='^' :
           yield g
           yield from step(goals)
           undo()

      else :
        for newgoals in unfold(g, goals):
          yield from step(newgoals)
          undo()

  # interp
  goal = goals[0]
  vs = list(vars_of(goal))
  yield from step((goal, ()))

# encapsulates reading code, guery and REPL
class natlog:
  # builds Natlog machine from text, rule file, ground facts tuple store
  def __init__(self, text=None, file_name=None, db_name=None):
    if file_name:
      text = self.consult(file_name)
    self.css = tuple(parse(text, ground=False, rule=True))
    if db_name:
      self.db= db.db()
      self.db.load(db_name)
    else:
      self.db=None
  # answer generator for given quest
  def solve(self, quest):
    goals = tuple(parse(quest, ground=False, rule=False))
    yield from interp(self.css, goals, db=self.db)

  # answer counter
  def count(self, quest):
    c = 0
    for a in self.solve(quest):
      c += 1
    return c

  # show answers for given query
  def query(self, quest):
    if self.db : db=self.db
    else : db=None
    goals = tuple(parse(quest, ground=False, rule=False))
    print('GOAL PARSED:', goals)
    for answer in interp(self.css, goals, db=db):
      print('ANSWER:', answer)
    print('')

  # consults rule file
  def consult(self, file_name):
    with open(file_name, 'r') as f:
      text = f.read()
      return text

  # read-eval-print-loop
  def repl(self):
    print("Type ENTER to quit.")
    while (True):
      q = input('?- ')
      if not q: return
      self.query(q)


  # shows tuples of Nalog rule base
  def __repr__(self):
    xs = [str(cs) + '\n' for cs in self.css]
    return "".join(xs)

if __name__ == '__main__':
  print('See tests.py for examples of code running.')
