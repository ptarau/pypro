import sys

sys.setrecursionlimit(2 ** 15)

from .scanner import Int
from .parser import parse
from .unify import unifyWithEnv, extractTerm, \
    isvar, extendTo, vars_of
from .db import Db
# from .Ndb import Ndb
from .conslist import *


def to_python(t):
    """
    turns Int to int in ground terms
    """
    if isinstance(t, Int):
        return t.val
    if isinstance(t, tuple):
        return tuple(map(to_python, t))
    if isvar(t):
        return None
    return t


def from_python(t):
    """
    turns int to Int in ground terms
    """
    if isinstance(t, int):
        return Int(t)
    if isinstance(t, tuple):
        return tuple(map(from_python, t))
    return t


# unfolds repeatedly; when done yields answer
def interp(css, goals, transformer, db=None):
    def step(goals):
        """
        reduces goals and yields answer when no more goals
        """

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
                h = relocate(h)
                if not unifyWithEnv(h, g, vs, trail=trail, ocheck=False):
                    undo()
                    continue  # FAILURE
                else:
                    bs1 = relocate(bs)
                    bsgs = gs
                    for b1 in reversed(bs1):
                        # b1=extractTerm(b1,vs) # slower!
                        bsgs = (b1, bsgs)
                    yield bsgs  # SUCCESS

        ## special operators

        # yields facts matching g in Db
        def db_call(g, goals):
            for ok in db.unify_with_fact(g, vs, trail):
                if not ok:  # FAILURE
                    undo()
                    continue
                yield from step(goals)  # SUCCESS
                undo()

        # simple call to Python (e.g., print, no return expected)
        def python_call(g, goals):
            f = eval(g[0])
            args = to_python(g[1:])
            f(*args)

        def python_fun(g, goals):
            """
            function call to Python, last arg unified with result
            """
            f = eval(g[0])
            g = g[1:]
            v = g[-1]
            args = to_python(g[:-1])
            r = f(*args)
            r = from_python(r)
            if not unifyWithEnv(v, r, vs, trail=trail, ocheck=False):
                undo()
            else:
                yield from step(goals)

        # unifies with last arg yield from a generator
        # and first args, assumed ground, passed to it
        def gen_call(g, goals):
            gen = transformer(g[0])
            # gen=eval(g0)
            g = g[1:]
            v = g[-1]
            args = to_python(g[:-1])
            for r in gen(*args):
                r = from_python(r)
                if unifyWithEnv(v, r, vs, trail=trail, ocheck=False):
                    yield from step(goals)
                undo()

        def dispatch_call(op, g, goals):
            """
            dispatches several types of calls to Python
            """
            if op == '~':  # matches against database of facts
                yield from db_call(g, goals)
            elif op == '^':  # yield g as an answer directly
                yield g
                yield from step(goals)
            elif op == '`':  # function call, last arg unified
                yield from python_fun(g, goals)
            elif op == "``":  # generator call, last arg unified
                yield from gen_call(g, goals)
            else:  # op == '#',  simple call, no return
                python_call(g, goals)
                yield from step(goals)
            undo()

        # step
        if goals == ():
            yield extractTerm(goal, vs)
        else:
            trail = []
            vtop = len(vs)
            g, goals = goals
            op = g[0]

            if op in ["~", "`", "``", "^", "#"]:
                g = extractTerm(g[1:], vs)
                yield from dispatch_call(op, g, goals)
            else:
                for newgoals in unfold(g, goals):
                    yield from step(newgoals)
                    undo()

    # interp
    goal = goals[0]
    vs = list(vars_of(goal))
    yield from step((goal, ()))


# encapsulates reading code, guery and REPL
class Natlog:
    """ builds Natlog machine from text, rule file, ground facts tuple store"""

    def __init__(self, text=None, file_name=None, db_name=None):
        if file_name:
            text = self.consult(file_name)
        self.css = tuple(parse(text, ground=False, rule=True))
        if db_name:
            self.db_init()
            self.db.load(db_name)
        else:
            self.db = None

    def db_init(self):
        """
        overridable database initializer
        sets the type of the database (default or neuro-symbolic)
        """
        self.db = Db()

    def generator_transformer(self):
        """
        overridable opportunity to refine eval
        e.g., to handle out of scope calls or
        enforce only 'safe' functions to be called
        """

        def eval_it(x):
            f = eval(x)
            return f

        return eval_it

    def solve(self, quest):
        """
         answer generator for given question
        """
        goals = tuple(parse(quest, ground=False, rule=False))
        yield from interp(self.css, goals, self.generator_transformer(), db=self.db)

    def count(self, quest):
        """
        answer counter
        """
        c = 0
        for _ in self.solve(quest):
            c += 1
        return c

    def query(self, quest):
        """
        show answers for given query
        """
        if self.db:
            db = self.db
        else:
            db = None
        goals = tuple(parse(quest, ground=False, rule=False))
        print('GOAL PARSED:', goals)
        for answer in interp(self.css, goals, self.generator_transformer(), db=db):
            print('ANSWER:', answer)
        print('')

    def consult(self, file_name):
        """
        consults rule file
        """
        with open(file_name, 'r') as f:
            text = f.read()
            return text

    def repl(self):
        """
        read-eval-print-loop
        """
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
