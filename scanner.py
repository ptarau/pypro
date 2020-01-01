import re

class Int :
  def __init__(self,val):
    if not isinstance(val,int) :
      val=int(val)
    self.val=val

  def __eq__(self, other):
    if isinstance(other,Int) :
      return self.val == other.val
    return False

  def __repr__(self):
    return "Int("+str(self.val)+")"

def qtrim(s) :
  return s[1:-1]
        
class scanner:
  def __init__(self,text,ground=True):
    self.text=text
    self.syms=dict()
    self.ground=ground
    self.Scanner = re.Scanner([
      (r"[-+]?\d+\.\d+", lambda sc, tok: ("FLOAT", float(tok))),
      (r"[-+]?\d+", lambda sc, tok: ("INT", Int(tok))),
      (r"[a-z]+[\w]*", lambda sc, tok: ("ID", tok)),
      (r"'[\w\s\-\.\/,%=!\+\(\)]+'", lambda sc, tok: ("ID", qtrim(tok))),
      (r"[A-Z_]+[\w]*", lambda sc, tok: ("VAR", self.sym(tok))),
      (r"~|``|`|\^|#", lambda sc, tok: ("OP", tok)),
      (r"[(]", lambda sc, tok: ("LPAR", tok)),
      (r"[)]", lambda sc, tok: ("RPAR", tok)),
      (r"[.?]", lambda sc, tok: ("END", self.newsyms())),
      (r"[:]", lambda sc, tok: ("IF", tok)),
      (r"[,]", lambda sc, tok: ("AND", tok)),
 #     (r"[;]", lambda sc, tok: ("OR", tok)),
      (r"\s+", None),  # None == skip tok.
    ])

  def newsyms(self) :
    self.syms=dict()
    return "."

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
  sent = \
    "(The ~ cat -42) (~ 'sits on' (the mat 0.42)). \n the ` Dog _barks . (` a `` b) and (`b `a) ."
  s=scanner(sent)
  print(list(s.run()))

if __name__=='__main__' :
  stest()
