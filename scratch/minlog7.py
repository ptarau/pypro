from mparser import mparse
from mscanner import VarNum


class Var:
    def __init__(self):
        self.val = None

    def bind(self, val, trail):
        self.val = val
        trail.append(self)

    def unbind(self):
        self.val = None

    def __repr__(self):
        v = deref(self)
        if isinstance(v, Var) and v.val is None:
            return "_" + str(id(v))
        else:
            return repr(v)

def is_compound(t):
    return isinstance(t,tuple) or isinstance(t,list)

def deref(v):
    while isinstance(v, Var):
        if v.val is None:
            return v
        v = v.val
    return v

def new_var(t, d):
    v = d.get(t.val, None)
    if v is None:
        v = Var()
        d[t.val] = v
    return v

def relocate(y, d):
    if isinstance(y, VarNum):
        return new_var(y, d)
    elif not isinstance(y,tuple):
        return y
    rstack = []
    x = []
    rstack.append(y)
    rstack.append(x)
    while rstack:
        x1 = rstack.pop()
        x2 = rstack.pop()
        if is_compound(x2):
            for t in x2:
                if isinstance(t, VarNum):
                    u = new_var(t, d)
                elif isinstance(t,tuple):
                    u = []
                else:
                    u = t
                x1.append(u)
                rstack.append(t)
                rstack.append(u)
    return x


def unify(x, y, trail, d):
    ustack = []
    ustack.append(y)
    ustack.append(x)
    while ustack:
        x1 = deref(ustack.pop())
        x2 = deref(ustack.pop())

        if isinstance(x1, VarNum):
            x1 = new_var(x1, d)
            x1.bind(x2, trail)
        elif x1 == x2:
            continue
        elif isinstance(x1, Var):
            x1.bind(x2, trail)
        elif isinstance(x2, Var):
            x1 = relocate(x1, d)
            x2.bind(x1, trail)
        elif is_compound(x2):
            arity = len(x2)
            if len(x1) != arity:
                return False
            x1 = relocate(x1, d)
            for i in range(arity - 1, -1, -1):
                ustack.append(x2[i])
                ustack.append(x1[i])
        else:
            return False
    return True


def interp(css, goal):
    def step(goals):

        def undo(trail):
            while trail:
                v = trail.pop()
                v.unbind()

        def unfold(g, gs):
            for (h, bs) in css:
                d = dict()
                # h = relocate(h, d)
                if not unify(h, g, trail, d):
                    undo(trail)
                    continue  # FAILURE
                else:
                    bs1 = relocate(bs, d)
                    bsgs = gs
                    for b1 in reversed(bs1):
                        bsgs = (b1, bsgs)
                    yield bsgs  # SUCCESS

        if goals == ():
            yield goal
        else:
            trail = []
            g, gs = goals
            for newgoals in unfold(g, gs):
                yield from step(newgoals)
                undo(trail)

    yield from step((goal, ()))


class MinLog:
    def __init__(self, text=None, file_name=None):
        if file_name:
            with open(file_name, 'r') as f:
                self.text = f.read()
        else:
            self.text = text
        self.css = tuple(mparse(self.text, ground=False, rule=True))

    def solve(self, quest):
        """
         answer generator for given question
        """
        goal_cls = next(mparse(quest, ground=False, rule=False))
        goal = relocate(goal_cls, dict())
        yield from interp(self.css, goal)

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
        for answer in self.solve(quest):
            print('ANSWER:', answer)
        print('')

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
        return " ".join(xs)


def test_minlog():
    n = MinLog(file_name="../natprogs/tc.nat")
    print(n)
    n.query("tc Who is animal ?")

    # n = MinLog(file_name="../natprogs/queens.nat")
    # n.query("goal8 Queens?")

    n = MinLog(file_name="../natprogs/perm.nat")
    print(n)
    n.query("perm (1 (2 (3 ())))  X ?")


if __name__ == "__main__":
    # test_unify()
    test_minlog()
