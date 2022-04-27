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


def deref(v):
    while isinstance(v, Var):
        if v.val is None:
            return v
        v = v.val
    return v


def unify(x, y, trail):
    ustack = []
    ustack.append(y)
    ustack.append(x)
    while ustack:
        x1 = deref(ustack.pop())
        x2 = deref(ustack.pop())
        if x1 == x2: continue
        if isinstance(x1, Var):
            x1.bind(x2, trail)
        elif isinstance(x2, Var):
            x2.bind(x1, trail)
        elif not isinstance(x1, tuple):
            return False
        else:  # assumed x1 is a tuple
            arity = len(x1)
            if len(x2) != arity:
                return False
            for i in range(arity - 1, -1, -1):
                ustack.append(x2[i])
                ustack.append(x1[i])
    return True


def activate(t, d):
    if isinstance(t, VarNum):
        v = d.get(t, None)
        if v is None:
            v = Var()
            d[t] = v
        return v
    elif not isinstance(t, tuple):
        return t
    else:
        return tuple(activate(x, d) for x in t)


def extractTerm(t):
    if isinstance(t, Var):
        return deref(t)
    elif not isinstance(t, tuple):
        return t
    else:
        return tuple(map(extractTerm, t))


def const_of(t):
    def const_of0(t):
        if isinstance(t, Var):
            pass
        elif isinstance(t, tuple):
            for x in t:
                yield from const_of0(x)
        else:
            yield t

    return set(const_of0(t))


def vars_of(t):
    def vars_of0(t):
        if isinstance(t, Var):
            yield t
        elif isinstance(t, tuple):
            for x in t:
                yield from vars_of0(x)
        else:
            pass

    return set(vars_of0(t))
