import scanner

trace=False

def to_list(xy):
  if xy==None :
    return ()
  elif not isinstance(xy,tuple) :
    return xy
  else:
    x,y=xy
    t=to_list(x)
    ts=to_list(y)
    return (t,)+ts

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
    t = to_list(self.par())
    if trace : print("PARSED",t)
    return t

def parse(text,ground=False) :
  s=scanner.scanner(text,ground=ground)
  for ws in s.run() :
    ws = ("(",) + ws + (")",)
    if trace : print('SCANNED',ws)
    p=parser(ws)
    yield p.run()

def ptest() :
  text = """
    app () (). 
      app (X Xs) Ys (X Zs) : 
        app Xs Ys Zs.
        
    nrev () ().
    nrev (X Xs) Zs : nrev Xs Ys, app Ys, (X) Zs.
    """
  for c in parse(text,ground=True) :
    print(c)
  print('')
  for c in parse(text):
    print(c)

def ptest1() :
  ws="( x y ( a ( b ( c 1 2 ) ) d ) ( xx yy ) )".split()
  #ws = "( x ( x x ) x x )".split()

  p=parser(ws)
  print(ws)
  r=p.par()
  print(r)
  print(to_list(r))
  print(p.words)
  print('WS',ws)
  print(parser(ws).run())

if __name__=='__main__' :
  ptest()
