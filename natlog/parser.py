from .scanner import scanner

trace=False

# turns cons-like tuples into long tuples
def to_tuple(xy):
  if xy==None :
    return ()
  elif not isinstance(xy,tuple) :
    return xy
  else:
    x,y=xy
    t=to_tuple(x)
    ts=to_tuple(y)
    return (t,)+ts

# simple LL(1) recursive descent parser
# supporting parenthesized tuples
# scanned from whitespace separated tokens
class parser:
  def __init__(self,words) :
    self.words=words

  def get(self) :
    if self.words :
      w=self.words[0]
      self.words=self.words[1:]
      return w
    else :
      return None

  def peek(self) :
    if self.words :
      w=self.words[0]
      return w
    else :
      return None

  def par(self) :
    w=self.get()
    assert w == '('
    return self.pars()

  def pars(self) :
    w=self.peek()
    if w==')' :
      self.get()
      return None
    elif w=='(':
      t = self.par()
      ts=self.pars()
      return (t,ts)
    else :
      self.get()
      ts = self.pars()
      return (w,ts)

  def run(self):
    t = to_tuple(self.par())
    if trace : print("PARSED",t)
    return t

# extracts a Prolog-like clause made of tuples
def to_clause(xs) :
  if ':' not in xs : return (xs,())
  neck = xs.index(':')
  head = xs[:neck]
  body = xs[neck+1:]
  if ',' not in xs : return (head,(body,))
  bss=[]
  bs=[]
  for b in body :
    if b==',' :
      bss.append(tuple(bs))
      bs=[]
    else :
      bs.append(b)
  bss.append(tuple(bs))
  return (head,tuple(bss))

# main exported parser + scanner
def parse(text,ground=False,rule=False) :
  s= scanner(text, ground=ground)
  for ws in s.run() :
    ws = ("(",) + ws + (")",)
    p=parser(ws)
    r = p.run()
    if rule : r=to_clause(r)
    yield r


# tests

def ptest() :
  text = """
       app () Ys Ys. 
       app (X Xs) Ys (X Zs) : 
           app Xs Ys Zs.

       nrev () ().
       nrev (X Xs) Zs : nrev Xs Ys, app Ys (X) Zs.
       """
  for c in parse(text,ground=True):
    print(c)
  print('')
  for c in parse(text,ground=False,rule=True) :
    print(c)
  print('')
  ptest1()


def ptest1() :
  xs=('a',0,1,2, ':', 'b', 0 ,',', 'c', 0 , 1,',','d',1,2)
  print(to_clause(xs))

def ptest2() :
  ws="( x y ( a ( b ( c 1 2 ) ) d ) ( xx yy ) )".split()
  #ws = "( x ( x x ) x x )".split()

  p=parser(ws)
  print(ws)
  r=p.par()
  print(r)
  print(to_tuple(r))
  print(p.words)
  print('WS',ws)
  print(parser(ws).run())

if __name__=='__main__' :
  ptest()
