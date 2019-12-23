import re

class Int :
  def __init__(self,val):
    if not isinstance(val,int) :
      val=int(val)
    self.val=val
  def __repr__(self):
    return "Int("+str(self.val)+")"

class scanner:
  def __init__(self,text,ground=True):
    self.text=text
    self.syms=dict()
    self.ground=ground
    self.Scanner = re.Scanner([
      (r"[-+]?\d+\.\d+", lambda sc, tok: ("FLOAT", float(tok))),
      (r"[-+]?\d+", lambda sc, tok: ("INT", Int(tok))),
      (r"[a-z]+[\w]*", lambda sc, tok: ("ID", tok)),
      (r"[A-Z_]+[\w]*", lambda sc, tok: ("VAR", self.sym(tok))),
      (r"[(]", lambda sc, tok: ("LPAR", tok)),
      (r"[)]", lambda sc, tok: ("RPAR", tok)),
      (r"[.?]", lambda sc, tok: ("END", '.')),
      (r"[:]", lambda sc, tok: ("IF", tok)),
      (r"[,]", lambda sc, tok: ("AND", tok)),
      (r"[;]", lambda sc, tok: ("OR", tok)),
      (r"\s+", None),  # None == skip tok.
    ])

  def sym(self,w) :
    if self.ground : return w
    i=self.syms.get(w)
    if  i is None :
      i=len(self.syms)
      self.syms[w]=i
    return i

  def run(self) :
    toks,_= self.Scanner.scan(self.text)
    ts=[]
    for (_,x) in toks :
      if x=='.' :
        yield  tuple(ts)
        ts=[]
      else :
        ts.append(x)


# tests

def stest() :
  sent = "(The cat -42) (sits on (the mat 0.42)). \n the Dog _barks ."
  s=scanner(sent)
  print(list(s.run()))

if __name__=='__main__' :
  stest()
