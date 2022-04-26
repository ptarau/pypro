# simple call to Python (e.g., print, no return expected)
def python_call(g, goals):
    f = eval(g[0])
    args = to_python(g[1:])
    f(*args)

to_python = lambda x: x
from_python = lambda x :x

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

    if not unify(r,v, trail=trail):
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
        if unify(v, r, vs, trail=trail):
            yield from step(goals)
        undo()


def dispatch_call(op, g, goals):
    """
    dispatches several types of calls to Python
    """
    if op == 'not':
        if neg(g):
            yield from step(goals)
    elif op == '~':  # matches against database of facts
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
